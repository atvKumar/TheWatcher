import wx
import wx.propgrid as pg


class log_dialog (wx.Dialog):
	
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Logging", 
			pos=wx.DefaultPosition, size=wx.DefaultSize, 
			style=wx.DEFAULT_DIALOG_STYLE)
		
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
		
		self.tc_Timestamp = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_AAA.Add(self.tc_Timestamp, 0, wx.ALL|wx.EXPAND, 5)
		
		self.lbl_LogFormat = wx.StaticText(self, wx.ID_ANY, u"Output Format", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_LogFormat.Wrap(-1)
		sizer_AAA.Add(self.lbl_LogFormat, 0, wx.ALL, 5)
		
		self.tc_LogFormat = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
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
			wx.propgrid.PG_HIDE_MARGIN|wx.propgrid.PG_STATIC_LAYOUT)
		self.pgItem_Name = self.pg_LogDetails.Append(pg.StringProperty(u"Name", 
			u"Name")) 
		self.pgItem_Size = self.pg_LogDetails.Append(pg.StringProperty(u"Size", 
			u"Size")) 
		sizer_AAA.Add(self.pg_LogDetails, 0, wx.ALL|wx.EXPAND, 5)
		
		
		sizer_AA.Add(sizer_AAA, 1, wx.EXPAND, 5)
		
		
		sizer_A.Add(sizer_AA, 1, wx.EXPAND, 5)
		
		sizer_AB = wx.StdDialogButtonSizer()
		self.sizer_ABSave = wx.Button(self, wx.ID_SAVE )
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
		self.btn_CheckLogs.Bind(wx.EVT_BUTTON, self.checkOldLogs)
		self.btn_ClearLogs.Bind(wx.EVT_BUTTON, self.clearLogs)
		self.sizer_ABCancel.Bind(wx.EVT_BUTTON, self.cancel)
		self.sizer_ABSave.Bind(wx.EVT_BUTTON, self.save)
	
	def __del__(self):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def checkOldLogs(self, event):
		event.Skip()
	
	def clearLogs(self, event):
		event.Skip()
	
	def cancel(self, event):
		event.Skip()
	
	def save(self, event):
		event.Skip()
