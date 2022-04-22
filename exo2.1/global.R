library(mongolite)
library(tidyr)
library(leaflet)
library(jsonlite)
library(tidyverse)
library(shiny) 
library(shinydashboard)
library(shinyWidgets)
coll <- mongo("dump_Jan2022", url ="mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/doctolib",options = ssl_options(allow_invalid_hostname=TRUE, weak_cert_validation=TRUE))


#question4

requete='[
  {"$geoNear" : {
      "near": {"type": "Point", "coordinates": [-1.6777926, 48.117266]},
      "distanceField": "distance",
      "maxDistance": 50000
  }},
{"$unwind":"$visit_motives"},
{"$unwind":"$visit_motives.slots"},
{"$match": {"visit_motives.slots":{"$gte":{"$date":"2022-01-26T00:00:00Z"},"$lte":{"$date":"2022-01-29T00:00:00Z"}}}},
{"$group": {"_id": "$name",
            "loc" : {"$addToSet":"$location.coordinates"},
            "url" : {"$addToSet":"$url_doctolib"},
            "nb" : {"$sum":1}
            }}            
  ]'

centre = coll$aggregate(requete)
centre$loc=as.character(centre$loc)
centre$loc=substr(centre$loc,3,30)
centre$loc=substr(centre$loc,1,nchar(centre$loc)-2)
centre=centre%>%separate(loc,sep=",",into=c("lat","lon"))
colnames(centre)=c("nom","long","lat","url","nombre_creneaux")
centre$long=as.numeric(centre$long)
centre$lat=as.numeric(centre$lat)




req2='[
  {"$geoNear" : {
      "near": {"type": "Point", "coordinates": [-1.6777926, 48.117266]},
      "distanceField": "distance",
      "maxDistance": 50000
  }},
{"$unwind":"$visit_motives"},
{"$unwind":"$visit_motives.slots"},
{"$match": {"visit_motives.slots":{"$gte":{"$date":"2022-01-01T00:00:00Z"},"$lte":{"$date":"2022-06-01T00:00:00Z"}}}},
{"$group": {"_id": "$name",
            "loc" : {"$addToSet":"$location.coordinates"},
            "url" : {"$addToSet":"$url_doctolib"},
            "motif" : {"$addToSet":"$visit_motives.name"},
            "nb" : {"$sum":1}
            }}            
  ]'

total = coll$aggregate(req2)
total$loc=as.character(total$loc)
total$loc=substr(total$loc,3,30)
total$loc=substr(total$loc,1,nchar(total$loc)-2)
total=total%>%separate(loc,sep=",",into=c("lat","lon"))
colnames(total)=c("nom","long","lat","url","motif","nb_creneaux")
total$long=as.numeric(total$long)
total$lat=as.numeric(total$lat)

req3='[
  {"$geoNear" : {
      "near": {"type": "Point", "coordinates": [-1.6777926, 48.117266]},
      "distanceField": "distance",
      "maxDistance": 50000
  }},
{"$unwind":"$visit_motives"},
{"$unwind":"$visit_motives.slots"},

{"$match": {"visit_motives.slots":{"$gte":{"$date":"2022-01-01T00:00:00Z"},"$lte":{"$date":"2022-06-01T00:00:00Z"}}}},
{"$group": {"_id": {
      "name": "$name",
      "motif": "$visit_motives.first_shot_motive"
    },
            "loc" : {"$addToSet":"$location.coordinates"},
            "url" : {"$addToSet":"$url_doctolib"},
            "motif" : {"$addToSet":"$visit_motives.first_shot_motive"},
            "nb" : {"$sum":1}
            }}            
  ]'


dose1 = coll$aggregate(req3)%>%filter(motif==TRUE)%>%select(-motif)
dose1$loc=as.character(dose1$loc)
dose1$loc=substr(dose1$loc,3,30)
dose1$loc=substr(dose1$loc,1,nchar(dose1$loc)-2)
dose1=dose1%>%separate(loc,sep=",",into=c("lat","lon"))
colnames(dose1)=c("nom","long","lat","url","nb_creneaux")
dose1$long=as.numeric(dose1$long)
dose1$lat=as.numeric(dose1$lat)
dose1$url=as.character(dose1$url)
dose1=data.frame(dose1$nom$name,dose1$long,dose1$lat,dose1$url,dose1$nb_creneaux)
colnames(dose1)=c("nom","long","lat","url","nb_creneaux")