import traceback

import system.log

from . import database
from . import httpCodes
from . import message


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

        except (database.NotFound, httpCodes.Page404) as e:
            system.log.info(traceback.format_exc() + str(e))
            transfer.send('/error', {
                'done': False,
                'error': 'Data by current url not found',
                'code': 404,
                'traceback': traceback.format_exc()
            })

        except database.Database as e:
            system.log.critical(traceback.format_exc() + str(e))
            transfer.send('/error', {
                'done': False,
                'error': str(e),
                'code': 500,
                'traceback': traceback.format_exc()
            })

        except httpCodes.Page403 as e:
            system.log.error(str(e))
            transfer.send('/error', {
                'done': False,
                'error': str(e)
            })

        except httpCodes.HttpError as e:
            system.log.warn(traceback.format_exc() + str(e))
            transfer.send('/error', {
                'done': False,
                'error': str(e),
                'code': e.getCode(),
                'traceback': traceback.format_exc()
            })

        except message.Message as e:
            transfer.send('/error', {
                'done': False,
                'error': str(e)
            })

        except Exception as e:
            system.log.critical(traceback.format_exc() + str(e))
            transfer.send('/error', {
                'done': False,
                'error': str(e),
                'code': 500,
                'traceback': traceback.format_exc()
            })

    return wrapped
