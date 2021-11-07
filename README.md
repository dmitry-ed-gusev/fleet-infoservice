# Fleet Info Service
Dmitrii Gusev, Sergei Lukin (C), 2020 - 2022


## Service Description
Fleet Info Service is a data aggregator for the world fleet. Info Service process and merge data from the 
open data sources and provides analytics, based on aggregated data.  


## Data Sources
Project uses various public data sources. See description below.

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

### Project Setup (for Developer)
Project setup for developer is simple enough and consists of the following steps:
  - install **python v3.9+** (for MacOS it is recommended to use **Homebrew**)
  - install **pip v21.3+** (the latest is better)
  - install common dependencies (for the current user or for the whole environment):
    + **jupyter** [optional] (the latest is better) - used for some playground (there are some notebooks in the project)
    + **pipenv v2021.5.29+** (the latest is better) - manage project environment
    + **build v0.7.0+** (the latest is better) - just a simple build tool for distribution creation, used by setuptools
      (usually setuptools - dependency of the pip itself)
  - clone the project repository from **github**, all following commands should be executed within the project root dir
  - install all pipenv dependencies (they are listed in files [Pipfile](Pipfile) and [Pipfile.lock](Pipfile.lock)) with 
    the command:  
    `pipenv install --dev`
  - check pre-commit shook config in the file [.pre-commit-config.yaml](.pre-commit-config.yaml) and activate git 
    pre-commit hook with the command [optional]:  
    `pipenv run pre-commit install`
  - build project (usual steps with running unit tests and quality control tools) with the provided build 
    script [build.sh](build.sh) with the command:  
    `./build.sh` or `pipenv run ./build.sh`
  - more info see in the build info comments itself

### Installing The Library in the local pipenv (for Developer)
Usually it is not necessary, because library itself is put as a dependency to [Pipfile](Pipfile), but just
in case you need it, use the following command:  
`pipenv install -e . `

### Installing The Library (for User)
TBD

### Quality Control
We used the following tools for the quality management:
  - for testing we use **pytest** library
  - for static types check we use **mypy** library
  - for check code formatting and alignment with the PEP8 we use **flake8** library
  - for the actual code formatting we use **black** library
For all the mentioned tools we use the latest available versions (see [Pipfile](Pipfile)).

#### Quality Control Defaults
  - max line length = 110 symbols
  - ???


## pipenv dependencies FAQ
  - If you can't install black with pipenv - use option --pre with pipenv install:  
    `pipenv install black --dev --pre`
