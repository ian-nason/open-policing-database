# open-policing Data Dictionary

Source: [Stanford Open Policing Project standardized data](https://openpolicing.stanford.edu/data/); column definitions in `docs/data_readme.md`.
Columns named raw_* are location-specific source fields kept as text; the readme's per-location sections explain them.
`v_stops_by_year` counts stops, searches, contraband hits, arrests, citations and warnings per location and year.

## stops

One row per police stop (traffic and pedestrian) from every Stanford Open Policing Project location, 2000s-2020s: the project's standardized columns (date, time, place, subject demographics, outcome, search, contraband, vehicle) typed, plus each location's raw_* source columns as text; location_id/state/city say where a row came from

Rows: 801,325

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| location_id | VARCHAR | 0.0% | az_mesa | Source location (state_city or state_statewide); joins stops to locations |
| state | VARCHAR | 0.0% | AZ |  |
| city | VARCHAR | 21.6% | hartford |  |
| date | DATE | 0.0% | 2000-01-11 |  |
| time | TIME | 12.2% | 00:00:00 |  |
| raw_row_number | VARCHAR | 0.0% | 1 | Row number(s) in the project's raw extract for the location (pipe-joined when rows were merged) |
| location | VARCHAR | 0.1% | ??v, MESA |  |
| geocode_source | VARCHAR | 80.6% | GM |  |
| county_name | VARCHAR | 22.2% | Afton County |  |
| neighborhood | VARCHAR | 100.0% |  |  |
| beat | VARCHAR | 100.0% |  |  |
| district | VARCHAR | 97.9% | ASYLUM HILL |  |
| subdistrict | VARCHAR | 100.0% |  |  |
| division | VARCHAR | 100.0% |  |  |
| subdivision | VARCHAR | 100.0% |  |  |
| police_grid_number | VARCHAR | 100.0% |  |  |
| precinct | VARCHAR | 100.0% |  |  |
| region | VARCHAR | 100.0% |  |  |
| reporting_area | VARCHAR | 100.0% |  |  |
| sector | VARCHAR | 100.0% |  |  |
| subsector | VARCHAR | 100.0% |  |  |
| substation | VARCHAR | 100.0% |  |  |
| service_area | VARCHAR | 100.0% |  |  |
| zone | VARCHAR | 100.0% |  |  |
| subject_race | VARCHAR | 0.1% | asian/pacific islander |  |
| subject_sex | VARCHAR | 0.5% | female |  |
| officer_id_hash | VARCHAR | 0.0% | 0001846379 | Hashed officer identifier, consistent within a location only |
| officer_race | VARCHAR | 100.0% |  |  |
| officer_sex | VARCHAR | 100.0% |  |  |
| officer_assignment | VARCHAR | 100.0% |  |  |
| department_id | VARCHAR | 79.7% | 201 |  |
| department_name | VARCHAR | 41.2% | Hartford |  |
| unit | VARCHAR | 100.0% |  |  |
| type | VARCHAR | 1.2% | pedestrian |  |
| disposition | VARCHAR | 100.0% |  |  |
| violation | VARCHAR | 80.4% | 10-1-18C5 MOTOR SKTBOARD 30MPH |  |
| outcome | VARCHAR | 1.5% | arrest |  |
| search_basis | VARCHAR | 98.2% | consent |  |
| reason_for_arrest | VARCHAR | 100.0% |  |  |
| reason_for_frisk | VARCHAR | 100.0% | Erratic/Suspicious Behavior |  |
| reason_for_search | VARCHAR | 98.9% | Erratic/Suspicious Behavior |  |
| reason_for_stop | VARCHAR | 41.2% | Administrative Offense |  |
| use_of_force_description | VARCHAR | 100.0% |  |  |
| use_of_force_reason | VARCHAR | 100.0% |  |  |
| vehicle_color | VARCHAR | 100.0% |  |  |
| vehicle_make | VARCHAR | 100.0% |  |  |
| vehicle_model | VARCHAR | 100.0% |  |  |
| vehicle_type | VARCHAR | 100.0% |  |  |
| vehicle_registration_state | VARCHAR | 100.0% |  |  |
| notes | VARCHAR | 100.0% |  |  |
| officer_age | INTEGER | 100.0% |  |  |
| subject_age | INTEGER | 0.4% | 10 |  |
| vehicle_year | INTEGER | 100.0% |  |  |
| charged_speed | DOUBLE | 100.0% |  |  |
| lat | DOUBLE | 78.3% | 32.152271546000065 |  |
| lng | DOUBLE | 78.3% | -109.24715491399996 |  |
| officer_years_of_service | DOUBLE | 100.0% |  |  |
| posted_speed | DOUBLE | 100.0% |  |  |
| speed | DOUBLE | 100.0% |  |  |
| arrest_made | BOOLEAN | 21.6% | false |  |
| citation_issued | BOOLEAN | 21.6% | false |  |
| contraband_alcohol | BOOLEAN | 100.0% |  |  |
| contraband_drugs | BOOLEAN | 98.9% | false |  |
| contraband_found | BOOLEAN | 98.2% | false |  |
| contraband_other | BOOLEAN | 100.0% |  |  |
| contraband_weapons | BOOLEAN | 98.9% | false |  |
| frisk_performed | BOOLEAN | 43.5% | false |  |
| search_conducted | BOOLEAN | 41.2% | false |  |
| search_person | BOOLEAN | 43.5% | false |  |
| search_vehicle | BOOLEAN | 41.2% | false |  |
| warning_issued | BOOLEAN | 21.6% | false |  |
| raw_race_fixed | VARCHAR | 80.4% | A |  |
| raw_ethnicity_fixed | VARCHAR | 80.4% | H |  |
| raw_charge | VARCHAR | 80.4% | ----- |  |
| raw_subject_race_code | VARCHAR | 97.7% | A |  |
| raw_subject_ethnicity_code | VARCHAR | 97.7% | H |  |
| raw_search_authorization_code | VARCHAR | 97.7% | C |  |
| raw_intervention_disposition_code | VARCHAR | 97.7% | I |  |
| raw_ethnicity | VARCHAR | 43.5% | H |  |
| raw_race | VARCHAR | 22.0% | A |  |
| raw_action_description | VARCHAR | 43.5% | Citation Issued |  |
| raw_sex | VARCHAR | 78.4% | F |  |
| raw_streetnbr | VARCHAR | 79.0% | - |  |
| raw_street | VARCHAR | 78.5% | "A" ST / CENTER |  |

## locations

One row per source file: state, city or statewide, release date, rows loaded, observed first/last stop dates, the data readme's stated coverage and data notes

Rows: 4

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| location_id | VARCHAR | 0.0% | az_mesa | Source location (state_city or state_statewide); joins stops to locations |
| state | VARCHAR | 0.0% | AZ |  |
| city | VARCHAR | 25.0% | hartford |  |
| statewide | BOOLEAN | 0.0% | false |  |
| release_date | DATE | 0.0% | 2020-04-01 |  |
| druid | VARCHAR | 0.0% | wb225bk3255 |  |
| source_file | VARCHAR | 0.0% | wb225bk3255_az_mesa_2023_01_26.csv.zip |  |
| rows | BIGINT | 0.0% | 157015 |  |
| unparsed_dates | BIGINT | 0.0% | 0 |  |
| first_stop | DATE | 0.0% | 2000-01-11 |  |
| last_stop | DATE | 0.0% | 2012-12-31 |  |
| readme_coverage | VARCHAR | 0.0% | 2000-01-11 to 2015-12-31 |  |
| readme_notes | VARCHAR | 0.0% | Data is deduplicated on raw columns InterventionDateTime,
search rate is susp... |  |
| raw_columns | VARCHAR | 0.0% | raw_row_number, raw_ethnicity, raw_race, raw_action_description |  |

## v_stops_by_year


| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| location_id | VARCHAR | 0.0% | az_mesa | Source location (state_city or state_statewide); joins stops to locations |
| state | VARCHAR | 0.0% | AZ |  |
| city | VARCHAR | 7.1% | hartford |  |
| year | BIGINT | 0.0% | 2000 |  |
| stops | BIGINT | 0.0% | 15927 |  |
| searches | BIGINT | 0.0% | 0 |  |
| contraband_found | BIGINT | 0.0% | 0 |  |
| arrests | BIGINT | 0.0% | 0 |  |
| citations | BIGINT | 0.0% | 0 |  |
| warnings | BIGINT | 0.0% | 0 |  |
