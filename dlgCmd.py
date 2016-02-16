import wx


class command_dialog (wx.Dialog):
	
	def __init__(self, parent):
		wx.Dialog.__init__ (self, parent, id = wx.ID_ANY, title = u"Commands", 
			pos = wx.DefaultPosition, size = wx.DefaultSize, 
			style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
		self.parent = parent
		self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
		
		sizer_A = wx.BoxSizer(wx.VERTICAL)
		
		sizer_A.SetMinSize(wx.Size(400,-1)) 
		sizer_AA = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, 
			u"Application"), wx.VERTICAL)
		
		sizer_AAA = wx.FlexGridSizer(0, 2, 0, 0)
		sizer_AAA.AddGrowableCol(1)
		sizer_AAA.SetFlexibleDirection(wx.BOTH)
		sizer_AAA.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		self.lbl_Execute = wx.StaticText(self, wx.ID_ANY, u"Execute", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_Execute.Wrap(-1)
		sizer_AAA.Add(self.lbl_Execute, 0, wx.ALL, 5)
		
		self.fp_Command = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, 
			u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, 
			wx.FLP_DEFAULT_STYLE)
		sizer_AAA.Add(self.fp_Command, 0, wx.ALL|wx.EXPAND, 5)
		
		self.lbl_Parameters = wx.StaticText(self, wx.ID_ANY, u"Parameters", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_Parameters.Wrap(-1)
		sizer_AAA.Add(self.lbl_Parameters, 0, wx.ALL, 5)
		
		self.tc_Parameters = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_AAA.Add(self.tc_Parameters, 0, wx.ALL|wx.EXPAND, 5)
		
		
		sizer_AA.Add(sizer_AAA, 1, wx.EXPAND, 5)
		
		
		sizer_A.Add(sizer_AA, 1, wx.EXPAND, 5)
		
		sizer_B = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Options"), 
			wx.VERTICAL)
		
		self.cb_Quiet = wx.CheckBox(self, wx.ID_ANY, 
			u"Start Application Silently in the Background (Hide Shell)", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_B.Add(self.cb_Quiet, 0, wx.ALL, 5)
		
		self.cb_Sequence = wx.CheckBox(self, wx.ID_ANY, 
			u"Wait for Application to Exit after each Event"
			" (Sequential Execution)", wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_B.Add(self.cb_Sequence, 0, wx.ALL, 5)
		
		
		sizer_A.Add(sizer_B, 1, wx.EXPAND, 5)
		
		sizer_C = wx.StdDialogButtonSizer()
		self.sizer_CSave = wx.Button(self, wx.ID_SAVE)
		sizer_C.AddButton(self.sizer_CSave)
		self.sizer_CCancel = wx.Button(self, wx.ID_CANCEL)
		sizer_C.AddButton(self.sizer_CCancel)
		sizer_C.Realize();
		
		sizer_A.Add(sizer_C, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5)
		
		
		self.SetSizer(sizer_A)
		self.Layout()
		sizer_A.Fit(self)
		
		self.Centre(wx.BOTH)
		self.cb_Quiet.SetValue(True)
		self.cb_Sequence.SetValue(True)
		self.cb_Sequence.Disable()
		# Connect Events
		self.Bind(wx.EVT_INIT_DIALOG, self.dlgInit)
		self.sizer_CCancel.Bind(wx.EVT_BUTTON, self.cancel)
		self.sizer_CSave.Bind(wx.EVT_BUTTON, self.save)
	
	def __del__(self):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def dlgInit(self, event):
		if self.parent.cmdData != None:
			self.fp_Command.SetPath(self.parent.cmdData["cmd"])
			self.tc_Parameters.SetValue(self.parent.cmdData["flags"])
			self.cb_Quiet.SetValue(self.parent.cmdData["shell"])
			self.cb_Sequence.SetValue(self.parent.cmdData["seq"])
	

	def cancel(self, event):
		event.Skip()
	

	def save(self, event):
		if self.fp_Command.GetPath() == u'':
			self.parent.cmdData = None
			self.Close()
			return
		data = {"cmd": self.fp_Command.GetPath(),
				"flags": self.tc_Parameters.GetValue(),
				"shell": self.cb_Quiet.GetValue(),
				"seq": self.cb_Sequence.GetValue()}
		self.parent.cmdData = data
		self.Close()
	
