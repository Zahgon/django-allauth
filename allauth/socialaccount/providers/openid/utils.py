import base64
import pickle  # nosec
from collections import UserDict

from openid.association import Association as OIDAssociation
from openid.extensions.ax import FetchResponse
from openid.extensions.sreg import SRegResponse
from openid.store.interface import OpenIDStore as OIDStore

from allauth.account.internal.emailkit import valid_email_or_none

from .models import OpenIDNonce, OpenIDStore


class JSONSafeSession(UserDict):
    """
    openid puts e.g. class OpenIDServiceEndpoint in the session.
    Django 1.6 no longer pickles stuff, so we'll need to do some
    hacking here...
    """

    def __init__(self, session):
        UserDict.__init__(self)
        self.data = session

    def __setitem__(self, key, value):
        data = base64.b64encode(pickle.dumps(value)).decode("ascii")
        return UserDict.__setitem__(self, key, data)

    def __getitem__(self, key):
        data = UserDict.__getitem__(self, key)
        # We can avoid all of this once this is released:
        #     https://github.com/necaris/python3-openid/pull/71
        # We're not loading pickled data from an external source, so this
        # is safe.
        return pickle.loads(base64.b64decode(data.encode("ascii")))  # nosec


class OldAXAttribute:
    PERSON_NAME = "http://openid.net/schema/namePerson"
    PERSON_FIRST_NAME = "http://openid.net/schema/namePerson/first"
    PERSON_LAST_NAME = "http://openid.net/schema/namePerson/last"


class AXAttribute:
    CONTACT_EMAIL = "http://axschema.org/contact/email"
    PERSON_NAME = "http://axschema.org/namePerson"
    PERSON_FIRST_NAME = "http://axschema.org/namePerson/first"
    PERSON_LAST_NAME = "http://axschema.org/namePerson/last"


AXAttributes = [
    AXAttribute.CONTACT_EMAIL,
    AXAttribute.PERSON_NAME,
    AXAttribute.PERSON_FIRST_NAME,
    AXAttribute.PERSON_LAST_NAME,
    OldAXAttribute.PERSON_NAME,
    OldAXAttribute.PERSON_FIRST_NAME,
    OldAXAttribute.PERSON_LAST_NAME,
]


class SRegField:
    EMAIL = "email"
    NAME = "fullname"


SRegFields = [
    SRegField.EMAIL,
    SRegField.NAME,
]


class DBOpenIDStore(OIDStore):
    max_nonce_age = 6 * 60 * 60

    def storeAssociation(self, server_url, assoc=None):
        pass

    def getAssociation(self, server_url, handle=None):
        pass

    def removeAssociation(self, server_url, handle):
        pass

    def useNonce(self, server_url, timestamp, salt):
        pass


def get_email_from_response(response):
    email = None
    sreg = SRegResponse.fromSuccessResponse(response)
    if sreg:
        email = valid_email_or_none(sreg.get(SRegField.EMAIL))
    if not email:
        ax = FetchResponse.fromSuccessResponse(response)
        if ax:
            try:
                values = ax.get(AXAttribute.CONTACT_EMAIL)
                if values:
                    email = valid_email_or_none(values[0])
            except KeyError:
                pass
    return email


def get_value_from_response(response, sreg_names=None, ax_names=None):
    value = None
    if sreg_names:
        sreg = SRegResponse.fromSuccessResponse(response)
        if sreg:
            for name in sreg_names:
                value = sreg.get(name)
                if value:
                    break

    if not value and ax_names:
        ax = FetchResponse.fromSuccessResponse(response)
        if ax:
            for name in ax_names:
                try:
                    values = ax.get(name)
                    if values:
                        value = values[0]
                except KeyError:
                    pass
                if value:
                    break
    return value
