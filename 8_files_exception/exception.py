

# try:

#    f2=open('/Users/hemantwagh/Desktop/fessorpro/data.txt','r')
#    d=f2.read()
#    print(d)
#    print(100/0)
# except:
#    print('something went wrong')
# print('this is very important line')






try:

   f2=open('/Users/hemantwagh/Desktop/fessorpro/data.txt','r')
   d=f2.read()
   print(d)
   print(100/10)
except Exception as e:
   print(e)
   print('something went wrong')
print('this is very important line')
