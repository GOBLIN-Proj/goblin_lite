"""
Data Grapher Module
====================

The Data Grapher module is an experimental tool designed to visualize various environmental data sets. It primarily serves as a visualization aid, assisting users in interpreting complex environmental data through graphical representations. 
The module leverages data obtained from the DataFetcher class and provides functionalities to create diverse plots for different scenarios.

This module is still under development and may not function as intended in all situations. 
Users are encouraged to use this module as a basis for further customization and to adapt it to their specific data visualization needs.

Class Overview
--------------
The DataGrapher class offers methods to plot data related to crop and livestock life cycle assessment (LCA) emissions, land use emissions, forest carbon flux, and more. 
Each method is tailored to visualize specific types of data, providing insights into environmental impacts across various scenarios.

The class is designed to be flexible and user-friendly, allowing for easy integration with existing data analysis workflows. 
It is particularly useful for environmental researchers, policy makers, and analysts who require visual representations of data to support their work.

Attributes
----------
- None: The class does not require initialization with specific attributes.

Methods
-------
- plot_crop_livestock_lca_emissions_by_category(path): Visualizes combined crop and livestock LCA emissions by category for different scenarios.
- plot_crop_lca_emissions_by_category(path): Displays crop LCA emissions by category for various scenarios.
- plot_animal_lca_emissions_by_category(path): Shows livestock LCA emissions by category across different scenarios.
- plot_land_use_emissions(path): Creates plots for land-use emissions by gas for each scenario.
- plot_forest_flux(path, detail=False): Visualizes forest carbon annual flux for different scenarios.
- plot_forest_aggregate(path, detail=False): Depicts aggregated forest carbon data over time.
- plot_forest_flux_subplot(path): Generates subplots of forest carbon annual flux for each scenario.
- get_combined_crop_and_livestock_pathway_frames(): Retrieves combined dataframes for crop and livestock pathway emissions.
- rank_chart(target, gas, path): Creates a scatter plot showing the ranking and percentage change in GHG, ammonia, eutrophication, and protein output from the baseline.

Usage
-----
To use the DataGrapher class, simply create an instance of the class and call the desired plotting method with the appropriate parameters. 
The methods will generate plots based on the provided data and save them to the specified file path.

Example:
    >>> data_grapher = DataGrapher()
    >>> data_grapher.plot_crop_livestock_lca_emissions_by_category("output/path")

Note
----
- This module is experimental and may not cover all possible scenarios or data types. Users may need to modify or extend the module's capabilities to suit their specific requirements.
- The module relies on data provided by the DataFetcher class. Ensure that the data is correctly formatted and available before using the plotting methods.
- The plots generated by this module are intended for data visualization and should be interpreted cautiously, especially in the context of complex environmental data.

"""

from goblin_lite.resource_manager.data_fetcher import DataFetcher
from scenario_assessment.filter import FilterResults
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import math


class DataGrapher:
    """
    A class used to organize methods for data visualization. The current collection is relatively limited, however, utilization of the
    DataFetcher class will allow users to output dataframes and easily construct their plots.

    Though this class is still very much in development, it should still provide inspiration for various plotting pathways.

    Attributes
    ----------
    DATABASE_PATH : str, optional
        Path to the external database, if None, default internal database used.

    Methods
    -------
    plot_crop_livestock_lca_emissions_by_category(path):
        Plot combined crop and livestock life cycle assessment (LCA) emissions by category for different scenarios.

    plot_crop_lca_emissions_by_category(path):
        Plot crop LCA emissions by category (CO2E, NH3, and PO4E) for different scenarios.

    plot_animal_lca_emissions_by_category(path):
        Plot livestock LCA emissions by category (CO2E, NH3, and PO4E) for different scenarios.

    plot_land_use_emissions(path):
        Plot land-use emissions by gas (CO2, CH4, N2O) for different scenarios.

    plot_forest_flux(path, detail=False):
        Plot forest carbon annual flux (tons of carbon) for different scenarios.

    plot_forest_aggregate(path, detail=False):
        Plot aggregated forest carbon (tons of carbon) for different scenarios.

    plot_forest_flux_subplot(path):
        Plot multiple subplots of forest carbon annual flux (tons of carbon) for each scenario.

    get_combined_crop_and_livestock_pathway_frames():
        Get combined dataframes for crop and livestock pathway emissions.

    rank_chart(target, gas, path):
        Plot a scatter plot of ranking and percentage change in greenhouse gas (GHG), ammonia, eutrophication, and protein output from the baseline.

    """

    def __init__(self, DATABASE_PATH=None):
        self.data_fetcher_class = DataFetcher(DATABASE_PATH)

    def plot_crop_livestock_lca_emissions_by_category(self, path):
        """Plot combined crop and livestock life cycle assessment (LCA) emissions by category for different scenarios.

        This method generates a bar plot to visualize the emissions from combined crop and livestock activities for different scenarios. The emissions are
        categorized into different components, such as manure management, enteric emissions, emissions from grassland soils, and emissions from crop soils.
        Each component is represented by a different color for easy identification.

        The bar plot is organized into three subplots, each corresponding to a different environmental impact category: climate change, air quality, and eutrophication.

        Parameters:
            path (str): The file path where the plot will be saved, including the file name and a legal format (e.g., png, jpg).

        Returns:
            None: The plot is saved as an image file in the specified file path.

        Note:
            The method utilizes the `DataFetcher` class to retrieve dataframes containing emissions data. It calls the `get_combined_crop_and_livestock_pathway_frames()`
            method to obtain the necessary data for plotting.

        Example:
            >>> data_grapher = DataGrapher()
            >>> data_grapher.plot_crop_livestock_lca_emissions_by_category("path/to/directory")
        """
        categories = {
            "manure_management": "royalblue",
            "enteric": "indianred",
            "grassland_soils": "green",
            "crop_soils": "darkorange",
        }

        frames = self.get_combined_crop_and_livestock_pathway_frames()

        xlabels = [label -1 for label in frames[0].index]

        sns.set()
        sns.set_style("white")

        param_dict = {
            0: ["Climate Change", "CO2e kt"],
            1: ["Air Quality", "NH3 kt"],
            2: ["Eutrophication", "PO4e kt"],
        }

        fig, axes = plt.subplots(1, 3, figsize=(16, 4))

        for col, frame in enumerate(frames):
            plot_legend = False  # set plot_legend to False for all plots except one

            # create a dictionary of category-to-column mappings
            category_to_col = {}
            colors = []
            for category in categories:
                if category in frame.columns:
                    category_to_col[category] = category
                    colors.append(categories[category])

            ax = frame.plot(
                kind="bar", stacked=True, ax=axes[col], color=colors, legend=plot_legend
            )
            ax.set_ylabel(param_dict[col][1])
            ax.set_title(f"{param_dict[col][0]}")
            ax.set_xticklabels(xlabels, rotation=360)
            ax.set_xlabel("Scenario")

            # create legend with all categories
            if category_to_col:
                ax.legend(
                    category_to_col.keys(),
                    bbox_to_anchor=(1.05, 1),
                    loc="upper left",
                    borderaxespad=0.0,
                )

        plt.tight_layout()

        plt.savefig(
            os.path.join(path, "Crop_and_Livestock_LCA.png"),
            dpi=400,
            bbox_inches="tight",
        )

        plt.close()

    def plot_crop_lca_emissions_by_category(self, path):
        """Plot crop life cycle assessment (LCA) emissions by category for different scenarios.

        This method generates a bar plot to visualize the emissions from crop activities for different scenarios. The emissions are
        categorized into different components, such as emissions from soils. Each component is represented by a different color for easy identification.

        The bar plot is organized into three subplots, each corresponding to a different environmental impact category: climate change, air quality, and eutrophication.

        Parameters:
            path (str): The file path where the plot will be saved, including the file name and a legal format (e.g., png, jpg).

        Returns:
            None: The plot is saved as an image file in the specified file path.

        Note:
            The method utilizes the `DataFetcher` class to retrieve dataframes containing emissions data. It calls the necessary methods from `DataFetcher`
            (e.g., `get_crop_emissions_by_category_co2e`, `get_eutrophication_crop_emissions_by_category`, and `get_air_quality_crop_emissions_by_category`)
            to obtain the necessary data for plotting.

        Example:
            >>> data_grapher = DataGrapher()
            >>> data_grapher.plot_crop_lca_emissions_by_category("path/to/directory")
        """
        categories = {"soils": "darkorange"}

        climate_change = self.data_fetcher_class.get_crop_emissions_by_category_co2e()
        climate_change = climate_change[["soils"]].copy()
        eutrophication = (
            self.data_fetcher_class.get_eutrophication_crop_emissions_by_category()
        )
        air_quality = (
            self.data_fetcher_class.get_air_quality_crop_emissions_by_category()
        )

        xlabels = [label for label in climate_change.index]
        frames = [climate_change, air_quality, eutrophication]

        sns.set()
        sns.set_style("white")

        param_dict = {
            0: ["Climate Change", "CO2e kt"],
            1: ["Air Quality", "NH3 kt"],
            2: ["Eutrophication", "PO4e kt"],
        }

        fig, axes = plt.subplots(1, 3, figsize=(16, 4))

        for col, frame in enumerate(frames):
            plot_legend = False  # set plot_legend to False for all plots except one

            # create a dictionary of category-to-column mappings
            category_to_col = {}
            colors = []
            for category in categories:
                if category in frame.columns:
                    category_to_col[category] = category
                    colors.append(categories[category])

            ax = frame.plot(
                kind="bar", stacked=True, ax=axes[col], color=colors, legend=plot_legend
            )
            ax.set_ylabel(param_dict[col][1])
            ax.set_title(f"{param_dict[col][0]}")
            ax.set_xticklabels(xlabels, rotation=360)
            ax.set_xlabel("Scenario")

            # create legend with all categories
            if category_to_col:
                ax.legend(
                    category_to_col.keys(),
                    bbox_to_anchor=(1.05, 1),
                    loc="upper left",
                    borderaxespad=0.0,
                )

        plt.tight_layout()

        plt.savefig(os.path.join(path, "Crop_LCA.png"), dpi=400, bbox_inches="tight")

        plt.close()

    def plot_animal_lca_emissions_by_category(self, path):
        """Plot animal life cycle assessment (LCA) emissions by category for different scenarios.

        This method generates a bar plot to visualize the emissions from animal-related activities for different scenarios. The emissions are
        categorized into different components, such as emissions from manure management and enteric fermentation. Each component is represented
        by a different color for easy identification.

        The bar plot is organized into three subplots, each corresponding to a different environmental impact category: climate change, air quality, and eutrophication.

        Parameters:
            path (str): The file path where the plot will be saved, including the file name and a legal format (e.g., png, jpg).

        Returns:
            None: The plot is saved as an image file in the specified file path.

        Note:
            The method utilizes the `DataFetcher` class to retrieve dataframes containing emissions data. It calls the necessary methods from `DataFetcher`
            (e.g., `get_animal_emissions_by_category_co2e`, `get_eutrophication_animal_emissions_by_category`, and `get_air_quality_animal_emissions_by_category`)
            to obtain the necessary data for plotting.

        Example:
            >>> data_grapher = DataGrapher()
            >>> data_grapher.plot_animal_lca_emissions_by_category("path/to/directory")
        """

        categories = {
            "manure_management": "royalblue",
            "enteric": "indianred",
            "soils": "darkorange",
            "upstream": "green",
        }

        climate_change = self.data_fetcher_class.get_animal_emissions_by_category_co2e()
        eutrophication = (
            self.data_fetcher_class.get_eutrophication_animal_emissions_by_category()
        )
        air_quality = (
            self.data_fetcher_class.get_air_quality_animal_emissions_by_category()
        )

        xlabels = [label for label in climate_change.index]
        frames = [climate_change, air_quality, eutrophication]

        sns.set()
        sns.set_style("white")

        param_dict = {
            0: ["Climate Change", "CO2e kt"],
            1: ["Air Quality", "NH3 kt"],
            2: ["Eutrophication", "PO4e kt"],
        }

        fig, axes = plt.subplots(1, 3, figsize=(16, 4))

        for col, frame in enumerate(frames):
            plot_legend = False  # set plot_legend to False for all plots except one

            # create a dictionary of category-to-column mappings
            category_to_col = {}
            colors = []
            for category in categories:
                if category in frame.columns:
                    category_to_col[category] = category
                    colors.append(categories[category])

            ax = frame.plot(
                kind="bar", stacked=True, ax=axes[col], color=colors, legend=plot_legend
            )
            ax.set_ylabel(param_dict[col][1])
            ax.set_title(f"{param_dict[col][0]}")
            ax.set_xticklabels(xlabels, rotation=360)
            ax.set_xlabel("Scenario")

            # create legend with all categories
            if category_to_col:
                ax.legend(
                    category_to_col.keys(),
                    bbox_to_anchor=(1.05, 1),
                    loc="upper left",
                    borderaxespad=0.0,
                )

        plt.tight_layout()

        plt.savefig(
            os.path.join(path, "Livestock_LCA.png"), dpi=400, bbox_inches="tight"
        )

        plt.close()

    def plot_land_use_emissions(self, path):
        """Plot land use emissions for different gases and scenarios.

        This method generates a set of stacked bar plots to visualize the land use emissions for different gases and scenarios.
        The emissions are categorized by different land use types (e.g., forests, croplands, grasslands).

        The bar plots are organized in a 2x2 grid, with each plot representing a different gas: CO2, CH4, N2O, and F-gases.

        Parameters:
            path (str): The file path where the plot will be saved, including the file name and a legal format (e.g., png, jpg).

        Returns:
            None: The plot is saved as an image file in the specified file path.

        Note:
            The method utilizes the `DataFetcher` class to retrieve dataframes containing land use emissions data.
            It calls the necessary methods from `DataFetcher` (e.g., `get_landuse_emissions_totals`) to obtain the necessary data for plotting.

        Example:
            >>> data_grapher = DataGrapher()
            >>> data_grapher.plot_land_use_emissions("path/to/directory")
        """

        land_emissions_df = self.data_fetcher_class.get_landuse_emissions_totals()

        # Melt data

        land_emissions_df.rename_axis(index="index", inplace=True)
        land_emissions_df["scenario"] = land_emissions_df.index

        data = land_emissions_df[(land_emissions_df["land_use"] != "total")]

        melted_df = pd.melt(
            data,
            id_vars=["land_use", "year", "scenario"],
            var_name="gas",
            value_name="emissions",
        )

        pivot_table = pd.pivot_table(
            melted_df,
            values="emissions",
            index=["scenario", "gas"],
            columns=["land_use"],
        )
        pivot_table.fillna(0)

        sns.set()
        sns.set_style("white")

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        for i, g in enumerate(pivot_table.index.get_level_values("gas").unique()):
            row = i // 2
            col = i % 2

            ax = axes[row, col]

            plot_legend = False  # set plot_legend to False for all plots except one

            pivot_table.loc[:, g, :].plot(
                kind="bar", stacked=True, ax=ax, legend=plot_legend
            )

            ax.axhline(y=0, color="black", linewidth=0.5)
            ax.set_xlabel("Scenario")

            ax.set_ylabel("Emissions in kt")

            ax.set_title(f"{g}")

            ax.set_xticklabels(
                list(pivot_table.index.get_level_values("scenario").unique()),
                rotation=360,
            )

        plt.legend(
            bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0
        )  # create one legend outside the plot area
        plt.tight_layout()

        plt.savefig(
            os.path.join(path, "climate_change_land_use.png"),
            dpi=400,
            bbox_inches="tight",
        )
        plt.close()


    def plot_forest_flux(self, path, detail=False):
        """Plot forest carbon flux over time.

        This method generates a line plot to visualize the forest carbon flux over time. The forest carbon flux represents
        the net change in carbon stored in forests over different years and scenarios.

        Parameters:
            path (str): The file path where the plot will be saved, including the file name and a legal format (e.g., png, jpg).
            detail (bool, optional): If True, the plot will include additional details by plotting individual variables
                                    along with different scenarios. If False, the plot will only show scenarios without individual variables.

        Returns:
            None: The plot is saved as an image file in the specified file path.

        Note:
            The method utilizes the `DataFetcher` class to retrieve the forest carbon flux data.
            It calls the necessary methods from `DataFetcher` (e.g., `get_forest_flux`) to obtain the necessary data for plotting.

        Example:
            >>> data_grapher = DataGrapher()
            >>> data_grapher.plot_forest_flux("path/to/directory", detail=True)
        """

        cbm_flux = self.data_fetcher_class.get_forest_flux()

        data = pd.melt(cbm_flux, ["Year", "Scenario"])

        if detail:
            ax = sns.lineplot(
                data=data, x="Year", y="value", hue="variable", style="Scenario"
            )
        else:
            ax = sns.lineplot(data=data, x="Year", y="value", hue="Scenario")

        ax.set(xlabel="Year", ylabel="t/Carbon")

        plt.legend(
            title="Scenario",
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            borderaxespad=0,
        )

        plt.tight_layout()

        plt.savefig(os.path.join(path, "forest_carbon_flux.png"), dpi=400)

        plt.close()

    def plot_forest_aggregate(self, path, detail=False):
        """Plot aggregated forest carbon data over time.

        This method generates a line plot to visualize the aggregated forest carbon data over time.
        The aggregated forest carbon data represents the total carbon stored in forests over different years and scenarios.

        Parameters:
            path (str): The file path where the plot will be saved, including the file name and a legal format (e.g., png, jpg).
            detail (bool, optional): If True, the plot will include additional details by plotting individual variables
                                    along with different scenarios. If False, the plot will only show scenarios without individual variables.

        Returns:
            None: The plot is saved as an image file in the specified file path.

        Note:
            The method utilizes the `DataFetcher` class to retrieve the aggregated forest carbon data.
            It calls the necessary methods from `DataFetcher` (e.g., `get_forest_aggregate`) to obtain the necessary data for plotting.

        Example:
            >>> data_grapher = DataGrapher()
            >>> data_grapher.plot_forest_aggregate("path/to/directory", detail=True)
        """

        cbm_aggregate = self.data_fetcher_class.get_forest_aggregate()

        data = pd.melt(cbm_aggregate, ["Year", "Scenario"])

        if detail:
            ax = sns.lineplot(
                data=data, x="Year", y="value", hue="variable", style="Scenario"
            )

        else:
            ax = sns.lineplot(data=data, x="Year", y="value", hue="Scenario")

        ax.set(xlabel="Year", ylabel="t/Carbon")

        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
        plt.tight_layout()
        plt.savefig(os.path.join(path, "forest_carbon_aggregate.png"), dpi=400)

        plt.close()

    def plot_forest_flux_subplot(self, path):
        """Plot forest carbon flux data for multiple scenarios using subplots.

        This method generates a set of line plots arranged in subplots to visualize the forest carbon flux data
        for multiple scenarios over time. Each subplot represents a different scenario, and the lines in each subplot
        represent the carbon flux values for different variables.

        Parameters:
            path (str): The file path where the plot will be saved, including the file name and a legal format (e.g., png, jpg).

        Raises:
            Exception: If there are more than 20 scenarios present in the data, as it may lead to an overcrowded plot.

        Returns:
            None: The plot is saved as an image file in the specified file path.

        Note:
            The method utilizes the `DataFetcher` class to retrieve the forest carbon flux data for multiple scenarios.
            It calls the necessary methods from `DataFetcher` (e.g., `get_forest_flux`) to obtain the necessary data for plotting.

        Example:
            >>> data_grapher = DataGrapher()
            >>> data_grapher.plot_forest_flux_subplot("path/to/directory")
        """

        cbm_flux = self.data_fetcher_class.get_forest_flux()

        data = pd.melt(cbm_flux, ["Year", "Scenario"])

        subplot_number = len(data["Scenario"].unique())

        if subplot_number > 20:
            raise Exception("Too many scenarios present, max = 20")
        else:
            cols = 4
            rows = math.ceil(subplot_number / cols)

            fig, axes = plt.subplots(rows, cols, figsize=(12, 4))

            scenario = -1
            for r in range(rows):
                for c in range(cols):
                    mask = data["Scenario"] == scenario
                    if rows != 1:
                        if scenario in data["Scenario"].values:
                            sns.lineplot(
                                ax=axes[r, c],
                                data=data.loc[mask],
                                x="Year",
                                y="value",
                                hue="variable",
                                legend=True,
                            )
                            axes[r, c].set_title(f"Scenario: {scenario}")
                            axes[r, c].get_legend().remove()
                            axes[r, c].set_ylabel("t/Carbon")
                            axes[r, c].set_xlabel("Year")
                        else:
                            fig.delaxes(axes[r, c])

                    else:
                        if scenario in data["Scenario"].values:
                            sns.lineplot(
                                ax=axes[c],
                                data=data.loc[mask],
                                x="Year",
                                y="value",
                                hue="variable",
                                legend=True,
                            )
                            axes[c].set_title(f"Scenario: {scenario}")
                            axes[c].get_legend().remove()
                            axes[c].set_ylabel("t/Carbon")
                            axes[c].set_xlabel("Year")
                        else:
                            fig.delaxes(axes[c])

                    scenario += 1

            if rows != 1:
                handles, labels = axes[0, 0].get_legend_handles_labels()

            else:
                handles, labels = axes[0].get_legend_handles_labels()

            fig.legend(handles, labels, bbox_to_anchor=(1.15, 0.6))
            fig.tight_layout()
            fig.savefig(
                os.path.join(path, "forest_flux_subplot.png"),
                dpi=400,
                bbox_inches="tight",
            )

            plt.close()

    def get_combined_crop_and_livestock_pathway_frames(self):
        """Retrieve and combine the data related to combined crop and livestock pathway frames.

        This method fetches data from different sources for livestock and crop emissions related to various environmental factors.
        It then combines the data into three distinct dataframes: one for climate change, one for eutrophication, and one for air quality.
        The data is collected from the `DataFetcher` class, which provides separate methods to obtain livestock and crop emissions data
        for different environmental factors.

        Returns:
            list: A list of three dataframes containing combined crop and livestock pathway data for climate change, eutrophication,
                and air quality, respectively.

        Note:
            The `DataFetcher` class is utilized to fetch the necessary data for livestock and crop emissions. The dataframe columns
            represent different environmental factors and pathways, such as "manure_management," "enteric," "grassland_soils," and "crop_soils."
            The data is combined appropriately into each of the three dataframes, with common columns for the respective environmental factors.

        Example:
            >>> data_grapher = DataGrapher()
            >>> combined_frames = data_grapher.get_combined_crop_and_livestock_pathway_frames()
            >>> climate_change_frame = combined_frames[0]
            >>> eutrophication_frame = combined_frames[1]
            >>> air_quality_frame = combined_frames[2]
        """

        climate_change_livestock = (
            self.data_fetcher_class.get_animal_emissions_by_category_co2e()
        )
        eutrophication_livestock = (
            self.data_fetcher_class.get_eutrophication_animal_emissions_by_category()
        )
        air_quality_livestock = (
            self.data_fetcher_class.get_air_quality_animal_emissions_by_category()
        )

        climate_change_crop = (
            self.data_fetcher_class.get_crop_emissions_by_category_co2e()
        )
        climate_change_crop = climate_change_crop[["soils"]].copy()

        eutrophication_crop = (
            self.data_fetcher_class.get_eutrophication_crop_emissions_by_category()
        )
        air_quality_crop = (
            self.data_fetcher_class.get_air_quality_crop_emissions_by_category()
        )

        climate_cols = ["manure_management", "enteric", "grassland_soils", "crop_soils"]
        other_cols = ["manure_management", "grassland_soils", "crop_soils"]

        climate_change = pd.DataFrame(columns=climate_cols)
        eutrophication = pd.DataFrame(columns=other_cols)
        air_quality = pd.DataFrame(columns=other_cols)

        climate_change["manure_management"] = climate_change_livestock[
            "manure_management"
        ].values

        climate_change["enteric"] = climate_change_livestock["enteric"].values
        climate_change["grassland_soils"] = climate_change_livestock["soils"].values - climate_change_crop["soils"].values
        climate_change["crop_soils"] = climate_change_crop["soils"].values

        eutrophication["manure_management"] = eutrophication_livestock[
            "manure_management"
        ].values
        eutrophication["grassland_soils"] = eutrophication_livestock["soils"].values - eutrophication_crop["soils"].values
        eutrophication["crop_soils"] = eutrophication_crop["soils"].values

        air_quality["manure_management"] = air_quality_livestock.loc[
            :, "manure_management"
        ].values
        air_quality["grassland_soils"] = air_quality_livestock["soils"].values - air_quality_crop["soils"].values
        air_quality["crop_soils"] = air_quality_crop["soils"].values

        frames = [climate_change, air_quality, eutrophication]

        return frames

    def rank_chart(self, target, gas, path):
        """
        Produces a scatter plot that visualizes the data output from the Filter_results.search() method.
        The data returned from Filter_results.search() is plotted along the x and y axes. The y-axis represents the percentage change in
        the specific variable from the baseline, and the x-axis represents the ranking of scenarios based on the "cost" calculated in the
        Filter_results.search() method. The "cost" is determined by the overall impact on total livestock output (beef and milk) from the baseline.

        Parameters
        ----------
        target : str
            The target scenario or variable to compare. It can be "ghg" (Greenhouse Gas emissions), "ammonia" (ammonia emissions),
            "eutrophication" (eutrophication emissions), or "production" (protein output).

        gas : str
            The selected gas emissions to consider. This can be "CO2e" (Carbon Dioxide Equivalent), "NH3" (ammonia), or "PO4" (eutrophication).

        path : str
            The file path where the scatter plot will be saved, including the file name and a legal format (e.g., png, jpg).

        Returns
        -------
        Scatter Plot
            A scatter plot representing the ranking of scenarios on the x-axis and the percentage change in the specified variable
            (e.g., greenhouse gas emissions, ammonia emissions, eutrophication emissions, or protein output) from the baseline on the y-axis.

        Examples
        --------
        >>> data_grapher = DataGrapher()
        >>> target_variable = "ghg"
        >>> selected_gas = "CO2e"
        >>> plot_path = "path/to/directory"
        >>> data_grapher.rank_chart(target_variable, selected_gas, plot_path)

        Note
        ----
        - The method utilizes the `DataFetcher` class to fetch data related to climate change, eutrophication, air quality, and protein output.
        - It then combines the fetched data into a dictionary containing the scenario and relevant values for ranking, percentage changes in
        greenhouse gas emissions, ammonia emissions, eutrophication emissions, and protein output from the baseline.
        - The scatter plot is generated with each scenario's rank on the x-axis and the percentage change in the specified variable on the y-axis.
        - The plot includes multiple scatter plots, each representing one of the selected variables (e.g., gas emissions, eutrophication,
        ammonia, and protein output) to compare changes across different scenarios.
        - The scenarios are displayed on the secondary x-axis (ax2) with their corresponding ranks.

        """
        fetch_class = DataFetcher()

        climate = fetch_class.get_climate_change_emission_totals()
        eutrophication = fetch_class.get_eutrophication_emission_totals()
        air = fetch_class.get_air_quality_emission_totals()
        products = fetch_class.get_livestock_output_summary()

        emission_dict = {
            "climate_change": climate,
            "air_quality": air,
            "eutrophication": eutrophication,
            "protein_output": products,
        }



        filter_class = FilterResults(target, gas, emission_dict)

        data = filter_class.search()

        rank = [v for d in data for k, v in data[d].items() if k == "rank"]

        gas_percent = [v for d in data for k, v in data[d].items() if k == "gas_change"]

        eutrophication_percent = [
            v for d in data for k, v in data[d].items() if k == "eutrophication_change"
        ]

        ammonia_percent = [
            v for d in data for k, v in data[d].items() if k == "ammonia_change"
        ]

        production_percent = [
            v for d in data for k, v in data[d].items() if k == "production_cost"
        ]

        # Stem plot
        fig, ax = plt.subplots()
        # Scatter plot for gas_percent

        _, first_element_value = next(iter(data.items()))
        ax.scatter(
            rank,
            gas_percent,
            label=f"{first_element_value.get('gas')} Percentage Change",
            marker="o",
        )

        # Scatter plot for eutrophication_percent
        ax.scatter(
            rank,
            eutrophication_percent,
            label="Eutrophication Percentage Change",
            marker="s",
        )

        # Scatter plot for ammonia_percent
        ax.scatter(rank, ammonia_percent, label="Ammonia Percentage Change", marker="D")

        ax.scatter(
            rank, production_percent, label="Protein Percentage Change", marker="^"
        )

        ax.xaxis.set_ticks(range(0, (len(data) + 1), 1))

        ax.vlines(
            rank,
            ymin=ax.get_ylim()[0],
            ymax=ax.get_ylim()[1],
            colors="gray",
            linestyles="dashed",
            zorder=-1,
            alpha=0.25,
        )

        # Add x and y axis labels
        ax.set_xlabel("Rank")
        ax.set_ylabel("Percentage")

        scenarios = [d for d in data]
        ax2 = ax.twiny()

        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticks(rank)
        ax2.set_xticklabels(scenarios)
        ax2.tick_params(axis="x", rotation=360)

        ax2.set_xlabel("Scenarios")

        # Dummy plot on ax2
        ax2.plot([], [])

        # Add legend to the plot
        handles, labels = ax.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        plt.legend(
            handles + handles2,
            labels + labels2,
            bbox_to_anchor=(1.05, 1.0),
            loc="upper left",
        )

        plt.tight_layout()

        fig.savefig(os.path.join(path, "scenario_rank_chart.png"), dpi=400)

        plt.close()
