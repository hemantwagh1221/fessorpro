


#iterable / looping / iteration
l1=[44,55,66,77]

#print(46 in l1)

#type 1 loop
total=0

for i in l1:
    total=total+i
print(total)    

l2=[10,10,10,10,10]
wallet=0
for i in l2:
    wallet=wallet+i
print(wallet)
num=len(l2)
print(num)
print(wallet/num)

l3=(4,5,6)
t=0
for i in l3:
    t=t+i
print(t/len(l3))    

#type 2 loop
print('hello')
print(list(range(20)))

for i in range(10):
    print('hello',i)

#generate a list of 50 even numbers
l4=[]
for i in range(100):
    if i%2==0:
        l4.append(i)
print(l4)        


#type 3 loop
#index

l1=[55,66,77,88,99]
for i in range(len(l1)):
    print(l1[i])
