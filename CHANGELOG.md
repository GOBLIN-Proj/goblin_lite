## [Unreleased]
### Added
- Integration tests for `landcover_assignment` package with `goblin_lite`.
- Dependency update: `goblin_cbm_runner` version 0.4.2 required.
  - Includes support for user-defined afforestation delays and default afforestation configurations during the delay period.

### Changed
- Updated CI/CD workflows to include integration testing for `landcover_assignment` package with `goblin_lite`.
- Enhanced `land_distribution` logic to better handle rewetted organic areas.

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

---