import sys
import traceback
from typing import Optional, cast

class DocumentPortalException(Exception):
    def __init__(self, error_message, error_details: Optional[object] = None):
        # Normalize message
        if isinstance(error_message, BaseException):
            norm_msg = str(error_message)
        else:
            norm_msg = str(error_message)

        # Resolve exc_info (supports: sys module, Exception object, or current context)
        exc_type = exc_value = exc_tb = None
        if error_details is None:
            exc_type, exc_value, exc_tb = sys.exc_info()
        else:
            if hasattr(error_details, "exc_info"):  # e.g., sys
                #exc_type, exc_value, exc_tb = error_details.exc_info()
                exc_info_obj = cast(sys, error_details)
                exc_type, exc_value, exc_tb = exc_info_obj.exc_info()
            elif isinstance(error_details, BaseException):
                exc_type, exc_value, exc_tb = type(error_details), error_details, error_details.__traceback__
            else:
                exc_type, exc_value, exc_tb = sys.exc_info()

        # Walk to the last frame to report the most relevant location
        last_tb = exc_tb
        while last_tb and last_tb.tb_next:
            last_tb = last_tb.tb_next

        self.file_name = last_tb.tb_frame.f_code.co_filename if last_tb else "<unknown>"
        self.lineno = last_tb.tb_lineno if last_tb else -1
        self.error_message = norm_msg

        # Full pretty traceback (if available)
        if exc_type and exc_tb:
            self.traceback_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        else:
            self.traceback_str = ""

        super().__init__(self.__str__())

    def __str__(self):
        # Compact, logger-friendly message (no leading spaces)
        base = f"Error in [{self.file_name}] at line [{self.lineno}] | Message: {self.error_message}"
        if self.traceback_str:
            return f"{base}\nTraceback:\n{self.traceback_str}"
        return base

    def __repr__(self):
        return f"DocumentPortalException(file={self.file_name!r}, line={self.lineno}, message={self.error_message!r})"




if __name__ == "__main__":
    # --- SENIOR DEV HACK: Fix imports for standalone testing ---
    # Since we are running this file directly, we need to tell Python 
    # where to look for the 'logger' folder (which is one level up).
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # 1. Import your Logger
    from logger.custom_logger import CustomLogger

    # 2. Initialize the Logger
    logger = CustomLogger().get_logger()

    logger.info("Starting Exception Test...")

    # 3. Simulate a Crash and Log it
    try:
        a = 1 / 0  # The Crime
    except Exception as e:
        # The Investigation (Wrap the error)
        custom_err = DocumentPortalException("Intentional Division Fail", e)
        
        # The Report (Write to file)
        logger.error(custom_err) 
        
        # Optional: Print to console just so you see it happened
        print("Error has been logged! Check your logs folder.")

    
# if __name__ == "__main__":
#     # Demo-1: generic exception -> wrap
#     try:
#         a = 1 / 0
#     except Exception as e:
#         raise DocumentPortalException("Division failed", e) from e


# ... (Keep your Class definition above exactly as it is) ...
    # Demo-2: still supports sys (old pattern)
    # try:
    #     a = int("abc")
    # except Exception as e:
    #     raise DocumentPortalException(e, sys)