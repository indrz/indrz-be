# CHANGELOG.md

## Types of changes

[reference keepachangelog](https://keepachangelog.com/en/1.1.0/)
* `Added` for new features.
* `Changed` for changes in existing functionality.
* `Deprecated` for soon-to-be removed features.
* `Removed` for now removed features.
* `Fixed` for any bug fixes.
* `Security` in case of vulnerabilities.

## [4.0.1] - 2025-12-06

### Changed

* Migrated frontend to Vue 3, Nuxt 4, Vuetify 3 and Vite.
* Replaced Vuex with Pinia and removed remaining Vue 2 compatibility helpers.
* Centralised HTTP calls on the ofetch-based `api` helper and removed remaining axios references.

## [3.4.1] - Unreleased

in-progress

## [3.4.0] - Unreleased

### Added

* Added CHANGELOG.md to track version changes
* Added zoom argument to click on zoom to campus function

### Changed

* WCAG compliance adjustments to buttons and lists
* Token handling active storage
* Enabled full zoom no more constraint on zoom level of background map

### Removed

* Removed no longer needed attribute in POI admin add poi function

### Fixed

* POI Manager edit multiple POI bug
