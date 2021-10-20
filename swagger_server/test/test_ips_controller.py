# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.information_package import InformationPackage  # noqa: E501
from swagger_server.models.ip_manifest import IpManifest  # noqa: E501
from swagger_server.models.package_details import PackageDetails  # noqa: E501
from swagger_server.models.representation import Representation  # noqa: E501
from swagger_server.models.upload import Upload  # noqa: E501
from swagger_server.models.validation_report import ValidationReport  # noqa: E501
from swagger_server.test import BaseTestCase


class TestIpsController(BaseTestCase):
    """IpsController integration test stubs"""

    def test_delete_ip(self):
        """Test case for delete_ip

        Delete information packages.
        """
        response = self.client.open(
            '/ips',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_ip_by_uid(self):
        """Test case for delete_ip_by_uid

        Delete IP by uid.
        """
        response = self.client.open(
            '/ips/{uid}'.format(uid='38400000-8cf0-11bd-b23e-10b96e4ef00d'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_ip_by_uid(self):
        """Test case for get_ip_by_uid

        Get package info.
        """
        response = self.client.open(
            '/ips/{uid}'.format(uid='38400000-8cf0-11bd-b23e-10b96e4ef00d'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_ip_manifests(self):
        """Test case for get_ip_manifests

        Get package manifests.
        """
        response = self.client.open(
            '/ips/{uid}/manifests'.format(uid='38400000-8cf0-11bd-b23e-10b96e4ef00d'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_ip_representations(self):
        """Test case for get_ip_representations

        Get package representations.
        """
        response = self.client.open(
            '/ips/{uid}/representations'.format(uid='38400000-8cf0-11bd-b23e-10b96e4ef00d'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_ips(self):
        """Test case for get_ips

        Retrieve package binary details.
        """
        response = self.client.open(
            '/ips',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_ip(self):
        """Test case for post_ip

        Upload package binary.
        """
        data = dict(sha1='sha1_example',
                    file_name='file_name_example')
        response = self.client.open(
            '/ips',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_validate(self):
        """Test case for validate

        Synchronous package valdition.
        """
        headers = [('sha1', 'sha1_example')]
        data = dict(sha1='sha1_example',
                    file_name='file_name_example')
        response = self.client.open(
            '/validate',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
