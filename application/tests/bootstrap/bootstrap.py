import sys
import os
import unittest
import importlib

from . import core

testLoader = unittest.TestLoader()


def start_application():
    if len(sys.argv) == 1:
        sys.argv.append("tests/")

    import_files(sys.argv[1])
    del sys.argv[1]


def import_files(path):
    test_file_strings = []

    print("Files for test:")

    if path[-7:] == 'Test.py':
        print('    ' + path.replace('.py', ''))
        test_file_strings.append(path.replace('.py', '').replace('/', '.'))
    else:
        for cdir, subdir, files in os.walk(path):
            for file_test in files:
                if file_test[-7:] != 'Test.py':
                    continue

                print('    ' + (cdir + '/' + file_test).replace('//', '/'))
                fileName = (cdir + '/' + file_test)\
                    .replace('.py', '')\
                    .replace('//', '/')\
                    .replace('/', '.')

                test_file_strings.append(fileName)
    print("\n\n")

    suites = []
    for mod in test_file_strings:
        importlib.import_module(mod)
        suites.append(unittest.defaultTestLoader.loadTestsFromName(mod))

    testSuite = unittest.TestSuite(suites)
    result = unittest.TextTestRunner().run(testSuite)
    sys.exit(len(result.errors) + len(result.failures))


def create_core_for_test():
    return core.Core()
