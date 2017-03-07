import notify2
import sys
import os
import os.path

_initted = False

def _init_nofify():
    """
    """

    global _initted
    if not notify2.init("Borgmatic notifications"):  
        raise ValueError('Notification initialize failed') 
    else: 
        _initted = True

def send_user_notification(cfg):
    """
    """

    DEFAULT_MSG="This is the default message"
    global _initted
    if cfg.get('notify_enable'): 
        if not _initted: 
            _init_nofify()
        
        if not cfg.get('notify_msg') and not cfg.get('notify_icon'):
            n = notify2.Notification("Borgmatic-Backup",DEFAULT_MSG)
        elif os.path.isfile(cfg.get('notify_icon')) and os.access(cfg.get('notify_icon'),os.R_OK):
            n = notify2.Notification("Borgmatic-Backup",cfg.get('notify_msg'),"file://" + cfg.get('notify_icon'))
        else: 
            n = notify2.Notification("Borgmatic-Backup",cfg.get('notify_msg'))
        n.show()
    else: 
        None

