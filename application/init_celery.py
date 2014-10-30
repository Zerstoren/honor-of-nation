from celery import Celery
import config
import sys

import controller.CeleryController
celeryController = controller.CeleryController.CeleryPrivateController()

sys.argv = [sys.argv[0]]

app = Celery(
    'hn',
    broker=config.get('celery.broker'),
    backend=config.get('celery.backend')
)

@app.task
def builds(message):
    celeryController.buildComplete(message)


if __name__ == '__main__':
    if 1 in sys.argv:
        sys.argv[1] = 'worker'
    else:
        sys.argv.append('worker')

    app.start()