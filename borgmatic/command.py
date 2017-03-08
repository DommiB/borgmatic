from __future__ import print_function
from argparse import ArgumentParser
import os
from subprocess import CalledProcessError
import sys

from borgmatic import borg
from borgmatic.config import parse_configuration, split_configs, CONFIG_FORMAT
from borgmatic.hook import run_user_hook 
from borgmatic.notification import send_user_notification 


DEFAULT_CONFIG_FILENAME = '/etc/borgmatic/config'
DEFAULT_EXCLUDES_FILENAME = '/etc/borgmatic/excludes'


def parse_arguments(*arguments):
    '''
    Given the name of the command with which this script was invoked and command-line arguments,
    parse the arguments and return them as an ArgumentParser instance. Use the command name to
    determine the default configuration and excludes paths.
    '''
    parser = ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        dest='config_filename',
        default=DEFAULT_CONFIG_FILENAME,
        help='Configuration filename',
    )
    parser.add_argument(
        '--excludes',
        dest='excludes_filename',
        default=DEFAULT_EXCLUDES_FILENAME if os.path.exists(DEFAULT_EXCLUDES_FILENAME) else None,
        help='Excludes filename',
    )
    parser.add_argument(
        '-v', '--verbosity',
        type=int,
        help='Display verbose progress (1 for some, 2 for lots)',
    )

    return parser.parse_args(arguments)


def main():
    try:
        args = parse_arguments(*sys.argv[1:])
        config = parse_configuration(args.config_filename, CONFIG_FORMAT)
        repository = config.location['repository']
        remote_path = config.location.get('remote_path')
        hook_cfg_pre,hook_cfg_post,hook_cfg_error = split_configs(config.hooks) 
        nfc_cfg_pre,nfc_cfg_post,nfc_cfg_error = split_configs(config.notifications)
        run_user_hook(hook_cfg_pre)
        send_user_notification(nfc_cfg_pre)
#        borg.initialize(config.storage)
#        borg.create_archive(
#            args.excludes_filename, args.verbosity, config.storage, **config.location
#        )
#        borg.prune_archives(args.verbosity, repository, config.retention, remote_path=remote_path)
#        borg.check_archives(args.verbosity, repository, config.consistency, remote_path=remote_path)
        print ("Some Borg action")
        run_user_hook(hook_cfg_post)
        send_user_notification(nfc_cfg_post)
    except (ValueError, IOError, CalledProcessError,FileNotFoundError) as error:
        print(error, file=sys.stderr)
        run_user_hook(hook_cfg_error)
        send_user_notification(nfc_cfg_error)
        sys.exit(1)
