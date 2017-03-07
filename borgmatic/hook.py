import subprocess

def run_user_hook(cfg):
    print("This is hook")
    print(cfg.get('hook_path'))
    return 1
