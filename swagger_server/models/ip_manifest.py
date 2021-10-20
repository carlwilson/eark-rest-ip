# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.manifest import Manifest  # noqa: F401,E501
from swagger_server import util


class IpManifest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, uid: str=None, manifest: Manifest=None):  # noqa: E501
        """IpManifest - a model defined in Swagger

        :param uid: The uid of this IpManifest.  # noqa: E501
        :type uid: str
        :param manifest: The manifest of this IpManifest.  # noqa: E501
        :type manifest: Manifest
        """
        self.swagger_types = {
            'uid': str,
            'manifest': Manifest
        }

        self.attribute_map = {
            'uid': 'uid',
            'manifest': 'manifest'
        }
        self._uid = uid
        self._manifest = manifest

    @classmethod
    def from_dict(cls, dikt) -> 'IpManifest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ipManifest of this IpManifest.  # noqa: E501
        :rtype: IpManifest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def uid(self) -> str:
        """Gets the uid of this IpManifest.


        :return: The uid of this IpManifest.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid: str):
        """Sets the uid of this IpManifest.


        :param uid: The uid of this IpManifest.
        :type uid: str
        """

        self._uid = uid

    @property
    def manifest(self) -> Manifest:
        """Gets the manifest of this IpManifest.


        :return: The manifest of this IpManifest.
        :rtype: Manifest
        """
        return self._manifest

    @manifest.setter
    def manifest(self, manifest: Manifest):
        """Sets the manifest of this IpManifest.


        :param manifest: The manifest of this IpManifest.
        :type manifest: Manifest
        """

        self._manifest = manifest
