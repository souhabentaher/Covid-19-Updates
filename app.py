from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from datetime import datetime
import os
import urllib.request as urlrequest
import json

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html')

@app.route('/')
def main():
	#Read all countries in the text file
	country_list_file = open('countries.txt', 'r')
	country_list = country_list_file.readlines()
	#Get the current country in the url parameter
	get_country = request.args.get('country', default='World')
	#get current date
	date = datetime.today().strftime('%Y-%m-%d')

	return render_template('main.html', 
		countries=country_list, url_country=get_country, date=date)

@app.route('/tableview')
def table():
	# get API Data
	with urlrequest.urlopen('https://coronavirus-19-api.herokuapp.com/countries') as response:
		source = response.read()
		data = json.loads(source)

	#get current date
	date = datetime.today().strftime('%Y-%m-%d')
	return render_template('table.html', date=date, jsonData=data, table=True)

@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
	app.run()