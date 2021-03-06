###### Loading the pickle data and save it

# require("reticulate")
# use_python("/usr/local/bin/python3")
# py_install("numpy", pip3 = TRUE)
# py_install("pandas", pip3 = TRUE)
# source_python("/Users/niloofar/Documents/insight/data/cleaned/pickle_reader.py")
# pickle_data <- read_pickle_file("/Users/niloofar/Documents/insight/data/cleaned/hotel2/sentiment_topic_final")
# save (pickle_data,file="/Users/niloofar/Documents/insight/data/cleaned/hotel2/sentiment_topic_final.RData")
# 
#####################################
library(randomForest)
require(Matrix)
require(data.table)
library(dplyr)
library(ggplot2)

load("./sentiment_topic_final.RData")

pickle_data$Reviewer_Score=as.integer(pickle_data$Reviewer_Score)

pickle_data$Date <- as.Date(pickle_data$Review_Date)
pickle_data$Time <- format(as.POSIXct(pickle_data$Review_Date) ,format = "%H:%M:%S") 
pickle_data$month<-month(as.Date(pickle_data$Date))
sdate = as.Date("2013-01-01") 
edate =as.Date("2020-01-01")  
delta = edate - sdate
year=(delta/365)
year_seq=seq(as.Date("2013/01/01"), as.Date("2020/1/1"), "years")
month_table=c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")

# month_seq=seq(as.Date("2020/01/01"), as.Date("2020/12/01"), "months")
# month=month(as.Date(month_seq))

year_label=c("2019","2018","2017","2016","2015","2014","2013")

for (i in 1:7){
  nam <- paste("G", i, sep = "")
  assign(nam,pickle_data[pickle_data$Date>=year_seq[i] & pickle_data$Date<year_seq[i+1], ])}


feature_imp=function(data){
  x_column=c("amenities", "extracharge", "location","parking", "staff")
  fit_rf = randomForest(Reviewer_Score~amenities+extra_charge+location+parking+staff,mtry=3, na.action=na.omit,data=data,importance=TRUE)
  imp=importance(fit_rf,type=1)
  imp=cbind(x_column,imp)
  imp=data.frame(imp)
  rownames(imp)=NULL
  imp$rank=as.numeric(as.character(imp$X.IncMSE))
  imp$rank=round(imp$rank, digits = 2)
  imp=imp[c("x_column","rank")]
  imp=feature_imp(data)
  imp <- arrange(imp, rank)
  imp$features <- factor(imp$features, levels = imp$features)
  return(imp)
}

     
 library(shiny)
      
      # Define UI for random distribution app ----
      ui <- fluidPage(
        
        # App title ----
        titlePanel("Dynamic Hotel Review"),
        
        # Sidebar layout with input and output definitions ----
        sidebarLayout(
          
          # Sidebar panel for inputs ----
        sidebarPanel(
            
          
              
              # Input: Choose dataset ----
              selectInput("date", "Select the year:",
                          choices = year_label),
              
              selectInput("month", "Select the month:",
                          choices = month_table)
              
              # 
              # sliderInput("month", "Select the period:",
              #             min = "Jan", max = "Dec", value = c("Jan","Feb"))
        ),
              
              
              
              
        
            
          
          
          # Main panel for displaying outputs ----
          mainPanel(
            
            tabsetPanel(type = "tabs",
                        tabPanel("Overal rating during the year", plotOutput("plot1")),
                        tabPanel("Average Rating per month", plotOutput("plot2")),
                        tabPanel("Significant Feature", plotOutput("plot3")),
                        tabPanel("Recommendations", textOutput("text")))
                        
                        
                
          )
        ))
      













server <- function(input, output) {
  
  # Reactive expression to generate the requested distribution ----
  # This is called whenever the inputs change. The output functions
  # defined below then use the value computed from this expression
  datasetInput <- reactive({
    switch(input$date,
           "2013" = G1,
           "2014" = G2,
           "2015" = G3,
           "2016"= G4,
           "2017"= G5,
           "2018"=G6,
           "2019"=G7
    )})
  
  
  # Generate a plot of the data ----
  # Also uses the inputs to build the plot label. Note that the
  # dependencies on the inputs and the data reactive expression are
  # both tracked, and all expressions are called in the sequence
  # implied by the dependency graph.
  
  output$plot1<-renderPlot({
    data=pickle_data
    data_new=data[c("Date","Reviewer_Score")]
    # data_new$Date=format(as.Date(data_new$Date, format="%d/%m/%Y"),"%Y")
    data_new=aggregate(Reviewer_Score~Date, data_new, mean)
    data_new$Reviewer_Score=data_new$Reviewer_Score/10
    ggplot(data_new,aes(x=Date,y=Reviewer_Score))+geom_line(colour='black',size=2)},
    height = 400,width = 600)
  
  
  
  output$plot2<-renderPlot({
    data=datasetInput( )
    data_new=data[c("Date","Reviewer_Score")]
    data_new=aggregate(Reviewer_Score~Date, data_new, mean)
    data_new$Reviewer_Score=data_new$Reviewer_Score/10
    ggplot(data_new,aes(x=Date,y=Reviewer_Score))+geom_line(colour='blue',size=2)},
    height = 400,width = 600)
  

  output$plot3<-renderPlot({
    data=datasetInput( )
    x_column=c("amenities", "extracharge", "location","parking", "staff")
    train<-sample_frac(data, 0.8)
    sid<-as.numeric(rownames(train)) # because rownames() returns character
    test<-data[-sid,]
    
    set.seed(4543)
    fit_rf = randomForest(Reviewer_Score~amenities+extra_charge+location+parking+staff,mtry=3, na.action=na.omit,data=data,importance=TRUE)
    
    imp=importance(fit_rf,type=1)
    imp=cbind(x_column,imp)
    imp=data.frame(imp)
    
    colnames(imp)=c("features","rank")
    rownames(imp)=NULL
    # counts <- c(imp$rank)
    imp$rank=as.numeric(as.character(imp$rank))
    imp$rank=round(imp$rank, digits = 2)
    
    imp <- arrange(imp, rank)
    imp$features <- factor(imp$features, levels = imp$features)
    ggplot(imp, aes(features, rank, fill = features)) + geom_col() + coord_flip() +
      scale_fill_brewer(palette="Spectral")+theme(axis.text=element_text(size=14),
                                                  axis.title=element_text(size=16,face="bold"))
    
  })
   

  
   output$text<- renderUI({
     data=datasetInput( )
     index=which(month_table %in% input$month )
     data=data[data$mont==index,]
     print(data)
     x_column=c("amenities", "extracharge", "location","parking", "staff")
     train<-sample_frac(data, 0.8)
     sid<-as.numeric(rownames(train)) # because rownames() returns character
     test<-data[-sid,]
     
     set.seed(4543)
     fit_rf = randomForest(Reviewer_Score~amenities+extra_charge+location+parking+staff,mtry=3, na.action=na.omit,data=data,importance=TRUE)
     
     imp=importance(fit_rf,type=1)
     imp=cbind(x_column,imp)
     imp=data.frame(imp)
     
     colnames(imp)=c("features","rank")
     rownames(imp)=NULL
     # counts <- c(imp$rank)
     imp$rank=as.numeric(as.character(imp$rank))
     imp$rank=round(imp$rank, digits = 2)
     
     imp <- arrange(imp, rank)
     imp$features <- factor(
      imp$features, levels = imp$features)
     imp=imp[imp$rank!=0,]
     
     str1= paste(imp$x_column[i],"has positive effect on  rating in",input$month )
     # for (i in 1:nrow(imp)){
     #   name <- paste("str", i, sep = "")
     #   if (imp$rank[i]>0){
     #   assign(name, paste(imp$x_column[i],"has positive effect on  rating in",input$month ))}
     #   else if (imp$rank[i]<0){
     #     assign(name, paste(imp$x_column[i],"has negative effect on  rating in",input$month ))}
     #   # HTML(paste(str1, str2, sep = '<br/>'))
     # }
      HTML(str1)
     
  
 
    
  })
  
  }

 
    
    
    


# Create Shiny app ----
options(shiny.port = 8100)
shinyApp(ui, server)
          
      



