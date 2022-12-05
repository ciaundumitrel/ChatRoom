l1 = [1, 2]
l2 = [1, 2]

def f1(l):
    l[0]=10

def f2(l):
    l = [0, 0]

print(id(l1))
f1(l1)
print(id(l1))

print(id(l2))

f2(l2)
print(id(l2))