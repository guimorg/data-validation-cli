class BaseException(Exception):
    """Base class for exceptions"""


class InvalidConfiguration(BaseException):
    """Abstraction for invalid configuration file"""


class ValidationFunctionNotFound(BaseException):
    """Abstraction for missing Marshmarllow's Validation Function"""
