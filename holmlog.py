import requests
from datetime import datetime
import time
import pickle

update_interval = 20
times = ['01', '06', '11', '16', '21', '26', '31', '36', '41', '46', '51', '56']
prevtime = ''
try_again = False
slow = False

def open_file(d):
    try:
        with open('holmdata-' + d.strftime('%b-%d')+'.pkl', 'rb') as holm_r:
            f = pickle.load(holm_r)
    except FileNotFoundError:
        print('New file created')
        f = []
    return f

def get_data():
    
    r = requests.get('https://memberjourneyhub.com/holmesplace/api/admin/capacity/check?clubExternalIds[]=8,6,19,11&regionId=5')
    
    return r
    

def save_file(d, g):
    with open('holmdata-' + d.strftime('%b-%d') + '.pkl', 'wb') as holm_w:
        pickle.dump(g, holm_w)
        
flag = True
while flag == True:
    
    now = datetime.now()
    minn = now.strftime('%M')
    hrr = int(now.strftime('%H'))
    print('\ntick:', now.strftime('%H:%M:%S'), 'prevtime', prevtime, 'minn', minn, 'slow', slow, 'retry', try_again)
    
    # Retry
    
    if try_again == True:
        
        print('Retry')
        
        if slow == True:
            slow = False
        
        now = datetime.now()
        
        holmdata = open_file(now)
        data = get_data()

        try:
            checkins = data.json()['6']['currentlyCheckedInCount']
            print(now.strftime('%H:%M:%S'), 'Got data:', checkins)
            prevtime = minn
            try_again = False
        except:
            checkins = -1
            print(now.strftime('%H:%M:%S'), 'No data')
            try_again = True
        
        holmdata.append({'Timestamp' : now, 'Checkins' : int(checkins)})

        save_file(now, holmdata)
        del holmdata
            
    # End Retry
    
    # Init
    
    if prevtime == '':

        holmdata = open_file(now)
        data = get_data()

        try:
            checkins = data.json()['6']['currentlyCheckedInCount']
            print(now.strftime('%H:%M:%S'), 'Got data:', checkins)
            prevtime = minn
        except:
            checkins = -1
            print(now.strftime('%H:%M:%S'), 'No data')
            try_again = True
        
        holmdata.append({'Timestamp' : now, 'Checkins' : int(checkins)})

        save_file(now, holmdata)
        del holmdata
        
    # Slow
    
    if slow == True:
        
        print('Hourly update')
        
        holmdata = open_file(now)
        data = get_data()
        
        try:
            checkins = data.json()['6']['currentlyCheckedInCount']
            print(now.strftime('%H:%M:%S'), 'Got data:', checkins)
            prevtime = minn
        except:
            checkins = -1
            print(now.strftime('%H:%M:%S'), 'No data')
            try_again = True
        
        holmdata.append({'Timestamp' : now, 'Checkins' : int(checkins)})

        save_file(now, holmdata)
        del holmdata
    
    # Main
    
    if (minn != prevtime) & (minn in times) & (try_again == False) & (slow == False):        
        
        holmdata = open_file(now)
        data = get_data()

        try:
            checkins = data.json()['6']['currentlyCheckedInCount']
            print(now.strftime('%H:%M:%S'), 'Got data:', checkins)
            prevtime = minn
        except:
            checkins = -1
            print(now.strftime('%H:%M:%S'), 'No data')
            try_again = True

        holmdata.append({'Timestamp' : now, 'Checkins' : int(checkins)})

        save_file(now, holmdata)
        del holmdata
    
    if (hrr > 21) | (hrr < 6):
        slow = True
        print('Club is closed - update interval will be slow')
    else:
        slow = False
        print('Club is open')
        
    if (try_again == False) & (slow == True):
        update_interval = 1800
        print('Slow now - waiting 30 minutes')
    if try_again == True:
        update_interval = 10
        print('Need to try again - waiting 10 seconds')
    if (slow == False) & (try_again == False):
        update_interval = 20
        print('Normal - waiting 20 seconds')
    
    time.sleep(update_interval)