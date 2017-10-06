import urllib, json
import codecs
from tipo_pagina import Tipo as tipo
import datetime

class FacebookCrawler():

    def __init__(self):
        self.directory_to_save = "/home/yurifw/"
        
        # dados do aplicativo EventCrawler
        #self.ap_id = "1802872966407095" #n esta sendo necssario por enquanto
        # app_token na verdade e o User Token, conseguido na pagina https://developers.facebook.com/tools/accesstoken/
        self.app_token = "EAAZAntBK847cBAKOrrZCFTKZAkRBIc2iPXFXixTZCOZBzo3nz0Gps1ChwvYhlsJcLir9BFNQHMtzpPayeKyDr5PToVLOerCNTa3cKdz1DdTkVonhgssZCZAbuLE3onFEtdRGKdP4b11lTMmP9hBrpMCuQjcOdIZBhNYZD"  # lint:ok  # lint:ok  # lint:ok
        self.token = self.app_token

        #para encontrar o id de uma pagina veja https://stackoverflow.com/questions/16324638/facebook-how-to-get-page-id
        #ou entao abra a pagina no facebook, abra o codigo fonte e de um ctrl+f em page_id
        self.pages = [
            {"nome":"Buffalo's Bar", "id":"1626656364254996", "tipo": tipo.bar()},
            {"nome":"Calabouco", "id":"191383484276075", "tipo": tipo.bar()},
            {"nome":"Megadeth", "id":"7709052329", "tipo": tipo.banda()}
            ]


    def start_crawling(self):
        events = list()
        for page in self.pages:
            #https://graph.facebook.com/v2.10/1626656364254996/events?access_token=EAAZAntBK847cBAKOrrZCFTKZAkRBIc2iPXFXixTZCOZBzo3nz0Gps1ChwvYhlsJcLir9BFNQHMtzpPayeKyDr5PToVLOerCNTa3cKdz1DdTkVonhgssZCZAbuLE3onFEtdRGKdP4b11lTMmP9hBrpMCuQjcOdIZBhNYZD
            url_request = "https://graph.facebook.com/v2.10/{page_id}/events?access_token={token}".format(page_id = page["id"], token=self.token)
            response = urllib.urlopen(url_request)
            data = json.loads(response.read())
            for e in data['data']:
                e['tipo'] = page['tipo']
                e['pagina'] = page['nome']
                events.append(e)
        return events

    def write_to_file(self):
        data = self.start_crawling()
        result={}
        page_header = "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/></head>"
        for event in data:
            dia = datetime.datetime.strptime(event['start_time'][:-5], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%y')
            nome = event['name']
            event_id = event['id']
            link = "https://www.facebook.com/events/"+event_id
            line = u"{nome} - {dia}<br><a href='{link}'>{link}</a><hr>".format(
                nome=event['pagina']+": "+nome,
                dia=dia,
                link=link)

            if ("Rio" not in event['place']['location']['city']):
                continue
            
            line = (result.get(event['tipo'].nome) or page_header ) + line
            result[event['tipo'].nome] = line

        for t in result.keys():    
            f = codecs.open(self.directory_to_save+t+'.html' , 'w', encoding='utf8')
            f.write(result[t])