from __future__ import print_function

import sys

from ckan import model
from ckan.logic import get_action

from ckan.lib.cli import CkanCommand


class Admintools(CkanCommand):
    '''A collection of scripts that make admin easier.

    Usage:

      admintools private
        - Changes the status of all datasets to `private`.

      admintools public
        - Changes the status of all datasets to `public`.
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 1
    min_args = 1

    def __init__(self, name):

        super(Admintools, self).__init__(name)

    def command(self):
        self._load_config()

        # We'll need a sysadmin user to perform most of the actions
        # We will use the sysadmin site user (named as the site_id)
        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        self.admin_user = get_action('get_site_user')(context, {})

        print('')

        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)
        cmd = self.args[0]
        if cmd == 'private':
            self.private()
        elif cmd == 'public':
            self.public()
        else:
            print('Command {0} not recognized'.format(cmd))

    def _load_config(self):
        super(Admintools, self)._load_config()

    def private(self):
        context = {'model': model, 'user': self.admin_user['name']}
        get_action('make_datasets_private')(context, {})

    def public(self):
        context = {'model': model, 'user': self.admin_user['name']}
        get_action('make_datasets_public')(context, {})
