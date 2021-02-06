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
import numpy as np
#from forms import MusicSearchForm

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

LOCAL = True
Bilboard_ES = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'



@app.route('/MusicSearch', methods=('GET', 'POST'))
def MusicSearch():
    """
    Création de la barre de recherche ainsi que de l'affichage des données, et affichage du bargraph
    """

    pass



@app.route('/result/<search_word>')
def sucess(search_word):
    """
    Affichage des résultats de la recherche en fonction des artistes et albums.
    """
    pass


def generate_data(documents):
    """
    Génération des données cherchées
    """
    for docu in documents:
        yield {
            "_index": "lyrics",
            "_type": "lyrics",
            "_source": {k:v if v else None for k,v in docu.items()},
        }

@app.route('/MusicSearchSinger', methods=('GET', 'POST'))       
def search_singer(singer):
    singer_name = str(singer).lower() + "~"
    QUERY = {
      "query": {
        "match_phrase" : { 
            "artist" : singer_name,
            }
      },
      "from":0,
      "size":10
    }
    result = Bilboard_ES.search(index="lyrics", body=QUERY)
    return [elt['_source']['title'] for elt in result["hits"]["hits"]]

@app.route('/MusicSearchTitle', methods=('GET', 'POST'))
def search_title(title):
    title_name = str(title).lower() + "~"
    QUERY = {
      "query": {
        "match_phrase" : { 
            "title" : title_name,
            } 
      },
      "from":0,
      "size":10
    }
    result = Bilboard_ES.search(index="lyrics", body=QUERY)
    return [elt['_source']['title'] for elt in result["hits"]["hits"]]

@app.route('/MusicSearchLyrics', methods=('GET', 'POST'))
def search_lyrics(lyrics):
    lyrics_name = str(lyrics).lower() + "~"
    QUERY = {
      "query": {
        "match" : { 
            "lyrics" : lyrics_name, 
            } 
      },
      "from":0,
      "size":10
    }
    result = Bilboard_ES.search(index="lyrics", body=QUERY)
    return [elt['_source']['title'] for elt in result["hits"]["hits"]]

if __name__ == '__main__':
    print("Running...")
    app.run(debug=True)