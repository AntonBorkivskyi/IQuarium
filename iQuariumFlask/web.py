from flask import Flask, render_template, request
from random import randrange
from webbrowser import open_new_tab
import urllib.request
import cgi, cgitb
from time import time, localtime

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

    
@app.route('/time', methods=['POST'])
def time_last():
    all_time = time()
    extra_time = (46*365+11)*24*60*60
    time_from_2015 = all_time - extra_time
    current_time= int(time_from_2015)
    
    with open('static/time.txt') as time_file:
        last_feed = time_file.readline().strip()
        
    with open('static/frequency.txt') as freq_file:
        frequency = int(freq_file.readline().strip())
    
    time_to_feed = current_time-int(last_feed)
    time_to_feed = frequency - time_to_feed
    if time_to_feed <= 0:
        with open('static/time.txt', 'w') as time_file:
            time_file.write(str(current_time))
        with open('static/last_feeds.txt') as last_feeds_file:
            last_feeds = last_feeds_file.readlines()
        feeds_list = [el.strip() for el in last_feeds]
            
        new_feed_time = localtime(current_time+extra_time)
        new_feed = str(new_feed_time[0])+'/'+str(new_feed_time[1])+'/'+str(new_feed_time[2])+' '+str(new_feed_time[3])+':'+str(new_feed_time[4])+':'+str(new_feed_time[5])
        feeds_list.append(new_feed)
        if len(feeds_list) > 5:
            feeds_list.remove(feeds_list[0])
        with open('static/last_feeds.txt','w') as last_feeds_file:
            for el in feeds_list:
                last_feeds_file.write(el+'\n')
            
        time_to_feed = frequency
    time_lst = []
    
    time_lst.append(time_to_feed//3600)
    time_lst.append((time_to_feed-3600*time_lst[0])//60)
    time_lst.append(time_to_feed-3600*time_lst[0]-60*time_lst[1])
    
    
    for i in range(len(time_lst)):
        if time_lst[i] > 9:
            time_lst[i] = str(time_lst[i])
        else:
            time_lst[i] = '0'+str(time_lst[i])
    return(':'.join(time_lst))
    
    
@app.route('/feeds', methods=['POST'])
def get_feeds():
    with open('static/last_feeds.txt','r') as last_feeds_file:
        last_feeds = last_feeds_file.readlines()
    res = ''
    for el in last_feeds:
        res+='<br>'+el.strip()
    return res


@app.route('/temperature', methods=['POST'])
def temp():
    
    '''
    with open('static/temperature.txt') as temp_file:
        temp = eval(temp_file.readline().strip())
    
    if temp - norm_temp > 0 or norm_temp - temp > 0:
        with open('static/heat_water.txt','w') as heat_file:
            if norm_temp - temp > 0:
                heat_file.write('True')
            if temp - norm_temp > 0:
                heat_file.write('False')
    with open('static/temperature.txt','w') as temp_file:
        temp_file.write(str(round(temp-0.01,2)))
    '''
    #with open('static/norm_temp.txt') as norm_temp_file:
    #    norm_temp = round(int(norm_temp_file.readline().strip()),2)
    
    '''
    try:
        urllib.request.urlopen('http://172.16.36.108/', timeout=1)
    except urllib2.URLError as err: 
        return 'NULL'
    '''
    # url = 'http://172.16.36.108/' #AS@UCU
    # url = 'http:/10.0.128.83/' #CS@UCU
    url = 'http:/192.168.43.24/'
    #anton
    req=url
    #req =  urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}) 
    resp = urllib.request.urlopen(req)
    temp = float(resp.read().decode('utf-8'))
    
    '''
    with open('static/heat_water.txt','w') as heat_file:
            if norm_temp - temp > 0:
                heat_file.write('True')
            if temp - norm_temp >= 0:
                heat_file.write('False')
    '''
    
    if temp < -125:
        return 'NULL'
    return str(temp)
    #return '--.--'

    
@app.route('/heat', methods=['POST'])
def heat():
    with open('static/heat_water.txt') as heat_file:
        heating = heat_file.readline().strip()
        if heating == 'True':
            with open('static/temperature.txt') as temp_file:
                temp = eval(temp_file.readline().strip())
            with open('static/temperature.txt','w') as temp_file:
                temp_file.write(str(round(temp+0.1,2)))
            return('True')
        else:
            return('False')

            
@app.route('/freq', methods=['POST'])
def get_freq():
    with open('static/frequency.txt','r') as freq_file:
        frequency = int(freq_file.readline().strip())
    time_lst = []
    
    time_lst.append(frequency//3600)
    time_lst.append((frequency-3600*time_lst[0])//60)
    time_lst.append(frequency-3600*time_lst[0]-60*time_lst[1])
    for i in range(len(time_lst)):
        if time_lst[i] > 9:
            time_lst[i] = str(time_lst[i])
        else:
            time_lst[i] = '0'+str(time_lst[i])
    return(':'.join(time_lst))


@app.route('/set_freq', methods=['POST'])
def set_freq():
    data = request.get_data().decode('utf-8')
    with open('static/frequency.txt','w') as freq_file:
        freq_file.write(data)
    return 'True'
    
@app.route('/set_norm_temp', methods=['POST'])
def set_norm_temp():
    data = eval(request.get_data().decode('utf-8'))
    data = int(data)
    with open('static/norm_temp.txt','w') as freq_file:
        freq_file.write(str(data))
    return 'True'
    
@app.route('/new_freq_page')
def new_freq_page():
    return render_template('new_time.html')

@app.route('/new_temp_page')
def new_temp_page():
    return render_template('new_norm_temp.html')

if __name__ == '__main__':
    open_new_tab('http://localhost:8000')
    #app.run(debug=True,port=8000) if using open(url) - two tabs opening
    app.run(port=8000)
    
    