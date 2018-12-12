import unittest
import Sima.Controller.LoginController as login

class BaseWidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget("The widget")
        
class LoginTestCase(BaseWidgetTestCase):
    def testGoodLogin(self):
        assert(login)
        
    def testAdminLogin(self):
        assert(login)
    
    def testGuestLogin(self):
        assert(login)
    
    def testUserNotExist(self):
        assert(login)
    
    def testInvalidCred(self):
        assert(login)