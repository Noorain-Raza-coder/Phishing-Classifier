from src.logger import logging
import sys


def error_message_detail(error , error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message_detial = f"Error occured in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message [{str(error)}] "
    
    return error_message_detial


class CustomException(Exception):      # CustomException class using the properties of exception class
    
    def __init__(self, error_message , error_detail : sys):
        super().__init__(error_message)
        self.error_message =  error_message_detail(error_message , error_detail = error_detail)

    def __str__(self) -> str:
        return self.error_message