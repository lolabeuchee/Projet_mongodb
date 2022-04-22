rsconnect::setAccountInfo(name='elouangirot',
                          token='79174AF35DB4D3F8B3D0F378FB48A578',
                          secret='99QkWcIGsC1ldpydXYlsKNWgz6bNA68DubB162lk')
library(shiny)


# Define UI for application that draws a histogram
ui <- dashboardPage(
  skin = "blue",
  title = "Projet de visualisation",
  
  dashboardHeader(title =""),
  
  dashboardSidebar(
    width = 290,
    sidebarMenu(
      menuItem("Centre de vaccination",tabName = "carte",icon=icon("syringe")),
      menuItem("Distinction 1ère/Tous motifs confondus",tabName = "carte2",icon=icon("syringe")))),
              
      

  
  dashboardBody(
    tabItems(
      tabItem(tabName = "carte",
              fluidRow(
              p("Cette cartographie permet de visualiser les centres de vaccination situé à moins de 50km de Rennes et proposant des doses entre le 26 janvier et le 29 janvier. Au survol, il est possible de voir le nombre de dose proposer par le centre ainsi que le lien vers le site de reservation.",style="text-align:justify;color:black;background-color:lavender;padding:15px;border-radius:10px"),
              
              box(
                solidHeader = T,
                width = 12, collapsible = T,
                leafletOutput("carte1")))),
      tabItem(tabName = "carte2",
              fluidRow(
                p("Cette deuxième cartographie s'intéresse aux centres de vaccinations proposant des doses entre le 1er janvier et le 1er juin. Il est possible de choisir de visualiser uniquement les premières doses disponible ou bien la totalité des doses proposée",style="text-align:justify;color:black;background-color:lavender;padding:15px;border-radius:10px"),
                
                
                  
                
                  box(
                    radioGroupButtons(
                      inputId = "choix_dose",
                      label = "   Choisir le motif",
                      choices = c("Tous motif","1ère dose"),
                      selected = list("Tous motif"),
                      status = "success"),
                  solidHeader = T,
                  width = 12, collapsible = T,
                  leafletOutput("carte2")))))))
