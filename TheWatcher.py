# -*- coding: utf-8 -*- 

import wx
import wx.dataview as dv
import wx.lib.newevent
import logging
import thread
import time
import random
from os import path
from os.path import expanduser
from wx.lib.wordwrap import wordwrap
from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


__author__ = "Kumaran S/O Murugun"
__application__ = "The Watcher"
__version__ = "1.0 (Beta)"

IS_OSX = wx.Platform == "__WXMAC__"
IS_WIN = wx.Platform == "__WXMSW__"

# This creates a new Event class and a EVT binder function
(UpdateLogEvent, EVT_UPDATE_LOG) = wx.lib.newevent.NewEvent()


class LogEventHandler(FileSystemEventHandler):
    def __init__(self, win):
        self.win = win

    def on_created(self, event):
        super(LogEventHandler, self).on_created(event)

        what= 'Directory' if event.is_directory else 'File'
        msg = UpdateLogEvent(logmsg="%s ... created %s" % (what, event.src_path))
        wx.PostEvent(self.win, msg)


################################################################################
## Class Watcher
################################################################################

class Watcher:
    def __init__(self, win, watchpath):
        self.win = win
        self.path = watchpath
        self.event_handler = LogEventHandler(self.win)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        # print "Watcher created ", self.win, self.path


    def Start(self):
        self.keepGoing = self.running = True
        thread.start_new_thread(self.observer.start, ())
        # self.observer.start()
        print "Thread Started..."


    def Stop(self):
        self.keepGoing = False
        self.running = False


    def IsRunning(self):
        return self.running
        self.observer.stop()


    def Run(self): pass
        # while self.keepGoing:
        #     event = UpdateLogEvent(logmsg="Watching %s ... %d" % (self.path, random.randint(1, 10)))
        #     wx.PostEvent(self.win, event)

        #     sleeptime = (random.random() * 2) + 0.5
        #     time.sleep(sleeptime/4)
        # self.running = False

################################################################################
## Class MyLog
################################################################################

class MyLog(wx.PyLog):
    def __init__(self, textCtrl, logTime=0):
        wx.PyLog.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime

    def DoLogText(self, message):
        if self.tc:
            if self.tc.TopLevelParent.log_switch is True:
                lineLenght = self.tc.GetLineLength(0)
                self.tc.Remove(0, lineLenght+1)
                self.tc.SetInsertionPointEnd()
            self.tc.AppendText(message + '\n')


################################################################################
## Class addDirectory
################################################################################

class addDirectory (wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id = wx.ID_ANY, 
            title = u"Add New Directory", pos = wx.DefaultPosition, 
            size = wx.Size(500, 480), style = wx.DEFAULT_DIALOG_STYLE)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        colSizer_main = wx.BoxSizer(wx.VERTICAL)
        
        colGrpSizer_a = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Directory"), wx.VERTICAL)
        
        rowSizer_aa = wx.FlexGridSizer(0, 2, 0, 0)
        rowSizer_aa.AddGrowableCol(1)
        rowSizer_aa.SetFlexibleDirection(wx.BOTH)
        rowSizer_aa.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.lblDirectory = wx.StaticText(self, wx.ID_ANY, u"Directory", 
            wx.DefaultPosition, wx.Size(-1,-1), 0)
        self.lblDirectory.Wrap(-1)
        rowSizer_aa.Add(self.lblDirectory, 0, 
            wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.dirPicker = wx.DirPickerCtrl(self, wx.ID_ANY, 
            u"Please enter a valid path...", u"Select a folder", 
            wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        rowSizer_aa.Add(self.dirPicker, 0, wx.ALL|wx.EXPAND, 5)
        
        
        colGrpSizer_a.Add(rowSizer_aa, 1, wx.EXPAND, 5)
        
        
        colSizer_main.Add(colGrpSizer_a, 0, wx.EXPAND, 5)
        
        colGrpSizer_b = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Options"), wx.VERTICAL)
        
        rowSizer_ab = wx.FlexGridSizer(0, 5, 0, 0)
        rowSizer_ab.SetFlexibleDirection(wx.BOTH)
        rowSizer_ab.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.lblEvents = wx.StaticText(self, wx.ID_ANY, u"Events", 
            wx.DefaultPosition, wx.Size(50,-1), 0)
        self.lblEvents.Wrap(-1)
        rowSizer_ab.Add(self.lblEvents, 0, wx.ALL, 5)
        
        self.cbNewFiles = wx.CheckBox(self, wx.ID_ANY, u"New Files", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.cbNewFiles.SetValue(True) 
        rowSizer_ab.Add(self.cbNewFiles, 0, wx.ALL, 5)
        
        self.cbModifications = wx.CheckBox(self, wx.ID_ANY, u"Modifications", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        rowSizer_ab.Add(self.cbModifications, 0, wx.ALL, 5)
        
        self.cbDeletions = wx.CheckBox(self, wx.ID_ANY, u"Deletions", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        rowSizer_ab.Add(self.cbDeletions, 0, wx.ALL, 5)
        
        self.cbRenames = wx.CheckBox(self, wx.ID_ANY, u"Renames", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        rowSizer_ab.Add(self.cbRenames, 0, wx.ALL, 5)
        
        
        colGrpSizer_b.Add(rowSizer_ab, 0, wx.EXPAND, 5)
        
        rowSizer_ac = wx.FlexGridSizer(0, 2, 0, 0)
        rowSizer_ac.SetFlexibleDirection(wx.BOTH)
        rowSizer_ac.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.lblOptions = wx.StaticText(self, wx.ID_ANY, u"Options", 
            wx.DefaultPosition, wx.Size(50,-1), 0)
        self.lblOptions.Wrap(-1)
        rowSizer_ac.Add(self.lblOptions, 0, wx.ALL, 5)
        
        self.cbSubdirectories = wx.CheckBox(self, wx.ID_ANY, 
            u"Monitor events of subdirectories", wx.DefaultPosition, 
            wx.DefaultSize, 0)
        self.cbSubdirectories.SetValue(True) 
        rowSizer_ac.Add(self.cbSubdirectories, 0, wx.ALL, 5)
        
        
        colGrpSizer_b.Add(rowSizer_ac, 0, wx.EXPAND, 5)
        
        rowSizer_ad = wx.FlexGridSizer(0, 4, 0, 0)
        rowSizer_ad.SetFlexibleDirection(wx.BOTH)
        rowSizer_ad.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.lblTypes = wx.StaticText(self, wx.ID_ANY, u"Types", 
            wx.DefaultPosition, wx.Size(50,-1), 0)
        self.lblTypes.Wrap(-1)
        rowSizer_ad.Add(self.lblTypes, 0, wx.ALL, 5)
        
        self.rbAll = wx.RadioButton(self, wx.ID_ANY, u"Directories and Files", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        rowSizer_ad.Add(self.rbAll, 0, wx.ALL, 5)
        
        self.rbFiles = wx.RadioButton(self, wx.ID_ANY, u"Files Only", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.rbFiles.SetValue(True) 
        rowSizer_ad.Add(self.rbFiles, 0, wx.ALL, 5)
        
        self.rbDirectories = wx.RadioButton(self, wx.ID_ANY, 
            u"Directories Only", wx.DefaultPosition, wx.DefaultSize, 0)
        rowSizer_ad.Add(self.rbDirectories, 0, wx.ALL, 5)
        
        
        colGrpSizer_b.Add(rowSizer_ad, 0, wx.EXPAND, 5)
        
        
        colSizer_main.Add(colGrpSizer_b, 0, wx.EXPAND, 5)
        
        colGrpSizer_c = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Filters"), wx.VERTICAL)
        
        rowSizer_ae = wx.FlexGridSizer(0, 3, 0, 0)
        rowSizer_ae.AddGrowableCol(1)
        rowSizer_ae.SetFlexibleDirection(wx.BOTH)
        rowSizer_ae.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.lblPattern = wx.StaticText(self, wx.ID_ANY, u"Pattern", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblPattern.Wrap(-1)
        rowSizer_ae.Add(self.lblPattern, 0, wx.ALL, 5)
        
        self.txtPattern = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
            wx.DefaultPosition, wx.DefaultSize, 0)
        rowSizer_ae.Add( self.txtPattern, 0, wx.ALL|wx.EXPAND, 5)
        
        self.btnAddPattern = wx.Button(self, wx.ID_ANY, u"Add", 
            wx.DefaultPosition, wx.Size( 50,-1 ), 0)
        rowSizer_ae.Add(self.btnAddPattern, 0, wx.ALL, 5)
        
        
        colGrpSizer_c.Add(rowSizer_ae, 0, wx.EXPAND, 5)
        
        rowSizer_af = wx.FlexGridSizer(0, 1, 0, 0)
        rowSizer_af.AddGrowableCol(0)
        rowSizer_af.SetFlexibleDirection(wx.BOTH)
        rowSizer_af.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.lblExPatterns = wx.StaticText(self, wx.ID_ANY, u"Exclude Patterns", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblExPatterns.Wrap(-1)
        rowSizer_af.Add(self.lblExPatterns, 0, wx.ALL, 5)
        
        lbExPatternsChoices = []
        self.lbExPatterns = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, 
            wx.Size(-1,120), lbExPatternsChoices, wx.LB_NEEDED_SB)
        rowSizer_af.Add(self.lbExPatterns, 1, wx.ALL | wx.EXPAND, 5)
        
        
        colGrpSizer_c.Add(rowSizer_af, 0, wx.EXPAND, 5)
        
        
        colSizer_main.Add(colGrpSizer_c, 0, wx.EXPAND, 5)
        
        rowSizer_ag = wx.FlexGridSizer( 0, 2, 0, 0 )
        rowSizer_ag.SetFlexibleDirection( wx.BOTH )
        rowSizer_ag.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.btnSave = wx.Button(self, wx.ID_ANY, u"Save", wx.DefaultPosition, 
            wx.DefaultSize, 0)
        rowSizer_ag.Add(self.btnSave, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.btnCancel = wx.Button(self, wx.ID_ANY, u"Cancel", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        rowSizer_ag.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        colSizer_main.Add(rowSizer_ag, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        self.SetSizer(colSizer_main)
        self.Layout()
        
        self.Centre(wx.BOTH)
        
        # Connect Events
        # self.cbNewFiles.Bind(wx.EVT_CHECKBOX, self.onEventChoice)
        # self.cbModifications.Bind(wx.EVT_CHECKBOX, self.onEventChoice)
        # self.cbDeletions.Bind(wx.EVT_CHECKBOX, self.onEventChoice)
        # self.cbRenames.Bind(wx.EVT_CHECKBOX, self.onEventChoice)
        # self.cbSubdirectories.Bind(wx.EVT_CHECKBOX, self.onEventChoice)
        # self.rbAll.Bind(wx.EVT_RADIOBUTTON, self.onTypes)
        # self.rbFiles.Bind(wx.EVT_RADIOBUTTON, self.onTypes)
        # self.rbDirectories.Bind(wx.EVT_RADIOBUTTON, self.onTypes)
        self.btnAddPattern.Bind(wx.EVT_BUTTON, self.addPattern)
        self.lbExPatterns.Bind(wx.EVT_LISTBOX_DCLICK, self.remPattern)
        self.btnSave.Bind(wx.EVT_BUTTON, self.save)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.cancel)
    
    def __del__(self):
        pass    
    
    # Virtual event handlers, overide them in your derived class
    # def onEventChoice(self, event):
    #     event.Skip()
    
    # def onTypes(self, event):
    #     event.Skip()

    def addPattern(self, event):
        pattern = self.txtPattern.GetValue()
        if pattern != "":
            listBoxCount = self.lbExPatterns.GetCount()
            self.lbExPatterns.InsertItems([pattern], listBoxCount)
            self.txtPattern.Clear()
        event.Skip()
    

    def remPattern(self, event):
        self.txtPattern.SetValue(self.lbExPatterns.GetStringSelection())
        self.lbExPatterns.Delete(self.lbExPatterns.GetSelection())
        event.Skip()


    def getEvents(self):
        results = []
        if self.cbNewFiles.GetValue():
            results.append("New Files")
        if self.cbModifications.GetValue():
            results.append("Modifications")
        if self.cbDeletions.GetValue():
            results.append("Deletions")
        if self.cbRenames.GetValue():
            results.append("Renames")
        return ", ".join(results)


    def getTypes(self):
        results = None
        if self.rbAll.GetValue():
            results = "Directories and Files"
        elif self.rbFiles.GetValue():
            results = "Files Only"
        elif self.rbDirectories.GetValue():
            results = "Directories Only"
        return results


    def clearAll(self):
        self.dirPicker.SetPath("Please enter a valid path...")
        self.cbNewFiles.SetValue(True)
        self.cbModifications.SetValue(False)
        self.cbDeletions.SetValue(False)
        self.cbRenames.SetValue(False)
        self.cbSubdirectories.SetValue(True)
        self.rbFiles.SetValue(True)
        self.txtPattern.Clear()
        self.lbExPatterns.Clear()


    def save(self, event):
        # self.Parent.clearLog(event)
        dirPath = self.dirPicker.GetPath()
        if dirPath != "Please enter a valid path...":
            events = self.getEvents()
            subDir = True if self.cbSubdirectories.GetValue() else False
            types = self.getTypes()
            exPatn = ", ".join(self.lbExPatterns.GetItems())
            self.Parent.addDirectoryToList([dirPath, events, subDir, types, 
                exPatn])
            self.clearAll()
        else:
            wx.MessageBox(u"Please specify a valid Directory!", 
                u"Infomation!", wx.OK | wx.ICON_EXCLAMATION)
            self.Parent.SetStatusText("Click the Browse Button")
        event.Skip()


    def cancel(self, event):
        self.clearAll()
        try:
            self.Destroy()
        except:
            pass
        event.Skip()


################################################################################
## Class mainFrame
################################################################################

class mainFrame(wx.Frame):
    def __init__(self, parent):
        # Variables ------------------------------------------------------------
        self.log_switch = False  # When log lenght is reached
        self.log_lenght = 33     # Lenght of log entries to show
        # self.isrunning = False   # Bool switch for RUN
        self.findData = wx.FindReplaceData()
        self.threads = []
        # ----------------------------------------------------------------------
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, 
            title = __application__ + " " + __version__, 
            pos = wx.DefaultPosition, 
            size = wx.Size( 640,800 ), 
            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        # Menu bar -------------------------------------------------------------
        self.menubar = wx.MenuBar(0)
        self.menu_dir = wx.Menu()  # Directory
        self.menu_log = wx.Menu()  # Log
        self.menu_pref = wx.Menu()  # Preferences
        self.menu_about = wx.Menu() # About
        
        # Menu Directory > Add
        self.mnuAddDir = wx.MenuItem(self.menu_dir, wx.ID_ANY, u"Add", 
            wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_dir.AppendItem(self.mnuAddDir)
        # Menu Directory > Remove
        self.mnuRemDir = wx.MenuItem(self.menu_dir, wx.ID_ANY, u"Remove", 
            wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_dir.AppendItem(self.mnuRemDir)

        # Menu Log > Clear
        self.mnuLogClear = wx.MenuItem(self.menu_dir, wx.ID_ANY, 
            u"Clear", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_log.AppendItem(self.mnuLogClear)
        # Menu Log > Save
        self.mnuLogSave = wx.MenuItem(self.menu_dir, wx.ID_ANY, 
            u"Save", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_log.AppendItem(self.mnuLogSave)
        # Menu Log > Load
        self.mnuLogLoad = wx.MenuItem(self.menu_dir, wx.ID_ANY, 
            u"Load", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_log.AppendItem(self.mnuLogLoad)
        # Menu Log > Find
        self.mnuLogFind = wx.MenuItem(self.menu_dir, wx.ID_ANY, 
            u"Find", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_log.AppendItem(self.mnuLogFind)
        
        # Menu Preferences > Log
        self.mnuLogPref = wx.MenuItem(self.menu_pref, wx.ID_ANY, u"Log", 
            wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_pref.AppendItem(self.mnuLogPref)
        # Menu Preferences > Email
        self.mnuEmailPref = wx.MenuItem(self.menu_pref, wx.ID_ANY, u"Email", 
            wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_pref.AppendItem(self.mnuEmailPref)
        # Menu Preferences > Command
        self.mnuCmdPref = wx.MenuItem(self.menu_pref, wx.ID_ANY, u"Command", 
            wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_pref.AppendItem(self.mnuCmdPref)

        # Menu About > TheWatcher
        self.mnuAbout = wx.MenuItem(self.menu_about, wx.ID_ANY, u"TheWatcher",
            wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_about.AppendItem(self.mnuAbout)

        self.menubar.Append(self.menu_dir, u"Directory")
        self.menubar.Append(self.menu_log, u"Log")
        self.menubar.Append(self.menu_pref, u"Preferences")
        self.menubar.Append(self.menu_about, u"About")
        self.SetMenuBar(self.menubar)
        # ----------------------------------------------------------------------
        rowSizer_a = wx.BoxSizer(wx.VERTICAL)
        
        colSizer_ab = wx.FlexGridSizer(0, 5, 0, 0)
        colSizer_ab.AddGrowableCol(1)
        colSizer_ab.SetFlexibleDirection(wx.BOTH)
        colSizer_ab.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        # Label Control --------------------------------------------------------
        self.lblPath = wx.StaticText(self, wx.ID_ANY, u" Directory Path ", 
            wx.DefaultPosition, wx.Size( -1,-1 ), 0)
        self.lblPath.Wrap(-1)
        self.lblPath.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        
        colSizer_ab.Add(self.lblPath, 1, wx.EXPAND, 5)
        # Directory Picker Control ---------------------------------------------
        self.dirPicker = wx.DirPickerCtrl(self, wx.ID_ANY, 
            u"Please enter a valid path...", u"Select a folder", 
            wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        colSizer_ab.Add(self.dirPicker, 1, wx.EXPAND, 5)
        # Button Add -----------------------------------------------------------
        self.btnAdd = wx.Button(self, wx.ID_ANY, u"Add", wx.DefaultPosition, 
            wx.Size(50,-1), 0)
        colSizer_ab.Add(self.btnAdd, 0, 0, 5)
        # Button Run -----------------------------------------------------------
        self.btnRun = wx.ToggleButton(self, wx.ID_ANY, u"RUN", 
            wx.DefaultPosition, wx.Size(60,-1), 0)
        #self.btnRun.SetValue(True) 
        colSizer_ab.Add(self.btnRun, 0, 0, 5)
        
        rowSizer_a.Add(colSizer_ab, 0, wx.EXPAND, 5)
        # Data View List Control -----------------------------------------------
        self.lstPath = dv.DataViewListCtrl(self, wx.ID_ANY, wx.DefaultPosition, 
            wx.Size(-1, 150))
        rowSizer_a.Add(self.lstPath, 0, wx.EXPAND, 5)
        # List Control Columns
        self.lstPath.AppendTextColumn('No', width=30)
        self.lstPath.AppendTextColumn('Directory', width=200)
        self.lstPath.AppendTextColumn('Events', width=100)
        self.lstPath.AppendToggleColumn('Subdirectories')
        self.lstPath.AppendTextColumn('Types', width=100)
        self.lstPath.AppendTextColumn('Exclude Patterns', width=100, 
            mode=dv.DATAVIEW_CELL_EDITABLE)
        # Tab Control ----------------------------------------------------------
        self.tabCtrl = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, 
            wx.DefaultSize, 0)
        # Log Panel
        self.tabLog = wx.Panel(self.tabCtrl, wx.ID_ANY, wx.DefaultPosition, 
            wx.DefaultSize, wx.TAB_TRAVERSAL)
        rowSizer_ab = wx.BoxSizer(wx.VERTICAL)
        # Text Box (Log) -------------------------------------------------------
        self.txtLog = wx.TextCtrl(self.tabLog, wx.ID_ANY, wx.EmptyString, 
            wx.DefaultPosition, wx.DefaultSize, 
            wx.TE_DONTWRAP | wx.TE_MULTILINE | wx.TE_RICH)

        # Custom wx.Log class
        self.log = MyLog(self.txtLog)  # Link to textCtrl
        wx.Log_SetActiveTarget(self.log)  # Redirect Log to textCtrl
        self.log.SetTimestamp("%d/%m/%Y %H:%M:%S %p")
        self.log.SetLogLevel(5)
        # self.log.SetVerbose(True)

        rowSizer_ab.Add(self.txtLog, 1, wx.EXPAND, 5)
        self.tabLog.SetSizer(rowSizer_ab)
        self.tabLog.Layout()
        rowSizer_ab.Fit(self.tabLog)
        self.tabCtrl.AddPage(self.tabLog, u"Log", False)
        
        rowSizer_a.Add(self.tabCtrl, 1, wx.EXPAND, 5)
        
        self.SetSizer(rowSizer_a)
        self.Layout()
        # Status Bar -----------------------------------------------------------
        self.statusBar = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

        # ------------------------------------------------------ Binding Events
        self.Bind(wx.EVT_MENU, self.addDirectory, self.mnuAddDir)
        self.Bind(wx.EVT_MENU, self.remDirectory, self.mnuRemDir)
        self.Bind(wx.EVT_TEXT, self.onLog)
        self.Bind(wx.EVT_MENU, self.clearLog, self.mnuLogClear)
        self.Bind(wx.EVT_MENU, self.findInLog, self.mnuLogFind)
        self.Bind(wx.EVT_MENU, self.saveLog, self.mnuLogSave)
        self.Bind(wx.EVT_MENU, self.loadLog, self.mnuLogLoad)
        self.Bind(wx.EVT_MENU, self.onAbout, self.mnuAbout)
        self.lstPath.Bind(dv.EVT_DATAVIEW_COLUMN_HEADER_CLICK, 
            self.remDirectory)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.quickAdd)
        # self.Bind(wx.EVT_TOGGLEBUTTON, self.run, self.btnRun)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.run_watchdog, self.btnRun)
        self.Bind(EVT_UPDATE_LOG, self.OnUpdate)        


    def __del__(self):
        pass


    def onAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = __application__ + " " + __version__
        info.Copyright = "(C) 2015, Angel Broadcasting Network Pte. Ltd."
        info.Description = wordwrap("A Simple Program to Watch Folders and "
            "Files. Complete with Logging and Notification Systems built in."
            " Able to chain commands and call external programs.", 340, 
            wx.ClientDC(self))
        info.WebSite = ("http://www.github.com/atvKumar", __author__)
        info.Developers = [__author__]
        info.Licence = "Apache License v2.0"
        wx.AboutBox(info)
        event.Skip()


    def addDirectoryToList(self, record):
        lstRowCount = self.lstPath.GetStore().GetCount()
        newRecord = [lstRowCount] + record
        self.lstPath.AppendItem(newRecord)


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


    def quickAdd(self, event):
        dirPath = self.dirPicker.GetPath()
        if dirPath != u"Please enter a valid path...":
            self.addDirectoryToList([dirPath, "New Files, Modifications", True, 
                "Files Only", None])
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


    def OnUpdate(self, event):
        wx.LogMessage(event.logmsg)


    def OnFind(self, event):
        wx.LogMessage(event.GetFindString())


    def OnFindClose(self, event):
        event.GetDialog().Destroy()


    # def run(self, event):
    #     # print event.GetId()
    #     # print event.IsChecked()
    #     self.threads.append(Watcher(self, "Thread1"))
    #     # self.threads.append(Watcher(self, "Thread2"))
    #     # self.threads.append(Watcher(self, "Thread3"))
    #     # self.threads.append(Watcher(self, "Thread4"))
    #     # self.threads.append(Watcher(self, "Thread5"))
    #     # self.threads.append(Watcher(self, "Thread6"))
    #     # self.threads.append(Watcher(self, "Thread7"))
    #     # self.threads.append(Watcher(self, "Thread8"))
    #     if event.IsChecked() is True:
    #         # Run Code here
    #         print "Running..."
    #         # self.isrunning = True
    #         for t in self.threads:
    #             t.Start()
    #     elif event.IsChecked() is False:
    #         # Stop Code here
    #         print "Stopped..."
    #         # self.isrunning = False
    #         for t in self.threads:
    #             t.Stop()


    def getPathListData(self):
        data = []
        lsCtrlStore = self.lstPath.GetStore()
        rowCount = lsCtrlStore.GetCount()
        # print "Total Rows =", rowCount
        for i in range(0, rowCount):
            row = []
            # print "Row %d ..." % i
            row.append(lsCtrlStore.GetValueByRow(i, 1))
            row.append(lsCtrlStore.GetValueByRow(i, 2))
            row.append(lsCtrlStore.GetValueByRow(i, 3))
            row.append(lsCtrlStore.GetValueByRow(i, 4))
            row.append(lsCtrlStore.GetValueByRow(i, 5))
            data.append(row)
        return data


    def run_watchdog(self, event):
        if event.IsChecked():
            # Get the number of entries in Path List
            lst = self.getPathListData()
            for i in range(0, len(lst)):
                # print lst[i][0]
                self.threads.append(Watcher(self, lst[i][0]))
            for t in self.threads:
                t.Start()
        else:
            for t in self.threads:
                t.Stop()
            print "Stopped..."
    

if __name__ == '__main__':
    app = wx.App(False)
    app.SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)
    app.SetAppName(__application__)
    app.SetVendorName(__author__)
    frame = mainFrame(None)
    frame.Show(True)
    app.MainLoop()