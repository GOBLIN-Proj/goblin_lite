class GoblinDataManager:
    def __init__(self, AR_VALUE="AR5"):
        self.AR4_values = {"CH4": 25, "N2O": 298, "CO2e": 3.67}

        self.AR5_values = {"CH4": 28, "N2O": 265, "CO2e": 3.67}

        if AR_VALUE.upper() == "AR4":
            self.AR_values = self.AR4_values
        elif AR_VALUE.upper() == "AR5":
            self.AR_values = self.AR5_values
        else:
            raise ValueError(
                "Invalid AR_VALUE. AR_VALUE must be either 'AR4' or 'AR5'."
            )

        self.climate_change_livestock_emissions_groups = {
            "CH4": ["enteric_ch4", "manure_management_CH4"],
            "N2O": ["soils_N2O", "manure_management_N2O"],
            "CO2": ["soils_CO2"],
        }

        self.climate_change_livestock_emissions_categories = {
            "manure_management": ["manure_management_N2O", "manure_management_CH4"],
            "enteric": ["enteric_ch4"],
            "soils": ["soils_CO2", "soils_N2O"],
        }

        self.climate_change_livestock_conversion_groups = {
            "CH4": ["enteric_ch4", "manure_management_CH4"],
            "N2O": ["soils_N2O", "manure_management_N2O"],
            "CO2": ["soils_CO2"],
        }

        self.climate_change_crops_emissions_groups = {
            "N2O": ["soils_N2O"],
            "CO2": ["soils_CO2"],
        }

        self.climate_change_crop_conversion_groups = {
            "N2O": ["soils_N2O"],
            "CO2": ["soils_CO2"],
        }
