#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.backend.t_models.generic import Backend_Models_Generic
from libs.mongo import mongo

from models.User.UserDomain import UserDomain


class Backend_Models_User_Generic(Backend_Models_Generic):

    def _getFromBaseUser(self, user):
        assert isinstance(user, UserDomain)
        data = mongo.users.find_one({"_id": user.getId()})

        if data is None:
            self.fail("User is not find in database")

        return data
