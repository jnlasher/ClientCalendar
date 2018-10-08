import json
import requests
import time

SUCCESS        = 200
DELETE_SUCCESS = 204
BAD_REQUEST    = 400
UNAUTHORIZED   = 401
FORBIDDEN      = 403
AUTH_PENDING   = 428
SLOW_DOWN      = 429

class GoogleConnector:
    """
    Creates a connection to the Google calendar API server.
    This connection must be an OAuth2-type connection
    """
    def __init__(self, jsonFile):
        self.__CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar"
        self.__AUTH_SERVER = "https://accounts.google.com/o/oauth2/device/code"
        self.__POLLING_URL = "https://www.googleapis.com/oauth2/v3/token"
        self.__GRANT_TYPE = "http://oauth.net/grant_type/device/1.0"

        data = self.__readFile(jsonFile)
        ## JSON attributes
        self.__clientID      = data["installed"]["client_id"]
        self.__project_id    = data["installed"]["project_id"]
        self.__auth_uri      = data["installed"]["auth_uri"]
        self.__token_uri     = data["installed"]["token_uri"]
        self.__auth_provider = data["installed"]["auth_provider_x509_cert_url"]
        self.__client_secret = data["installed"]["client_secret"]
        self.__redirect_uris = data["installed"]["redirect_uris"]
        ## Auth server attributes
        self._deviceCode     = ""
        self._userCode       = ""
        self._verification   = ""
        self._codeExpiresIn  = ""
        self._interval       = ""
        ## Auth response attributes
        self._accessToken    = ""
        self._tokenExpiresIn = ""
        self._tokenType      = ""
        self._refreshToken   = ""

        self._headers = {'Content-Type':'application/x-www-form-urlencoded'}


    ## --------------------------------------------------------------------- ##
    ## Begin public helper methods
    ## --------------------------------------------------------------------- ##
    def Connect(self, emulateDevice=True):
        """
        Attempts to make the connection to the Google server
        using the provided information. Google has several supported flows
        and emulateDevice can specify to use the IoT flow, otherwise,  the
        browser will make the browser auth flow.

        :param: emulateDevice - Identifies if the connection attempt should be
        a device flow
        """
        payload = {
            'client_id': self.__clientID,
            'scope': self.__CALENDAR_SCOPE
        }
        headers = self._headers
        response = requests.request('POST', self.__AUTH_SERVER, data=payload, headers=headers)
        if response.status_code == SUCCESS:
            res = response.json()
            self._deviceCode = res["device_code"]
            self._userCode = res["user_code"]
            self._verification = res["verification_url"]
            self._codeExpiresIn = res["expires_in"]
            self._interval = res["interval"]
        elif response.status_code == FORBIDDEN:
            ## TODO - Create custom error handler for this one
            raise RuntimeError("Request quota exceeded. Use backoff process.")
        else:
            raise Exception("Unexpected response from server.")

    def CheckUpdates(self):
        """
        Checks to see if the user has granted (or denied) access to the app.
        The polling time is dependent on the interval specified by the
        Google authentication server.
        """
        permissionGranted = False
        payload = {
            'client_id': self.__clientID,
            'client_secret': self.__client_secret,
            'code': self._deviceCode,
            'grant_type': self.__GRANT_TYPE
        }
        headers = self._headers
        response = requests.request('POST', self.__POLLING_URL, data=payload, headers=headers)

        while response.status_code in (AUTH_PENDING, SLOW_DOWN):
            if response.status_code == AUTH_PENDING:
                time.sleep(self._interval)
            elif response.status_code == SLOW_DOWN:
                time.sleep(self._interval * 2)
            response = requests.request('POST', self.__POLLING_URL, data = payload, headers=headers)

        if response.status_code == SUCCESS:
            res = response.json()
            self._accessToken = res['access_token']
            self._tokenExpiresIn = res['expires_in']
            self._tokenType = res['token_type']
            self._refreshToken = res['refresh_token']
            permissionGranted = True
        elif response.status_code == FORBIDDEN:
            self._accessToken = ""
            self._tokenExpiresIn = ""
            self._tokenType = ""
            self._refreshToken = ""
            permissionGranted = False
        elif response.status_code == UNAUTHORIZED:
            ## TODO - better handle edge cases
            raise Exception("An error occurred: {}".format(
                response.json()["error"]
            ))
        else:
            print('response code: {}'.format(response.status_code))
            raise Exception("Bad Request attempt \n Check for invalid data: {} {}".format(
                response.json()["error"], response.json()["error_description"]
            ))

        return permissionGranted

    ## --------------------------------------------------------------------- ##
    ## Begin class properties
    ## --------------------------------------------------------------------- ##
    @property
    def deviceCode(self):
        """ Unique device code, used to determine if a given device has been
        granted access to the services it is trying to access """
        return self._deviceCode

    @property
    def userCode(self):
        """ Code the user enters to validate an application """
        return self._userCode

    @property
    def codeExpiresIn(self):
        """ Time in seconds until the devices code and user code are invalid """
        self.__begin_countdown()
        return self._codeExpiresIn

    @property
    def verification(self):
        """ URL that should be used with the user code to authenticate a device """
        return self._verification

    @property
    def interval(self):
        """ Amount of time in seconds to wait between polling requests """
        return self._interval

    @property
    def accessToken(self):
        return self._accessToken

    @property
    def tokenExpiresIn(self):
        return self._tokenExpiresIn

    @property
    def tokenType(self):
        return self._tokenType

    @property
    def refreshToken(self):
        return self._refreshToken

    ## --------------------------------------------------------------------- ##
    ## Begin private helper methods
    ## --------------------------------------------------------------------- ##
    def __beginCountdown(self):
        #TODO - handle timeout/countdown of the user code
        pass

    def __readFile(self, jsonClientData):
        try:
            with open(jsonClientData, encoding='utf-8', errors='strict') as f:
                data = json.load(f)
        except ValueError as e:
            raise("ValueError, encoding issue: {}".format(e))
        except OSError as e:
            raise("OSError - reason: {}".format(e))
        return data
