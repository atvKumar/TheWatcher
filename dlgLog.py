import wx
import wx.propgrid as pg
from __versions__ import IS_OSX, IS_WINDOWS
from os import stat, remove
from os.path import isfile, join as joinPath


def getFileSize(filepath):
    """Calculate size of a file size in KB/MB/GB/TB"""
    file_bytes = stat(filepath).st_size
    if IS_OSX:
        file_blocks = stat(filepath).st_blocks
        if file_bytes < 1024 * 1024: #KB
            return str(round(file_blocks * 512e-3, 1)) + ' KB'
        elif file_bytes < 1024 * 1024 * 1024: #MB
            return str(round(file_blocks * 512e-6, 1 )) + ' MB'
        elif file_bytes < 1024 * 1024 * 1024 * 1024: #GB
            return str(round(file_blocks * 512e-6 / 1000, 2)) + ' GB'
        elif file_bytes < 1024 * 1024 * 1024 * 1024 * 1024 : #TB
            return str(round(file_blocks * 512e-6 / 1000 / 1000, 2 )) + ' TB'
    elif IS_WINDOWS:
        file_blocks = 0
        if file_bytes < 1024 * 1024: #KB
            return str(round(file_bytes / 1024.0, 1)) + ' KB'
        elif file_bytes < 1024 * 1024 * 1024: #MB
            return str(round(file_bytes / 1024 / 1024.0, 1)) + ' MB'
        elif file_bytes < 1024 * 1024 * 1024 * 1024: #GB
            return str(round(file_bytes / 1024 / 1024 / 1024.0, 2)) + ' GB'
        elif file_bytes < 1024 * 1024 * 1024 * 1024 * 1024 : #TB
            return str(round(file_bytes / 1024 / 1024 / 1024 / 1024.0, 2))+' TB'


class log_dialog (wx.Dialog):
	
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Logging", 
			pos=wx.DefaultPosition, size=wx.DefaultSize, 
			style=wx.DEFAULT_DIALOG_STYLE)
		self.parent = parent
		self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
		
		sizer_A = wx.BoxSizer(wx.VERTICAL)
		
		sizer_AA = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Log File"), 
			wx.VERTICAL)
		
		sizer_AAA = wx.FlexGridSizer(0, 2, 0, 0)
		sizer_AAA.AddGrowableCol(1)
		sizer_AAA.SetFlexibleDirection(wx.BOTH)
		sizer_AAA.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		self.cb_Logging = wx.CheckBox(self, wx.ID_ANY, u"File Logging Enabled", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_AAA.Add(self.cb_Logging, 0, wx.ALL, 5)
		
		
		sizer_AAA.AddSpacer(( 0, 0), 1, wx.EXPAND, 5)
		
		self.lbl_LogPath = wx.StaticText(self, wx.ID_ANY, u"Log File Path:", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_LogPath.Wrap(-1)
		sizer_AAA.Add(self.lbl_LogPath, 0, wx.ALL, 5)
		
		self.dp_LogPath = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, 
			u"Select a folder", wx.DefaultPosition, wx.DefaultSize, 
			wx.DIRP_DEFAULT_STYLE)
		self.dp_LogPath.SetMinSize(wx.Size( 350,-1 ))
		
		sizer_AAA.Add(self.dp_LogPath, 0, wx.ALL, 5)
		
		self.cb_Timestamp = wx.CheckBox(self, wx.ID_ANY, u"Timestamp Enabled", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.cb_Timestamp.SetValue(True) 
		sizer_AAA.Add(self.cb_Timestamp, 0, wx.ALL, 5)
		
		self.tc_Timestamp = wx.TextCtrl(self, wx.ID_ANY, "%d/%m/%Y %I:%M:%S %p", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_AAA.Add(self.tc_Timestamp, 0, wx.ALL|wx.EXPAND, 5)
		
		self.lbl_LogFormat = wx.StaticText(self, wx.ID_ANY, u"Output Format", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_LogFormat.Wrap(-1)
		sizer_AAA.Add(self.lbl_LogFormat, 0, wx.ALL, 5)
		
		self.tc_LogFormat = wx.TextCtrl(self, wx.ID_ANY, 
			"%(asctime)-15s - %(levelname)s - %(message)s", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_AAA.Add(self.tc_LogFormat, 0, wx.ALL|wx.EXPAND, 5)
		
		sizer_AAAA = wx.BoxSizer(wx.VERTICAL)
		
		
		sizer_AAAA.AddSpacer(( 0, 0), 1, wx.EXPAND, 5)
		
		self.btn_CheckLogs = wx.Button(self, wx.ID_ANY, u"Check Old Logs ", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_AAAA.Add(self.btn_CheckLogs, 0, 
			wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 2)
		
		self.btn_ClearLogs = wx.Button(self, wx.ID_ANY, u"Clear Log Now", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_AAAA.Add(self.btn_ClearLogs, 0, 
			wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 2)
		
		
		sizer_AAA.Add(sizer_AAAA, 1, 
			wx.ALIGN_CENTER|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
		
		self.pg_LogDetails = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, 
			wx.DefaultSize, wx.propgrid.PG_BOLD_MODIFIED|\
			wx.propgrid.PG_HIDE_MARGIN) #|wx.propgrid.PG_STATIC_LAYOUT
		self.pgItem_Name = self.pg_LogDetails.Append(pg.StringProperty(u"Name", 
			u"Name")) 
		self.pgItem_Size = self.pg_LogDetails.Append(pg.StringProperty(u"Size", 
			u"Size")) 
		sizer_AAA.Add(self.pg_LogDetails, 0, wx.ALL|wx.EXPAND, 5)
		
		
		sizer_AA.Add(sizer_AAA, 1, wx.EXPAND, 5)
		
		
		sizer_A.Add(sizer_AA, 1, wx.EXPAND, 5)
		
		sizer_AB = wx.StdDialogButtonSizer()
		self.sizer_ABSave = wx.Button(self, wx.ID_SAVE)
		sizer_AB.AddButton(self.sizer_ABSave)
		self.sizer_ABCancel = wx.Button(self, wx.ID_CANCEL)
		sizer_AB.AddButton(self.sizer_ABCancel)
		sizer_AB.Realize();
		
		sizer_A.Add(sizer_AB, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 
			10)
		
		
		self.SetSizer(sizer_A)
		self.Layout()
		sizer_A.Fit(self)
		
		self.Centre(wx.BOTH)
		
		# Connect Events
		self.Bind(wx.EVT_INIT_DIALOG, self.dlgInit)
		self.btn_CheckLogs.Bind(wx.EVT_BUTTON, self.checkOldLogs)
		self.btn_ClearLogs.Bind(wx.EVT_BUTTON, self.clearLogs)
		self.sizer_ABCancel.Bind(wx.EVT_BUTTON, self.cancel)
		self.sizer_ABSave.Bind(wx.EVT_BUTTON, self.save)
	
	def __del__(self):
		pass


	def dlgInit(self, event):
		if self.parent.logData != None:
			# data = self.parent.logData
			self.cb_Logging.SetValue(self.parent.logData["log"])
			self.dp_LogPath.SetPath(self.parent.logData["path"])
			self.cb_Timestamp.SetValue(self.parent.logData["timestamp"])
			self.tc_Timestamp.SetValue(self.parent.logData["ts_format"])
			self.tc_LogFormat.SetValue(self.parent.logData["log_format"])
	
	
	# Virtual event handlers, overide them in your derived class
	def checkOldLogs(self, event):
		path = self.dp_LogPath.GetPath()
		if path:
			logFile = joinPath(path, "TheWatcher.log")
			if isfile(logFile):
				self.pg_LogDetails.SetPropertyValue("Name", "TheWatcher.log")
				# size = "%d %s" % (stat(logFile).st_size, "bytes")
				self.pg_LogDetails.SetPropertyValue("Size", getFileSize(logFile))

	
	def clearLogs(self, event):
		path = self.dp_LogPath.GetPath()
		if path:
			logFile = joinPath(path, "TheWatcher.log")
			if isfile(logFile):
				remove(logFile)

	
	def cancel(self, event):
		event.Skip()

	
	def save(self, event):
		data = {"log" : self.cb_Logging.GetValue(),
				"path" : self.dp_LogPath.GetPath(),
				"timestamp" : self.cb_Timestamp.GetValue(),
				"ts_format" : self.tc_Timestamp.GetValue(),
				"log_format" : self.tc_LogFormat.GetValue()}
		self.parent.logData = data
		self.parent.setupFileLogging()
		self.Close()

