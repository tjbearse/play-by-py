

def fib(n=2):
    if n <= 2:
        return 1
    return fib(n-1) + fib(n-2)

fib = fib(n=4)
print(fib)
