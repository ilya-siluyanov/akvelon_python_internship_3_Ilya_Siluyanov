def fibonacci(n: int) -> int:
    """
    >>> fibonacci(0)
    0
    >>> fibonacci(1)
    1
    >>> fibonacci(10)
    55
    :param n:
    :return: n-th Fibonacci sequence number
    """
    if n < 0:
        # FIXME: raise an exception
        return 0
    a = 1
    if n == 1:
        return a
    b = 1
    if n == 2:
        return b
    for i in range(3, n + 1):
        c = a + b
        a, b = b, c
    return b
