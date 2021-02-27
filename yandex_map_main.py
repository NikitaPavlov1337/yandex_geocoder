# https://geocode-maps.yandex.ru/1.x/?apikey=Your API key&geocode=28.978798,41.006543&lang=en_US

import csv
from yandex_map_config import token
import requests



def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()[8000:8999] # puts the file into an array
    fileObj.close()
    return words


def fetch_coordinates(token, place):
    defolt_lat = 0
    defolt_lon = 0
    defolt_country = 0
    defolt_subject = 0
    defolt_city = 0
    defolt_street = place
    defolt_house = 0
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": token, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']

    try:
        most_relevant = places_found[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        # country = most_relevant['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName']
        lst = most_relevant['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components']
        new_dict = {}
        new_list = []
        new_list.append(lon)
        new_list.append(lat)
        for dct in lst:
            for k, v in dct.items():
                if k != 'name':
                    i = v
                for key, value in dct.items():
                    if key != 'kind':
                        new_dict[i] = value
        for keys, values in new_dict.items():
            if keys != 'area' and keys != 'district':
                new_list.append(values)

        print(new_list)
        return new_list

    except:
        return defolt_country,defolt_subject,defolt_city,defolt_street, defolt_house,defolt_lat, defolt_lon


file = readFile('in/to_match4.csv')


stopwords = ['нежилое','помещение','торговый','нежилого', 'территории','нежилых','в части','часть','пом',
             'назначение','в части отдельно стоящего здания','нежилые помещения','подъезд','номера на поэтажном плане',
             'номера помещений на поэтажном плане','номера на поэтажном плане','от жилого дома','на поэтажном плане',
             'на первом этаже','пом.','расположенный в нежилом встроенном помещении','в районе дома','участок',
             'нестационарный объект','номера на поэтажном','жилого дома','пом.iv','торгово-выставочный комплекс','этаж',
             'помещения на поэтажном плане','здание литер под/у','по техническому плану','от земельного участка','коридор без номера',
             'номера на поэтажном плане','(нежилые помещения','расположенные']
result = []
for str in file:
    str = str.lower()
    list = str.split(', ')
    proverka = [s for s in list if not any(w in stopwords for w in s.split())]
    proverka = ",".join(proverka)
    print(proverka)
    callback = fetch_coordinates(token,proverka)
    result.append(callback)


file2 = open('out/new_output10.csv', 'w+', newline='')
with file2:
    write = csv.writer(file2)
    write.writerows(result)



if __name__ == '__main__':
    pass
