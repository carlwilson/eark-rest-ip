# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Representation(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None):  # noqa: E501
        """Representation - a model defined in Swagger

        :param name: The name of this Representation.  # noqa: E501
        :type name: str
        """
        self.swagger_types = {
            'name': str
        }

        self.attribute_map = {
            'name': 'name'
        }
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'Representation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The representation of this Representation.  # noqa: E501
        :rtype: Representation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Representation.


        :return: The name of this Representation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Representation.


        :param name: The name of this Representation.
        :type name: str
        """

        self._name = name