import wx, time, thread, logging, subprocess
from __versions__ import __author__, __application__, IS_OSX, IS_WINDOWS
from os.path import expanduser, join as joinPath
from dlgAddDirectory import addDirectory
from dlgEmail import email_dialog
from dlgLog import log_dialog
from dlgCmd import command_dialog
from observatory import Watcher
from frmWatcher import mainFrame
from Email import Email, EmailConnection


class TheWatcher(mainFrame):

    def addDirectory(self, event):
        addDirDlg = addDirectory(self)
        addDirDlg.Show()


    def remDirectory(self, event):
        rowID = self.lstPath.GetSelectedRow()
        numOfRows = self.lstPath.GetStore().GetCount()
        if numOfRows > 1 and rowID != -1:
            self.lstPath.DeleteItem(rowID)
        elif numOfRows == 1 and rowID != -1:
            self.lstPath.DeleteAllItems()


    def addDirectoryToList(self, record):
        lstRowCount = self.lstPath.GetStore().GetCount()
        newRecord = [lstRowCount] + record
        self.lstPath.AppendItem(newRecord)


    def quickAdd(self, event):
        dirPath = self.dirPicker.GetPath()
        if dirPath != u"Please enter a valid path...":
            self.addDirectoryToList([dirPath, "New Files, Modifications", True, 
                "Files Only", None, None])
        else:
            wx.MessageBox(u"Please specify a valid Directory!", 
                u"Infomation!", wx.OK | wx.ICON_EXCLAMATION)
            self.statusBar.SetStatusText("Click the Browse Button")


    def clearLog(self, event):
        self.txtLog.Clear()
        self.log_switch = False


    def onGuiLogUpdate(self, event):
        if self.log_switch is False:
            numOfLines = self.txtLog.GetNumberOfLines()
            if numOfLines >= self.log_lenght:
                self.log_switch = True


    def saveLog(self, event):
        defaultPath = ""
        
        if IS_OSX:
            defaultPath = expanduser("~/Desktop")
        if IS_WIN:
            defaultPath = expanduser("~")
        
        logFileDlg = wx.DirDialog(self, "Location...", defaultPath)
        logFileDlg.ShowModal()
        logFile = path.join(logFileDlg.GetPath(), "Log.txt")
        self.txtLog.SaveFile(logFile)


    def loadLog(self, event):
        logFileDlg = wx.FileDialog(self, "Select your log file")
        logFileDlg.ShowModal()
        self.txtLog.LoadFile(logFileDlg.GetPath())


    def BindFindEvents(self, win):
        win.Bind(wx.EVT_FIND, self.OnFind)
        # win.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        # win.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        # win.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)
        win.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)


    def findInLog(self, event):
        dlg = wx.FindReplaceDialog(self, self.findData, "Find in Log", 
            wx.FR_NOUPDOWN | wx.FR_NOMATCHCASE | wx.FR_NOWHOLEWORD)
        self.BindFindEvents(dlg)
        dlg.Show(True)


    def OnFind(self, event):
        wx.LogMessage(event.GetFindString())


    def OnFindClose(self, event):
        event.GetDialog().Destroy()


    def SendEmail(self, event):
        if self.emailData != None:
            ts = time.strftime(self.log.GetTimestamp(), 
                    time.localtime(event.GetTimestamp()))
            data = self.emailData
            data["pathType"] = event.pathType
            data["evt_type"] = event.evt_type
            data["evt_src"] = event.evt_src
            data["timestamp"] = ts
            data["filename"] = event.filename
            # if "evt_dest" in dir(event):
            if hasattr(event, "evt_dest"):
                data["evt_dest"] = event.evt_dest
            attach = None if self.emailData["attachments"] == u'' else \
                     self.emailData["attachments"]
            email = Email(from_=self.emailData["userName"],
                          to=self.emailData["emailTO"],  #TODO: Multiple receipt
                          subject=self.emailData["emailSubject"].format(**data),
                          message=self.emailData["emailMessage"].format(**data),
                          attachments=attach)
            # email.debug(True)
            with EmailConnection(self.emailData["smtpServer"], 
                                 self.emailData["userName"], 
                                 self.emailData["password"]) as server:
                server.send(email)


    def checkEmail(self, event):
        if self.emailData != None and self.emailData["sendEmail"] == True:
            if (self.emailData["delay"] == True and 
                self.eventCount >= self.emailData["delayCount"]):
                thread.start_new_thread(self.SendEmail, (event,))
                # self.SendEmail(event) # Send the email
                self.eventCount = 0  # Reset the counter
                return
            if self.emailData["delay"] == False:
                thread.start_new_thread(self.SendEmail, (event,))


    def emailSettings(self, event):
        emailDlg = email_dialog(self)
        emailDlg.Show()


    def logSettings(self, event):
        logDlg = log_dialog(self)
        logDlg.Show()


    def cmdSettings(self, event):
        cmdDlg = command_dialog(self)
        cmdDlg.Show()


    def setupFileLogging(self):
        self.fileLogger = logging.getLogger(__application__)
        self.fileLogger.setLevel(logging.DEBUG)
        if self.logData != None:
            log_format = self.logData["log_format"]
            logfilename = joinPath(self.logData["path"], "TheWatcher.log")
            if self.logData["timestamp"] == True:
                timestamp = self.logData["ts_format"]
            else:
                timestamp = "%d/%m/%Y %I:%M:%S %p"
        else:
            log_format = "%(asctime)-15s - %(levelname)s - %(message)s"
            logfilename = "TheWatcher.log"
            timestamp = "%d/%m/%Y %I:%M:%S %p"
        self.loggingFileHandler = logging.FileHandler(logfilename)
        fmt = logging.Formatter(log_format, datefmt=timestamp)
        self.loggingFileHandler.setFormatter(fmt)
        self.fileLogger.addHandler(self.loggingFileHandler)


    def LogToFile(self, event):
        if self.logData != None:
            if self.logData["log"] == True:
                self.fileLogger.info("%s %s" % (event.pathType, event.logmsg))


    def CallCmd(self, event):
        if self.cmdData != None:
            if self.cmdData["cmd"]:
                cmd = []
                data = {}
                cmd.append(self.cmdData["cmd"])
                if self.cmdData["flags"]:
                    data["evt_src"] = event.evt_src
                    data["filename"] = event.filename
                    if hasattr(event, "evt_dest"):
                        data["evt_dest"] = event.evt_dest
                    flags = str(self.cmdData["flags"].format(**data))
                    # if IS_OSX:
                    #     flags = flags.replace(" ", "\\ ")
                    flags = [expanduser(x) for x in flags.split(",")]
                    cmd = cmd + flags
                # print " ".join(cmd)
                subprocess.call(cmd)


    def onUpdate(self, event):  #TODO: Less Checks, Speed, Single Log Function.
        self.eventCount += 1
        event.SetTimestamp(time.time()) #Manually set timestamp to log events
        wx.LogMessage(event.logmsg)  # Log to Gui
        self.LogToFile(event)  # Log to File
        self.CallCmd(event)  # Call External Cmd
        self.checkEmail(event)  # Send Email


    def GetPathListData(self):
        data = []
        lsCtrlStore = self.lstPath.GetStore()
        colCount = len(self.lstPath.GetColumns()) - 1
        rowCount = lsCtrlStore.GetCount()
        for i in range(0, rowCount):
            row = []
            for colNum in range(1, colCount + 1):
                row.append(lsCtrlStore.GetValueByRow(i, colNum))
            data.append(row)
        return data


    def ProcessRowData(self, rowData):
        watch_path = rowData[0]
        # print "Line 754 rowData >", repr(rowData[4]), repr(rowData[5])
        if rowData[4] != None:
            ignore_patterns = str(rowData[4]).split(', ') if ',' in rowData[4] \
                              else [str(rowData[4])]
        else:
            ignore_patterns = rowData[4]
        if rowData[5] != None:
            patterns = str(rowData[5]).split(', ') if ',' in rowData[5] \
                              else [str(rowData[5])]
        else:
            patterns = rowData[5]
        ignore_directories = True if rowData[3] == 'Files Only' else False
        case_sensitive = False
        create = True if 'New Files' in rowData[1] else False
        modify = True if 'Modifications' in rowData[1] else False
        delete = True if 'Deletions' in rowData[1] else False
        rename = True if 'Renames' in rowData[1] else False
        subDir = rowData[2]
        return [watch_path, patterns, ignore_patterns, ignore_directories, 
                case_sensitive, create, modify, delete, rename, subDir]


    def run_watchdog(self, event):
        if event.IsChecked():
            # Get the number of entries in Path List
            lst = self.GetPathListData()
            for i in range(0, len(lst)):
                # print lst[i][0]
                rowData = self.ProcessRowData(lst[i])
                # print "Main >", rowData[1]
                # print "Main >", rowData[2]
                self.threads.append(Watcher(self, *rowData))
            for t in self.threads:
                t.Start()
        else:
            for t in self.threads:
                t.Stop()
                self.threads = []  # Reset the threads to none.


if __name__ == '__main__':
    app = wx.App(False)
    app.SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)
    app.SetAppName(__application__)
    app.SetVendorName(__author__)
    frame = TheWatcher(None)
    frame.Show(True)
    app.MainLoop()