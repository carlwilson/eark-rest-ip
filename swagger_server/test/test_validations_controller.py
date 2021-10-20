# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.validation_report import ValidationReport  # noqa: E501
from swagger_server.test import BaseTestCase


class TestValidationsController(BaseTestCase):
    """ValidationsController integration test stubs"""

    def test_get_validation_result(self):
        """Test case for get_validation_result

        Get validation result
        """
        response = self.client.open(
            '/validations/{uid}'.format(uid='38400000-8cf0-11bd-b23e-10b96e4ef00d'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_validations(self):
        """Test case for get_validations

        Retrieve valdiation results
        """
        response = self.client.open(
            '/validations',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
