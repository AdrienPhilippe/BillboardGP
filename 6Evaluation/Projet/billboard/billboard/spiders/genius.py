import re
import scrapy
import numpy as np
import pandas as pd

dfTitreArtist = pd.read_csv("D:/GITHUB/BillboardGP/6Evaluation/Projet/billboard/billboard/dataGoogle3.csv")
dfGenius = pd.read_csv("D:/GITHUB/BillboardGP/6Evaluation/Projet/billboard/billboard/dataGoogle2.csv")
i = 0

class GeniusSpider(scrapy.Spider):
    global i
    name = 'genius'
    allowed_domains = ['genius.com']
    start_urls = ['https://genius.com/'+str(dfGenius['artist'][i])+"-"+str(dfGenius['title'][i])+"-lyrics"]

    def parse(self, response):
        global i
        lyricsBrut = response.css('div.Lyrics__Container-sc-1ynbvzw-2.jgQsqn').get()
        
        yield {
            'artist': dfTitreArtist['artist'][i],
            'title': dfTitreArtist['title'][i],
            'lyrics': re.sub(r"<.*?>"," ", lyricsBrut)
        }

        i = i + 1
        next_song_string = str(dfGenius['artist'][i])+"-"+str(dfGenius['title'][i]+"-lyrics")
        next_page_url = f'https://genius.com/{next_song_string}'
        yield scrapy.Request(next_page_url, callback=self.parse)