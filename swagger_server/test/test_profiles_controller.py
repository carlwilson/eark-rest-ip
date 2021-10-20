# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.profile_details import ProfileDetails  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProfilesController(BaseTestCase):
    """ProfilesController integration test stubs"""

    def test_get_profile(self):
        """Test case for get_profile

        Retrieve a validation profile.
        """
        response = self.client.open(
            '/profiles/{type}/{version}'.format(type='type_example', version='version_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_profiles(self):
        """Test case for get_profiles

        Retrieve validation profiles.
        """
        response = self.client.open(
            '/profiles',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
