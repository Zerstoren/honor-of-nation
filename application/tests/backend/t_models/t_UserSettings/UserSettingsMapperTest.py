from tests.backend.t_models.t_UserSettings import generic


class Backend_Models_UserSettings_UserSettingsMapperTest(generic.Backend_Models_Settings_Generic):
    def testGetDefaultSettings(self):
        user = self.fixture.getUser(0)
        settings = user.getSubDomainSettings()

        self.assertEqual(
            settings.getName(),
            1
        )

    def testSetGetSettings(self):
        user = self.fixture.getUser(0)
        settings = user.getSubDomainSettings()

        self.assertEqual(
            settings.getName(),
            1
        )

        edit = settings.edit()
        edit.setName(25)
        edit.getMapper().save(edit)

        self.assertEqual(
            settings.getName(),
            25
        )
