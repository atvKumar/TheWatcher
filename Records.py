import wx
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