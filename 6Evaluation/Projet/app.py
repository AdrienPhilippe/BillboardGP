"""
Permet l'affichage web des données scrapées
en utilisant Flask, MongoDB et ElasticSearch 
"""

from flask import Flask
from flask import request
from flask import render_template, render_template_string
from flask import flash, redirect, request, url_for

import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import json
import re
import numpy as np
from bar import SearchBar

# from bokeh.embed import json_item
# from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
# from bokeh.models.glyphs import VBar
# from bokeh.plotting import figure
# from bokeh.embed import components
# from bokeh.models.sources import ColumnDataSource
# from bokeh.resources import CDN
# from jinja2 import Template
# from bokeh.io import show, output_file
import os
from pymongo import MongoClient
# from search_bar import SearchBar
# #from graphs import create_bargraph

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

LOCAL = False
Bilboard_ES = Elasticsearch(hosts="http://localhost", port=9200)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def mainpage():
  data = pd.read_csv("lien.csv")
  documents = data.fillna("").to_dict(orient="records")
  bulk(Bilboard_ES, generate_data(documents))
  return redirect("/MusicbarLooker")
#   return render_template('mainpage.html')

@app.route('/MusicbarLooker', methods=('GET', 'POST'))
def MusicSearch():
    """
    Création de la barre de recherche ainsi que de l'affichage des données, et affichage du bargraph
    """
    form = SearchBar()
    if form.validate_on_submit():
        lookfor = re.sub('[^A-Za-z0-9]','_', form.typing.data)
        return redirect('/MusicSearchLyrics/'+lookfor)
    return render_template('search.html',form=form)

def generate_data(documents):
    """
    Génération des données cherchées
    """
    for docu in documents:
        yield {
            "_index": "artist",
            "_type": "artist",
            "_source": {k:v if v else None for k,v in docu.items()},
        }


@app.route('/MusicSearchSinger/<search_word>', methods=('GET', 'POST'))       
def search_singer(search_word):
    artist = re.sub('_',' ', search_word)
    QUERY = {
      "query": {
        "term" : { 
            "artist" : artist.lower()} 
      }
    }

    result = Bilboard_ES.search(index="artist", body=QUERY)
    source = result["hits"]["hits"]
    seen = set()
    new_source = []
    for d in source:
        t = tuple(d["_source"].items())
        if t not in seen:
            seen.add(t)
            new_source.append(d)
    
    artist = [elt['_source']['artist'] for elt in new_source]
    title = [elt['_source']['title'] for elt in new_source]
    lyrics = [elt['_source']['lyrics'] for elt in new_source]

    return render_template('results_singer.html',title=title,artists=artist,lyrics=lyrics)

@app.route('/MusicSearchTitle/<search_word>', methods=('GET', 'POST'))
def search_title(search_word):
    title = re.sub('_',' ', search_word)
    QUERY = {
      "query": {
        "match" : { 
            "title" : title.lower()} 
      }
    }
    result = Bilboard_ES.search(index="artist", body=QUERY)
    source = result["hits"]["hits"]
    seen = set()
    new_source = []
    for d in source:
        t = tuple(d["_source"].items())
        if t not in seen:
            seen.add(t)
            new_source.append(d)
    
    artist = [elt['_source']['artist'] for elt in new_source]
    title = [elt['_source']['title'] for elt in new_source]
    lyrics = [elt['_source']['lyrics'] for elt in new_source]

    return render_template('results_title.html',title=title,artists=artist,lyrics=lyrics)

@app.route('/MusicSearchLyrics/<search_word>', methods=('GET', 'POST'))
def search_lyrics(search_word): 
    lyrics = re.sub('_',' ', search_word)
    lyrics += "*"
    
    QUERY = {
      "query": {
        "match" : { 
            "lyrics" : lyrics.lower()} 
      }
    }


    QUERY2 = {
        "query": {
            "function_score": {
            "boost_mode": "multiply", 
            "query": {
                "common": {
                "lyrics": {
                    "query": lyrics.lower(),
                    "cutoff_frequency": 0.001,
                    "low_freq_operator": "and"
                }
                }
            },
            }
        }
    }


    result = Bilboard_ES.search(index="artist", body=QUERY2)
    source = result["hits"]["hits"]
    seen = set()
    new_source = []
    for d in source:
        t = tuple(d["_source"].items())
        if t not in seen:
            seen.add(t)
            new_source.append(d)
    
    artist = [elt['_source']['artist'] for elt in new_source]
    title = [elt['_source']['title'] for elt in new_source]

    print(artist)
    print(title)
    # lyrics = [elt['_source']['lyrics'] for elt in new_source]

    return render_template('results_lyrics.html',title=title,artists=artist,lyrics=lyrics)

if __name__ == '__main__':
    print("Running...")
    app.run(debug=True, port=2746)