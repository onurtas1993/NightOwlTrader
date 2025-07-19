import logging
import threading

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('NightOwlTraderLogger')

# Global callback function
log_callback = None

# Lock for thread safety
log_lock = threading.Lock()


def set_log_callback(callback):
    global log_callback
    with log_lock:
        log_callback = callback


def log_message(message):
    with log_lock:
        logger.info(message)
        if log_callback:
            log_callback(message)
