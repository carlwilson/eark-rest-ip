# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.severity import Severity  # noqa: F401,E501
from swagger_server import util


class TestResult(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, rule_id: str=None, location: str=None, message: str=None, severity: Severity=None):  # noqa: E501
        """TestResult - a model defined in Swagger

        :param rule_id: The rule_id of this TestResult.  # noqa: E501
        :type rule_id: str
        :param location: The location of this TestResult.  # noqa: E501
        :type location: str
        :param message: The message of this TestResult.  # noqa: E501
        :type message: str
        :param severity: The severity of this TestResult.  # noqa: E501
        :type severity: Severity
        """
        self.swagger_types = {
            'rule_id': str,
            'location': str,
            'message': str,
            'severity': Severity
        }

        self.attribute_map = {
            'rule_id': 'ruleId',
            'location': 'location',
            'message': 'message',
            'severity': 'severity'
        }
        self._rule_id = rule_id
        self._location = location
        self._message = message
        self._severity = severity

    @classmethod
    def from_dict(cls, dikt) -> 'TestResult':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The testResult of this TestResult.  # noqa: E501
        :rtype: TestResult
        """
        return util.deserialize_model(dikt, cls)

    @property
    def rule_id(self) -> str:
        """Gets the rule_id of this TestResult.


        :return: The rule_id of this TestResult.
        :rtype: str
        """
        return self._rule_id

    @rule_id.setter
    def rule_id(self, rule_id: str):
        """Sets the rule_id of this TestResult.


        :param rule_id: The rule_id of this TestResult.
        :type rule_id: str
        """

        self._rule_id = rule_id

    @property
    def location(self) -> str:
        """Gets the location of this TestResult.


        :return: The location of this TestResult.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location: str):
        """Sets the location of this TestResult.


        :param location: The location of this TestResult.
        :type location: str
        """

        self._location = location

    @property
    def message(self) -> str:
        """Gets the message of this TestResult.


        :return: The message of this TestResult.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this TestResult.


        :param message: The message of this TestResult.
        :type message: str
        """

        self._message = message

    @property
    def severity(self) -> Severity:
        """Gets the severity of this TestResult.


        :return: The severity of this TestResult.
        :rtype: Severity
        """
        return self._severity

    @severity.setter
    def severity(self, severity: Severity):
        """Sets the severity of this TestResult.


        :param severity: The severity of this TestResult.
        :type severity: Severity
        """

        self._severity = severity
