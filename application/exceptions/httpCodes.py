class HttpError(Exception):
    code = 500

    def show(self, requestHandler):
        """
        :type requestHandler: tornado.web.RequestHandler
        """

        requestHandler.set_header(self.code, 'Error')

    def getCode(self):
        return self.code


class Page404(HttpError):
    code = 404


class Page403(HttpError):
    code = 403


class Page401(HttpError):
    code = 401
