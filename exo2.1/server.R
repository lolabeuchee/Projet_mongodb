#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define server logic required to draw a histogram
server <- function(input, output,session) {

    output$carte1 <- renderLeaflet({
      
      ColorPal1 <- colorNumeric(scales::seq_gradient_pal(low = "#008000", high = "#f00020",
                                                         space = "Lab"), domain = c(0,330))

      m<- leaflet(data = centre) %>% 
        addTiles() %>%
        addCircleMarkers(~ long, ~ lat,
                         fillOpacity = 1,
                         color=~ColorPal1(nombre_creneaux),
                         popup = ~paste(paste("Centre :  ",as.character(nom),sep=": "),paste("Nombre de créneaux ",nombre_creneaux,sep=": "),paste("Lien vers le site de réservation ",url,sep=": "),sep="<br/>"))
      
      
      m

    })
    output$carte2 <- renderLeaflet({
      
      max<- reactive({
        switch(input$choix_dose,
               "Tous motif" = 700,
               "1ère dose"=350)
        
      })
      
      ColorPal1 <- colorNumeric(scales::seq_gradient_pal(low = "#008000", high = "#f00020",
                                                         space = "Lab"), domain = c(0,max()))
      
      motif<- reactive({
        switch(input$choix_dose,
               "Tous motif" = total,
               "1ère dose"=dose1)
               
      })
      
      m<- leaflet(data = motif()) %>% 
        addTiles() %>%
        addCircleMarkers(~ long, ~ lat,
                         fillOpacity = 1,
                         color=~ColorPal1(nb_creneaux),
                         popup = ~paste(paste("Centre :  ",as.character(nom),sep=": "),paste("Nombre de créneaux ",nb_creneaux,sep=": "),paste("Lien vers le site de réservation ",url,sep=": "),sep="<br/>"))
      
      
      m
      
    })

}
