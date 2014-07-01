from tests.backend.t_models.t_UserState import generic
import libs.mongo


class Backend_Models_State_StateDomainTest(generic.Backend_Models_State_Generic):
    def testState_GetError_TargetNotExist(self):
        user = self.fixture.getUser(0)
        state = user.getSubDomainState()

        self.assertRaises(
            AssertionError,
            state.getStateTo,
            libs.mongo.types.ObjectId('000000000000000000000000')
        )

    def testState_Create_IfUserIsNotKnow(self):
        user = self.fixture.getUser(0)
        other = self.fixture.getUser(1)

        state = user.getSubDomainState()

        self.assertEqual(
            state.STATE_NUETRAL,
            state.getStateTo(other)
        )
