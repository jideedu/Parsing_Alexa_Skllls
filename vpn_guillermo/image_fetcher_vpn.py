import json
from bs4 import BeautifulSoup
import requests
from time import sleep
import shutil
import os 
from pymongo import MongoClient
import sys


from vpnocchio import VPN, init_logging
from threading import Thread

init_logging()

# set your dir with ovpn files, default is:
VPN.conf_dir = './ovpn_tcp'
# set minimum seconds must elapse between reconnects
VPN.min_time_before_reconnect = 15

credentials = [('guillermo.suarez.tangil@gmail.com', 'tcFI+9cyjOE2', '')]




client = MongoClient()
db = client['meme']

gallery_col = db['memes_image_galleries']

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def push_to_mongo(url, html):
    if gallery_col.find({'url':url}).count() == 0:
        gallery_col.insert_one({'url': url, 'html':html})
        print("Pushed to mongo. URL = %s" % url)
    else:
        print("Found in mongod")

def exists_in_mongo(url):
    if gallery_col.find({'url':url}).count() == 0:
        return False
    else:
        return gallery_col.find_one({'url':url})['html']


def crawl_kym(*args):
    vpn = VPN(*args)
    out_dir  = './memes_gallery_metadata/'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    proxy_count = 0
    meme_count =0
    requests_count = 0
    with open('memes_latest.json', 'r') as f:
        for line in f:
            data = json.loads(line)
            url = data['url']
            try:
                title = data['title']
            except KeyError:
                continue
            meme_count+=1
            page_count = 1
            name = url.split('/')[-1]
            output_name = out_dir + name + '.txt'
            if os.path.exists(output_name):
                print("Skipping %s" % output_name )
                continue
            output = open(out_dir + name + '.txt', 'w')
            while(1):
                requested= False
                url_page = url + '/photos/page/' + str(page_count)                
                try:
                    res = vpn.get(url_page, headers=headers)
                    requests_count+=1
                except:
                    proxy_count+=1
                    continue
                print("URL = %s Meme count =%d Status = %s" %(url_page,meme_count,str(res.status_code) ))
                proxy_count+=1
                html = res.content
                if('Your ip address' in html):
                    print("IP banned")
                    vpn.new_ip()
                    continue
                    #sys.exit()
                #print html
                page_count+=1
                soup = BeautifulSoup(html, "lxml")
                try:
                    scroller = soup.find("div", {"id": "infinite-scroll-wrapper"})
                    images = scroller.find_all("img")
                except Exception as e:
                    print("****** Error " + str(e))
                    push_to_mongo(url_page, html)
                    continue
                if len(images) == 0: 
                    break
                else:
                    push_to_mongo(url_page, html)
                    for img in images:
                        output.write(name + '\t' + str(img['data-src']) + '\n' )
                if requests_count % 20 == 0:
                    vpn.new_ip()

                #print("sleeping....")
                #sleep(5)
            output.close()        # it has requests inside

    vpn.disconnect()

for username, password, match_config_name in credentials:
    Thread(target=crawl_kym,
           args=(username,
                 password,
                 match_config_name)).start()






