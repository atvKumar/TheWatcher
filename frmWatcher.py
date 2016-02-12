import wx
import wx.dataview as dv
from __versions__ import __author__, __application__, __version__
from wx.lib.wordwrap import wordwrap
from wxEventHandler import EVT_UPDATE_LOG
from logs import MyLog


class mainFrame(wx.Frame):
    def __init__(self, parent):
        # Variables ------------------------------------------------------------
        self.log_switch = False  # When log lenght is reached
        self.log_lenght = 33     # Lenght of log entries to show
        # self.isrunning = False   # Bool switch for RUN
        self.findData = wx.FindReplaceData()
        self.threads = []
        self.emailData = None    # Email Settings Dialog Data Dict
        self.eventCount = 0
        self.logData = None
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
        self.lstPath.AppendTextColumn('Ignore Patterns', width=100, 
            mode=dv.DATAVIEW_CELL_EDITABLE)
        self.lstPath.AppendTextColumn('Watch Patterns', width=100, 
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
        self.log.SetTimestamp("%d/%m/%Y %I:%M:%S %p")
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
        self.Bind(wx.EVT_TEXT, self.onGuiLogUpdate)
        self.Bind(wx.EVT_MENU, self.clearLog, self.mnuLogClear)
        self.Bind(wx.EVT_MENU, self.findInLog, self.mnuLogFind)
        self.Bind(wx.EVT_MENU, self.saveLog, self.mnuLogSave)
        self.Bind(wx.EVT_MENU, self.loadLog, self.mnuLogLoad)
        self.Bind(wx.EVT_MENU, self.emailSettings, self.mnuEmailPref)
        self.Bind(wx.EVT_MENU, self.logSettings, self.mnuLogPref)
        self.Bind(wx.EVT_MENU, self.onAbout, self.mnuAbout)
        self.lstPath.Bind(dv.EVT_DATAVIEW_COLUMN_HEADER_CLICK, 
            self.remDirectory)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.quickAdd)
        # self.Bind(wx.EVT_TOGGLEBUTTON, self.run, self.btnRun)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.run_watchdog, self.btnRun)
        self.Bind(EVT_UPDATE_LOG, self.onUpdate) 
        # UpdateLogEvent 
        # self.setupFileLogging()


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


    def addDirectory(self, event):
        pass


    def remDirectory(self, event):
        pass


    def quickAdd(self, event):
        pass


    def clearLog(self, event):
        pass


    def onGuiLogUpdate(self, event):
        pass


    def saveLog(self, event):
        pass


    def loadLog(self, event):
        pass


    def findInLog(self, event):
        pass


    def emailSettings(self, event):
        pass


    def logSettings(self, event):
        pass


    def setupFileLogging(self):
        pass


    def onUpdate(self, event):
        pass


    def run_watchdog(self, event):
        pass
