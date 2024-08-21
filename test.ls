def hi(x,y) { return x+y }

def mul(x,y) { return x*y }

def equel(x,y) {return x==y }

def fact(n) {
    return (n == 0) || (n * fact(n - 1))
} 

def fib(n) {
    return ((n == 0) || (n == 1)) || (fib(n-1) + fib(n-2))
}

def fact_nsc(n) {
    while (n == 0) {
        return 1
    }
    return n * fact_nsc(n - 1)
}

#Recursion without short-circut
print(fact_nsc(3))

while (true){
    print(3)
    break
}

#lite(lambda) Function test of mul
print((lite (x,y) x/y)(48,4))

#Recursion test
print(fib(5))
print(fact(3))

#Function test of equel
print(equel(4,4))
print(equel(4,5))

#Function test of add
print(hi(4,2))

#test Function composition
print(hi(hi(3,4),5))

#operation test

#arithmatic operation
print(3+4)
print(3-4)
print(3*4)
print(5/2)
print(3%1)

#logical operation
print(3 == 4)
print(3 != 4)
print(3 > 4)
print(3 < 4)
print(4 >= 4)
print(3 <= 3)

#conditional operation
print(false && true)
print(true || false)
print(!true)

#lite(lambda) test Function composition in mul by zero
print((lite (x,y) x/y)((lite(x,y) x/y)(4,5),0))