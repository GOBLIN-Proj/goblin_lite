# 💻 Goblin lite, for the generation of static scenarios using the GOBLIN modelling framework

Based on the [GOBLIN](https://gmd.copernicus.org/articles/15/2239/2022/) (**G**eneral **O**verview for a **B**ackcasting approach of **L**ivestock **IN**tensification) Scenario module

The package makes use of several other custom packages that are designed around the original GOBLIN model and the Geo GOBLIN model. It is called "GOBLIN lite" more so for the fact that it does not rely on heavy code base found in previous GOBLIN models. Instead, the GOBLIN lite package coordinates stand alone packages related to herd generation, grassland production, land use, forest carbon sequestration, scenario generation and scenario assessment. 

In addition to climate change impact categories, goblin lite also produces eutrophication and air quality impacts as well. 

There are specific classes for the retrieval of input and output dataframes, and the production of a limited number of graphics. 

GOBLIN lite also has the capacity to rank scenarios based on environmental impacts and the overall change in protein production. 

## Installation

Install from git hub. 

When prompted enter your ```<username>``` and password, which is your ```<access_token>```.

```<access_token>``` is provided by the repo manager.

```<username>``` pass your own github username.


```bash
pip install "goblin_lite@git+https://github.com/colmduff/goblin_lite.git@main" 

```

## Usage
Firstly, the config.json file should look like the following. The example shows a single scenario. 

To add additional scenarios, simply repeat the inputs given here, update the values, including the sceanrio numbers. 

Remember that each scenario takes 4 rows, 1 for each livestock system.
```json
[{
    "Scenarios": 0,
    "Cattle systems": "Dairy",
    "Manure management": "tank liquid",
    "Dairy pop": 1060000,
    "Beef pop":0,
    "Dairy prod":0,
    "Beef prod":0,
    "Forest area":1,
    "Conifer proportion":0.7,
    "Broadleaf proportion": 0.3,
    "Conifer harvest": 0.05,
    "Conifer thinned": 0.1,
    "Broadleaf harvest": 0,
    "Crop area": 0,
    "Wetland area":0,
    "Grass management":0,
    "Upland sheep pop": 0,
    "Lowland sheep pop": 0,
    "Dairy Pasture fertilisation": 150,
    "Beef Pasture fertilisation": 110,
    "Afforest year": 2080   
},
{
    "Scenarios": 0,
    "Cattle systems": "Beef",
    "Manure management": "tank liquid",
    "Dairy pop": 0,
    "Beef pop":1128000,
    "Dairy prod":0,
    "Beef prod":0,
    "Forest area":1,
    "Conifer proportion":0.7,
    "Broadleaf proportion": 0.3,
    "Conifer harvest": 0.05,
    "Conifer thinned": 0.1,
    "Broadleaf harvest": 0,
    "Crop area": 0,
    "Wetland area":0,
    "Grass management":0,
    "Upland sheep pop": 0,
    "Lowland sheep pop": 0,
    "Dairy Pasture fertilisation": 150,
    "Beef Pasture fertilisation": 110,
    "Afforest year": 2080   
},
{
    "Scenarios": 0,
    "Cattle systems": "Lowland sheep",
    "Manure management": "tank solid",
    "Dairy pop": 0,
    "Beef pop":0,
    "Dairy prod":0,
    "Beef prod":0,
    "Forest area":1,
    "Conifer proportion":0.7,
    "Broadleaf proportion": 0.3,
    "Conifer harvest": 0.05,
    "Conifer thinned": 0.1,
    "Broadleaf harvest": 0,
    "Crop area": 0,
    "Wetland area":0,
    "Grass management":0,
    "Upland sheep pop": 2036000,
    "Lowland sheep pop": 0,
    "Dairy Pasture fertilisation": 150,
    "Beef Pasture fertilisation": 110,
    "Afforest year": 2080   
},
{
    "Scenarios": 0,
    "Cattle systems": "Upland sheep",
    "Manure management": "tank solid",
    "Dairy pop": 0,
    "Beef pop":0,
    "Dairy prod":0,
    "Beef prod":0,
    "Forest area":1,
    "Conifer proportion":0.7,
    "Broadleaf proportion": 0.3,
    "Conifer harvest": 0.05,
    "Conifer thinned": 0.1,
    "Broadleaf harvest": 0,
    "Crop area": 0,
    "Wetland area":0,
    "Grass management":0,
    "Upland sheep pop": 0,
    "Lowland sheep pop": 509000,
    "Dairy Pasture fertilisation": 150,
    "Beef Pasture fertilisation": 110,
    "Afforest year": 2080   
},
]
```

The model also requires a yaml file to set specific parameters for the CBM CFS3 model 

```yaml
Classifiers:
  baseline:
    clearfell: 0.02 
    thinning: 0.02
    
  classifier_id:
      1: 
        name: 
          - _CLASSIFIER
          - BL #Broad leaf forest 
          - CF #Conifer Forest 
        description:
          - Species
          - Sycamore
          - Sitka spruce
      2:
        name:
          - _CLASSIFIER
          - L
          - A

        description:
          - Forest type
          - Legacy
          - Afforestation
      3:
        name:
          - _CLASSIFIER
          - mineral
          - peat

        description:
          - Soil classes
          - Mineral
          - Peat
      4:
        name: 
          - _CLASSIFIER
          - YC10 
          - YC16 
          - YC20
          - YC24
        description:
          - Yield classes
          - Yield class 10
          - Yield class 16
          - Yield class 20
          - Yield class 24


  age_classifier:
    name:  
      - AGEID0
      - AGEID1
      - AGEID2
      - AGEID3
      - AGEID4
      - AGEID5
      - AGEID6
      - AGEID7
      - AGEID8


    description:
      - Age bins
      - Age 0
      - Age 10
      - Age 20
      - Age 30
      - Age 40
      - Age 50
      - Age 60
      - Age 70
      - Age 80
  
  age_classes:
    max_age: 80
    age_interval: 10

  #Yield class and distribution sourced from NIR
  yield_class:
    CF:
      - YC10: 0.37
      - YC16: 0.26
      - YC20: 0.20
      - YC24: 0.17
    BL:
      - YC10: 1 #FGB in NIR, related to sycamore 
    
    MF:
      - YC10: 1

  #disturbances 
  distubance_type:
    id:
      - DISTID1
      - DISTID2
      - DISTID3
      - DISTID4 
    name:
      - Clearcut
      - Thinning
      - Fire
      - Afforestation

  historical_disturbance:
    L:
      CF: DISTID1
      BL: DISTID3
      MF: DISTID1
    A:
      CF: DISTID3
      BL: DISTID3
      MF: DISTID3

  #Inventory build 
  inventory:
    species:
      - CF:
          type: 
            - L
            - A
          soil:
            - peat
            - mineral
                
          yield_class:
            - YC10
            - YC16
            - YC20
            - YC24

      - BL:
          type: 
            - L
            - A

          soil:
            - peat
            - mineral

          yield_class:
            - YC10

```

Below is an example of the model, which generates scenarios, and the uses the results to generate graphics.

```python
from goblin_lite.goblin import ScenarioRunner
from goblin_lite.data_grapher import DataGrapher
import shutil
import os

def main():

    #configuration 

    goblin_config = "./data/config.json"
    cbm_config = "./data/cbm_factory.yaml"
    ef_country = "ireland"
    baseline_year = 2020
    target_year = 2050

    #output dir 
    os.mkdir("./graph_data")
    data_path = "./graph_data"

    #class instances
    runner_class = ScenarioRunner(ef_country, baseline_year,target_year, goblin_config, cbm_config)
    graph_class = DataGrapher()

    #run scenarios
    runner_class.run_scenarios()

    #plot data 
    graph_class.plot_animal_lca_emissions_by_category(data_path)
    graph_class.plot_land_use_emissions(data_path)
    graph_class.plot_forest_flux(data_path, detail=True)
    graph_class.plot_forest_aggregate(data_path)
    graph_class.plot_forest_flux_subplot(data_path)
    graph_class.plot_crop_lca_emissions_by_category(data_path)
    graph_class.plot_crop_livestock_lca_emissions_by_category(data_path)

    #ranking variables 
    target = 0.02
    gas = "CO2e"

    #plot ranks
    graph_class.rank_chart(target, gas, data_path)

    #remove graph dir 
    shutil.rmtree(data_path)

if __name__ == "__main__":
    main()
    
```
## License
This project is licensed under the terms of the GPL-3.0-or-later license.
