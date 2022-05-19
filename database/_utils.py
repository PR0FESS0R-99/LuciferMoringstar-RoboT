import os


class temp(object):
    ME = None # User Id
    Bot_Username = None # Username
    Bot_Name = None # Full Name 
    BUTTONS = {} # AutoFilter
    CURRENT=int(os.environ.get("SKIP", 2)) # Skip Files
    CANCEL = False # Cancel Index
