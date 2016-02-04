import wx


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
        self.rbDirectories.Disable() # Disabled
        
        colGrpSizer_b.Add(rowSizer_ad, 0, wx.EXPAND, 5)
        
        
        colSizer_main.Add(colGrpSizer_b, 0, wx.EXPAND, 5)
        
        colGrpSizer_c = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Filters"), wx.VERTICAL)
        
        rowSizer_ae = wx.FlexGridSizer(0, 4, 0, 0)
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
        
        self.btnIgnorePattern = wx.Button(self, wx.ID_ANY, u"Ignore", 
            wx.DefaultPosition, wx.Size( 70,-1 ), 0)
        rowSizer_ae.Add(self.btnIgnorePattern, 0, wx.ALL, 5)

        self.btnWatchPattern = wx.Button(self, wx.ID_ANY, u"Watch", 
            wx.DefaultPosition, wx.Size( 70,-1 ), 0)
        rowSizer_ae.Add(self.btnWatchPattern, 0, wx.ALL, 5)

        
        colGrpSizer_c.Add(rowSizer_ae, 0, wx.EXPAND, 5)
        
        rowSizer_af = wx.FlexGridSizer(1, 0, 0, 0)
        rowSizer_af.AddGrowableCol(0)
        rowSizer_af.SetFlexibleDirection(wx.BOTH)
        rowSizer_af.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        
        lbExPatternsChoices = []
        self.lbIgnorePatterns = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, 
            wx.Size(-1,140), lbExPatternsChoices, wx.LB_NEEDED_SB)
        rowSizer_af.Add(self.lbIgnorePatterns, 1, wx.ALL | wx.EXPAND, 5)
        
        self.lbWatchPatterns = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, 
            wx.Size(220,140), lbExPatternsChoices, wx.LB_NEEDED_SB)
        rowSizer_af.Add(self.lbWatchPatterns, 1, wx.ALL | wx.EXPAND, 5)
        
        
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
        self.btnIgnorePattern.Bind(wx.EVT_BUTTON, self.addIgnorePattern)
        self.lbIgnorePatterns.Bind(wx.EVT_LISTBOX_DCLICK, self.remIgnorePattern)
        self.btnWatchPattern.Bind(wx.EVT_BUTTON, self.addWatchPattern)
        self.lbWatchPatterns.Bind(wx.EVT_LISTBOX_DCLICK, self.remWatchPattern)
        self.btnSave.Bind(wx.EVT_BUTTON, self.save)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.cancel)
    
    def __del__(self):
        pass    
    

    def addIgnorePattern(self, event):
        pattern = self.txtPattern.GetValue()
        if pattern != "":
            listBoxCount = self.lbIgnorePatterns.GetCount()
            self.lbIgnorePatterns.InsertItems([pattern], listBoxCount)
            self.txtPattern.Clear()
        event.Skip()
    

    def remIgnorePattern(self, event):
        self.txtPattern.SetValue(self.lbIgnorePatterns.GetStringSelection())
        self.lbIgnorePatterns.Delete(self.lbIgnorePatterns.GetSelection())
        event.Skip()


    def addWatchPattern(self, event):
        pattern = self.txtPattern.GetValue()
        if pattern != "":
            listBoxCount = self.lbWatchPatterns.GetCount()
            self.lbWatchPatterns.InsertItems([pattern], listBoxCount)
            self.txtPattern.Clear()
        event.Skip()
    

    def remWatchPattern(self, event):
        self.txtPattern.SetValue(self.lbWatchPatterns.GetStringSelection())
        self.lbInPatterns.Delete(self.lbWatchPatterns.GetSelection())
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
        self.lbIgnorePatterns.Clear()
        self.lbWatchPatterns.Clear()


    def save(self, event):
        # self.Parent.clearLog(event)
        dirPath = self.dirPicker.GetPath()
        if dirPath != "Please enter a valid path...":
            events = self.getEvents()
            subDir = True if self.cbSubdirectories.GetValue() else False
            types = self.getTypes()
            _ignore_patterns = self.lbIgnorePatterns.GetItems()
            _watch_patterns = self.lbWatchPatterns.GetItems()
            # print "Add Directory >", _ignore_patterns, _watch_patterns
            exPatn = ", ".join(_ignore_patterns) if _ignore_patterns != [] \
                        else None
            watchPatn = ", ".join(_watch_patterns) if _watch_patterns != [] \
                        else None
            self.Parent.addDirectoryToList([dirPath, events, subDir, types, 
                exPatn, watchPatn])
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