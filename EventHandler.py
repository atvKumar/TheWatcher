import wx
import wx.lib.newevent
from watchdog.events import PatternMatchingEventHandler
from os import path

(UpdateLogEvent, EVT_UPDATE_LOG) = wx.lib.newevent.NewEvent()
################################################################################
## Class wxLogEventHandler
################################################################################

class wxLogEventHandler(PatternMatchingEventHandler):
    def __init__(self, win, patterns=None, ignore_patterns=None, 
                 ignore_directories=False, case_sensitive=False,
                 create=True, modify=True, delete=False, rename=False):
        self._case_sensitive = case_sensitive
        self._ignore_patterns = ignore_patterns
        self._patterns = patterns
        self._ignore_directories = ignore_directories
        self.win = win
        self.evt_onCreated = create
        self.evt_onModified = modify
        self.evt_onDeleted = delete
        self.evt_onRenamed = rename
        # print "wxLogEventHandler >", self._ignore_patterns
        # print "wxLogEventHandler >", self._patterns

    def process(self, event):
        # print event.src_path, ">", event.event_type, type(event)
        what = 'Directory' if event.is_directory else 'File'

        if event.event_type == 'created' and self.evt_onCreated:
            # print what, "Created! |", event.src_path
            msg = UpdateLogEvent(logmsg="Created! | %s" % event.src_path, 
                    evt_type='created', filename=path.basename(event.src_path))
            wx.PostEvent(self.win, msg)
        if event.event_type == 'modified' and self.evt_onModified:
            # print what, "Modified! |", event.src_path
            msg = UpdateLogEvent(logmsg="Modified! | %s" % event.src_path, 
                    evt_type='modified', filename=path.basename(event.src_path))
            wx.PostEvent(self.win, msg)
        if event.event_type == 'deleted' and self.evt_onDeleted:
            # print what, "Deleted! |", event.src_path
            msg = UpdateLogEvent(logmsg="Deleted! | %s" % event.src_path, 
                    evt_type='deleted', filename=path.basename(event.src_path))
            wx.PostEvent(self.win, msg)
        if event.event_type == 'moved' and self.evt_onRenamed:
            # print what, "Moved! |", event.src_path, event.dest_path
            msg = UpdateLogEvent(logmsg="Moved! | %s to %s" % 
                                 (event.src_path, event.dest_path), 
                                 evt_type='moved', 
                                 filename=path.basename(event.dest_path))
            wx.PostEvent(self.win, msg)

    def on_moved(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)