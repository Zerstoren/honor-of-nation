
class Builds(Exception):
    pass


class BuildsQueue(Exception):
    pass


class WrongCreateBuildLevel(BuildsQueue):
    pass


class WrongQueueChain(BuildsQueue):
    pass