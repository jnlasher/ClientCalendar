from auth import GoogleOAuth
import time

class GoogleController:
    """ Creates the initial connection to the Google Calendar """
    def __init__(self, jsonFile):
        self.connection = auth.GoogleConnector(jsonFile)
        try:
            self.connection.Connect()
        except RuntimeError as err:
            self.__backoff(connection)
        print("connection made")

    def DisplayCode(self):
        print(self.connection.userCode)
        print(self.connection.verificationURL)

    def Permission(self):
        status = self.connection.CheckUpdates()
        if status:
            print("Connection was good!")
        else:
            print("Permission was denied.")

    def __backoff(self, connectionObject):
        """
        Handles an error that occurs when too many attempts to get a deviceCode
        are made to the Google server.
        :param: connectionObject object making the connection to the server
        """
        result = None
        while result is None:
            time.sleep(10)
            try:
                result = connectionObject.Connect()
            except RuntimeError:
                result = None
