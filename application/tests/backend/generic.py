from tests.generic import Generic

import subprocess

import sys
import config

import init_celery

import os
import imp


class Backend_Generic(Generic):
    execution = 'backend'

    celeryDebug = False
    _useCelery = False

    def setUp(self):
        super().setUp()

        if config.get('system.pycharm') == 'True':
            path = sys.path[1]
        else:
            path = sys.path[0]


        if self._useCelery:
            imp.reload(init_celery)

            self._managedProcessCelery = subprocess.Popen(
                [
                    'python3',
                    '-B',
                    'init_celery.py',
                    '--type=%s' % config.configType,
                    '--database=%s' % self.core.database_name
                ],
                cwd=str(os.path.dirname(os.path.realpath(__file__))) + '/../../',
                stdout=sys.stdout if self.celeryDebug else subprocess.PIPE,
                stderr=sys.stderr if self.celeryDebug else subprocess.PIPE
            )

    def tearDown(self):
        if self._useCelery:
            self._managedProcessCelery.kill()

        super().tearDown()

    def initCelery(self, debug=False):
        os.remove('/tmp/celery-sheduler')
        self._useCelery = True
        self.celeryDebug = debug

    def getUserTransfer(self):
        raise Exception('Is not created')
