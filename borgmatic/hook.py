import subprocess
import os
import os.path

def run_user_hook(cfg):
    if cfg.get('hook_enable'):
        if os.path.isfile(cfg.get('hook_path')) and os.access(cfg.get('hook_path'),os.X_OK):
            if cfg.get('hook_args'):
                subprocess.run(args= [cfg.get('hook_path'),cfg.get('hook_args')], check=True)
            else:
                subprocess.run(args= [cfg.get('hook_path')], check=True)
        else:
            raise FileNotFoundError('User Script {} not found or executable'.format(cfg.get('hook_path')))
