# Fix for PyCharm run.
import sys
import os
if sys.argv[0].find('/utrunner.py') != -1:
    sys.path[0] = sys.path[3]
    sys.argv[0] = sys.path[3]
    sys.argv[1] = '--type=test_server'
    sys.argv[2] = '--pycharm=True'


import configparser
from optparse import OptionParser

# Valid config type: dev, test_server, product
configType = 'dev'

_config = configparser.ConfigParser()
_config.read(os.path.dirname(os.path.abspath(__file__)) + '/config/application.ini')

_arguments = OptionParser()
_arguments.add_option("-l", "--host", help="Select listening host", default=None)
_arguments.add_option("-p", "--port", help="Select listening port", default=None)
_arguments.add_option("-d", "--database", help="Select database", default=None)
_arguments.add_option("-s", "--domain", help="Select domain", default=None)
_arguments.add_option("-t", "--type", help="Select run type", default=None)
_arguments.add_option("-j", "--pycharm", help="Is flag using for pycharm unit test", default=None)
_arguments.add_option("-f", "--balancer_full", help="Set flag for start sub system celery and backend", default=None)
_arguments.add_option("-w", "--balancer_back_workers", help="How many workers need start", default=None)
_arguments.add_option("-b", "--balancer_port", help="set balancer client and server ports", default=None)


(options, args) = _arguments.parse_args()

if options.port:
    _config['default']['server.port'] = options.port

if options.host:
    _config['default']['server.host'] = options.host

if options.domain:
    _config['default']['server.domain'] = options.domain

if options.database:
    _config['default']['database.mongodb.db'] = options.database

if options.balancer_full:
    _config['default']['balancer.backend'] = 'True'
    _config['default']['balancer.celery'] = 'True'

if options.balancer_back_workers:
    _config['default']['balancer.backend.workers'] = str(options.balancer_back_workers)

if options.balancer_port:
    _config['default']['balancer.backend.server.port'] = options.balancer_port
    _config['default']['balancer.backend.client.port'] = options.balancer_port

if options.type:
    configType = options.type

if options.pycharm:
    _config['default']['system.pycharm'] = str(options.pycharm is not None)


def getRoutes():
    _config = configparser.ConfigParser()
    _config.read(os.path.dirname(os.path.abspath(__file__)) + '/config/router.ini')

    return _config['routes']


def getDatabase():
    _config = configparser.ConfigParser()
    _config.read(os.path.dirname(os.path.abspath(__file__)) + '/config/database.ini')

    return _config


def get(name):
    if name in _config[configType]:
        return _config[configType][name]
    elif name in _config['default']:
        return _config['default'][name]
    else:
        raise Exception("Config attribute %s not found" % name)
