# CHANGELOG.md

## Types of changes 

[reference keepachangelog](https://keepachangelog.com/en/1.1.0/)
* `Added` for new features.
* `Changed` for changes in existing functionality.
* `Deprecated` for soon-to-be removed features.
* `Removed` for now removed features.
* `Fixed` for any bug fixes.
* `Security` in case of vulnerabilities.


## [3.1.3] - Unreleased

### Changed
  - Upgrade to Geoserver 2.27.0 latest production stable 
  - updated users model
  - updated all model migrations to latest version
  - updated poi views with newest api models
  - upgrade to Django 4.2.20
  - update dns
  - update environment variables

## [3.1.2] - 2025-05-01

### Added
  - sentry-url to settings.py as environment variable
  - zoneplan users
  - fixed database health check status message

### Fixed

  - fixed bug in libxml2 for python 3.10
  - fixed nightly import
