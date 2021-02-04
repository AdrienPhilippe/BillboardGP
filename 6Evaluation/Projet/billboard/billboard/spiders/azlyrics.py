import re
import scrapy
import numpy as np
import pandas as pd

dfGoogle = pd.read_csv("D:/GITHUB/BillboardGP/6Evaluation/Projet/billboard/billboard/dataGoogle.csv")

class GeniusSpider(scrapy.Spider):
    name = 'genius'
    allowed_domains = ['genius.com', 'google.fr']
    i = 0
    start_urls = ['https://google.fr/search?q='+str('genius')+"+"+str(dfGoogle['artist'][i])+"+"+str(dfGoogle['title'][i])]

    def parseGoogle(self, response):

        lienBrut = response.css('a::attr(href)')[18].extract()
        lienClean = re.findall(r"q=(\D+lyrics)", lienBrut)

        yield scrapy.Request(lienClean, callback=self.parseGenius)

    def parseGenius(self, response):
        lyricsBrut = response.css('div.Lyrics__Container-sc-1ynbvzw-2.jgQsqn').get()
        lyricsClean = re.sub(r"<.*?>"," ", lyricsBrut)

        for hit in lyricsBrut:
            yield {
                'title': dfGoogle['title'][i],
                'artist': dfGoogle['artist'][i],
                'lyrics': lyricsClean
            }

        i = i + 1
        next_song_string = +str(genius)+"+"+str(dfGoogle['artist'][i])+"+"+str(dfGoogle['title'][i])
        next_page_url = f'https://google.fr/search?q={next_song_string}'
        yield scrapy.Request(next_page_url, callback=self.parseGoogle)
