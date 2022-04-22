#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 18:52:07 2022

@author: lolabeuchee
"""

from pymongo import MongoClient
from pprint import pprint
import datetime
import pandas as pd
import json
from bokeh.plotting import figure, show
from bokeh.tile_providers import  get_provider, Vendors
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, ColorPicker, Legend
from bokeh.models.widgets import Tabs, Panel


db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri,tls=True,tlsAllowInvalidCertificates=True)
db_name = "food"
db = client[db_name]
coll_name = "NYfood"
coll = db[coll_name]

datefin=datetime.datetime.strptime("2015/01/01", "%Y/%m/%d")
datedebut=datetime.datetime.strptime("2012/01/01", "%Y/%m/%d")
    

cursor=coll.find({"cuisine": "Italian",
                  "grades.grade": "A",
                  "$nor": [{"grades.date": {"$size": 0}}, 
                           {"grades.date": {"$exists": False}}, 
                           {"grades.date": {"$gte": datefin}}, 
                           {"grades.date": {"$lte": datedebut} }]
                  }, 
                 {"address.loc.coordinates":True, 
                  "address.street":True, 
                  "name":True,
                  "borough":True}
                 )

dico={}
liste_lat=[]
liste_long=[]
liste_name=[]
liste_street=[]
liste_quartier=[]
for objet in list(cursor):
    liste_lat.append(objet["address"]["loc"]["coordinates"][1])
    liste_long.append(objet["address"]["loc"]["coordinates"][0])
    liste_name.append(objet["name"])
    liste_street.append(objet["address"]["street"])
    liste_quartier.append(objet["borough"])


dico={"name":liste_name, "latitude":liste_lat, "longitude":liste_long, "street":liste_street, "quartiers": liste_quartier}
data=pd.DataFrame(dico)



############ réalisation de la carte ################




# dico_quartier={}
# for quartier in list(set(data.quartiers)): 
#     print(quartier)
#     liste=[]
#     for val in data.quartiers:
#         if val==quartier:
#             liste.append(1)
#         else:
#             liste.append(0)
#     print(liste)
#     dico_quartier[quartier]=liste
# data_quartier=pd.DataFrame(dico_quartier)
# print(data_quartier)

# df=data.merge(data_quartier,how='left', left_index=True, right_index=True)


source=ColumnDataSource(data)



p = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", title="Capitales des pays du monde")
tile_provider = get_provider('CARTODBPOSITRON')
p.add_tile(tile_provider)
p.triangle(x='latitude',y='longitude',source =source,size =5, color="red")
#Affichage au survol des points : nom du pays et de la capitale
hover_tool = HoverTool(tooltips=[( 'quartier', '@quartiers'),( 'street', '@street')]) 
p.add_tools(hover_tool)
show(p)














