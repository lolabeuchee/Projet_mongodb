from pymongo import MongoClient
from pprint import pprint
import pandas as pd
import networkx as nx
from bokeh.plotting import output_file
from bokeh.io import  show
from bokeh.models import Range1d, Circle, MultiLine,Div
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral8
from bokeh.transform import linear_cmap
from bokeh.models.widgets import Panel,Tabs
from bokeh.layouts import  column


db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri,tls=True,tlsAllowInvalidCertificates=True)
db_name = "publications"
db = client[db_name]
coll_name = "hal_irisa_2021"
coll = db[coll_name]

cursor=coll.aggregate([
    {"$unwind": "$authors"},
    {"$unwind": "$title"},
    {"$group":  {"_id": { "nom" : "$authors"},
            "publications": { "$push":  { "title": "$title" }},
        "nb_publis": {"$sum":1}
    }},
    {"$sort": {"nb_publis": -1}},
    {"$limit":20}
]
)



liste_nom=[]
liste_prenom=[]
liste_publication=[]
for objet in list(cursor):
    liste_prenom.append((objet['_id']['nom']['firstname']))
    liste_nom.append((objet['_id']['nom']['name']))
    liste_publication.append((objet['publications']))

    
liste_publi=[[dico_title['title'] for dico_title in publis] for publis in liste_publication]

# creation du dico 

dico={}
for i in range (0,len(liste_prenom)):
    dico[str((liste_prenom[i])+str(liste_nom[i]))]=liste_publi[i]


noeud=list(dico.keys())
taille=[len(n) for n in dico.values()]
test=pd.DataFrame(taille)
test["noeud"]=noeud


liste_neoud_i=[]
liste_neoud_j=[]
liste_com=[]
for i in range(0,20):  
    for j in range(0,20):
        nb_commun=0
        if noeud[i]!=noeud[j] and noeud[j] not in liste_neoud_i:
            for val in dico[noeud[i]]:
                if val in dico[noeud[j]]:
                    nb_commun+=1
            liste_neoud_i.append(noeud[i])
            liste_neoud_j.append(noeud[j])
            liste_com.append(nb_commun)


df = pd.DataFrame({'noeud1':liste_neoud_i,'noeud2':liste_neoud_j,'nb_commun':liste_com})




df.columns = ['source','target','weight']




gr=df.groupby('source',as_index=False).agg({'weight':sum})
gr=gr[gr.weight==0]
gr['target']=gr.source


df2=df[ df.weight !=0 ]

df2=pd.concat([df2, gr])

nb_publi=[(nom,len(taille)) for nom,taille in dico.items()]

G1 = nx.from_pandas_edgelist(df2, 'source', 'target', 'weight')


title = 'Réseau de publications scientifiques'


HOVER_TOOLTIPS = [
       ("Auteur", "@index"),
        ("nombre de publication", "@adjusted_node_size")
]

plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-1.2,1.2), y_range=Range1d(-1.2, 1.2), title=title)


network_graph = from_networkx(G1, nx.spring_layout)

#####

adjusted_node_size = dict(nb_publi)
nx.set_node_attributes(G1, name='adjusted_node_size', values=adjusted_node_size)

color_by_this_attribute = 'adjusted_node_size'


color_palette = Spectral8

#network_graph = from_networkx(G1, nx.spring_layout)
network_graph = from_networkx(G1, nx.spring_layout)


commun={}
for  (u, v, d) in G1.edges(data=True):
    if u!=v:
        commun[(u, v)] = d['weight']
    
nx.set_edge_attributes(G1, commun, "weight")



minimum_value_color = min(network_graph.node_renderer.data_source.data[color_by_this_attribute])
maximum_value_color = max(network_graph.node_renderer.data_source.data[color_by_this_attribute])
network_graph.node_renderer.glyph = Circle(size=15,fill_color=linear_cmap(color_by_this_attribute, color_palette, minimum_value_color, maximum_value_color))
network_graph.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width="weight")



plot.renderers.append(network_graph)

div = Div(text="""
<h1> Explication </h1>
<p> Ce réseau permet de visualiser les liens entre les auteurs de publications scientifiques, en utilisant un code couleur qui permette de distinguer les auteurs par leurs nombres de publications et en représentant les liens (co-publications) existant entre les auteurs. l’épaisseur des traits joignant deux auteurs est proportionnelle au nombre de publications communes entre ceux-ci (Il peut être nécéssaire de zoomer pour s'en rendre compte).</p>""",style={'text-align':'justify','color':'black','background-color':'lavender','padding':'15px','border-radius':'10px'})

tab = column(div,plot)

output_file("exo2.2.html")

show(tab)