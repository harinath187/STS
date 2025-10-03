import logging
import os

# Create a logger instance
logger = logging.getLogger("HMSLogger")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if this file is imported multiple times
if not logger.hasHandlers():
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # File handler
    file_handler = logging.FileHandler(os.path.join(log_dir, "sts.log"))
    file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    # Attach formatter to both handlers
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
