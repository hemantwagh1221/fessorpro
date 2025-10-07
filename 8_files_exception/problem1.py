
p1=open('/Users/hemantwagh/Desktop/fessorpro/8_files_exception/story.txt','r')
d=p1.read()
print(d)
l=d.split('\n')
print(l)
# l.reverse()
print(l)
p1.close()

new_list=[]
for i in range(-1,-(len(l)+1),-1):
    new_list.append(l[i])
l=new_list
print(l)

p2=open('/Users/hemantwagh/Desktop/fessorpro/8_files_exception/story.txt','w')
for i in l:
    p2.write(i+'\n')
p2.close()