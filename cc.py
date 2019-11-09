import requests
import json
import threading
import queue
import argparse

class commonCrawlDataClass():

    def __init__(self,domain):
        self.jsonIndexData = ""
        self.domain = domain
        self.domains = []
        self.q = queue.Queue()

    def getIndexes(self):
        indexURL = "https://index.commoncrawl.org/collinfo.json"
        r = requests.get(indexURL)
        jsonIndexData = json.loads(r.text)
        for index in jsonIndexData:
            self.q.put(index['id'])

    def getIndexData(self,indexID):
        try:
	    commonCrawlURL = "http://index.commoncrawl.org/"+indexID+"-index?url="+self.domain+"/*&output=json"
            r = requests.get(commonCrawlURL)
            data = r.text.split("\n")[:-1]
            for entry in data:
                url = json.loads(entry)['url']
                if url not in self.domains:
                    self.domains.append(url)
                    print(url)
        except:
            pass
    def worker(self):
        while 1:
            indexID = self.q.get()
            self.getIndexData(indexID)
            self.q.task_done()

    def start(self):
        self.getIndexes()
        for i in range(0,10):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
        self.q.join()


parser = argparse.ArgumentParser()
parser.add_argument("-d","--domain", help="Domain Name; EX: test.com")
args = parser.parse_args()

if args.domain:
    domain = args.domain
    cc = commonCrawlDataClass(domain)
    cc.start()
