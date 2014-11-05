import subprocess
import sys
import config

import os


class Process():
    workers = []
    celery = None

    def run(self):
        if config.get('balancer.backend') == 'True':
            self._startBackend()

        if config.get('balancer.celery') == 'True':
            self._startCelery()

    def _startBackend(self):
        workers = int(config.get('balancer.backend.workers'))
        debug = config.get('balancer.backend.debug') == 'True'
        for i in range(workers):
            process = subprocess.Popen([
                    'python3',
                    '-B',
                    '%s/init_backend.py' % os.getcwd()
                ],
                stdout=sys.stdout if debug else subprocess.PIPE,
                stderr=sys.stderr if debug else subprocess.PIPE
            )

            print('Server start. Pid ' + str(process.pid))
            self.workers.append(process)

    def _startCelery(self):
        debug = config.get('balancer.celery.debug') == 'True'

        self.celery = subprocess.Popen([
                'python3',
                '-B',
                '%s/init_celery.py' % os.getcwd()
            ],
            stdout=sys.stdout if debug else subprocess.PIPE,
            stderr=sys.stderr if debug else subprocess.PIPE
        )

        print('Celery start. Pid ' + str(self.celery.pid))

    def stop(self):
        for i in self.workers:
            i.terminate()

        if self.celery:
            self.celery.terminate()
