from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route("/")
def searchPage():
    product = request.args.get("product")
    websites = request.args.getlist("website")
    results = {}
    for website in websites:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        if website == "amazon":
            html = requests.get("http://amazon.com/s?k=" + product,headers=headers)
            amazon_data = html.content
            amazon_soup = BeautifulSoup(amazon_data, 'lxml')
            amazon_results = amazon_soup.find_all('div', 's-result-list s-search-results sg-row')
            for link in amazon_results[0].findAll('a'):
                link['href'] = link['href'].replace('/gp/', 'https://www.amazon.com/gp/')
            results['amazon'] = amazon_results[0]
        elif website == "ebay":
            html = requests.get("http://ebay.com/sch/i.html?_nkw=" + product,headers=headers)
            ebay_data = html.content
            ebay_soup = BeautifulSoup(ebay_data, 'lxml')
            ebay_results = ebay_soup.find_all('li', 's-item')
            results['ebay'] = ebay_results
    return render_template("test.html", websites=request.args.getlist("website"), results=results)
@app.route("/<path:url>")
def directedPage(url):
    if "/dp/" in url:
        return redirect("https://www.amazon.com/" + url)
app.run()

