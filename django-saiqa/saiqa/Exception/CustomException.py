# Custom exceptions
class Error(Exception):
    pass

class EmptyFormError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class FormatError(Exception):
    pass

class PasswordMismatchError(Exception):
    pass

class DuplicateUserError(Error):
    pass