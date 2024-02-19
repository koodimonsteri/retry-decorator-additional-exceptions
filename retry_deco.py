import time
from requests import HTTPError, ConnectionError
from functools import wraps


def retry(retry_on_exception, max_retries=3, delay_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            all_errors = retry_on_exception + kwargs.get('retry_exceptions', ())
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except all_errors as e:
                    print(f"Caught exception: {e}. Retrying...")
                    retries += 1
                    time.sleep(delay_seconds)
            raise HTTPError(f"Max retries reached for {func.__name__}")

        return wrapper
    return decorator


class MyError(HTTPError):
    pass


class MyAPI:

    def __init__(self):
        self.name = 'MyAPI'

    @retry((ConnectionError,))
    def _make_request(self, url, retry_exceptions=None):
        print('making request to:', url)
        raise MyError()
    
    def get_data(self):
        return self._make_request('testi')
    
    def get_data2(self):
        return self._make_request('testi2', retry_exceptions=(MyError,))


def main():
    my_api = MyAPI()
    try:
        my_api.get_data()
    except Exception:
        print('get_data failed')
        
    
    try:
        my_api.get_data2()
    except Exception:
        print('get_data2 failed')
        


if __name__ == '__main__':
    main()
