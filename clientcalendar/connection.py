from enum import Enum

from auth import GoogleOAuth, GraphAuth, ExchangeAuth, Office365Basic

class Connection:
    def __init__(self, server_type, auth_type):
        self.server_type = self.__set_server_type(server_type.upper())
        self.auth_type = self.__set_auth_type(auth_type.upper())
        self.serv = self.ServerType
        self.auth = self.AuthType

    def connect(self, username=None, password=None,
                json_file=None, application_id=None,
                client_secret=None, **kwargs):

        if self.server_type is self.serv.EXCHANGE:
            assert((username & password) is not None)
            handler = ExchangeAuth()

        elif self.server_type is self.serv.GOOGLE:
            assert(json_file is not None)
            handler = GoogleOAuth(json_file)

        elif self.server_type is self.serv.OFFICE365:
            if self.auth_type is self.auth.BASIC:
                assert((username & password) is not None)
                handler = Office365Basic()

            elif self.auth_type is self.auth.OAUTHV2:
                handler = GraphAuth(application_id, client_secret)


    def __set_server_type(self, server_type):
        return self.serv[server_type]

    def __set_auth_type(self, auth_type):
        if self.server_type == self.serv.EXCHANGE:
            # Exchange supports Basic and NTLM
            assert(auth_type is not self.auth["OAUTHV2"])
        elif self.server_type == self.serv.OFFICE365:
            # Office 365 supports Basic and OAuthv2
            assert(auth_type is not self.auth["NTLM"])
        elif self.server_type == self.serv.GOOGLE:
            # Google only support OAuthv2
            assert(auth_type is self.auth["OAUTHV2"])

        return self.auth[auth_type]


class ServerType(Enum):
    EXCHANGE = "exchange"
    OFFICE365 = "office365"
    GOOGLE = "google"


class AuthType(Enum):
    BASIC  = "basic"
    NTLM   = "ntlm"
    OAUTHV2 = "oauthv2"
