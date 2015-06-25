from tests.generic import Generic

import subprocess

import sys
import config

import init_celery

import os
import imp
import signal


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
            pythonPath = os.getcwd() + '/' + (os.getenv('PYTHONPATH') if os.getenv('PYTHONPATH') else '')
            self._managedProcessCelery = subprocess.Popen(
                [
                    'python3',
                    '-B',
                    '%s/init_celery.py' % (config.get('project.dir') + '/' + config.get('project.application')),
                    '--type=%s' % config.configType,
                    '--database=%s' % self.core.database_name
                ],
                cwd=str(os.path.dirname(os.path.realpath(__file__))) + '/../../',
                stdout=sys.stdout if self.celeryDebug else subprocess.PIPE,
                stderr=sys.stderr if self.celeryDebug else subprocess.PIPE,
                preexec_fn=os.setsid
            )

    def tearDown(self):
        if self._useCelery:
            os.killpg(self._managedProcessCelery.pid, signal.SIGKILL)

        super().tearDown()

    def initCelery(self, debug=False):
        try:
            os.remove('/tmp/celery-sheduler')
        except FileNotFoundError:
            pass

        self._useCelery = True
        self.celeryDebug = debug

    def getUserTransfer(self):
        raise Exception('Is not created')
