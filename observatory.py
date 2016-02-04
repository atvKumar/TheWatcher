import thread
from watchdog.observers import Observer
from EventHandler import wxLogEventHandler
################################################################################
## Class Watcher
################################################################################

class Watcher:
    def __init__(self, win, watchpath, patterns=None, ignore_patterns=None, 
                 ignore_directories=False, case_sensitive=False,
                 create=True, modify=True, delete=False, rename=False, 
                 subDir=True):
        self.win = win
        self.path = watchpath
        # self.ignore_patterns = ignore_patterns
        # self.patterns = patterns
        self.event_handler = wxLogEventHandler(self.win, patterns, 
                                ignore_patterns, ignore_directories, 
                                case_sensitive, create, modify, delete, rename)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=subDir)
        # print "Watcher created ", self.win, self.path


    def Start(self):
        self.running = True
        thread.start_new_thread(self.observer.start, ())
        # self.observer.start()
        print "Thread %s Started..." % self.path
        # print "Ignore Pattern", self.ignore_patterns
        # print "Watch Pattern", self.patterns


    def Stop(self):
        self.running = False
        self.observer.stop()
        print "Thread %s Stopped..." % self.path


    def IsRunning(self):
        return self.running