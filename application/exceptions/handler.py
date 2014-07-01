import traceback

from . import database
from . import httpCodes


def handle(fn):
    def wrapped(transfer, data):
        """
        :type transfer: system.UserTransfer.UserTransfer
        :type data: dict
        """

        if fn is False:
            transfer.send('/error', {
                'done': False,
                'error': 'Data by current url not found',
                'code': 404
            })

            return False

        try:
            return fn(transfer, data)

        except (database.NotFound, httpCodes.Page404):
            print(traceback.format_exc())
            transfer.send('/error', {
                'done': False,
                'error': 'Data by current url not found',
                'code': 404,
                'traceback': traceback.format_exc()
            })

        except database.Database as e:
            print(traceback.format_exc())
            transfer.send('/error', {
                'done': False,
                'error': str(e),
                'code': 500,
                'traceback': traceback.format_exc()
            })

        except httpCodes.HttpError as e:
            print(traceback.format_exc())
            transfer.send('/error', {
                'done': False,
                'error': str(e),
                'code': e.getCode(),
                'traceback': traceback.format_exc()
            })

        except Exception as e:
            print(traceback.format_exc())
            transfer.send('/error', {
                'done': False,
                'error': str(e),
                'code': 500,
                'traceback': traceback.format_exc()
            })

    return wrapped
