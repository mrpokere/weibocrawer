# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 18:51:27 2019

@author: 2271057973
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 19:10:12 2018

@author: 2271057973
"""

import requests
import threading
import os
from bs4 import BeautifulSoup
from hashlib import md5
import re
import time
import tkinter as tk
from os.path import join, abspath

window = tk.Tk()
window.title('微博下载专用工具')
window.geometry ('+500+300')
window.geometry ('400x400')
pause_lock = threading.Event()
l = tk.Label(window,bg = 'yellow',width=20,text='网址')
l.grid(row=1,column=1)
e = tk.Entry(window,show=None)
e.grid(row=1,column=2)
l = tk.Label(window,bg = 'yellow',width=20,text='页数')
l.grid(row=2,column=1)
d = tk.Entry(window,show=None)
d.grid(row=2,column=2)    



def get_pictureandvideo(ID,x,page):
    
    baseurl = 'https://m.weibo.cn/api/container/getIndex?' 
    y = x.split('&')
    l = {'type':'uid'}
    for i in y:
        if 'https://m.weibo.cn' in i:       
            i = i.split('?')
            l['value'] = i[0][-10:-1]      
            i = i[1].split('=')
            l[i[0]] = i[1]        
        else:
            i = i.split('=')
            l[i[0]] = i[1]
    
    url = x
    headers = {'User-Agent':'Mozill\
                   a/5.0 (\Linux; Android 6.0; Nexus 5 Build/MRA58\
                   N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7\
                   0.0.3538.110 Mobile Safari/537.36'}
    res= requests.get(url,headers = headers)
    data = res.text
    pat = '"value":"(.*?)"}]'
    target = re.compile(pat).findall(data)[0]
    l['containerid'] = '107603{}'.format(target)
    l['page'] = str(page)
    params = l
    
    res = requests.get(baseurl,params = params,headers = headers)
    data = res.json()
    cards = data.get('data','None').get('cards','None')
    for item in cards:
        mblog = item.get('mblog','0')
        if mblog == '0':continue
        title = mblog.get('text','0')
        user = mblog.get('user','0')['screen_name']
        text=tk.Text(window,width=20,height=20)
        text.grid(row=6,column=1)
        text.insert(tk.END,'用户:'+user)
        text.see(tk.END)
        text.update()
        
        title = BeautifulSoup(title,'html.parser')
        title1 = str(title)
        title1 = re.sub(r'<.*>','',title1).strip()
        #print(title)
        
        title = title.find_all('span',class_="surl-text")
        #print(title)
        title_ = [item.string for item in title]
        temp_title = ''
        for item in title_:
            if '#' in item:
                item = item
                temp_title += item
            elif '' == item:
                temp_title += ''
            else:
                item = '#'+item+'#'
                temp_title += item
        title = title1 + temp_title
        pics = mblog.get('pics','0')
        if pics != '0':
            title_picture = mblog.get('text','0')#图片标题
            title_picture = BeautifulSoup(title_picture,'lxml').get_text().strip().replace('.','').replace('\n','')
            title_picture = re.sub(r'[<|>|\|/|:|"|*|? ]','',title_picture)
            #print(title_picture)
            if not os.path.exists('./{}/picture/{}'.format(ID,title_picture)):
                    os.mkdir('./{}/picture/{}'.format(ID,title_picture))
            for item in pics:
                picture = item.get('large','0').get('url','0')#图片
                #print(picture)
                if picture == '':
                    continue
                r = requests.get(picture)
                
                with open(r'./{0}/picture/{1}/{2}.jpg'.format(ID,title_picture,md5(r.content).hexdigest()),'wb') as f:
                    f.write(r.content)
        page_info = mblog.get('page_info','0')
        if page_info == '0':continue
        media_info = page_info.get('media_info','0')
        if media_info == '0':continue
        video_url = media_info.get('stream_url','0')#视频
        r = requests.get(video_url,headers=headers)
        title = re.sub(user+r'的.*视频','',title)
        title = title.replace('###','#')
        title = re.sub(r'[<|>|\|/|:|"|*|? ]','',title)
        if title[-2] + title[-1] == '##':
            title = title.replace('##','')
        print(title)
        with open('./{}/vedio/{}.mp4'.format(ID,title),'wb') as f:
            f.write(r.content)
        print()

def main_pictureandvideo(event):
    requests.utils.DEFAULT_CA_BUNDLE_PATH = join(abspath('.'), 'cacert.pem')
    event.wait()
    x = e.get()
    page = d.get()
    ID = x[21:31]
    #.format(x[21:31])
    if not os.path.exists('./{}'.format(ID)):
        os.mkdir('./{}'.format(ID))
    elif os.path.exists('./{}'.format(ID)):
        pass
    if not os.path.exists('./{}/picture'.format(ID)):
        os.mkdir('./{}/picture'.format(ID))
    elif os.path.exists('./{}/picture'.format(ID)):
        pass
    if not os.path.exists('./{}/vedio'.format(ID)):
        os.mkdir('./{}/vedio'.format(ID))
    elif os.path.exists('./{}/vedio'.format(ID)):
        pass
    for i in range(2,int(page)):#页数
        event.wait()
        time.sleep(2)
        try:
            print(i)
            get_pictureandvideo(ID,x,i)
        except:
            pass
      

def get_picture(ID,x,page):
    baseurl = 'https://m.weibo.cn/api/container/getIndex?'
    y = x.split('&')
    l = {'type':'uid'}
    for i in y:
        if 'https://m.weibo.cn' in i:       
            i = i.split('?')
            l['value'] = i[0][-10:-1]      
            i = i[1].split('=')
            l[i[0]] = i[1]        
        else:
            i = i.split('=')
            l[i[0]] = i[1]
    url = x
    headers = {'User-Agent':'Mozill\
                   a/5.0 (\Linux; Android 6.0; Nexus 5 Build/MRA58\
                   N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7\
                   0.0.3538.110 Mobile Safari/537.36'}
    res= requests.get(url,headers = headers)
    data = res.text
    pat = '"value":"(.*?)"}]'
    target = re.compile(pat).findall(data)[0]
    l['containerid'] = '107603{}'.format(target)
    l['page'] = str(page)
    params = l  
    res = requests.get(baseurl,params = params,headers = headers)
    data = res.json()
    cards = data.get('data','None').get('cards','None')
    for item in cards:
        mblog = item.get('mblog','0')
        if mblog == '0':continue
        title = mblog.get('text','0')
        user = mblog.get('user','0')['screen_name']
        
        pics = mblog.get('pics','0')
        
        if pics != '0':
            title_picture = mblog.get('text','0')#图片标题
            title_picture = BeautifulSoup(title_picture,'lxml').get_text().strip().replace('.','').replace('\n','')
            title_picture = re.sub(r'[<|>|\|/|:|"|*|? ]','',title_picture)
            print(title_picture)
            if not os.path.exists('./{}/picture/{}'.format(ID,title_picture)):
                    os.mkdir('./{}/picture/{}'.format(ID,title_picture))
            for item in pics:
                picture = item.get('large','0').get('url','0')#图片
                #print(picture)
                if picture == '':
                    continue
                r = requests.get(picture)
                
                with open(r'./{0}/picture/{1}/{2}.jpg'.format(ID,title_picture,md5(r.content).hexdigest()),'wb') as f:
                    f.write(r.content)
        
        print()

def main_picture(event):
    requests.utils.DEFAULT_CA_BUNDLE_PATH = join(abspath('.'), 'cacert.pem')
    x = e.get()
    event.wait()
    page = d.get()
    ID = x[21:31]
    #.format(x[21:31])
    
    if not os.path.exists('./{}'.format(ID)):
        os.mkdir('./{}'.format(ID))
    elif os.path.exists('./{}'.format(ID)):
        pass
    if not os.path.exists('./{}/picture'.format(ID)):
        os.mkdir('./{}/picture'.format(ID))
    elif os.path.exists('./{}/picture'.format(ID)):
        pass
    for i in range(1,int(page)):#页数
        time.sleep(2)
        event.wait()
        try:
            get_picture(ID,x,i)
            print(i)
        except:
            pass
        
               

def get_vedio(ID,x,page):
    
    baseurl = 'https://m.weibo.cn/api/container/getIndex?' 
    y = x.split('&')
    l = {'type':'uid'}
    for i in y:
        if 'https://m.weibo.cn' in i:       
            i = i.split('?')
            l['value'] = i[0][-10:-1]      
            i = i[1].split('=')
            l[i[0]] = i[1]        
        else:
            i = i.split('=')
            l[i[0]] = i[1]
    
    url = x
    headers = {'User-Agent':'Mozill\
                   a/5.0 (\Linux; Android 6.0; Nexus 5 Build/MRA58\
                   N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7\
                   0.0.3538.110 Mobile Safari/537.36'}
    res= requests.get(url,headers = headers)
    data = res.text
    pat = '"value":"(.*?)"}]'
    target = re.compile(pat).findall(data)[0]
    l['containerid'] = '107603{}'.format(target)
    l['page'] = str(page)
    params = l
    
    res = requests.get(baseurl,params = params,headers = headers)
    data = res.json()
    cards = data.get('data','None').get('cards','None')
    for item in cards:
        mblog = item.get('mblog','0')
        if mblog == '0':continue
        title = mblog.get('text','0')
        user = mblog.get('user','0')['screen_name']
        
        text=tk.Text(window,width=20,height=20)
        text.grid(row=6,column=1)
        text.insert(tk.END,'用户:'+user)
        text.see(tk.END)
        text.update()
        title = BeautifulSoup(title,'html.parser')
        title1 = str(title)
        title1 = re.sub(r'<.*>','',title1).strip()
        #print(title)
        
        title = title.find_all('span',class_="surl-text")
        #print(title)
        title_ = [item.string for item in title]
        temp_title = ''
        for item in title_:
            if '#' in item:
                item = item
                temp_title += item
            elif '' == item:
                temp_title += item
            else:
                item = '#'+item+'#'
                temp_title += item
        title = title1 + temp_title
        
                
        page_info = mblog.get('page_info','0')
        if page_info == '0':continue
        media_info = page_info.get('media_info','0')
        if media_info == '0':continue
        video_url = media_info.get('stream_url','0')#视频
        r = requests.get(video_url)
        title = re.sub(user+r'的.*视频','',title)
        title = title.replace('###','#')
        title = re.sub(r'[<|>|\|/|:|"|*|? ]','',title)
        if title[-2] + title[-1] == '##':
            title = title.replace('##','')
        print(title)
        #title = title.replace('##的秒拍视频','')
        #title = re.sub('[#.]','',title)
        with open('./{}/vedio/{}.mp4'.format(ID,title),'wb') as f:
            f.write(r.content)
        #print(title)
        #print(video_url)
        
        print()

def main_vedio(event):
    x = e.get()
    requests.utils.DEFAULT_CA_BUNDLE_PATH = join(abspath('.'), 'cacert.pem')
    event.wait()
    page = d.get()
    ID = x[21:31]
    #.format(x[21:31])
    if not os.path.exists('./{}'.format(ID)):
        os.mkdir('./{}'.format(ID))
    elif os.path.exists('./{}'.format(ID)):
        pass
    if not os.path.exists('./{}/vedio'.format(ID)):
        os.mkdir('./{}/vedio'.format(ID))
    elif os.path.exists('./{}/vedio'.format(ID)):
        pass
    for i in range(1,int(page)):#页数
        time.sleep(1)
        event.wait()
        try:
            get_vedio(ID,x,i)
            print(i)
        except:
            pass
       
          
           
def toggle(event,color,start = True):
    color['bg'] = 'red'
    if start:
        event.set()
        print('Starting Thread')
    else:
        event.clear()
        print('Pausing Thread')
    
#一起的
def picturevedio(line,color,text):
    color['bg'] = 'red'
    if text['text'] == '激活图片和视频功能':
        text['text'] = '已激活图片和视频功能'
    elif text['text'] == '激活图片功能':
        text['text'] = '已激活图片功能'
    elif text['text'] == '激活视频功能':
        text['text'] = '已激活视频功能'
    t = threading.Thread(target = line,args = (pause_lock,))
    t.start()
                    
#picture
selct_b = tk.Button(window,bg = 'white',text='激活图片和视频功能',width=15, height=2,
                  command=lambda : picturevedio(main_pictureandvideo,selct_b,selct_b))
start_b = tk.Button(window,bg = 'white',text='下载图片和视频',width=15, height=2,
                  command=lambda : toggle(pause_lock,start_b,True))
pause_b = tk.Button(window,bg = 'white',text='暂停下载',width=15, height=2,
                  command=lambda : toggle(pause_lock,pause_b,False))

selct_b.grid(row=3,column=1)
start_b.grid(row=3,column=2)
pause_b.grid(row=3,column=3)

selct_c = tk.Button(window,text='激活图片功能',width=15, height=2,
                  command=lambda : picturevedio(main_picture,selct_c,selct_c))
start_c = tk.Button(window,bg = 'white',text='下载图片',width=15, height=2,
                  command=lambda : toggle(pause_lock,start_c,True))
pause_c = tk.Button(window,bg = 'white',text='暂停下载',width=15, height=2,
                  command=lambda : toggle(pause_lock,pause_c,False))
selct_c.grid(row=4,column=1)
start_c.grid(row=4,column=2)
pause_c.grid(row=4,column=3)
selct_d = tk.Button(window,text='激活视频功能',width=15, height=2,
                  command=lambda : picturevedio(main_vedio,selct_d,selct_d))
start_d = tk.Button(window,bg = 'white',text='下载视频',width=15, height=2,
                  command=lambda : toggle(pause_lock,start_d,True))
pause_d = tk.Button(window,bg = 'white',text='暂停下载',width=15, height=2,
                  command=lambda : toggle(pause_lock,pause_d,False))
selct_d.grid(row=5,column=1)
start_d.grid(row=5,column=2)
pause_d.grid(row=5,column=3)

window.mainloop()