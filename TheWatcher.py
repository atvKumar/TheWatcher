import wx
from __versions__ import __author__, __application__, IS_OSX, IS_WINDOWS
from os.path import expanduser
from dlgAddDirectory import addDirectory
from observatory import Watcher
from frmWatcher import mainFrame


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


    def onLog(self, event):
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


    def ProcessEvent(self, event):
        if event.evt_type == 'created':
            print "Sending Email now..."


    def onUpdate(self, event):
        # print ">", event.evt_type
        self.ProcessEvent(event)
        wx.LogMessage(event.logmsg)


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