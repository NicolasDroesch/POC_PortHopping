# Writing by Atlas
# logger.py

import logging
import ctypes
import traceback
import os

class CustomFormatter(logging.Formatter):
    grey = "\x1b[90;20m"
    white = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s | %(asctime)s | %(filename)s | %(funcName)s | %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: white + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def enable_color_in_console():
    if os.name == "nt":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class Logger(logging.Logger):
    """ SINGLETON CLASS """        
    __instance = None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
            enable_color_in_console()
        return cls.instance
    
    def __init__(self):
        if not self.__instance:
            super().__init__("Logger")
            logging.basicConfig(level=logging.DEBUG)
            self.setLevel(logging.DEBUG)
            
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(CustomFormatter())
            self.addHandler(ch)
            self.__instance = 1

    def print_traceback(self, level=logging.ERROR):
        if self.isEnabledFor(level=level):
            msg = traceback.format_exc()
            self._log(level=level, msg=msg, args=None)

if __name__ == "__main__":
    def testColors() -> None:
        for i in range(0, 11):
            for j in range(0, 10):
                n = 10 * i + j
                if(n > 108):
                    return
                print(f"\x1b[{n}m {n}\x1b[m", end='')
            print("")

    # Print color in Shell
    testColors()
    # Test Logger color
    Logger().debug("Debug")
    Logger().info("Info")
    Logger().warning("Warning")
    Logger().error("Error")
    Logger().critical("Critical")
    Logger().print_traceback()
