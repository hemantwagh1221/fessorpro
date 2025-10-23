

#install
#pip3 install module_name

#uninstall
#pip3 uninstall module_name

#list of modules
#pip3 list/freeze

#downgrading a module
#pip3 install module_name==version

#ugrade a module
#pip3 install --upgrade module_name



#prints every sec code 
def main_strategy():
    print('running main strategy')

import time
while True:
    dt1=dt.datetime.now()
    print(dt1)

    #every sec

    #every 5 min
    if dt1.second==1 and dt1.minute in range(0,50,5):
        main_strategy()
    #every 1 min
    if dt1.second==1 :
        main_strategy()

    
    time.sleep(1)











#pendulum
import pendulum as dt
import pandas as pd

# timezone='Asia/Kolkata'
timezone='America/New_York'
dt1=dt.datetime(2025,10,17)

print(dt1)
print(dt.now(tz=timezone))

start_hour,start_min=9,30
end_hour,end_min=10,5

current_time=dt.now(tz=timezone)

start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=timezone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=timezone)

print(current_time)
print(start_time)
print(end_time)

#before time
while True:
    if dt.now(tz=timezone)>start_time:
        break
    print('waiting for start time to reach',dt.now(tz=timezone))

def main_strategy():
    print('running main strategy')

import time
while True:

    dt1=dt.now(tz=timezone)    
    print(dt1)

   

    #every 5 min
    if dt1.second==1 and dt1.minute in range(0,50,1):
        main_strategy()
   
    
    time.sleep(1)


print('we have reach end time so closing program')    

