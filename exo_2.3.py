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
from bokeh.plotting import figure, show,ColumnDataSource,output_file
from bokeh.tile_providers import  get_provider, Vendors
from bokeh.models import HoverTool, ColumnDataSource, ColorPicker, Legend,Div
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import  column
import numpy as np


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




dico_quartier={}
for quartier in list(set(data.quartiers)):
    print(quartier)
    liste=[]
    for val in data.quartiers:
        if val==quartier:
            liste.append(1)
        else:
            liste.append(0)
    print(liste)
    dico_quartier[quartier]=liste
data_quartier=pd.DataFrame(dico_quartier)
print(data_quartier)

df=data.merge(data_quartier,how='left', left_index=True, right_index=True)


k=6378137
df['longitude']=df['longitude']*(k*np.pi/180.0)
df['latitude']=np.log(np.tan((90+df['latitude'])*np.pi/360.0))*k


source=ColumnDataSource(df)



manhattan = df['Manhattan'].apply(lambda x: x*6 if x>0 else 0)
queens = df['Queens'].apply(lambda x: x*6 if x>0 else 0)
brooklyn = df['Brooklyn'].apply(lambda x: x*6 if x>0 else 0)
staten = df['Staten Island'].apply(lambda x: x*6  if x>0 else 0)
bronx = df['Bronx'].apply(lambda x: x*6 if x>0 else 0)

source.add(manhattan,"manhattan")
source.add(queens,"queens")
source.add(brooklyn,"brooklyn")
source.add(staten,"staten")
source.add(bronx,"bronx") 

p = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", title="Restaurant Italiens à New-York",x_range=(-8340000, -8080000), y_range=(5000000, 5000099))
tile_provider = get_provider('OSM')
p.add_tile(tile_provider)

gl1 = p.scatter('longitude','latitude',size='manhattan', source=source,color="orange")
gl2 = p.scatter('longitude','latitude',size='queens',source=source,color="green")
gl3 = p.scatter('longitude','latitude',size='brooklyn',source=source,color="blue")
gl4 = p.scatter('longitude','latitude',size='staten',source=source,color="red")
gl5 = p.scatter('longitude','latitude',size='bronx',source=source,color="purple")
###


#Affichage au survol des points
hover_tool = HoverTool(tooltips=[( 'quartier', '@quartiers'),( 'street', '@street')]) 
p.add_tools(hover_tool)

picker1 = ColorPicker(title="Manhattan",color=gl1.glyph.line_color,width=100)
picker1.js_link('color', gl1.glyph, 'line_color')

picker2 = ColorPicker(title="Queens",color=gl2.glyph.line_color,width=100)
picker2.js_link('color', gl2.glyph, 'line_color')

picker3 = ColorPicker(title="Brooklyn",color=gl3.glyph.line_color,width=100)
picker3.js_link('color', gl3.glyph, 'line_color')

picker4 = ColorPicker(title="Staten Island",color=gl4.glyph.line_color,width=100)
picker4.js_link('color', gl4.glyph, 'line_color')

picker5 = ColorPicker(title="Bronx",color=gl5.glyph.line_color,width=100)
picker5.js_link('color', gl5.glyph, 'line_color')

legend = Legend(items=[("Manhattan", [gl1]),
    ("Queens", [gl2]),
    ("Brooklyn", [gl3]),
    ("Staten Island", [gl4]),
    ("Bronx", [gl5]),], location = 'top')
p.add_layout(legend,'below')

legend.click_policy="hide"
legend.title = "Cliquer sur les quartiers à afficher"

div = Div(text="""
<h1> Graphique n°4 </h1>
<p> Cette carte montre les restaurants italiens qui ont été noté au moins une fois A dont les notes ont été effectué entre "2015/01/01" et le "2012/01/01". Cette requete permet de recupérer la localisation, le nom de la rue du restaurant, le nom du restaurant et leurs quartiers.
Nous pouvons visualiser les quartiers selon leur couleurs. 
</p>
<p> Précision : Le widget permet de selectioner et deselctionner un/des quartiers pour ne visualiser seulement certains quartiers.</p>""",style={'text-align':'justify','color':'black','background-color':'lavender','padding':'15px','border-radius':'10px'})

tab = column(div,p)

output_file("exo2.3.html")

show(tab)














