import time

# based on https://stackoverflow.com/a/2785908/1056345                                                                                                                                                                                                                                                                         
def wait_until(somepredicate, timeout, period=1, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        if somepredicate(*args, **kwargs):
            return True
        time.sleep(period)
    return False
