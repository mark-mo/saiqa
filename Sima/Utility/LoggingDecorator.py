# A simple logger to log the path through the application
# Will remake to a decorator
class Loggingdec():
    def entry(self,func):
        print("Entering " + func)
    
    def exit(self,func):
        print("Exiting " + func)