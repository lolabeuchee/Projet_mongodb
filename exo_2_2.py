from pymongo import MongoClient
from pprint import pprint
import pandas as pd



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

