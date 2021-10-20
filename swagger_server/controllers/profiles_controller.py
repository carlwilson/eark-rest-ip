import connexion
import six

from swagger_server.models.profile_details import ProfileDetails  # noqa: E501
from swagger_server import util


def get_profile(type, version):  # noqa: E501
    """Retrieve a validation profile.

    Retrieve a validation profile by type and version # noqa: E501

    :param type: The type of profile to retrieve
    :type type: str
    :param version: The version of profile to retrieve
    :type version: str

    :rtype: ProfileDetails
    """
    return 'do some magic!'


def get_profiles():  # noqa: E501
    """Retrieve validation profiles.

    Retrieve a list of supported validation profiles # noqa: E501


    :rtype: List[ProfileDetails]
    """
    return 'do some magic!'
