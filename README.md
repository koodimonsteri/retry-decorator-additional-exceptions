# retry-decorator-additional-exceptions

Recently there was use case where I had retry decorator defined in general api function, however I needed to retry certain exception on another api function.
Modified existing retry decorator to also accept additional retry_exceptions as parameter.

Usage:

class MyAPI:

    def __init__(self):
        self.name = 'MyAPI'

    **general exceptions to retry defined here**
    @retry((ConnectionError,))
    def _make_request(self, url, retry_exceptions=None):
        print('making request to:', url)
        raise MyError()
    
    def get_data(self):
        return self._make_request('testi')
    
    def get_data2(self):
        **you can pass additional retry exceptions as parameter**
        return self._make_request('testi2', retry_exceptions=(MyError,))