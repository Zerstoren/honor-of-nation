from tests.generic import Generic

import subprocess

import sys
import config

import init_celery

import imp


class Backend_Generic(Generic):
    celeryDebug = False
    _useCelery = False

    def setUp(self):
        super().setUp()

        if self._useCelery:
            imp.reload(init_celery)
            self._managedProcess = subprocess.Popen(
                [
                    'python3',
                    '-B',
                    '%s/init_celery.py' % sys.path[1],
                    '--type=%s' % config.configType,
                    '--database=%s' % self.core.database_name
                ],
                stdout=sys.stdout if self.celeryDebug else subprocess.PIPE,
                stderr=sys.stderr if self.celeryDebug else subprocess.PIPE
            )

    def tearDown(self):
        if self._useCelery:
            self._managedProcess.terminate()
        super().tearDown()

    def initCelery(self):
        self._useCelery = True

    def getUserTransfer(self):
        raise Exception('Is not created')
