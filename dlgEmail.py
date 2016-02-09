import wx


class email_dialog(wx.Dialog):
	
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=wx.ID_ANY, 
			title = u"Email Settings", pos=wx.DefaultPosition, 
			size = wx.DefaultSize, 
			style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
		self.parent = parent
		self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
		
		sizer_main = wx.BoxSizer(wx.VERTICAL)
		
		sizer_A = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, 
			u"Account Settings"), wx.VERTICAL)
		
		sizer_AA = wx.FlexGridSizer(0, 6, 0, 0)
		sizer_AA.AddGrowableCol(1)
		sizer_AA.AddGrowableCol(3)
		sizer_AA.AddGrowableCol(5)
		sizer_AA.SetFlexibleDirection(wx.BOTH)
		sizer_AA.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		self.lbl_smtp = wx.StaticText(self, wx.ID_ANY, u"Smtp", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_smtp.Wrap(-1)
		sizer_AA.Add(self.lbl_smtp, 0, wx.ALL, 5)
		
		self.tc_smtp = wx.TextCtrl(self, wx.ID_ANY, u"smtp.gmail.com:587", 
			wx.DefaultPosition, wx.Size(150,-1), 0)
		sizer_AA.Add(self.tc_smtp, 1, wx.ALL|wx.EXPAND, 5)
		
		self.lbl_user = wx.StaticText(self, wx.ID_ANY, u"User", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_user.Wrap(-1)
		sizer_AA.Add(self.lbl_user, 0, wx.ALL, 5)
		
		self.tc_user = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_AA.Add(self.tc_user, 1, wx.ALL|wx.EXPAND, 5)
		
		self.lbl_password = wx.StaticText(self, wx.ID_ANY, u"Password", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_password.Wrap(-1)
		sizer_AA.Add(self.lbl_password, 0, wx.ALL, 5)
		
		self.tc_password = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
			wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD)
		sizer_AA.Add(self.tc_password, 1, wx.ALL|wx.EXPAND, 5)
		
		
		sizer_A.Add(sizer_AA, 1, wx.EXPAND, 5)
		
		
		sizer_main.Add(sizer_A, 0, wx.EXPAND, 5)
		
		sizer_B = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, 
			u"Email Settings"), wx.VERTICAL)
		
		self.cb_enableEmail = wx.CheckBox(self, wx.ID_ANY, 
			u"Sending Email Enabled", wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_B.Add(self.cb_enableEmail, 0, wx.ALL, 5)
		
		sizer_BA = wx.FlexGridSizer(0, 4, 0, 0)
		sizer_BA.AddGrowableCol(2)
		sizer_BA.SetFlexibleDirection(wx.BOTH)
		sizer_BA.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		self.lbl_sendTo = wx.StaticText(self, wx.ID_ANY, u"Send To:", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_sendTo.Wrap(-1)
		sizer_BA.Add(self.lbl_sendTo, 0, wx.ALL, 5)
		
		self.tc_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_BA.Add(self.tc_name, 0, wx.ALL, 5)
		self.tc_name.Disable() # TODO: Name support in email sending
		
		self.tc_emailAddress = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
			wx.DefaultPosition, wx.Size( 250,-1 ), 0)
		sizer_BA.Add(self.tc_emailAddress, 1, wx.ALL|wx.EXPAND, 5)
		
		self.btn_Add = wx.Button(self, wx.ID_ANY, u"Add", wx.DefaultPosition, 
			wx.Size(50,-1), 0)
		sizer_BA.Add(self.btn_Add, 0, wx.ALL, 5)
		
		
		sizer_B.Add(sizer_BA, 0, wx.EXPAND, 5)
		
		sizer_BB = wx.FlexGridSizer(4, 2, 0, 0)
		sizer_BB.AddGrowableCol(1)
		sizer_BB.SetFlexibleDirection(wx.BOTH)
		sizer_BB.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		self.lbl_recipients = wx.StaticText(self, wx.ID_ANY, u"Recipients", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_recipients.Wrap(-1)
		sizer_BB.Add(self.lbl_recipients, 0, wx.ALL, 5)
		
		self.tc_emailTO = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
			wx.DefaultPosition, wx.Size( 360,100 ), wx.TE_MULTILINE)
		sizer_BB.Add(self.tc_emailTO, 1, wx.ALL|wx.EXPAND, 5)
		
		self.lbl_subject = wx.StaticText(self, wx.ID_ANY, u"Subject:", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_subject.Wrap(-1)
		sizer_BB.Add(self.lbl_subject, 0, wx.ALL, 5)
		
		self.tc_emailSubject = wx.TextCtrl(self, wx.ID_ANY, 
			"TheWatcher : {pathType} {filename} {evt_type} at {timestamp}", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_BB.Add(self.tc_emailSubject, 1, wx.ALL|wx.EXPAND, 5)
		
		self.lbl_message = wx.StaticText(self, wx.ID_ANY, u"Message:", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_message.Wrap(-1)
		sizer_BB.Add(self.lbl_message, 0, wx.ALL, 5)
		
		self.tc_emailMessage = wx.TextCtrl(self, wx.ID_ANY, 
			"{pathType} {evt_type} : {evt_src} at {timestamp}", 
			wx.DefaultPosition, wx.Size( -1,100 ), wx.TE_MULTILINE)
		sizer_BB.Add(self.tc_emailMessage, 1, wx.ALL|wx.EXPAND, 5)
		
		self.lbl_attachments = wx.StaticText(self, wx.ID_ANY, u"Attachments", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl_attachments.Wrap(-1)
		sizer_BB.Add(self.lbl_attachments, 0, wx.ALL, 5)
		
		self.fp_attachments = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString,
			u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, 
			wx.FLP_DEFAULT_STYLE)
		sizer_BB.Add(self.fp_attachments, 1, wx.ALL|wx.EXPAND, 5)
		
		
		sizer_B.Add(sizer_BB, 0, wx.EXPAND, 5)
		
		
		sizer_main.Add(sizer_B, 1, wx.EXPAND, 5)
		
		sizer_C = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Rules"), 
			wx.VERTICAL)
		
		sizer_CA = wx.FlexGridSizer(0, 3, 0, 0)
		sizer_CA.SetFlexibleDirection(wx.BOTH)
		sizer_CA.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		self.cb_delay = wx.CheckBox(self, wx.ID_ANY, u"Wait for", 
			wx.DefaultPosition, wx.DefaultSize, 0)
		sizer_CA.Add(self.cb_delay, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		
		self.delay = wx.SpinCtrl(self, wx.ID_ANY, "1", 
			wx.DefaultPosition, wx.Size(50,-1), wx.SP_ARROW_KEYS, 1, 1000, 0)
		sizer_CA.Add(self.delay, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		
		self.lbl_delayTxt = wx.StaticText(self, wx.ID_ANY, 
			u"Events before sending Email", wx.DefaultPosition, wx.DefaultSize, 
			0)
		self.lbl_delayTxt.Wrap(-1)
		sizer_CA.Add(self.lbl_delayTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		
		
		sizer_C.Add(sizer_CA, 1, wx.EXPAND, 5)
		
		
		sizer_main.Add(sizer_C, 0, wx.EXPAND, 5)
		
		sizer_D = wx.StdDialogButtonSizer()
		self.sizer_DSave = wx.Button(self, wx.ID_SAVE)
		sizer_D.AddButton(self.sizer_DSave)
		self.sizer_DCancel = wx.Button(self, wx.ID_CANCEL)
		sizer_D.AddButton(self.sizer_DCancel)
		sizer_D.Realize();
		
		sizer_main.Add(sizer_D, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
		
		
		self.SetSizer(sizer_main)
		self.Layout()
		sizer_main.Fit(self)
		
		self.Centre(wx.BOTH)
		
		# Connect Events
		self.btn_Add.Bind(wx.EVT_BUTTON, self.addEmailAddress)
		self.sizer_DCancel.Bind(wx.EVT_BUTTON, self.cancel)
		self.sizer_DSave.Bind(wx.EVT_BUTTON, self.save)

		if self.parent.emailData != None:
			self.setData(self.parent.emailData)
	
	def __del__(self):
		pass

	
	def addEmailAddress(self, event):
		self.tc_emailTO.AppendText(self.tc_emailAddress.GetValue() + "\n")
		self.tc_emailAddress.Clear()


	def setData(self, data):
		""" Sets the Dialog with the given Data """
		self.tc_smtp.SetValue(data["smtpServer"])
		self.tc_user.SetValue(data["userName"])
		self.tc_password.SetValue(data["password"])
		self.cb_enableEmail.SetValue(data["sendEmail"])
		self.tc_emailTO.SetValue(data["emailTO"])
		self.tc_emailSubject.SetValue(data["emailSubject"])
		self.tc_emailMessage.SetValue(data["emailMessage"])
		self.fp_attachments.SetPath(data["attachments"])
		self.cb_delay.SetValue(data["delay"])
		self.delay.SetValue(data["delayCount"])


	def getData(self):
		""" Returns Data Retrieved from the Dialog """
		return {"smtpServer": self.tc_smtp.GetValue(),
				"userName": self.tc_user.GetValue(),
				"password": self.tc_password.GetValue(),
				"sendEmail": self.cb_enableEmail.GetValue(),
				"emailTO": self.tc_emailTO.GetValue(),
				"emailSubject": self.tc_emailSubject.GetValue(),
				"emailMessage": self.tc_emailMessage.GetValue(),
				"attachments": self.fp_attachments.GetPath(),
				"delay": self.cb_delay.GetValue(),
				"delayCount": self.delay.GetValue()} 


	def cancel(self, event):
		event.Skip()


	def save(self, event):
		self.parent.emailData = self.getData()
		self.Close()