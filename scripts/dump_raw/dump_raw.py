from pandas import DataFrame
from random import choice, randint
import random
from datetime import datetime, timedelta, time
from base64 import b64encode
from os import makedirs, path as Path
from utils import data
from elasticsearch import Elasticsearch
# from urllib3 import disable_warnings
# disable_warnings()

TEMP_FOLDER = "/mnt/data/cdr/raw"
ES_INDEX = "raw_cdr"
def create_row(flux="FLUX", techno="TECHNO"):
    current = datetime.now().strftime('%Y-%m-%d  %H')
    date = current.split("  ")[0]
    heure = current.split("  ")[1] 
    minute = randint(1, 59)
    seconde =randint(1, 59)
    nombre = randint(int( f'{date.replace("-", "")}{heure}{minute}{seconde}' ),int( f'{date.replace("-", "")}{heure}{minute}{seconde}' ))
    format_nombre = "%Y%m%d%H%M%S"
    nbr1 = random.randint(1, 120)
    resultat = str(nbr1) + ' m'
    # path = f"{item['chemin']}{date}{heure}.csv"
    row = {
        "type": "cdr",
        "Flux": item["flux"],
        "TECHNO": item["techno"],
        "ID_Appelant": randint(100000, 799999999),
        "ID_Destinataire": randint(100000, 799999999),
        "Date_appel": datetime.strptime(str(nombre), format_nombre),# datetime when cdr was received by the platform
        "Duree": resultat ,
        "Region": choice([ "Tanger-Tétouan-Al Hoceima", "L'Oriental","Fès-Meknès", "Beni Mellal-Khénifra", "Rabat-Salé-Kénitra", "Casablanca-Settat","Marrakech-Safi","Drâa-Tafilalet", "Souss-Massa", "Guelmim-Oued Noun", "Laâyoune-Sakia El Hamra", "Dakhla-Oued Ed Dahab"]),
        "Status": "succes",
        "col9": choice([2, 4, 1, 3, 10]),
        "col10": choice([0, 1]),
        "col11": choice([1, 2]),
    }
    return row


def create_csv(length=100):
    """Create a temp file with random data"""
    data = [create_row() for _ in range(length)]
    df = DataFrame(data)
    
    csv_content = df.to_csv(index=False, header=False)
    # print(df.head())
    return csv_content

# encode string to base64
def encode(string):
    return b64encode(string.encode('utf-8')).decode('utf-8')

if __name__ == "__main__":
    
    # to index data in elasticsearch
    es = Elasticsearch(['http://elasticsearch.monitoring.svc.cluster.local:9200'])
#     es = Elasticsearch(
#     ['https://elasticsearch-master.monitoring.svc.cluster.local:9200'],
#     http_auth=('elastic', 'ArNMA3e7ct0fuvdT'),
#     verify_certs=False
# )
    # es = Elasticsearch(['http://elasticsearch-master-headless.default.svc.cluster.local:9200'],http_auth=('elastic', 'hpTxdiShRYlyXrMt'))
    # es=Elasticsearch([{"host":"elasticsearch-master-headless.default.svc.cluster.local","port":9200}],http_auth=('elastic', 'slzIsnsUD2hicTPF'))
    # es = Elasticsearch('https://elasticsearch-master-headless:9200/')

    current = datetime.now().strftime('%Y-%m-%d  %H')
    print(f"{datetime.now()} - Start dumping raw data for date : {current}")
    date = current.split("  ")[0]
    heure = current.split("  ")[1]

    for item in data:
        print(f"{datetime.now()} - Dumping {item['flux']} - {item['techno']}")
        
        path = f"{TEMP_FOLDER}/{item['chemin']}/{item['chemin']}_{date}_{heure}.csv"
        length=randint(10000,20000)
        csv = create_csv(length)


        # encode csv rows to base64
        encoded = ""
        for row in csv.split("\n"):
            encoded += encode(row) + "\n"
        
        makedirs(Path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(encoded)
        print(f"{datetime.now()} - Dumping {item['flux']} - {item['techno']} done. {length} rows dumped")

        print(f"{datetime.now()} - File saved to {path}")
        
        print(f"{datetime.now()} - Indexing into elasticsearch")
        filename = path.replace("\\", "/").split("/")[-1].replace(".done", "")
        doc = {
            "type": "RAW",
            "date": date,
            "heure": heure,
            "count": length,
            "flux": item['flux'],
            "techno": item['techno'],
            "path": path,
            "executed_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        resp = es.index(index=ES_INDEX, document=doc)

        print(f"{datetime.now()} - Indexing into elasticsearch done. {resp['result']}")
