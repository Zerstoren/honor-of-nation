import sys
import threading

from celery import Celery

from tornado import ioloop

import balancer.celery_sender.sender
import config
import system.log


sys.argv = [sys.argv[0]]

app = Celery(
    'hn',
    broker=config.get('celery.broker') + config.get('database.mongodb.db'),
    backend=config.get('celery.backend') + config.get('database.mongodb.db')
)


def message(message, user):
    balancer.celery_sender.sender.Respondent.writeMessage(
        message,
        str(user.getId())
    )


@app.task(serializer='json', name='init_celery.builds')
def builds(message):
    import controller.TownBuildsController
    celeryController = controller.TownBuildsController.CeleryPrivateController()
    celeryController.buildComplete(message)


@app.task(serializer='json', name='init_celery.army')
def army(message):
    import controller.ArmyQueueController
    celeryController = controller.ArmyQueueController.CeleryPrivateController()
    celeryController.armyCreated(message)


if __name__ == '__main__':
    def ioLoop():
        ioloop.IOLoop.instance().start()

    if 1 in sys.argv:
        sys.argv[1] = 'worker'
    else:
        sys.argv.append('worker')

    if config.get('celery.debug') == 'True':
        if 2 in sys.argv:
            sys.argv[2] = '-l'
        else:
            sys.argv.append('-l')

        if 3 in sys.argv:
            sys.argv[3] = 'INFO'
        else:
            sys.argv.append('INFO')

    try:
        threading.Thread(target=ioLoop).start()
        app.start()
    except KeyboardInterrupt:
        ioloop.IOLoop.instance().stop()
