from saiqa.Model.UserModel import User
from saiqa.Service.UserService import UserService
from saiqa.Service.QuestionService import QuestionService

service = UserService('test')
qser = QuestionService('test')

# List of tests:
#   Good Login
#   User Does not Exist
#   Bad Login
#   Random Fact Returned
def testlogin(username, password):
    user = User(request.POST.get('username'), request.POST.get('password'))
    
    if user.getusername() == '':
        return 'Bad Login'
    # Log in
    foundU = service.findUser(user)
    if foundU == -1:
        # Replace with error
        logging.exit("LoginController.login")
        return 'User not found'
    user.setpermission(foundU)
    return user

# Tests a random fact being returned and not a blank string
def testrandfact():
    return qser.findbyrandom()