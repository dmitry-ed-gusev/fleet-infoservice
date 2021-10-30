# Fleet Info Service
Dmitrii Gusev, Sergei Lukin (C), 2020 - 2021  


## Service Description

Fleet Info Service is a data aggregator for the world fleet. Info Service process and merge data from the 
open data sources and provides analytics, based on aggregated data.  

Service aggregates the following public data sources:
  - [Russian Maritime Register of Shipping](https://rs-class.org/)
  - [Russian River Register](https://www.rivreg.ru/)
  - [Rosmorrechflot](http://morflot.gov.ru/)
  - [Rosmorrechflot - Open Data](http://opendata.morflot.ru/)
  - []()
  - []()

The list of related systems / sources of additional info:
  - [Центр СКО](https://www.c-sko.ru/)
  - [Vessels in Class - IACS](http://www.iacs.org.uk/ship-company-data/vessels-in-class/)
  - [World Shipping Register](https://world-ships.com/)


## Project Architecture

For creating the project architecture the service [draw.io/diagrams.net](https://www.diagrams.net/) was used.
  - RAW architecture file in the **draw.io** format: [architecture raw](docs/fleet_info_service.drawio)
  - architecture in the JPEG format: [architecture jpeg](docs/fleet_info_service.jpeg) 


## Building Project

TBD


## Tech Info
Related technical/technological info may be found here: [Tech Info](tech_info.md)

## pipenv dependencies
If you can't install black with pipenv - use option --pre with pipenv install:  
`pipenv install black --dev --pre`
