import connexion
import six

from swagger_server.models.information_package import InformationPackage  # noqa: E501
from swagger_server.models.ip_manifest import IpManifest  # noqa: E501
from swagger_server.models.package_details import PackageDetails  # noqa: E501
from swagger_server.models.representation import Representation  # noqa: E501
from swagger_server.models.upload import Upload  # noqa: E501
from swagger_server.models.validation_report import ValidationReport  # noqa: E501
from swagger_server import util


def delete_ip():  # noqa: E501
    """Delete information packages.

    Delete all information package binaries for this user. # noqa: E501


    :rtype: List[Upload]
    """
    return 'do some magic!'


def delete_ip_by_uid(uid):  # noqa: E501
    """Delete IP by uid.

    Delete information package binary by uid. # noqa: E501

    :param uid: UUID of the package to delete
    :type uid: 

    :rtype: Upload
    """
    return 'do some magic!'


def get_ip_by_uid(uid):  # noqa: E501
    """Get package info.

    Get the properties of an information package uid. # noqa: E501

    :param uid: UUID of the package to retrieve
    :type uid: 

    :rtype: InformationPackage
    """
    return 'do some magic!'


def get_ip_manifests(uid):  # noqa: E501
    """Get package manifests.

    Get any manifests for an information package. # noqa: E501

    :param uid: UUID of the package to retrieve
    :type uid: 

    :rtype: IpManifest
    """
    return 'do some magic!'


def get_ip_representations(uid):  # noqa: E501
    """Get package representations.

    Get the representations of an information package by uid. # noqa: E501

    :param uid: UUID of the package to retrieve
    :type uid: 

    :rtype: Representation
    """
    return 'do some magic!'


def get_ips():  # noqa: E501
    """Retrieve package binary details.

    Retrieve a list of package binaries uploaded to the validation service. # noqa: E501


    :rtype: List[Upload]
    """
    return 'do some magic!'


def post_ip(sha1=None, file_name=None):  # noqa: E501
    """Upload package binary.

    Upload a package binary for validation, returns process identifier and digest. # noqa: E501

    :param sha1: 
    :type sha1: str
    :param file_name: 
    :type file_name: strstr

    :rtype: PackageDetails
    """
    return 'do some magic!'


def validate(sha2=None, file_name=None, sha1=None):  # noqa: E501
    """Synchronous package valdition.

    Upload a package binary for validation and return validation result immediately. # noqa: E501

    :param sha2: 
    :type sha2: str
    :param file_name: 
    :type file_name: strstr
    :param sha1: SHA-1 hash of package to validate
    :type sha1: str

    :rtype: ValidationReport
    """
    return 'do some magic!'
