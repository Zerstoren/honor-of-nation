import config
import os
os.chdir(os.path.split(os.path.abspath(__file__))[0])

if config.options.type is None:
    config.configType = 'test_server'

import tests.bootstrap.bootstrap
tests.bootstrap.bootstrap.start_application()
