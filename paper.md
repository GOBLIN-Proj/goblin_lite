---
title: 'GOBLIN Lite: A National Land Balance Model for Assessment of Climate Mitigation Pathways for Ireland.'
tags:
  - Python
  - Land use change
  - climate change
  - environmental impact
authors:
  - name: Colm Duffy
    orcid: 0000-0002-0076-6749
    corresponding: true 
    affiliation: 1
  - name: Daniel Henn
    affiliation: 2
  - name: Remi Prudhomme
    orcid: 0000-0002-7042-4656
    affiliation: 3
  - name: David Styles
    orcid: 0000-0003-4185-4478
    affiliation: 1
affiliations:
 - name: University of Galway, Ireland
   index: 1
 - name: University of Limerick, Ireland
   index: 2
 - name: French Agricultural Research Centre for International Development, France
   index: 3
date: 02 April 2024
bibliography: paper.bib

---

# Summary

GOBLIN Lite is a Python-based tool for evaluating land balance and AFOLU (Agriculture, Forestry, and Other Land Use) scenarios specifically tailored to the Irish context. Building upon the GOBLIN framework, it offers increased resolution and aligns with Ireland's National Inventory Report methodologies (including the CBM-CFS3 carbon accounting model). This integration enhances accuracy and makes `GOBLIN Lite` a valuable tool for research, policymaking and education. `GOBLIN Lite` calculates emissions across diverse life cycle assessment impact categories, providing policymakers and researchers with a nuanced tool to explore the environmental and economic trade-offs of land-use decisions.

# Statement of need

Ireland's complex AFOLU emissions profile necessitates a modeling tool that captures both major sources and sinks. `GOBLIN Lite` is designed for this purpose. The package is based on the original GOBLIN (General Overview for a Backcasting approach to Livestock INtensification) model [@Duffy:2022], the package calculates CO2 fluxes from varied soil types and forests, along with CH4 emissions from livestock activities. Further, it models nitrogen (N) losses, including N2O, NH3, and dissolved forms, across the agricultural landscape.  

`GOBLIN Lite`'s enhanced resolution – in herd dynamics, soil-specific spared area modeling, and additional impact categories –  surpasses the original GOBLIN model [@Duffy:2022a]. It integrates Tier 3 forest modeling [@Kurz:2008] for additional resolution and alignment with Irish National Inventory reporting [@NIR]. This makes GOBLIN Lite a powerful asset for policymakers, researchers, and students, as evidenced by its use in impactful "net-zero" pathway studies.

The GOBLIN modeling framework has already been used in recent studies on pathways to "net-zero" for the AFOLU sector and evaluation of "net-zero definitions [@Bishop:2024; @Duffy2022b]. 


# Acknowledgements

This research was supported by EPA Research 2030, funded by Ireland’s Environment Protection Agency under grant number EPA-CCRP-MS.57, and by Ireland’s Department of Environment, Climate and Communications under FORESIGHT land use modelling services contract.

# References