# A simple logger to log the path through the application.  Will remake to a decorator.
#Created by Mark Mott
class Loggingdec():
    # Log entering a function
    def entry(self,func):
        print("Entering " + func)
    
    # Log exiting a function
    def exit(self,func):
        print("Exiting " + func)
    
    # Log an exception
    def error(self, exep):
        print("Exception: ", end='')
        print(exep)
