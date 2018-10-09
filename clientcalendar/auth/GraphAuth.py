import requests

class Office365OAuth:
    def __init__(self, applicationID, clientSecret, redirectURI=None):
        MOBILE_URI = "https://login.microsoftonline.com/common/oauth2/nativeclient"
        ## Client attributes
        self.__applicationID = applicationID
        self.__clientSecret  = clientSecret
        self.__redirectURI   = redirectURI if redirectURI is not None else MOBILE_URI
        self.__RESPONSE_TYPE = "code"
        self.__RESPONSE_MODE = "query"
        ## Server authorization details
        self.__AUTH_URL       = 'https://login.microsoftonline.com'
        self.__TENANT         = "common"
        self.__AUTH_ENDPOINT  = 'oauth2/v2.0/authorize'
        self.__TOKEN_ENDPOINT = 'oauth2/v2.0/token'
        self.__SCOPE          = ["Calendars.ReadWrite"]
        ## API Access information
        self.__RESOURCE_URL = "https://graph.microsoft.com/"
        self.__API_VERSION  = 'v1.0'

        self._headers = {'Content-Type': "application/x-www-form-urlencoded"}


    def Authorize(self):
        """ Attempts to make the connection to the Office 365 server """
        payload = {
            'client_id': self.__applicationID,
            'response_type': self.__RESPONSE_TYPE,
            'redirect_uri': self.__redirectURI,
            'response_mode': self.__RESPONSE_MODE,
            'scope': " ".join(self.__SCOPE),
            'state': self.__generateState()
        }
        request_url = "{}/{}/{}".format(self.__AUTH_URL,
                                        self.__TENANT,
                                        self.__AUTH_ENDPOINT)

        headers = self._headers
        res = requests.request('POST', url=request_url, data=payload, headers=headers)


    def __generateState():
        """ Generates a random state for the application to prevent
        Cross-Site forgery attacks by confirming the server is valid """
        #TODO
        return "123456"

## https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=9e542a09-ebea-482d-bb91-245198278b82&scope=Calendars.ReadWrite
code=OAQABAAIAAADXzZ3ifr-GRbDT45zNSEFEluXikXnXpP45rqjDjOMOw2PoMzp9vy868PTnR9pQH9tFrbGoumlx636JboClRR6bmG8iv_XgSNAIhrnqoeLVJ6d2-DngHiYhRjWvHlI0jHQh8298qxFJT2geWxWUf6o2EPuP_3d2y6HuL05jKsZ77ntiFINRUEtDBVpHlqeoGE-r17a5VjQR8Nx3XdfuCn8nsT9sles3iXzEWVWy-N8bM2LKvFkX1o7-PvB_gXKb15NdGe0lvUP9oU0Qoclvbsh1FMnz1vfIjgzAqppio3tMkJ-0F1f4-uTyTOAcflB6eM8Tt-Qo1FIfWyYYmc6dCGXWOPnKzoOr96jGK8vWfJbenjIsPIs6tG5_rc7fzMkLaZtt1_vlJcCB_gkcrHzDjO-nONNobgVeys0KgWGksWV7WkG19pubJnyGT27gPgO5IY5rVTa1N1MPmxlRzl_pRyUChyGLVDoc9u3ygd7RgsuuLKrXINpd3dzU1W-9WMBPZHHlXUk9cSgvJvida0VuXt-9DYxFreu6lRLO05x9RsUnlrTb7UaasAXFbsq19iJ3A7w_U9JIoPmrP5b-QMBudwRupKZ1Qni7JbrpE8XhxEWpasQiYjv7f8E8p5tfb03ibloeGh07m4StkNpS_szuszAahqwm6F-pCNQqAOBY7CWbeqaQHKOMQgPOJKl2Il38iArQtYa_ek5AAQ8X_o_fT2Q3ORbqq8mZ4vJedRolnDefFFs-1rQZzjFt_w48tO57nRwgAA
&state=123456
&session_state=ab573c3b-5dab-4d5c-bc9b-e5629d372392
