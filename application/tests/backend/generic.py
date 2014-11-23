from tests.generic import Generic

import subprocess

import sys
import config
import os
import signal

import init_celery

import imp


class Backend_Generic(Generic):
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

            self._managedProcess = subprocess.Popen(
                [
                    'python3',
                    '-B',
                    '%s/init_celery.py' % path,
                    '--type=%s' % config.configType,
                    '--database=%s' % self.core.database_name
                ],
                stdout=sys.stdout if self.celeryDebug else subprocess.PIPE,
                stderr=sys.stderr if self.celeryDebug else subprocess.PIPE
            )

    def tearDown(self):
        if self._useCelery:
            pid = str(self._managedProcess.pid)
            print("TRY KILL %s" % pid)
            self._managedProcess.terminate()
            os.kill(signal.SIGKILL, int(pid))


        super().tearDown()

    def initCelery(self):
        self._useCelery = True

    def getUserTransfer(self):
        raise Exception('Is not created')
