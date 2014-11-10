from celery import Celery
import config
import sys

sys.argv = [sys.argv[0]]

app = Celery(
    'hn',
    broker=config.get('celery.broker') + config.get('database.mongodb.db'),
    backend=config.get('celery.backend') + config.get('database.mongodb.db')
)


@app.task(serializer='json', name='init_celery.builds')
def builds(message):
    import controller.CeleryController
    celeryController = controller.CeleryController.CeleryPrivateController()
    celeryController.buildComplete(message)


if __name__ == '__main__':
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

    app.start()
else:
    import balancer.celery_sender.sender


def message(message, user):
    balancer.celery_sender.sender.Respondent.writeMessage(
        message,
        str(user.getId())
    )
