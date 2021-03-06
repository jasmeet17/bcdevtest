import re

class Helper(object):
    
    REQUEST_SUCCESS = {'success': True}
    REQUEST_FAIL = {'success': False, 'error':''}

    @staticmethod
    def parseException(e):
        """Parse an exception object and returns Type and Message"""
        exceptionType = Helper.parseExceptionType(e.args[0])
        message = Helper.parseExceptionMessage(e.args[0])
        
        return exceptionType, message

    @staticmethod
    def parseExceptionType(excMessage):
        """Parse Exception type from the Given String"""
        found = ''
        try:
            found = re.search('_mysql_exceptions.(.+?)error', excMessage).group(1)
        except AttributeError:
            found = 'Cannot find Type.'
        return found

    @staticmethod
    def parseExceptionMessage(excMessage):
        """Parse Exception Message from the Given String"""
        message = re.findall(r'"([^"]*)"', excMessage)
        
        if len(message)==1:
            return message[0]
        else:
            return "Cannot be parse."