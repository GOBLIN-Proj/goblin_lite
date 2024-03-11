from goblin_lite.goblin import ScenarioRunner
from goblin_lite.scenario_analysis.data_grapher import DataGrapher
import shutil
import os


def main():
    # configuration
    db_path = "./data/DATABASE/instance_1.db"
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
        ef_country, baseline_year, target_year, goblin_config, cbm_config, db_path
    )
    graph_class = DataGrapher(db_path)

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
