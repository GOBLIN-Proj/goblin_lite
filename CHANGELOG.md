## [Unreleased]
### Added
- Integration tests for `landcover_assignment` package with `goblin_lite`.
- Dependency update: `goblin_cbm_runner` version 0.5.0 required.
  - Includes support for user-defined afforestation delays and default afforestation configurations during the delay period.
- Ability to pull down tables related to actual areas afforested.
- New grassland production support with `grassland_production` version 0.3.6.
- Passing a resource/context manager to the model, rather than a list of parameters and paths.

### Changed
- Updated CI/CD workflows to include integration testing for `landcover_assignment` package with `goblin_lite`.
- Enhanced `land_distribution` logic to better handle rewetted organic areas.
- Updated documentation and examples to reflect the new changes.
- Updated the testing suite to cover new functionalities.

## [0.4.2] (goblin_cbm_runner)
### Added
- User-specified afforestation delay functionality. (Applies to scenarios only)
- Default afforestation rates and species ratios for delay periods in `cbm_factory.yaml`.

### Changed
- Updated logic for initializing scenarios with delayed afforestation.

### Fixed
- Resolved bugs in afforestation scenario initialization.

## [0.3.2] (goblin_lite)
### Added
- New integration test: `test_landcover_integration.py`.
- Better handling of `landcover_assignment` updates.

### Fixed
- Resolved discrepancies in land use and transition area calculations.

## [0.5.0] (goblin_lite)
### Added
- Spared area category totals. These are from the land use assignment module and they are outputed
automatically with every scenario run.
- Grass yield per hectare, output as part of the main scenario generation.
- Ability to pull down tables related to actual areas afforested.
- New grassland production support with `grassland_production` version 0.3.6.
- Passing a resource/context manager to the model, rather than a list of parameters and paths.

### Changed
- Updated CI/CD workflows to include integration testing for `landcover_assignment` package with `goblin_lite`.
- Enhanced `land_distribution` logic to better handle rewetted organic areas.
- Updated documentation and examples to reflect the new changes.
- Updated the testing suite to cover new functionalities.

### NOTE 
- Package is compatible with `landcover_assignment [0.4.0]`, which now uses pyomo to optimise land distribution.
- Package is NOT compatible with `goblin_cbm_runner [<0.5.0]`.
---