from flask import Flask
from flask import jsonify, request, render_template
import re
import pandas as pd
import numpy as np
import urllib.request
from flask_cors import CORS, cross_origin
from TurkishStemmer import TurkishStemmer
from bs4 import BeautifulSoup
import  json

app = Flask(__name__)
CORS(app)

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def cleanhtml(raw_html):
    cleanr = re.compile(r'<[^>]+>')
    cleantext = re.sub(cleanr, '', raw_html)

    cleanr = re.compile(r'[\W]')
    cleantext = re.sub(cleanr, " ", cleantext)
    cleantext = re.sub("\n|\r|\t", " ", cleantext)
    cleantext = re.sub("quot|nbsp", " ", cleantext)
    re.sub(' +', ' ', cleantext)
    cleantext = cleantext.lower()
    return cleantext


def getUrlContent(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    ss = cleanhtml(mystr)
    data = ss.split()
    data = [d for d in data if len(d) > 2]
    return data, mystr


def getUrlKeyWord(url):
    data, text = getUrlContent(url)
    turkStem = TurkishStemmer()
    kelimeler = []
    for w in data:
        kelimeler.append(turkStem.stem(w))

    ds = pd.Series(kelimeler)
    val = ds.value_counts()
    return val, text


def getsublink(val1, url, links, l, root=0, parent=""):
    if len(l)>10:
        return
    data, text = getUrlKeyWord(url)
    l.append(url)
    print(url, root, parent)
    kesisim = {}
    sum = 0
    skor = 0
    for index, v in val1.items():
        k = data[data.index == index]
        if not k.empty:
            if k[0] > 0:
                kesisim[index] = k[0]
                sum += k[0]
    if sum != 0:
        skor = sum / data.sum()
    else:
        skor = 0

    ks = pd.Series(kesisim)
    ks.sort_values(ascending=False)

    links.append({"link": url,
                  "skor": skor,
                  "kesisim": ks[:5].to_json(orient="index"),
                  "parent": parent})

    soup = BeautifulSoup(text, 'lxml')
    if root < 1:
        root += 1
        for link in soup.find_all('a'):
            sublink = link.get('href')
            if re.match(regex, link.get('href')) is not None and len(sublink) < 200:
                try:
                    # res = next((item for item in links if item["link"] == sublink), "True")
                    if sublink in l:
                        continue
                    getsublink(val1, sublink, links, l, root=root, parent=url)
                except:
                    print("error")


def getsublinkAlakali(alakali, url, links, l, root=0, parent=""):
    if len(l)>10:
        return
    data, text = getUrlKeyWord(url)
    l.append(url)
    print(url, root, parent)
    kesisim = {}
    sum = 0
    skor = 0
    for index, v in alakali.items():
        k = data[data.index == v]
        if not k.empty:
            kesisim[v] = k[0]
            sum += k[0]

    if sum != 0:
        skor = sum / data.sum()
    else:
        skor = 0

    ks = pd.Series(kesisim)
    ks.sort_values(ascending=False)

    links.append({"link": url,
                  "skor": skor,
                  "kesisim": ks[:5].to_json(orient="index"),
                  "parent": parent})

    soup = BeautifulSoup(text, 'lxml')
    if root < 1:
        root += 1
        for link in soup.find_all('a'):
            sublink = link.get('href')
            if re.match(regex, link.get('href')) is not None and len(sublink) < 200:
                try:
                    # res = next((item for item in links if item["link"] == sublink), "True")
                    if sublink in l:
                        continue
                    getsublink(alakali, sublink, links, l, root=root, parent=url)
                except:
                    print("error")



@app.route('/s1', methods=['POST', "OPTIONS"])
@cross_origin()
def soru1():
    url = request.json['url']
    data, _ = getUrlContent(url)
    ds = pd.Series(data)
    val = ds.value_counts()
    val = val[val > 2]
    val = val.sort_values(ascending=False)
    val = val.to_json()
    return val


@app.route('/s2', methods=['POST', "OPTIONS"])
@cross_origin()
def soru2():
    url = request.json['url']
    val, _ = getUrlKeyWord(url)
    val = val[val > 3]
    val = val.sort_values(ascending=False)
    val = val[:10]
    val = val.to_json()
    return val


@app.route('/s3', methods=['POST', "OPTIONS"])
@cross_origin()
def soru3():
    url1 = request.json['url']
    val1, _ = getUrlKeyWord(url1)

    url2 = request.json['url2']
    val2, _ = getUrlKeyWord(url2)

    sum = 0
    kesisim = {}
    for index, v in val1.items():
        k = val2[val2.index == index]
        if not k.empty:
            if k[0] > 0:
                kesisim[index] = k[0]
                sum += k[0]
    ks = pd.Series(kesisim)
    ks.sort_values(ascending=False)
    skor = sum / val2.sum()
    result = {
        "url1": val1[:10].to_json(),
        "url2": val2[:10].to_json(),
        "kesisim": ks[:10].to_json(),
        "skor": skor
    }
    return result


@app.route('/s4', methods=['POST', "OPTIONS"])
@cross_origin()
def soru4():
    l = []
    links = []
    url1 = request.json['url']
    val1, _ = getUrlKeyWord(url1)
    urls = request.json['urls']
    for url in urls:
        getsublink(val1, url, links, l, root=0, parent=url)
    df = pd.DataFrame(links)
    print(df.head())
    print("*************")
    return df.to_json(orient="records")

@app.route('/s5', methods=['POST', "OPTIONS"])
@cross_origin()
def soru5():
    f = "esanlamli.txt"
    dataSet = pd.read_csv(f, delimiter="\t")

    l = []
    links = []
    url1 = request.json['url']
    val1, _ = getUrlKeyWord(url1)
    alakali=[]
    for index, v in val1.items():
        k = dataSet[dataSet.Kelime == index]["Eşanlamlısı"]
        if not k.empty:
            alakali.extend(k)
    alakali = pd.Series(alakali)

    urls = request.json['urls']
    for url in urls:
        getsublinkAlakali(alakali, url, links, l, root=0, parent=url)
    df = pd.DataFrame(links)
    df["skor"] = df["skor"].astype(float)
    df = df.sort_values(by='skor', ascending=False)
    result = {
        "data":df.to_json(orient="records"),
        "alakali":alakali.to_json(orient="records")
    }
    return result


if __name__ == '__main__':
    app.run(debug=True)
