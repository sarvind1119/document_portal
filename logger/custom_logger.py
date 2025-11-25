import logging
import os
from datetime import datetime
import structlog

class CustomLogger:
    def __init__(self, log_dir="logs"):
        # Ensure the log directory exists
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Timestamped log file name
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)

    # <--- FIX: Indentation moved back (aligned with __init__)
    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)

        # Configure logging for console + file
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        # Setup standard logging
        # We check if handlers exist to avoid adding them twice if called multiple times
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s",
                handlers=[file_handler, console_handler]
            )

        # Configure structlog
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer() # <--- FIX: This must be LAST
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)

if __name__ == "__main__":
    custom_logger = CustomLogger()
    logger = custom_logger.get_logger(__file__)

    logger.info("This is an info message Arvind")
    logger.error("This is an error message", key2="value2")