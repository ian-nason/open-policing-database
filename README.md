# Stanford Open Policing Project stops as a DuckDB database

Every standardized stop released by the [Stanford Open Policing Project](https://openpolicing.stanford.edu/):
35 state patrols and 53 city or county police departments, roughly 2000-2020, in one table.
The project cleaned each agency's records into a common schema (Pierson et al., *Nature
Human Behaviour* 2020); this build types those columns and unions all 88 locations so a
single query runs across states.

| Table | One row per | Rows |
|-------|-------------|-----:|
| `stops` | police stop (vehicular or pedestrian) | [STOPS] |
| `locations` | source file: state, city or statewide, release, rows, observed and stated coverage, data notes | 88 |
| `v_stops_by_year` (view) | location x year: stops, searches, contraband hits, arrests, citations, warnings | |

`location_id` (for example `ca_statewide`, `il_chicago`) joins `stops` to `locations`.
Columns and null rates: `DICTIONARY.md`; the project's column definitions and per-location
notes: `docs/data_readme.md`.

## Quick start

```python
import datapond
con = datapond.connect("open-policing")
con.sql("""
    SELECT state, subject_race, COUNT(*) AS stops,
           ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted)
                 / COUNT(*) FILTER (WHERE search_conducted IS NOT NULL), 2) AS pct_searched
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

## How it was built

Each location's zipped CSV is loaded one at a time (DuckDB capped at 4 GB). The project's
standardized columns get types: `date` DATE, `time` TIME, the twelve yes/no fields
(`search_conducted`, `contraband_found`, `arrest_made`, ...) BOOLEAN, `subject_age`,
`vehicle_year`, `officer_age` INTEGER, `lat`, `lng`, speeds DOUBLE, everything else text.
The project's `NA` is NULL. Columns named `raw_*` are the extra source fields the project
carried through for a location (its readme explains each); they are stored lower-case as
text and are NULL for every other location. A column outside the standardized set that is
not `raw_*` fails the build.

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
- **License:** the project releases the data under ODC-By 1.0 and asks users to cite
  E. Pierson et al., "A large-scale analysis of racial disparities in police stops across
  the United States", *Nature Human Behaviour* 4, 736-745 (2020).

## Build

```bash
uv sync && ./download_data.sh        # 88 zipped CSVs, 4.8 GB, from stacks.stanford.edu
uv run python build_database.py      # one location at a time; ~[MINUTES] minutes, DuckDB capped at 4 GB
uv run python publish_to_hf.py --verify
```

## License

Code: MIT. Data: ODC-By 1.0 (Stanford Open Policing Project); attribution required.
