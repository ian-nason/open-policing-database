# Stanford Open Policing Project stops as a DuckDB database

Traffic and pedestrian stops released by the Stanford Open Policing Project for 35 state patrols and 53 city or county departments, roughly 2000–2020. Use stops for individual stop records and locations to choose a department, time window and fields with usable coverage. Agencies report different years and outcomes; a state-patrol file is not all policing in that state.

<a id="quick-start"></a>

## Start querying

Preview Connecticut stop records from 2015 onward. Participating agency coverage is uneven; this is not all policing in Connecticut.

Choose R or Python. Install datapond once: use `install.packages("datapond")` in R, or run `python -m pip install datapond` in a terminal.

### R

```r
library(datapond)
con <- dp_connect("open-policing")
tryCatch({
  DBI::dbExecute(con, "SET threads=1")
  DBI::dbExecute(con, "SET memory_limit='128MiB'")
  DBI::dbExecute(con, "SET max_temp_directory_size='0B'")
  print(DBI::dbGetQuery(con, "SELECT state,date,subject_race,search_conducted FROM stops WHERE date>=DATE '2015-01-01' AND state='CT' LIMIT 5"))
}, finally = dp_disconnect(con))
```

### Python

```python
import datapond
con = datapond.connect('open-policing')
try:
    con.execute("SET threads=1")
    con.execute("SET memory_limit='128MiB'")
    con.execute("SET max_temp_directory_size='0B'")
    print(con.execute("""SELECT state,date,subject_race,search_conducted FROM stops WHERE date>=DATE '2015-01-01' AND state='CT' LIMIT 5""").fetchall())
finally:
    con.close()
```

Queries run on your computer and read the byte ranges they need. A small result can still require a large scan. These examples limit DuckDB to one thread and a 128 MiB buffer pool with disk spill disabled; that is not a limit on the entire R or Python process. Larger analyses may need more memory or a local download with enough disk space.

<a id="additional-dataset-notes"></a>

## Tables, fields and joins

See the [data dictionary](https://github.com/ian-nason/open-policing-database/blob/main/DICTIONARY.md) for column definitions.

The 88 source locations share the project’s standardized stop schema, allowing queries across states.

| Table | One row per | Rows |
|-------|-------------|-----:|
| `stops` | police stop (vehicular or pedestrian) | 230,002,617 |
| `locations` | source file: state, city or statewide, release, rows, observed and stated coverage, data notes | 88 |
| `v_stops_by_year` (view) | location x year: stops, searches, contraband hits, arrests, citations, warnings | |

`location_id` (for example `ca_statewide`, `il_chicago`) joins `stops` to `locations`.
Columns and null rates: `DICTIONARY.md`; the project's column definitions and per-location
notes: `docs/data_readme.md`.

### Common fields and missing values

The common fields describe date, time, place, subject race/sex/age, outcome, search, contraband and vehicle. `date` is a DATE, `time` is a TIME, and the twelve yes/no fields (including `search_conducted`, `contraband_found` and `arrest_made`) are BOOLEAN. `subject_age`, `vehicle_year` and `officer_age` are INTEGER; `lat`, `lng` and speeds are DOUBLE; other fields are text.

The project’s `NA` is stored as NULL, not false or zero. Columns named `raw_*` preserve location-specific source fields as lower-case text; they are NULL for other locations. The project’s per-location readme explains these extra fields.

## Researcher caveats

- **Coverage differs by location and field.** Not every agency records searches,
  contraband, race or outcomes, and date ranges vary from a single year to two decades.
  `locations.readme_coverage` and the per-location null rates in `DICTIONARY.md` say what
  exists; `v_stops_by_year` shows when. Do not compare rates across locations without
  checking that the field is populated in both.
- **Two releases.** 2023-01-26 files replaced the 2020-04-01 files for the locations the
  project updated (`locations.release_date`); the others are the 2020 release.
- **Privacy sanitisation by the project.** Most free-text fields have digits replaced by
  `-`; `officer_id_hash` is consistent only within a location; some fields were removed
  before public release (see the readme's asterisked columns).
- **Statewide files are state patrols**, not all policing in the state; city files are
  single departments.

<a id="advanced-access-quick-start"></a>

## More example queries

The Python example opens a new connection without resource limits. Apply the settings from the first query before a broad analysis.

The search percentage uses stops with a recorded search flag as its denominator, not all stops. A missing flag is excluded rather than treated as “not searched.” Check location and field coverage before interpreting differences between groups.

```python
import datapond
con = datapond.connect("open-policing")
con.sql("""
    SELECT state, subject_race, COUNT(*) AS stops,
           ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted)
                 / NULLIF(COUNT(*) FILTER (WHERE search_conducted IS NOT NULL), 0), 2) AS pct_searched
    FROM stops WHERE date >= '2015-01-01' AND subject_race IN ('white', 'black', 'hispanic')
    GROUP BY 1, 2 ORDER BY 1, 2
""").show()
```

```sql
-- which locations record searches and contraband at all, and for which years
SELECT location_id, MIN(year) AS first_year, MAX(year) AS last_year, SUM(stops) AS stops,
       SUM(searches) AS searches, SUM(contraband_found) AS contraband_found
FROM v_stops_by_year GROUP BY 1 HAVING SUM(searches) > 0 ORDER BY stops DESC;
```

<a id="coverage-fields-and-sources"></a>

## Sources and maintenance

### Sources and attribution

Project home: [Stanford Open Policing Project](https://openpolicing.stanford.edu/).

Source: [Stanford Open Policing Project](https://openpolicing.stanford.edu/data/). License: ODC-By 1.0.

The project cleaned each agency’s records into a common schema; see Pierson et al., *Nature Human Behaviour* 2020.

- **License:** the project releases the data under ODC-By 1.0 and asks users to cite
  E. Pierson et al., "A large-scale analysis of racial disparities in police stops across
  the United States", *Nature Human Behaviour* 4, 736-745 (2020).

### How it was built

Each location's zipped CSV is loaded one at a time (DuckDB capped at 4 GB). This build types the standardized columns and unions all 88 locations. A column outside the standardized set that is not `raw_*` fails the build.

### Build

```bash
uv sync && ./download_data.sh        # 88 zipped CSVs, 4.8 GB, from stacks.stanford.edu
uv run python build_database.py      # one location at a time; ~75 minutes, DuckDB capped at 4 GB
uv run python publish_to_hf.py --verify
```

### License

Code: MIT. Data: ODC-By 1.0 (Stanford Open Policing Project); attribution required.
