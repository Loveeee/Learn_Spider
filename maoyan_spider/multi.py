from xml.etree.ElementTree import Element, ElementTree
from xml.dom.minidom import parse
from xml.dom import minidom
from threading import Thread
from threading import Event
from collections import deque
from queue import Queue
from io import StringIO
import requests
import csv

q2 = deque()


def pretty(e, level=0):
    if len(e) > 0:
        e.text = '\n' + '\t' * (level + 1)
        for child in e:
            pretty(child, level + 1)
            child.tail = child.tail[: - 1]
            e.tail = '\n' + '\t' * level


class DownloadThread(Thread):
    def __init__(self, sid, queue):
        Thread.__init__(self)
        self.sid = sid
        self.url = "http://table.finance.yahoo.com/table.csv?s=%s.sz"
        self.url %= str(sid).rjust(6, '0')
        self.queue = queue

    def download(self, url):
        proxies = {"http": "http://135.245.48.34:8000"}

        # response = requests.get(url,proxies=proxies)
        # response = requests.get(url)
        # if response.ok:
        # return StringIO(response.content)
        f = open("pingan.csv")
        # reader = csv.reader(f)
        # return StringIO(reader)
        return StringIO(f.read())

    def run(self):
        print("download ", self.sid, self.url)

        data = self.download(self.url)
        self.queue.put((self.sid, data))


class ConvertThread(Thread):

    def __init__(self, queue, cEvent, tEvent):
        Thread.__init__(self)
        self.queue = queue

        self.cEvent = cEvent
        self.tEvent = tEvent

    def createXmlFromCsv(self, scsv, fxml):
        root = minidom.Document()
        dataElement = root.createElement("Data")
        reader = csv.reader(scsv)
        headers = reader.next()
        headers = map(lambda h: h.replace(' ', ''), headers)
        for row in reader:
            rowElement = root.createElement("Row")
            for tag, text in zip(headers, row):
                item = root.createElement(tag)
                item.appendChild(root.createTextNode(text))
                rowElement.appendChild(item)
            dataElement.appendChild(rowElement)
        fxml.write(root.appendChild(dataElement).toprettyxml())
        # return root.appendChild(dataElement)

    def csvToXml(self, scsv, fname):
        reader = csv.reader(scsv)

        headers = reader.next()
        root = Element('Data')
        for row in reader:
            eRow = Element('Row')
        root.append(eRow)
        for tag, text in zip(headers, row):
            e = Element(str(tag).replace(" ", "_"))
        e.text = text
        eRow.append(e)
        pretty(root)
        et = ElementTree(root)
        et.write(fname)

    def run(self):
        count = 0

        while True:
            sid, data = self.queue.get()
            if sid == - 1:
                print("-1 was called")
            self.cEvent.set()
            self.tEvent.wait()
            break
            if data:
                print(f'Convert to XML ...{sid}')
            fname = str(sid).rjust(6, '0') + '.xml'
            with open(fname, 'wb') as wf:
                self.createXmlFromCsv(data, wf)
            # self.csvToXml(data,wf)
            count += 1
            if count == 5:
                self.cEvent.set()
            self.tEvent.wait()
            self.tEvent.clear()
            count = 0


class TarThread(Thread):
    def __init__(self, cEvent, tEvent):

        Thread.__init__(self)

        self.count = 0
        self.cEvent = cEvent
        self.tEvent = tEvent
        self.setDaemon(True)

    def tarXml(self):

        self.count += 1

        tfname = '%d.tgz' % self.count
        tf = tarfile.open(tfname, "w:gz")
        for fname in os.listdir('.'):
            if fname.endswith('.xml'):
                tf.add(fname)
        os.remove(fname)
        tf.close()
        if not tf.members:
            os.remove(tfname)

    def run(self):

        while True:
            self.cEvent.wait()
            self.tarXml()
            self.cEvent.clear()
            self.tEvent.set()


q = Queue()
cEvent = Event()
tEvent = Event()
dThreads = [DownloadThread(i, q) for i in xrange(1, 13)]
cThreads = ConvertThread(q, cEvent, tEvent)

tThread = TarThread(cEvent, tEvent)
for t in dThreads:
    t.start()

cThreads.start()
tThread.start()

for t in dThreads:
    t.join()

q.put((- 1, None))
