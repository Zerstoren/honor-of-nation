import sys
import threading

from celery import Celery
from datetime import timedelta

from tornado import ioloop

import balancer.celery_sender.sender
import config

import helpers.times


sys.argv = [sys.argv[0]]

app = Celery(
    'hn',
    broker=config.get('celery.broker') + config.get('database.mongodb.db'),
    backend=config.get('celery.backend') + config.get('database.mongodb.db')
)

app.conf.update(
    CELERY_TIMEZONE='Europe/Kiev',
    CELERY_ENABLE_UTC=True,
    CELERYBEAT_SCHEDULE = {
        'resources_update': {
            'task': 'init_celery.resources_update',
            'schedule': timedelta(minutes=int(config.get('resource_updates.celery')))
        },

        'population_up': {
            'task': 'init_celery.population_up',
            'schedule': timedelta(minutes=int(config.get('resource_updates.base')))
        },

        'resources_down': {
            'task': 'init_celery.resources_down',
            'schedule': timedelta(minutes=int(config.get('resource_updates.base')))
        }
    }
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


@app.task(serializer='json', name='init_celery.resources_update')
@helpers.times.decorate
def resources_update(*args, **kwargs):
    import controller.ResourceController
    celeryController = controller.ResourceController.CeleryPrivateController()
    celeryController.calculateResources()


@app.task(serialize='json', name='init_celery.population_up')
@helpers.times.decorate
def population_up():
    import controller.TownController
    celeryController = controller.TownController.CeleryPrivateController()
    celeryController.population_up()


@app.task(serialize='json', name='init_celery.resources_down')
@helpers.times.decorate
def resources_down():
    import controller.MapResourcesController
    celeryController = controller.MapResourcesController.CeleryPrivateController()
    celeryController.resourceDown()

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
        app.start(['celery','-A', 'init_celery', 'worker', '-B'])
    except KeyboardInterrupt:
        ioloop.IOLoop.instance().stop()
