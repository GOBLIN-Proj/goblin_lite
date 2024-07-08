# 🧌🏋️ Goblin lite, for the generation of static scenarios using the GOBLIN modelling framework

[![license](https://img.shields.io/badge/License-GPL%203.0-red)](https://github.com/GOBLIN-Proj/goblin_lite/blob/0.1.0/LICENSE)
[![python](https://img.shields.io/badge/python-3.9-blue?logo=python&logoColor=white)](https://github.com/GOBLIN-Proj/goblin_lite)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Based on the [GOBLIN](https://gmd.copernicus.org/articles/15/2239/2022/) (**G**eneral **O**verview for a **B**ackcasting approach of **L**ivestock **IN**tensification) Scenario module

The package makes use of several other custom packages that are designed around the original GOBLIN model and the Geo GOBLIN model. It is called "GOBLIN lite" more so for the fact that it does not rely on heavy code base found in previous GOBLIN models. Instead, the GOBLIN lite package coordinates stand alone packages related to herd generation, grassland production, land use, forest carbon sequestration, scenario generation and scenario assessment. 

In addition to climate change impact categories, goblin lite also produces eutrophication and air quality impacts as well. 

There are specific classes for the retrieval of input and output dataframes, and the production of a limited number of graphics. 

GOBLIN lite also has the capacity to rank scenarios based on environmental impacts and the overall change in protein production. 

For a full list of custom package documentation that GOBLIN lite relies on, please see the [FUSION research website](https://fusion-research.eu/goblin-package-documentation.html#goblin-package-documentation).

## Installation

Install from git hub. 

```bash
pip install "goblin_lite@git+https://github.com/GOBLIN-Proj/goblin_lite.git@main" 

```

Install from PyPI

```bash
pip install goblin_lite
```

## Usage
Firstly, the config.json file should look like the following. The example shows a two scenarios. 

To add additional scenarios, simply repeat the inputs given here, update the values, including the sceanrio numbers. 

In previous versions, each scenario took 4 rows, 1 for each livestock system. This has been reduced to a single row for each 
scenario with additional prameters. 

In addition, a csv file can now be used instead. Simply add the keys as columns and the values in the rows, with a row for every scenario.
```json
[{
    "Scenarios": 0,
    "Manure management cattle": "tank liquid",
    "Manure management sheep": "solid",
    "Dairy pop": 1060000,
    "Beef pop":10000,
    "Upland sheep pop": 3000,
    "Lowland sheep pop": 50000,
    "Dairy prod":0,
    "Beef prod":0,
    "Lowland sheep prod": 0,
    "Upland sheep prod": 0,
    "Forest area":1,
    "Conifer proportion":0.7,
    "Broadleaf proportion": 0.3,
    "Conifer harvest": 0.05,
    "Conifer thinned": 0.1,
    "Broadleaf harvest": 0,
    "Crop area": 0,
    "Wetland area":0,
    "Dairy GUE":0,
    "Beef GUE":0,
    "Dairy Pasture fertilisation": 150,
    "Beef Pasture fertilisation": 110,
    "Clover proportion": 0.5,
    "Clover fertilisation": 0,
    "Urea proportion": 0.2,
    "Urea abated proportion": 0,
    "Afforest year": 2051   
},
{
    "Scenarios": 1,
    "Manure management cattle": "tank liquid",
    "Manure management sheep": "solid",
    "Dairy pop": 1060000,
    "Beef pop":10000,
    "Upland sheep pop": 10000,
    "Lowland sheep pop": 10000,
    "Dairy prod":0,
    "Beef prod":0,
    "Lowland sheep prod": 0,
    "Upland sheep prod": 0,
    "Forest area":1,
    "Conifer proportion":0.7,
    "Broadleaf proportion": 0.3,
    "Conifer harvest": 0.05,
    "Conifer thinned": 0.8,
    "Broadleaf harvest": 0,
    "Crop area": 0,
    "Wetland area":0,
    "Dairy GUE":0,
    "Beef GUE":0,
    "Dairy Pasture fertilisation": 150,
    "Beef Pasture fertilisation": 110,
    "Clover proportion": 0.5,
    "Clover fertilisation": 0,
    "Urea proportion": 0.2,
    "Urea abated proportion": 0,
    "Afforest year": 2051  
}]
```

The model also requires a yaml file to set specific parameters for the CBM CFS3 model 

```yaml
Classifiers:

  harvest:
    clearfell:
      - conifer: 0.5
      - broadleaf: 0.06
    thinning:
      - conifer: 0.4
      - broadleaf: 0

  age_classes:
    max_age: 100
    age_interval: 5

  species:
    - Sitka
    - SGB

  yield_class:
    Sitka:
      - YC13_16: 0.37
      - YC17_20: 0.26
      - YC20_24: 0.20
      - YC24_30: 0.17
    SGB:
      - YC10: 1
```

Below is an example of the model, which generates scenarios, and the uses the results to generate graphics.

```python
from goblin_lite.goblin import ScenarioRunner
from goblin_lite.scenario_analysis.data_grapher import DataGrapher
import shutil
import os


def main():
    # configuration
    goblin_config = "./data/config.json"
    cbm_config = "./data/cbm_factory.yaml"
    ef_country = "ireland"
    baseline_year = 2020
    target_year = 2050

    data_path = "./graph_data"
    # remove graph dir
    shutil.rmtree(data_path)

    # output dir
    os.mkdir(data_path)


    # class instances
    runner_class = ScenarioRunner(
        ef_country, baseline_year, target_year, goblin_config, cbm_config
    )
    graph_class = DataGrapher()

    # run scenarios
    runner_class.run_scenarios()

    # plot data
    graph_class.plot_animal_lca_emissions_by_category(data_path)
    graph_class.plot_land_use_emissions(data_path)
    graph_class.plot_forest_flux(data_path, detail=True)
    graph_class.plot_forest_aggregate(data_path)
    graph_class.plot_forest_flux_subplot(data_path)
    graph_class.plot_crop_lca_emissions_by_category(data_path)
    graph_class.plot_crop_livestock_lca_emissions_by_category(data_path)

    # ranking variables
    target = 0.01
    gas = "CO2E"

    # plot ranks
    graph_class.rank_chart(target, gas, data_path)


if __name__ == "__main__":
    main()
```
## License
This project is licensed under the terms of the GPL-3.0-or-later license.
