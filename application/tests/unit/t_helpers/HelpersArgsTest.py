from tests.unit.t_helpers import generic
import helpers.args
import exceptions.args


class UnitTest_HelpersArgsTest(generic.UnitTest_Helpers_Generic):
    def testType_Normal(self):
        message = {'test': 'testing'}
        helpers.args.set(message, test={"type": str})
        self.assertEquals(message['test'], 'testing')

    def testType_Exceptions(self):
        for param in ['str', 1, ['list'], {'dict': 'dict'}, False]:
            for scalar in [str, bool, int, list, dict]:
                if type(param) is scalar:
                    continue

                message = {'test': param}

                self.assertRaises(
                    exceptions.args.WrongArgumentType,
                    helpers.args.set,
                    message,
                    test={"type": scalar}
                )

    def testClean_None(self):
        message = {'test': 'Some clear <is html> and disabled clear'}
        helpers.args.set(
            message,
            test={"type": str}
        )
        self.assertEquals(message['test'], 'Some clear <is html> and disabled clear')

    def testClean_Soft(self):
        message = {'test': 'Some clear <script> and disabled clear'}
        helpers.args.set(
            message,
            test={"type": str, "clean": 'soft'}
        )
        self.assertEquals(message['test'], 'Some clear  and disabled clear')

    def testClean_Strong(self):
        message = {'test': 'Some clear <is html> and disabled clear'}
        helpers.args.set(
            message,
            test={"type": str, "clean": 'strong'}
        )
        self.assertEquals(message['test'], 'Someclearishtmlanddisabledclear')

    def testRequired_IsOn(self):
        message = {}
        self.assertRaises(
            exceptions.args.NotEnoughArguments,
            helpers.args.set,
            message,
            test={"type": str, 'required': True}
        )

        message = {}
        self.assertRaises(
            exceptions.args.NotEnoughArguments,
            helpers.args.set,
            message,
            test={"type": str}
        )

    def testRequired_IsOff(self):
        for scalar in [str, bool, int, list, dict]:
            message = {}
            helpers.args.set(message, test={"type": scalar, "required": False})
            self.assertEquals(message['test'], scalar())

    def testDeleteKeys(self):
        message = {
            'first': 1,
            'second': 2,
            'three': 3,
            'four': 4
        }

        helpers.args.set(message,
            first={"type": int},
            second={"type": int},
            four={"type": int},
        )

        self.assertIn('first', message)
        self.assertIn('second', message)
        self.assertNotIn('three', message)
        self.assertIn('four', message)

    def _testDict_Normal(self):
        message = {
            'text': {
                '1': 1,
                '2': 2,
                '3': 3
            }
        }

        helpers.args.set(message,
            text={"type": dict, "subType": int, "subDict": ['1', '2', '3']}
        )

        self.assertEquals(message['text']['1'], 1)
        self.assertEquals(message['text']['2'], 2)
        self.assertEquals(message['text']['3'], 3)

    def testDict_WrongArguments(self):
        message = {
            'text': {
                '1': '1',
                '2': 2,
                '3': 3
            }
        }

        self.assertRaises(
            exceptions.args.WrongArgumentType,
            helpers.args.set,
            message,
            text={"type": dict, "subType": int, "subDict": ['1', '2', '3']}
        )

    def testDict_NotEnoughArguments(self):
        message = {
            'text': {
                '1': 1,
                '3': 3
            }
        }

        self.assertRaises(
            exceptions.args.NotEnoughArguments,
            helpers.args.set,
            message,
            text={"type": dict, "subType": int, "subDict": ['1', '2', '3']}
        )

    def testDict_DeepedException(self):
        message = {
            'text': {
                'deep': {
                    'deeped': {}
                }
            }
        }

        self.assertRaises(
            exceptions.args.WrongArgumentType,
            helpers.args.set,
            message,
            text={"type": dict, "subType": int, "subDict": ['deep']}
        )

    def testList_Normal(self):
        message = {
            'text': [1, 2, 3]
        }

        helpers.args.set(message,
            text={"type": list, "subType": int}
        )

        self.assertEquals(message['text'][0], 1)
        self.assertEquals(message['text'][1], 2)
        self.assertEquals(message['text'][2], 3)

    def testList_DeepedException(self):
        message = {
            'text': [{}, {}]
        }

        self.assertRaises(
            exceptions.args.DeepArgumentsError,
            helpers.args.set,
            message,
            text={"type": list, "subType": dict}
        )

    def testList_WrongType(self):
        message = {
            'text': [1, '2', 3]
        }

        self.assertRaises(
            exceptions.args.WrongArgumentType,
            helpers.args.set,
            message,
            text={"type": list, "subType": int}
        )

    def testUnitary_Normal(self):
        message = helpers.args.unitary('text', type=str)
        self.assertEquals(message, 'text')

    def testUnitary_WrongType(self):
        self.assertRaises(
            exceptions.args.WrongArgumentType,
            helpers.args.unitary,
            1,
            type=str
        )
