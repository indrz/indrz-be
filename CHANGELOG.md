# CHANGELOG.md

## Types of changes

[reference keepachangelog](https://keepachangelog.com/en/1.1.0/)
* `Added` for new features.
* `Changed` for changes in existing functionality.
* `Deprecated` for soon-to-be removed features.
* `Removed` for now removed features.
* `Fixed` for any bug fixes.
* `Security` in case of vulnerabilities.

## [] - unversioned

### Changed (unversioned)

* Frontend: refactored left panel navigation UX for improved consistency and usability
* Frontend: unified header across route and POI panels with consistent close behavior
* Frontend: simplified POI panel layout - moved title/info above actions, removed duplicate buttons
* Frontend: close button now properly closes drawer and returns to floating search bar

### Fixed (unversioned)

* Frontend: fixed floor URL parameter (`?floor=0`) not being respected on initial page load
* Frontend: fixed FloorChanger not syncing with URL floor parameter
* Frontend: fixed POI category loading race condition when using `?poi-cat-id=` URL parameter
* Frontend: fixed shelf edit modal not opening when clicking the pencil icon in ShelfDataList — `AddEditShelfData` was missing a `v-dialog` wrapper
* Frontend: fixed shelf data delete always deleting the row-selected item instead of the clicked row's item in ShelfDataList
* Frontend: fixed book shelf delete always deleting the row-selected item instead of the clicked row's item in BookShelfList
* Frontend: fixed `item.raw` usage in BookShelfList Vuetify 3 data table slots — Vuetify 3 provides the raw item directly as `item`
* Frontend: fixed Building select in AddEditShelf showing `[object Object]` — `item-text` renamed to `item-title` in Vuetify 3
* Frontend: fixed action icon clicks in data tables bubbling up to the row click handler — added `@click.stop`
* Frontend: fixed `currentShelfData` prop changes not syncing into the edit form in AddEditShelfData
* Frontend: fixed DELETE requests in shelf store sending an unnecessary FormData body — switched from `api.postRequest` to `api.request` with `method: 'DELETE'`

### Added (unversioned)

### Removed (unversioned)

* Frontend: removed redundant Info button from POI panel (info section always visible)
* Frontend: removed duplicate Share button from POI panel routing options

## [4.0.1] - 2025-12-06

### Changed

* Frontend: bumped version to 4.0.1 after completing migration to Vue 3, Nuxt 4 and Vuetify 3.
* Frontend: removed legacy Vuex, axios usage and Vue 2 compatibility helpers in favour of Pinia and the shared ofetch-based API helper.

## [3.1.3] - 2025

### Changed 2025

* Upgrade to Geoserver 2.28.2 latest production stable 
* updated users model
* updated all model migrations to latest version
* updated poi views with newest api models
* upgrade to Django 4.2.20
* update dns
* update environment variables

## [3.1.2] - 2025-05-01

### Added 2025-05-01

* sentry-url to settings.py as environment variable
* zoneplan users
* fixed database health check status message

### Fixed 2025-05-01

* fixed bug in libxml2 for python 3.10
* fixed nightly import
