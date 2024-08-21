def hi(x,y) { return x+y }

def mul(x,y) { return x*y }

def bool(x,y) {return x==y }

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

lite (x,y) {x/y}

#this is a comment
print(lite(48,4))
print(lite(lite(10,2),0))
print(fib(5))
print(fact(3))
print(bool(4,4))
print(bool(4,5))
print(mul(4,5))
print(hi(4,2))
print(hi(hi(3,4),5))

