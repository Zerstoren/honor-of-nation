#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.generic import Generic


class Backend_Generic(Generic):

    def getUserTransfer(self):
        raise Exception('Is not created')
