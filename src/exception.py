import sys
from src.logger import logging
# Sys contains information about python environment altogether

def error_message_detail(error ,error_details:sys):
   ## exc-tb will give error occured in which part of the python environment
   _,_,exc_tb =  error_details.exc_info()
   file_name = exc_tb.tb_frame.f_code.co_filename

   error_msg = 'Error occured in python script name [{0}] line number [{1}] error message [{2}]',format(
      file_name , exc_tb.tb_lineno , str(error)
    
   )
   return error_msg


#This class is inheriting from Exception class present in python
class CustomException(Exception):
    def __init__(self, error_message , error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message , error_details = error_detail)

    def __str__(self) -> str:
       return self.error_message



    

# if __name__ == '__main__':
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info('Divide by Zero')
#         raise CustomException(e , sys)