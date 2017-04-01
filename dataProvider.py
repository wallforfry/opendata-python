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


def get_consumption(html_data):
    parser = MyParser("consumption")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.consumptions[j]
        j += 1

    return d


def get_fossil(html_data):
    parser = MyParser("fossil")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.fossilPerc[j]
        j += 1

    return d


def get_nuclear(html_data):
    parser = MyParser("nuclear")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.nuclearPerc[j]
        j += 1

    return d


def get_hydroelectric(html_data):
    parser = MyParser("hydroelectric")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.hydroelectricPerc[j]
        j += 1

    return d


def get_other(html_data):
    parser = MyParser("other")
    parser.feed(html_data)
    d = {}
    j = 0
    for i in parser.countries:
        d[i] = parser.otherPerc[j]
        j += 1

    return d


def get_lat_long():
    """
    Retrieve lat and long with GoogleMaps Geocoding API and store it into countryCoordonates.json
    :return: None
    """
    infos = merge_info()
    result = []
    for elt in infos:
        result.append({"country": elt.get("country"), "coordonates": get_coordonates(elt.get("country"))})

    with open("countryCoordonates.json", mode="w") as f:
        f.write(json.dumps(result))


def merge_info():
    """
    Merge infos from web parsing and country's coordonates json file into data.json file
    :return: None
    """
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

    coordonates = json.loads(open("countryCoordonates.json", mode="r").read())
    i = 0

    consumption = get_consumption(dt[0])
    fossil = get_fossil(dt[1])
    nuclear = get_nuclear(dt[2])
    hydroelectric = get_hydroelectric(dt[3])
    other = get_other(dt[4])
    world = []
    for key in consumption.keys():
        c = {}
        c["country"] = key
        c["consumption"] = consumption.get(key)
        c["fossil"] = fossil.get(key)
        c["nuclear"] = nuclear.get(key)
        c["hydroelectric"] = hydroelectric.get(key)
        c["other"] = other.get(key)
        c["coordonates"] = coordonates[i].get("coordonates")
        world.append(c)

        i += 1

    with open("data.json", mode="w") as f:
        f.write(json.dumps(world))


def get_google_api_key():
    """
    Get GoogleMaps Geocoding api key from googleApiKey.txt file
    :return: String ApiKey
    """
    return open("googleApiKey.txt", mode="r").readline()


def get_coordonates(address):
    """
    Get coordonates (lat, lng) with GoogleMaps Geocoding API
    :param address: address you want to get
    :return: {"lat": LATITUDE, "lng": LONGITUDE}
    """
    apiKey = get_google_api_key()
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + urllib.request.quote(
        address) + "&key=" + apiKey
    try:
        html_data = urllib.request.urlopen(url)
        data = html_data.read().decode('utf8')
        result = json.loads(data)
        try:
            value = result["results"][0]["geometry"]["location"]
            return value
        except IndexError as e:
            print(e)

    except urllib.error.URLError as e:
        print("Pas de connexion internet")


def get_infos_for_basemap():
    """
    Return infos formated for basemap use

    :return: {"country": country_tab, "consumption": consumption_tab,
    "fossil": fossil_tab, "nuclear": nuclear_tab, "hydroelectric": hydroelectric_tab, "renewable": renewable_tab,
    "latitude": latitude_tab, "longitude": longitude_tab}
    """
    try:
        infos = json.load(open("data.json", mode="r"))

        country_tab = []
        consumption_tab = []
        fossil_tab = []
        nuclear_tab = []
        hydroelectric_tab = []
        renewable_tab = []
        longitude_tab = []
        latitude_tab = []

        for elt in infos:
            country = elt.get("country")
            country_tab.append(country)

            consumption = elt.get("consumption")
            consumption = consumption[:consumption.find(" ")].replace(",", ".")
            if consumption == "Non":
                consumption = "0"
            consumption_tab.append(float(consumption))

            fossil = str(elt.get("fossil"))
            fossil = fossil[:fossil.find("%")].replace(",", ".")
            if fossil == "Non":
                fossil = "0"
            fossil_tab.append(float(fossil))

            nuclear = str(elt.get("nuclear"))
            nuclear = nuclear[:nuclear.find("%")].replace(",", ".")
            if nuclear == "Non":
                nuclear = "0"
            nuclear_tab.append(float(nuclear))

            hydroelectric = str(elt.get("hydroelectric"))
            hydroelectric = hydroelectric[:hydroelectric.find("%")].replace(",", ".")
            if hydroelectric == "Non":
                hydroelectric = "0"
            hydroelectric_tab.append(float(hydroelectric))

            other = str(elt.get("other"))
            other = other[:other.find("%")].replace(",", ".")
            if other == "Non":
                other = "0"
            renewable_tab.append(float(other))

            longitude_tab.append(float(elt.get("coordonates").get("lng")))
            latitude_tab.append(float(elt.get("coordonates").get("lat")))

        return {"country": country_tab, "consumption": consumption_tab, "fossil": fossil_tab, "nuclear": nuclear_tab, "hydroelectric": hydroelectric_tab, "renewable": renewable_tab, "latitude": latitude_tab, "longitude": longitude_tab}

    except FileNotFoundError:
        merge_info()
        return get_infos_for_basemap()

if __name__ == "__main__":
    merge_info()
