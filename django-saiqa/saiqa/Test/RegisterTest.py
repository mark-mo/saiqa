from saiqa.Model.UserModel import User
from saiqa.Service.UserService import UserService
from saiqa.Service.QuestionService import QuestionService
from saiqa.Exception.CustomException import FormatError, PasswordMismatchError, EmptyFormError
import re

service = UserService('test')
qser = QuestionService('test')

# List of tests:
#   Good Register
#   Password Mismatch
#   Incorrect Username Format
#   Incorrect Password Format 1
#   Incorrect Password Format 2
#   Bad Register
#   Duplicate User
def testregister(username, password, repassword):
    user = User(username, password)
    
    try:
        if user.getpassword() == '':
            raise EmptyFormError
        if user.getpassword() != repassword:
            raise PasswordMismatchError
    except PasswordMismatchError: # This would kick a user back to the register screen
        return 'Passwords do not match'
    except EmptyFormError: # This would kick a user back to the register screen
        return 'Empty form'
    
    specres = re.findall('[$&+,=?@`~^*%!-_]', user.getpassword())
    upres = re.findall('[A-Z]', user.getpassword())
    
    try:
        if(len(user.getusername()) < 4 or len(user.getusername()) > 20):
            raise FormatError
        if(len(user.getpassword()) < 4 or len(user.getpassword()) > 20):
            raise FormatError
        if(len(specres) < 2 or len(upres) < 2):
            raise FormatError
    except FormatError:
        return 'Incorrect formatting'
    # If true, the user exists
    if not (service.createUser(user)):
        return 'Duplicate user'
    return 'Good registration'