import time
from selenium import webdriver


def wait(secs=2):
    """Makes the CPU sleep or stall for secs amount of time
    
    Keyword Arguments:
        secs {int} -- [number of seconds to wait] (default: {2})
    """
    time.sleep(secs)

def scroll_down(driver, pixels='document.body.scrollHeight'):
    pixels = str(pixels)
    driver.execute_script('window.scrollTo(0, %s);' % pixels)