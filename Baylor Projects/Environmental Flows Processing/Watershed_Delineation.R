library(httr)
library(jsonlite)
library(rgdal)
library(sp)
library(sf)
library(stringr)

##########################
### Read CSV Gage Data ###
##########################

# Set working directory
setwd("E:\\TPWD Project\\Anthropogenic Variables\\Flowline Model My Watershed\\")

# Read Gage information
nfgages<-read.csv("C:\\Users\\Jay_Oliver\\Documents\\Texas EFlow Spatial\\Watershed\\Non_Falcone_Gages_Delineate_My_Watershed.csv", colClasses = c("SOURCE_FEA" = "character"))
lnfgages<-as.list(nfgages$SOURCE_FEA)

###################
### API Headers ###
###################

### Header Watershed Delineation
headers = c(
  `accept` = 'application/json',
  `Authorization` = 'Token c684b2f9596b47b1fe3e4c57e2a9ae6a421b345e',
  `Content-Type` = 'application/json',
  `X-CSRFToken` = '9P7k41yjWNqVtysnv8iv2KfeW4vadHih1wKZWkN41Mln249QxEZVZHwfvKcufvBO',
  'Accept-Encoding' = 'gzip'
)

### Header Get Watershed Job 
headers_watershed = c('Accept-Encoding' = 'gzip',
                      `accept` = 'application/json',
                      `Authorization` = ' Token c684b2f9596b47b1fe3e4c57e2a9ae6a421b345e',
                      `X-CSRFToken` = '1I2YxuQlHlxpxPM09qZTlT6vEuFgucuaTpFDpN56MksR6lttbWGjiQnwdamAw0NH')

############################
### Create Watershed job ###
############################

# Select rows of gages
{
  nfgages_select <- nfgages[7:13,] #Select rows 
  # Note: The Api only works with a maximum of seven entries at a time. 
Point_X <- nfgages_select$POINT_X # Extract Point X from row
Point_Y <- nfgages_select$POINT_Y # Extract Point Y from row

# Create Empty Lists 
data <- list() # List for Data 
job_ID <- list() # List for Job ID
job_ID_Substr <-list() # List for Job ID Substring
}

# For loop 
for (i in 1:nrow(nfgages_select)) {
  gage_name <- as.character(nfgages_select$Gage.Number)
  # Set up data 
  # Location can be substituted with any location
  data[[i]] = paste0(
  '{  "location": [',Point_Y[i],',', Point_X[i],'],
  "snappingOn": true,  "simplify": 0.0001,  "dataSource": "nhd"}')
  
  for (j in data){
    res<-
      POST(url = 'https://modelmywatershed.org/api/watershed/',
           httr::add_headers(.headers = headers),
           body = j)
    api_char <- rawToChar(res$content)
    api_JSON<- jsonlite::fromJSON(api_char, flatten = TRUE)
    job_ID[[i]] <- paste0(gage_name[i], ":", api_JSON$job)
    
    # Split Job_ID 
    job_ID_Substr[[i]] <- sub(".*:","",job_ID[i])
  }
  } 

###########################
### Delineate Watershed ###
###########################

# For loop - Create Watershed Shapefiles 
for (i in job_ID){
  tryCatch({
  gage_name <- sub(":.*", "", i) # Extracts gage number
  job_ID_Substr <- sub(".*:","",i) # Extracts Job ID string
  url_1 <-paste0(URL='https://modelmywatershed.org/api/jobs/',job_ID_Substr , '/') # Creates URL with Job String
  res_job <- GET(url=url_1,  # Get the data to create the watershed
            add_headers(.headers = headers_watershed))
  Content_response <- content(res_job, "text", encoding= "UTF-8")
  
   # Convert Response to Usable Data
  Watershed_char <- rawToChar(res_job$content)
  Watershed_JSON <- fromJSON(Watershed_char, flatten = TRUE)
  watershed_Results <- Watershed_JSON$result
  
  #Extract Coordinates
  Watershed_Coords <- watershed_Results$watershed$geometry$coordinates
  
  
  lat <- Watershed_Coords[,,2] # Extract Latitude Value
  lon <- Watershed_Coords[,,1] # Extract Longitude Value
  xym <- cbind(lon, lat) # Combine Lat and Long
  
  # Create Spatial Polygon 
  p = Polygon(xym)
  ps = Polygons(list(p),1)
  sps = SpatialPolygons(list(ps))
  proj4string(sps) = CRS("+proj=longlat +datum=WGS84 +no_defs")
  data <- data.frame(FID=gage_name, Area=0)
  spdf <- SpatialPolygonsDataFrame(sps, data)
  
  # Write spatial polygon dataframe into Shapefile
  writeOGR(spdf, dsn=".", layer = gage_name, driver = "ESRI Shapefile")
  print(paste0 ("Done", ":", gage_name))
 }, error=function(e){cat("ERROR :",conditionMessage(e), ":", gage_name,"\n")})
}


rm(Watershed_char, Watershed_JSON, watershed_Results, Watershed_Coords, api_JSON,
   Content_response, res_job, job_ID_Substr, lat,lon,xym,p, ps, sps,spdf, data, Point_X, Point_Y,
   i,j, job_ID, res, gage_name, api_char, nfgages_select)

