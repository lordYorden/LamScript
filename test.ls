def hi(x,y) { return x+y }

def fact(n) {
    return (n == 0) || (n * fact(n - 1))
} 

def fib(n) {
    return ((n==0) || (n==1)) || (fib(n-1) + fib(n-2))
}

while (true){
    print(3)
    break
}

print(fib(5))
print(fact(3))
print(hi(4,2))