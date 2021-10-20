import connexion
import six

from swagger_server.models.validation_report import ValidationReport  # noqa: E501
from swagger_server import util


def get_validation_result(uid):  # noqa: E501
    """Get validation result

    Retrieve a validation result by uid # noqa: E501

    :param uid: UUID of the package to retrieve
    :type uid:

    :rtype: ValidationReport
    """
    return 'do some magic!'


def get_validations():  # noqa: E501
    """Retrieve valdiation results

    Retrieves a lits of available validation results # noqa: E501


    :rtype: List[ValidationReport]
    """
    return 'do some magic!'
