import concurrent.futures
import time
import urllib.request
import inspect

# URLS = [('http://www.foxnews.com/', 60),
#         ('http://www.cnn.com/', 60),
#         ('http://www.foxnews.com/', 60),
#         ('http://www.foxnews.com/', 60),
#         ('http://www.foxnews.com/', 60)]
#
#
# def load_url(url, timeout):
#     print(f"!({url} {timeout})!")
#     with urllib.request.urlopen(url, timeout=timeout) as conn:
#         return conn.read()


def start_thread_pool(f, args: list, threads=None):
    """
    Runs code in threads
    :param f: function
    :param args: array of tuple
    :param threads: Count of threads. If None - same as len of args
    :return:
    """
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_task = {executor.submit(f, *arg1): arg1 for arg1 in args}
        for future in concurrent.futures.as_completed(future_task):
            arg2 = future_task[future]
            try:
                res.append((arg2, future.result(), None))
            except Exception as exc:
                print(f"start_thread_pool exception: {str(str)}")
                res.append((arg2, None, exc))
    return res


v = [
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 2),
        (3, "2aS")
    ]


def f(a, b):
    print("!", a, b)
    time.sleep(1)
    return a+b


r = start_thread_pool(f, v)
print(r)
