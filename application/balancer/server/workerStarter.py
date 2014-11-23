import subprocess
import sys
import config

import os
import signal


class Process():
    workers = []
    celery = None

    def run(self):
        if config.get('balancer.backend') == 'True':
            self._startBackend()

        if config.get('balancer.celery') == 'True':
            self._startCelery()

        def sigterm_handler(_signo, _stack_frame):
            self.stop()

        for i in [x for x in dir(signal) if x.startswith("SIG")]:
            try:
                signum = getattr(signal,i)
                signal.signal(signum, sigterm_handler)
            except Exception:
                print("Skipping %s"%i)

    def _startBackend(self):
        workers = int(config.get('balancer.backend.workers'))
        debug = config.get('balancer.backend.debug') == 'True'
        for i in range(workers):
            args = [
                'python3',
                '-B',
                '%s/init_backend.py' % os.getcwd()
            ]

            self._appendArgs(args)

            process = subprocess.Popen(
                args,
                stdout=sys.stdout if debug else subprocess.PIPE,
                stderr=sys.stderr if debug else subprocess.PIPE
            )

            print('Server start. Pid ' + str(process.pid))
            self.workers.append(process)

    def _startCelery(self):
        debug = config.get('balancer.celery.debug') == 'True'

        args = [
            'python3',
            '-B',
            '%s/init_celery.py' % os.getcwd()
        ]

        self._appendArgs(args)

        self.celery = subprocess.Popen(
            args,
            stdout=sys.stdout if debug else subprocess.PIPE,
            stderr=sys.stderr if debug else subprocess.PIPE
        )

        print('Celery start. Pid ' + str(self.celery.pid))

    def _appendArgs(self, args):
        if config.options.type:
            args.append('--type=%s' % config.options.type)

        if config.options.database:
            args.append('--database=%s' % config.options.database)

        if config.options.port:
            args.append('--port=%s' % config.options.port)

        if config.options.balancer_port:
            args.append('--balancer_port=%s' % config.options.balancer_port)


    def stop(self):
        for i in self.workers:
            i.terminate()

        if self.celery:
            pid = self.celery.pid
            self.celery.send_signal(signal.SIGKILL)

