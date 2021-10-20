import connexion
import six

from swagger_server.models.ip_manifest import IpManifest  # noqa: E501
from swagger_server import util


def get_manifests():  # noqa: E501
    """Retrieve information package manifests

    Retrieve a list of information package manifests from different sources # noqa: E501


    :rtype: List[IpManifest]
    """
    return 'do some magic!'
