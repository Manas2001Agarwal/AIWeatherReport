import sys
from custom_logging.my_logger import logger

class WeatherReportException(Exception):
    
    def __init__(self,error_message,error_detail:sys):
        self.error_message = error_message
        _,_,exc_tb = error_detail.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return f"error occured in python script: {self.file_name}, line number: {self.lineno} error message: {str(self.error_message)}" 
    
if __name__ == "__main__":
    try:
        x = 2/0
    except Exception as e:
        custom_exception = WeatherReportException(e,sys)
        logger.error(custom_exception)
        raise custom_exception