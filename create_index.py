from data.personen import personen
from data.locaties import locaties
from data.commissies import commissies
from data.hoedanigheden import hoedanigheden
from data.organisaties import organisaties
from indexer import Indexer

def index_peronen():
    for pers in personen:
        element = {}
        element["id"] = pers["id"]
        element["name"] = pers["name"]
        element["category"] = 'Persoonsnaam'
        element["labels"] = pers["labels"]
        element = add_labels(element)
        element["raa"] = pers["raa"]
        element = add_raa(element)
        element["delegates"] = pers["delegates"]
        element = add_delegates(element)
        element["envoyes"] = pers["envoyes"]
        element = add_envoys(element)
        indexer.add_to_index(element)

def index_organisaties():
    for organisatie in organisaties:
        element = {}
        element["id"] = organisatie["id"]
        element["name"] = organisatie["name"]
        element["category"] = 'Organisatie'
        element["labels"] = organisatie["labels"]
        element = add_labels(element)
        element["links"] = organisatie["links"]
        indexer.add_to_index(element)

def index_commissies():
    for commissie in commissies:
        element = {}
        element["id"] = commissie["id"]
        element["name"] = commissie["name"]
        element["category"] = 'Commissie'
        if commissie["comment"]:
            element["comment"] = commissie["comment"]
        element["labels"] = commissie["labels"]
        element = add_labels(element)
        indexer.add_to_index(element)

def index_hoedanigheden():
    for hoedanigheid in hoedanigheden:
        element = {}
        element["id"] = hoedanigheid["id"]
        element["name"] = hoedanigheid["name"]
        element["category"] = 'Hoedanigheid'
        element["labels"] = hoedanigheid["labels"]
        element = add_labels(element)
        indexer.add_to_index(element)

def index_locaties():
    for locatie in locaties:
        element = {}
        element["id"] = locatie["id"]
        element["name"] = locatie["name"]
        try:
            element["comment"] = locatie["comment"]
        except:
            pass
        try:
            element["links"] = locatie["links"]
        except:
            pass
        element["geo_data"] = locatie["geo_data"]
        element["category"] = "Locatie"
        try:
            element["labels"] = locatie["labels"]
            element = add_labels(element)
        except:
            print("No labels")
        element = get_lat_lon(element)
        indexer.add_to_index(element)

def get_lat_lon(el):
    try:
        point = el["geo_data"]["coordinates"]
        point = point.replace("(", "");
        point = point.replace(")", "");
        latlon = point.split(',')
        el["geo_data"].update({'lat': latlon[0].strip(), 'lon': latlon[1].strip()})
    except Exception as error:
        print(error)
    return el

def add_raa(el):
    if el["raa"] and len(el["raa"]) > 0:
        buffer = []
        for element in el["raa"]:
            buffer.append({"name": element[0], "id": element[1]})
        el["raa"] = buffer
    else:
        el.pop('raa')
    return el

def add_delegates(el):
    if el["delegates"] and len(el["delegates"]) > 0:
        buffer = []
        for element in el["delegates"]:
            buffer.append({"name": element[0], "id": element[1]})
        el["delegates"] = buffer
        if not el["name"]:
            el["name"] = add_name(el["delegates"])
    else:
        el.pop('delegates')
    return el

def add_name(list):
    buffer = list[0][0].split(',')
    return buffer[0]

def add_envoys(el):
    if el["envoyes"] and len(el["envoyes"]) > 0:
        buffer = []
        item = {}
        for element in el["envoyes"]:
            if len(item) == 0:
                item['name'] = element
            else:
                if len(item) == 1:
                    item['link'] = element
                    buffer.append(item)
                    item = {}
        el["envoyes"] = buffer
        if not el['name']:
            el["name"] = el["envoyes"][0]["name"].split(',')[0]
    else:
        el.pop('envoyes')
    return el

def add_labels(el):
    if el["labels"] and len(el["labels"]) > 0:
        buffer = []
        for label in el["labels"]:
            buffer.append({"label": label})
        el["labels"] = buffer
    else:
        el.pop('labels')
    return el


indexer = Indexer()

index_peronen()
print("Persons indexed...")
index_locaties()
print("Locations indexed...")
index_commissies()
print("Commissions indexed...")
index_hoedanigheden()
print("Roles indexed...")
index_organisaties()
print("Organisations indexed...")
print("All done!")