"""
Created on May 14, 2014

.. moduleauthor:: Peter Morihladko <morihladko@atteq.com>
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from unittest import TestCase

from zsl import Zsl
from zsl.resource.model_resource import ModelResource
from tests.resource.resource_test_helper import UserModel,\
    create_resource_test_data, users, UserTuple, UserAppModel,\
    test_settings


class TestRestResource(ModelResource):
    __model__ = UserModel


class ModelResourceTest(TestCase):
    def setUp(self):
        Zsl(__name__, config_object=test_settings)
        create_resource_test_data()

    def _testAppModel(self, user, model, msg=None):
        # type: (UserTuple, UserAppModel, str) -> None

        self.assertEqual(user.id, model.id, msg)
        self.assertEqual(user.name, model.name, msg)

    def testReadOne(self):
        resource = TestRestResource()
        test_user = users[0]
        user = resource.read(test_user.id)

        self._testAppModel(test_user, user, "resource value should be equal its model")

    def testReadListAll(self):
        resource = TestRestResource()
        res_users = resource.read(args={'limit': 'unlimited'})

        self.assertEqual(len(users), len(res_users), "resources count should equal model count")

        for i, d in enumerate(res_users):
            self._testAppModel(users[i], d, "list item value should equal model item value")

    def testCreate(self):
        resource = TestRestResource()
        user_data = {'name': 'eleven'}
        user_result = resource.create(params=None, args={}, data=user_data)
        user = resource.read(user_result.get_id())

        self.assertEqual(user_data['name'], user.name, "resource value should equal model value")

    def testUpdateOne(self):
        resource = TestRestResource()
        updated_name = 'updated'
        user = resource.read().pop()
        resource.update(params=user.get_id(), args={}, data={'name': updated_name})
        user = resource.read(user.get_id())

        self.assertEqual(updated_name, user.name, "updated resource value should equal model value")

    def testUpdateAll(self):
        resource = TestRestResource()
        updated_users = [UserTuple(id=1, name='updated_1'), UserTuple(id=2, name='updated_2')]
        resource.update(params=None, args={}, data=[x._asdict() for x in updated_users])

        for dt in updated_users:
            self._testAppModel(dt, resource.read(dt.id), "updated resource value should equal model value")

    def testDeleteOne(self):
        resource = TestRestResource()
        user = resource.read().pop()
        resource.delete(user.get_id(), args={}, data=None)
        res_users = resource.read(args={'limit': 'unlimited'})

        self.assertEqual(len(users) - 1, len(res_users), "count of resources should decline by 1")

    def testDeleteAll(self):
        resource = TestRestResource()
        resource.delete(params=None, args={}, data=None)
        res_users = resource.read()

        self.assertEqual(0, len(res_users), "count of resources should be 0")
