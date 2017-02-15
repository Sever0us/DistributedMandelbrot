import time

GLOBAL_RATE_LIMIT = 1

def rate_limited(function):
    def wrapper(*args):
        # Start a timer
        function_start = time.time()

        # Execute function
        result = function(*args)

        elapsed_time = time.time() - function_start

        # If execution time is less that rate limit period, sleep
        remainder = GLOBAL_RATE_LIMIT - elapsed_time
        if remainder > 0:
            time.sleep(remainder)

        return result
    return wrapper
