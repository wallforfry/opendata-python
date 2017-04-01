"""
Project : OpenData-python
File : test.py
Author : COHEN Johana
Date : 29/03/2017
"""
import urllib.request
from html.parser import HTMLParser
import json
import time


class MyParser(HTMLParser):
    def error(self, message):
        print("erreur")
        pass

    def __init__(self, info):
        super().__init__()
        self.countries = []
        self.consumptions = []
        self.fossilPerc = []
        self.hydroelectricPerc = []
        self.otherPerc = []
        self.nuclearPerc = []
        self.country = False
        self.consumption = False
        self.fossil = False
        self.nuclear = False
        self.hydroelectric = False
        self.other = False
        self.info = info

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            if attrs[0][0] == 'class' and attrs[0][1] == 'country':
                self.country = True

            if attrs[0][0] == 'class' and attrs[0][1] == 'fieldData':
                if self.info == "consumption":
                    self.consumption = True

                elif self.info == "fossil":
                    self.fossil = True

                elif self.info == "nuclear":
                    self.nuclear = True

                elif self.info == "hydroelectric":
                    self.hydroelectric = True

                elif self.info == "other":
                    self.other = True

    def handle_endtag(self, tag):
        self.country = False
        self.consumption = False
        self.fossil = False
        self.nuclear = False
        self.hydroelectric = False
        self.other = False

    def handle_data(self, data):
        if self.country:
            self.countries.append(data)
        if self.consumption:
            self.consumptions.append(data[1:])
        if self.fossil:
            self.fossilPerc.append(data[1:])
        if self.nuclear:
            self.nuclearPerc.append(data[1:])
        if self.hydroelectric:
            self.hydroelectricPerc.append(data[1:])
        if self.other:
            self.otherPerc.append(data[1:])


def getConsumption(html_data):
    parser = MyParser("consumption")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.consumptions[j]
        j += 1

    return d


def getFossil(html_data):
    parser = MyParser("fossil")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.fossilPerc[j]
        j += 1

    return d


def getNuclear(html_data):
    parser = MyParser("nuclear")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.nuclearPerc[j]
        j += 1

    return d


def getHydroelectric(html_data):
    parser = MyParser("hydroelectric")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.hydroelectricPerc[j]
        j += 1

    return d


def getOther(html_data):
    parser = MyParser("other")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.otherPerc[j]
        j += 1

    return d


def mergeInfo():
    l = []
    l.append("https://www.cia.gov/library/publications/the-world-factbook/fields/2233.html#xx")
    l.append("https://www.cia.gov/library/publications/the-world-factbook/fields/2237.html#xx")
    l.append("https://www.cia.gov/library/publications/the-world-factbook/fields/2239.html#xx")
    l.append("https://www.cia.gov/library/publications/the-world-factbook/fields/2238.html#xx")
    l.append("https://www.cia.gov/library/publications/the-world-factbook/fields/2240.html#xx")

    dt = []
    for url in l:
        try:
            u = urllib.request.urlopen(url)
        except urllib.request.URLError:
            print("Pas de connexion internet")
            return
        data = u.read().decode('utf8')
        dt.append(data)

    consumption = getConsumption(dt[0])
    fossil = getFossil(dt[1])
    nuclear = getNuclear(dt[2])
    hydroelectric = getHydroelectric(dt[3])
    other = getOther(dt[4])
    world = []
    for key in consumption.keys():
        c = {}
        c["country"] = key
        c["consumption"] = consumption.get(key)
        c["fossil"] = fossil.get(key)
        c["nuclear"] = nuclear.get(key)
        c["hydroelectric"] = hydroelectric.get(key)
        c["other"] = other.get(key)
        c["coordonates"] = get_coordonates(key)
        #time.sleep(.15)
        world.append(c)

    return world


def getGoogleApiKey():
    return open("googleApiKey.txt", mode="r").readline()

def get_coordonates(address):
    apiKey = getGoogleApiKey()
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + urllib.request.quote(address)+"&key="+apiKey
    try:
        html_data = urllib.request.urlopen(url)
        data = html_data.read().decode('utf8')
        result = json.loads(data)
        try:
            value = result["results"][0]["geometry"]["location"]
            return value
        except IndexError as e:
            print(result)
            print(e)

    except urllib.error.URLError as e:
        print("Pas de connexion internet")


def get_infos():
    return mergeInfo()


def main(url):
    mergeInfo()

    # proxy_address = 'http://147.215.1.189:3128/'
    # proxy_handler = urllib.request.ProxyHandler({'http': proxy_address})
    # opener = urllib.request.build_opener(proxy_handler)
    # urllib.request.install_opener(opener)
    # print("td class=\"titleColumn\"")

    return None

if __name__ == "__main__":
    print(get_infos())