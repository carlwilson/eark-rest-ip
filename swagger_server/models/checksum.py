# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.checksum_alg import ChecksumAlg  # noqa: F401,E501
from swagger_server import util


class Checksum(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, algorithm: ChecksumAlg=None, value: str=None):  # noqa: E501
        """Checksum - a model defined in Swagger

        :param algorithm: The algorithm of this Checksum.  # noqa: E501
        :type algorithm: ChecksumAlg
        :param value: The value of this Checksum.  # noqa: E501
        :type value: str
        """
        self.swagger_types = {
            'algorithm': ChecksumAlg,
            'value': str
        }

        self.attribute_map = {
            'algorithm': 'algorithm',
            'value': 'value'
        }
        self._algorithm = algorithm
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'Checksum':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The checksum of this Checksum.  # noqa: E501
        :rtype: Checksum
        """
        return util.deserialize_model(dikt, cls)

    @property
    def algorithm(self) -> ChecksumAlg:
        """Gets the algorithm of this Checksum.


        :return: The algorithm of this Checksum.
        :rtype: ChecksumAlg
        """
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: ChecksumAlg):
        """Sets the algorithm of this Checksum.


        :param algorithm: The algorithm of this Checksum.
        :type algorithm: ChecksumAlg
        """

        self._algorithm = algorithm

    @property
    def value(self) -> str:
        """Gets the value of this Checksum.


        :return: The value of this Checksum.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value: str):
        """Sets the value of this Checksum.


        :param value: The value of this Checksum.
        :type value: str
        """

        self._value = value
