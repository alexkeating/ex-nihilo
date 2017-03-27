"""
app.exceptions
-----------------------
All exceptions used in the app code base are defined here.
"""


class AppException(Exception):
    """
    Base exception for the App.
    """


class MissingIdException(AppException):
    """
    No id at the top level of a json payload.
    """