
class CIFPException(Exception):
    def print_errors(self):
        for k in self.errors.keys():
            print(k,self.errors[k])


class InvalidFormat(CIFPException):
    def __init__(self, message, errors={}):            
        super().__init__(message)        
        self.errors = errors

class InvalidIntegerFormat(InvalidFormat):
    pass

class InvalidFloatFormat(InvalidFormat):
    pass
        
