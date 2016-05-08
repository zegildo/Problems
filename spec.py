#coding: utf-8
"""
Author: ZéGildo (zegilo@gmail.com)
---------------

Problem:
---------
Spec

Given a URL for a bitcointalk forum index (sample: https://bitcointalk.org/index.php?board=67.0), write a parser which returns the first 5 messages from the first 10 non-sticky topics.
Example Data

Example:
---------
Given the URL: https://bitcointalk.org/index.php?board=67.0

Should return something like:

[
    {
        'topic': "LISK investments are DONATIONS!",
        'messages': [
            {
                'user': 'Laniakea',
                'time': datetime.datetime(4, 25, 2016, 5, 23, 43),
                'message': '<html of message ...>',
            },
            {
                'user': 'thejaytiesto',
                'time': datetime.datetime(4, 25, 2016, 5, 27, 46),
                'message': '<html of message ...>',
            },
        ],
    },
    {
        'topic': '[XMR] Monero Speculation',
        'messages': [ ... etc ... ],
    },
    {
        'topic': 'Litecoin is officially living',
        'messages': [ ... etc ... ],
    },
    etc ...
]

"""
import sys
from lxml import html  
import requests  
from datetime import datetime

def getTopics(urls):
    topics = []
    for url in urls:
        topic = {}

        response = requests.get(url)  
        body = html.fromstring(response.text)
        pageTopic = body.xpath('//div[@class="nav"]/b/a[@class="nav"]/text()')[-1]
        topic['topic']  = pageTopic.encode('utf-8').strip()
        topic['messages'] = []

        users,times,messages = body.xpath('//td[@class="poster_info"]/b/a/text()'),body.xpath('//td[@valign="middle"]/div[@class="smalltext"]/text()'),body.xpath('//td[@class="td_headerandpost"]/div[@class="post"]/text()')
        for user,time,message in zip(users,times,messages):
            if(user != time and ',' in time):
                message = {'user':user, 'time':datetime.strptime(time, '%B %d, %Y, %I:%M:%S %p'), 'message':message}
                topic['messages'].append(message)
        topics.append(topic)
    print topics


"""
Script wrote to use with  *parallel -X*

O. Tange (2011): GNU Parallel - The Command-Line Power Tool,
;login: The USENIX Magazine, February 2011:42-47. 
                                                           ________.
python spec.py https://bitcointalk.org/index.php?board=67.|0      |
                                                          |-------|
                                                          |argv[1]|
                                                          |_______|
seq 0 40 37840 | parallel -X python Desktop/spec.py {}

"""
if __name__ == "__main__":

    ids = sys.argv[1:]
    
    for id in ids:

        URL = 'https://bitcointalk.org/index.php?board=67.%s'%(id)
        response = requests.get(URL)  
        body = html.fromstring(response.text)
        urls = body.xpath('//div[@class="tborder"]/table[@class="bordercolor"]/tr/td[@valign="middle"]/span[@id]/a/@href')
        getTopics(urls)

        