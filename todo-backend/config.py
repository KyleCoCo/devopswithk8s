import logging


def init_log_config():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,  # Adjust log level to DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    

