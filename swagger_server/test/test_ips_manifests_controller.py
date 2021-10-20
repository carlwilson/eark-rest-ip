# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.ip_manifest import IpManifest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestIpsManifestsController(BaseTestCase):
    """IpsManifestsController integration test stubs"""

    def test_get_manifests(self):
        """Test case for get_manifests

        Retrieve information package manifests
        """
        response = self.client.open(
            '/ips-manifests',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
