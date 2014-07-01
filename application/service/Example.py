from .Abstract import AbstractService

class Service_News(AbstractService.Service_Abstract):
    def getExample(self):
        return 'service example'

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_News
        """
        return super().decorate(*args)
