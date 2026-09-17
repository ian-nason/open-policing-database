# open-policing Data Dictionary

Source: [Stanford Open Policing Project standardized data](https://openpolicing.stanford.edu/data/); column definitions in `docs/data_readme.md`.
Columns named raw_* are location-specific source fields kept as text; the readme's per-location sections explain them.
`v_stops_by_year` counts stops, searches, contraband hits, arrests, citations and warnings per location and year.

## stops

One row per police stop (traffic and pedestrian) from every Stanford Open Policing Project location, 2000s-2020s: the project's standardized columns (date, time, place, subject demographics, outcome, search, contraband, vehicle) typed, plus each location's raw_* source columns as text; location_id/state/city say where a row came from

Rows: 230,002,617

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| location_id | VARCHAR | 0.0% | ar_little_rock | Source location (state_city or state_statewide); joins stops to locations |
| state | VARCHAR | 0.0% | AR |  |
| city | VARCHAR | 84.1% | albany |  |
| date | DATE | 0.1% | 1971-01-05 |  |
| time | TIME | 40.6% | 00:00:00 |  |
| raw_row_number | VARCHAR | 0.0% | 1 | Row number(s) in the project's raw extract for the location (pipe-joined when rows were merged) |
| location | VARCHAR | 31.1% | 

W. GRAND & TELEGRAPH AV |  |
| geocode_source | VARCHAR | 96.6% | GM |  |
| county_name | VARCHAR | 32.8% | 0 County |  |
| neighborhood | VARCHAR | 99.9% | -- |  |
| beat | VARCHAR | 92.1% | ! |  |
| district | VARCHAR | 68.3% | 0018 |  |
| subdistrict | VARCHAR | 99.9% | 0 |  |
| division | VARCHAR | 99.2% | ,VD |  |
| subdivision | VARCHAR | 100.0% | -1 |  |
| police_grid_number | VARCHAR | 99.7% | 1 |  |
| precinct | VARCHAR | 93.9% | 0 |  |
| region | VARCHAR | 86.7% | **UNUSED PIU CODE** |  |
| reporting_area | VARCHAR | 98.8% | 0 |  |
| sector | VARCHAR | 99.2% | 1 |  |
| subsector | VARCHAR | 99.9% | 1 |  |
| substation | VARCHAR | 99.5% | CENTRAL |  |
| service_area | VARCHAR | 99.0% | 011 |  |
| zone | VARCHAR | 98.3% | 1 |  |
| subject_race | VARCHAR | 7.7% | asian/pacific islander |  |
| subject_sex | VARCHAR | 18.2% | female |  |
| officer_id_hash | VARCHAR | 52.5% | 000001e6b6 | Hashed officer identifier, consistent within a location only |
| officer_race | VARCHAR | 90.1% | asian/pacific islander |  |
| officer_sex | VARCHAR | 92.0% | female |  |
| officer_assignment | VARCHAR | 99.6% | 1st District |  |
| department_id | VARCHAR | 85.8% | 0 |  |
| department_name | VARCHAR | 43.7% | 1015.00 |  |
| unit | VARCHAR | 97.0% | 001 |  |
| type | VARCHAR | 0.5% | pedestrian |  |
| disposition | VARCHAR | 97.9% | "DISMISSED; GUILTY, FINES ABATED" |  |
| violation | VARCHAR | 40.1% | ! HEADLIGHT OUT  DRIVERS SIDE |  |
| outcome | VARCHAR | 32.0% | arrest |  |
| search_basis | VARCHAR | 98.3% | consent |  |
| reason_for_arrest | VARCHAR | 100.0% | * |  |
| reason_for_frisk | VARCHAR | 100.0% | Erratic/Suspicious Behavior |  |
| reason_for_search | VARCHAR | 99.6% | * |  |
| reason_for_stop | VARCHAR | 55.7% | #NULL! |  |
| use_of_force_description | VARCHAR | 99.9% | NA\|NA\|handcuffed |  |
| use_of_force_reason | VARCHAR | 99.9% | NA\|NA\|NA\|no curb, no handcuff, no police vehicle |  |
| vehicle_color | VARCHAR | 84.9% | "ALUMINUM, SILVER" |  |
| vehicle_make | VARCHAR | 73.0% | "CENTURION INTL., INC." |  |
| vehicle_model | VARCHAR | 84.9% | "3" |  |
| vehicle_type | VARCHAR | 80.8% | $SED |  |
| vehicle_registration_state | VARCHAR | 86.1% | AK |  |
| notes | VARCHAR | 97.5% | 

 |  |
| officer_age | INTEGER | 94.0% | 11 |  |
| subject_age | INTEGER | 64.5% | 10 |  |
| vehicle_year | INTEGER | 76.0% | 10995 |  |
| charged_speed | DOUBLE | 99.7% | 0.0 |  |
| lat | DOUBLE | 74.1% | -34.23333056 |  |
| lng | DOUBLE | 74.1% | -0.000107693150045414 |  |
| officer_years_of_service | DOUBLE | 97.3% | -1.0 |  |
| posted_speed | DOUBLE | 97.6% | 1.0 |  |
| speed | DOUBLE | 97.8% | 1.0 |  |
| arrest_made | BOOLEAN | 53.3% | false |  |
| citation_issued | BOOLEAN | 29.1% | false |  |
| contraband_alcohol | BOOLEAN | 97.6% | false |  |
| contraband_drugs | BOOLEAN | 98.7% | false |  |
| contraband_found | BOOLEAN | 98.1% | false |  |
| contraband_other | BOOLEAN | 99.8% | false |  |
| contraband_weapons | BOOLEAN | 98.8% | false |  |
| frisk_performed | BOOLEAN | 77.7% | false |  |
| search_conducted | BOOLEAN | 21.4% | false |  |
| search_person | BOOLEAN | 59.3% | false |  |
| search_vehicle | BOOLEAN | 60.6% | false |  |
| warning_issued | BOOLEAN | 36.7% | false |  |
| raw_race_fixed | VARCHAR | 99.9% | A |  |
| raw_ethnicity_fixed | VARCHAR | 99.9% | H |  |
| raw_charge | VARCHAR | 99.9% | ----- |  |
| raw_race | VARCHAR | 38.7% | - |  |
| raw_search_basis | VARCHAR | 86.2% | Consent (negative), ---D Required |  |
| raw_location_code | VARCHAR | 86.2% | 1 |  |
| raw_ethnicity | VARCHAR | 85.3% | - |  |
| raw_driver_race | VARCHAR | 96.3% | A |  |
| raw_defendant_race | VARCHAR | 99.6% | A |  |
| raw_defendant_ethnicity | VARCHAR | 99.7% | DEFENDANT_H |  |
| raw_activity_division | VARCHAR | 99.9% | -ND DIVISION |  |
| raw_division | VARCHAR | 100.0% | - |  |
| raw_activity_beat | VARCHAR | 99.9% | BEAT - |  |
| raw_beat | VARCHAR | 100.0% | - |  |
| raw_persons_race | VARCHAR | 100.0% | A |  |
| raw_persons_ethnicity | VARCHAR | 100.0% | H |  |
| raw_driver_age_range | VARCHAR | 99.9% | -- - -- |  |
| raw_was_vehcile_searched | VARCHAR | 99.9% | NO |  |
| raw_citation_location | VARCHAR | 100.0% | - BLOCK   MM I ---- E |  |
| raw_searchtype | VARCHAR | 96.6% | - |  |
| raw_dfnd_race | VARCHAR | 99.6% | A |  |
| raw_posted_speed | VARCHAR | 99.4% | - |  |
| raw_actual_speed | VARCHAR | 99.4% | - |  |
| raw_search_reason | VARCHAR | 99.9% | - |  |
| raw_contraband_or_evidence | VARCHAR | 99.9% | No |  |
| raw_custodial_arrest_made | VARCHAR | 99.9% | No |  |
| raw_gender | VARCHAR | 100.0% | Female - F |  |
| raw_contraband_evidence | VARCHAR | 100.0% | C = Contraband or Evidence of Crime |  |
| raw_outcome_of_stop | VARCHAR | 100.0% | A = Arrest for Violation |  |
| raw_outcomeofstop | VARCHAR | 98.5% | AR |  |
| raw_reasonforstop | VARCHAR | 92.9% | 1 |  |
| raw_typeofsearch | VARCHAR | 99.9% | BI |  |
| raw_violationsobserved | VARCHAR | 99.1% | EQ |  |
| raw_statute_name | VARCHAR | 99.9% | BK |  |
| raw_statute_section | VARCHAR | 99.9% | - |  |
| raw_sex | VARCHAR | 95.5% | - |  |
| raw_officer_race | VARCHAR | 90.2% | A |  |
| raw_descent_description | VARCHAR | 97.6% | AMERICAN INDIAN |  |
| raw_subject_sdrace | VARCHAR | 99.9% | A |  |
| raw_subject_resultofencounter | VARCHAR | 99.9% | Citation |  |
| raw_subject_searchconducted | VARCHAR | 99.9% | No |  |
| raw_subject_typeofsearch | VARCHAR | 100.0% | Consent |  |
| raw_subject_resultofsearch | VARCHAR | 100.0% | Firearms, |  |
| raw_calltype | VARCHAR | 100.0% | CKS |  |
| raw_action_taken | VARCHAR | 99.8% | Citation |  |
| raw_subject_race_description | VARCHAR | 99.8% | ASIAN INDIAN |  |
| raw_search_vehicle_description | VARCHAR | 99.6% | No Search |  |
| raw_result_of_contact_description | VARCHAR | 99.6% | Citation |  |
| raw_search | VARCHAR | 99.9% | - |  |
| raw_call_desc | VARCHAR | 99.9% | ----AB          - VICIOUS ANIMAL (COMBINED EVENT) |  |
| raw_event_desc | VARCHAR | 99.9% | ARREST BY WARRANT |  |
| raw_result | VARCHAR | 100.0% | --Citation Issued |  |
| raw_subject_race_code | VARCHAR | 100.0% | A |  |
| raw_subject_ethnicity_code | VARCHAR | 100.0% | H |  |
| raw_search_authorization_code | VARCHAR | 100.0% | C |  |
| raw_intervention_disposition_code | VARCHAR | 100.0% | I |  |
| raw_subjectracecode | VARCHAR | 99.5% | A |  |
| raw_subjectethnicitycode | VARCHAR | 99.5% | H |  |
| raw_searchauthorizationcode | VARCHAR | 99.5% | C |  |
| raw_row_number_old | VARCHAR | 98.2% | ------- |  |
| raw_row_number_new | VARCHAR | 97.8% | ------- |  |
| raw_enforcementaction | VARCHAR | 97.0% | DVER Issued |  |
| raw_driverrace | VARCHAR | 94.5% | 1 |  |
| raw_typeofmovingviolation | VARCHAR | 94.5% | 0 |  |
| raw_resultofstop | VARCHAR | 94.2% | 0 |  |
| raw_actions_taken | VARCHAR | 99.8% | Evidence Seized: No |  |
| raw_subject_race | VARCHAR | 99.8% | AMER. IND. |  |
| raw_outcome | VARCHAR | 98.5% | ! citation; - warning issued. |  |
| raw_arrest_made | VARCHAR | 99.5% | - |  |
| raw_race_of_driver | VARCHAR | 99.7% | Asian |  |
| raw_action_description | VARCHAR | 89.3% | Citation Issued |  |
| raw_dept_lvl | VARCHAR | 96.1% | - |  |
| raw_dept | VARCHAR | 96.1% | ADAMS CO. S.O. HASTINGS |  |
| raw_race_cde | VARCHAR | 99.9% | A |  |
| raw_citation_response_dsc | VARCHAR | 99.9% | C |  |
| raw_township | VARCHAR | 98.3% | Aberdeen Twp |  |
| raw_action_taken_cid | VARCHAR | 99.9% | ARREST CAPIAS/WAR |  |
| raw_field_subject_cid | VARCHAR | 99.9% | - - BICYCLIST |  |
| raw_enforcement_taken | VARCHAR | 99.9% | Arrest |  |
| raw_disp_string | VARCHAR | 97.1% | --+ |  |
| raw_orc_string | VARCHAR | 98.5% | #----.-- |  |
| raw_dispositions | VARCHAR | 99.8% | -----,NE |  |
| raw_individual_contraband | VARCHAR | 99.2% | FALSE |  |
| raw_vehicle_contraband | VARCHAR | 99.2% | FALSE |  |
| raw_basisforstop | VARCHAR | 99.8% | AP |  |
| raw_operatorrace | VARCHAR | 99.8% | B |  |
| raw_operatorsex | VARCHAR | 99.8% | F |  |
| raw_searchresultone | VARCHAR | 100.0% | A |  |
| raw_searchresulttwo | VARCHAR | 100.0% | A |  |
| raw_searchresultthree | VARCHAR | 100.0% | A |  |
| raw_contact_type | VARCHAR | 91.2% | (------- row(s) affected) |  |
| raw_sectionnum | VARCHAR | 97.4% | - |  |
| raw_offensecode | VARCHAR | 97.4% | - |  |
| raw_contrabanddesc | VARCHAR | 100.0% | "BUD LIGHT" |  |
| raw_verbal_warning_issued | VARCHAR | 98.7% | FALSE |  |
| raw_written_warning_issued | VARCHAR | 98.9% | FALSE |  |
| raw_traffic_citation_issued | VARCHAR | 98.7% | FALSE |  |
| raw_misd_state_citation_issued | VARCHAR | 99.0% | FALSE |  |
| raw_suspect_ethnicity | VARCHAR | 98.7% | H |  |
| raw_driver_searched | VARCHAR | 98.7% | FALSE |  |
| raw_passenger_searched | VARCHAR | 98.7% | FALSE |  |
| raw_search_consent | VARCHAR | 98.7% | FALSE |  |
| raw_search_arrest | VARCHAR | 98.7% | FALSE |  |
| raw_search_warrant | VARCHAR | 98.7% | FALSE |  |
| raw_search_inventory | VARCHAR | 98.7% | FALSE |  |
| raw_search_plain_view | VARCHAR | 98.7% | FALSE |  |
| raw_orig_trfc_viol_cde | VARCHAR | 98.3% | - |  |
| raw_cnty_nbr | VARCHAR | 98.3% | - |  |
| raw_race_ind | VARCHAR | 98.3% | A |  |
| raw_sex_ind | VARCHAR | 98.3% | F |  |
| raw_1st_digit_race | VARCHAR | 100.0% | A |  |
| raw_4th_digit_final_outcome | VARCHAR | 100.0% | C |  |
| raw_6th_digit_search_outcome | VARCHAR | 100.0% | - |  |
| raw_person_search_search_based_on | VARCHAR | 100.0% | CONSENT |  |
| raw_person_search_search_discovered | VARCHAR | 100.0% | ALCOHOL |  |
| raw_person_searched | VARCHAR | 99.8% | NA\|NA\|NO = - |  |
| raw_vehicle_search_search_based_on | VARCHAR | 100.0% | CONSENT |  |
| raw_vehicle_search_search_discovered | VARCHAR | 100.0% | ALCOHOL |  |
| raw_vehicle_searched | VARCHAR | 99.8% | NA\|NO= - |  |
| raw_race_description | VARCHAR | 99.8% | AMERICAN INDIAN/ALASKAN NATIVE |  |
| raw_street_check_description | VARCHAR | 99.8% | AIRPORT SECURITY FO |  |
| raw_alleged_speed | VARCHAR | 99.9% | - |  |
| raw_contraband | VARCHAR | 100.0% | ' |  |
| raw_contraband_found | VARCHAR | 100.0% | *NON |  |
| raw_results | VARCHAR | 99.9% | ARR |  |
| raw_ha_race_sex | VARCHAR | 88.1% | AF |  |
| raw_ha_search_pc_boolean | VARCHAR | 89.0% | FALSE |  |
| raw_ha_search_concent_boolean | VARCHAR | 89.0% | FALSE |  |
| raw_ha_incidto_arrest_boolean | VARCHAR | 89.0% | FALSE |  |
| raw_ha_vehicle_invent_boolean | VARCHAR | 89.0% | FALSE |  |
| raw_stop_city | VARCHAR | 99.9% | Addison |  |
| raw_stop_reason_description | VARCHAR | 99.9% | (Winooski) Be On Look Rqst |  |
| raw_stop_search_description | VARCHAR | 99.9% | (Winooski) Passgr Srch |  |
| raw_stop_outcome_description | VARCHAR | 99.9% | Arrest for Violation |  |
| raw_driver_gender | VARCHAR | 96.3% | - |  |
| raw_type_description | VARCHAR | 99.9% | ABANDONED VEHICLE |  |
| raw_vehicle_description | VARCHAR | 100.0% | ---- ACUR  CA |  |
| raw_officer_gender | VARCHAR | 95.1% | - |  |
| raw_search_type | VARCHAR | 96.5% | A- |  |
| raw_enforcements | VARCHAR | 96.5% | - |  |
| raw_onhighwaydirection | VARCHAR | 99.6% | E |  |
| raw_onhighwayname | VARCHAR | 99.6% | -- |  |
| raw_fromatstreetname | VARCHAR | 99.7% | - |  |
| raw_individualsearchconducted | VARCHAR | 99.6% | N |  |
| raw_vehiclesearchconducted | VARCHAR | 99.5% | N |  |
| raw_individualcontraband | VARCHAR | 100.0% | -- |  |
| raw_vehiclecontraband | VARCHAR | 100.0% | -- |  |
| raw_summaryoutcome | VARCHAR | 99.5% | -- |  |
| raw_individualsearchbasis | VARCHAR | 100.0% | -- |  |
| raw_vehiclesearchbasis | VARCHAR | 100.0% | -- |  |
| raw_streetnbr | VARCHAR | 99.9% | - |  |
| raw_street | VARCHAR | 99.9% | "A" ST / CENTER |  |

## locations

One row per source file: state, city or statewide, release date, rows loaded, observed first/last stop dates, the data readme's stated coverage and data notes

Rows: 88

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| location_id | VARCHAR | 0.0% | ar_little_rock | Source location (state_city or state_statewide); joins stops to locations |
| state | VARCHAR | 0.0% | AR |  |
| city | VARCHAR | 37.5% | albany |  |
| statewide | BOOLEAN | 0.0% | false |  |
| release_date | DATE | 0.0% | 2020-04-01 |  |
| druid | VARCHAR | 0.0% | wb225bk3255 |  |
| source_file | VARCHAR | 0.0% | wb225bk3255_az_mesa_2023_01_26.csv.zip |  |
| rows | BIGINT | 0.0% | 10038706 |  |
| unparsed_dates | BIGINT | 0.0% | 0 |  |
| first_stop | DATE | 0.0% | 1971-01-05 |  |
| last_stop | DATE | 0.0% | 2010-07-29 |  |
| readme_coverage | VARCHAR | 0.0% | 1971-01-05 to 2016-06-26 |  |
| readme_notes | VARCHAR | 0.0% |  |  |
| raw_columns | VARCHAR | 0.0% | raw_row_number |  |

## v_stops_by_year


| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| location_id | VARCHAR | 0.0% | ar_little_rock | Source location (state_city or state_statewide); joins stops to locations |
| state | VARCHAR | 0.0% | AR |  |
| city | VARCHAR | 36.0% | albany |  |
| year | BIGINT | 0.0% | 1971 |  |
| stops | BIGINT | 0.0% | 1 |  |
| searches | BIGINT | 0.0% | 0 |  |
| contraband_found | BIGINT | 0.0% | 0 |  |
| arrests | BIGINT | 0.0% | 0 |  |
| citations | BIGINT | 0.0% | 0 |  |
| warnings | BIGINT | 0.0% | 0 |  |
