# Fleet Info Service
Dmitrii Gusev, Sergei Lukin (C), 2020 - 2021  


## Service Description

Fleet Info Service is a data aggregator for the world fleet. Info Service process and merge data from the 
open data sources and provides analytics, based on aggregated data.  

## Data Sources

### Main Data Sources

The service aggregates the following **public data sources**:
  - [Russian Maritime Register of Shipping](https://rs-class.org/)
  - [Russian Maritime Register of Shipping - Register Book](https://rs-class.org/)
  - [Russian River Register](https://www.rivreg.ru/)
  - [Russian River Register - Register Book](https://www.rivreg.ru/activities/class/regbook/)
  - [GIMS (official)](https://www.mchs.gov.ru/ministerstvo/uchrezhdeniya-mchs-rossii/gosudarstvennaya-inspekciya-po-malomernym-sudam)
  - [GIMS (unofficial)](http://www.gims.ru)
  - [RosMorRechFlot](http://morflot.gov.ru/)
  - [RosMorRechFlot - Open Data](http://opendata.morflot.ru/)
  - [Clarksons](https://www.clarksons.net)
  - [MorFlot](???)
  - [Vessel Finder](???)
  - [Marine Traffic](???)

### Additional Data Sources

The list of related systems / sources of additional info:
  - [Центр СКО](https://www.c-sko.ru/)
  - [Vessels in Class - IACS](http://www.iacs.org.uk/ship-company-data/vessels-in-class/)
  - [World Shipping Register](https://world-ships.com/)


## Project Architecture and Tech Details

For creating the project architecture the service [draw.io/diagrams.net](https://www.diagrams.net/) was used.
  - RAW architecture file in the **draw.io** format: [architecture raw](docs/fleet_info_service.drawio)
  - Architecture in the JPEG format: [architecture jpeg](docs/fleet_info_service.jpeg) 

### Project Setup for Developer
  - install python 3.9+ (for MacOS - use Homebrew)
  - install pip 21.3+
  - install common dependencies (for user / the whole environment):
    - jupyter [optional] - used for some playground
    - pipenv - manage project environment
  - install pipenv dependencies (they are listed in files [Pipfile](Pipfile) and [Pipfile.lock](Pipfile.lock))
  - activate git pre-commit hook [optional] - `pipenv run pre-commit install`, before - check pre-commit hook 
config [.pre-commit-config.yaml](.pre-commit-config.yaml)
  - ???

### Build Project
For the project build it is recommended to use shell script [build.sh](build.sh).

### Quality Control
We used the following tools for the quality management:
  - for testing we use **pytest** library
  - for static types check we use **mypy** library
  - for check code formatting and alignment with the PEP8 we use **flake8** library
  - for the actual code formatting we use **black** library 

#### Quality Control Defaults
  - max line length = 110 symbols
  - ???

### Tech Info
Related technical/technological info may be found here: [Tech Info](tech_info.md)

## pipenv dependencies
If you can't install black with pipenv - use option --pre with pipenv install:  
`pipenv install black --dev --pre`
