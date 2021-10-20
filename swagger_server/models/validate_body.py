# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ValidateBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, sha1: str=None, file_name: str=None):  # noqa: E501
        """ValidateBody - a model defined in Swagger

        :param sha1: The sha1 of this ValidateBody.  # noqa: E501
        :type sha1: str
        :param file_name: The file_name of this ValidateBody.  # noqa: E501
        :type file_name: str
        """
        self.swagger_types = {
            'sha1': str,
            'file_name': str
        }

        self.attribute_map = {
            'sha1': 'sha1',
            'file_name': 'fileName'
        }
        self._sha1 = sha1
        self._file_name = file_name

    @classmethod
    def from_dict(cls, dikt) -> 'ValidateBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The validate_body of this ValidateBody.  # noqa: E501
        :rtype: ValidateBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sha1(self) -> str:
        """Gets the sha1 of this ValidateBody.


        :return: The sha1 of this ValidateBody.
        :rtype: str
        """
        return self._sha1

    @sha1.setter
    def sha1(self, sha1: str):
        """Sets the sha1 of this ValidateBody.


        :param sha1: The sha1 of this ValidateBody.
        :type sha1: str
        """

        self._sha1 = sha1

    @property
    def file_name(self) -> str:
        """Gets the file_name of this ValidateBody.


        :return: The file_name of this ValidateBody.
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        """Sets the file_name of this ValidateBody.


        :param file_name: The file_name of this ValidateBody.
        :type file_name: str
        """

        self._file_name = file_name
