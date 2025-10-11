

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