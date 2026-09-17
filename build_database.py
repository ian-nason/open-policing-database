#!/usr/bin/env python3
"""Build open-policing.duckdb from the Stanford Open Policing Project's standardized stop data.
Source: https://openpolicing.stanford.edu/data/ -- one zipped CSV of cleaned, standardized
police stops per location (88 files: 35 state patrols and 53 city/county departments,
releases of 2020-04-01 and 2023-01-26). Run ./download_data.sh first.

Tables
    stops       one row per stop, every location unioned by column name: the project's
                standardized columns typed (dates, times, booleans, numbers), plus every
                location-specific raw_* column as text, plus location_id / state / city
    locations   one row per source file: state, city, release, rows loaded, observed date
                range, the readme's stated coverage and data notes
Usage
    uv run python build_database.py [--only az_mesa ct_hartford ...] [--output open-policing.duckdb]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import zipfile
from pathlib import Path

from datapond_build import Checker, build_columns_table, ensure_metadata, export_dictionary
from datapond_build.session import connect

RAW = Path("data/raw")
TMP = Path("data/tmp")
DEFAULT_OUTPUT = "open-policing.duckdb"
SOURCE_URL = "https://openpolicing.stanford.edu/data/"
README_LOCATIONS = json.load(open("docs/locations_readme.json"))

# The project's standardized columns (data_readme.md) and their types. Anything else in a
# file is a location-specific raw_* column and stays text.
BOOL_COLS = {"arrest_made", "citation_issued", "warning_issued", "search_conducted", "search_person", "search_vehicle",
             "frisk_performed", "contraband_found", "contraband_drugs", "contraband_weapons", "contraband_alcohol", "contraband_other"}
INT_COLS = {"subject_age", "vehicle_year", "officer_age"}
DOUBLE_COLS = {"lat", "lng", "speed", "posted_speed", "charged_speed", "officer_years_of_service"}
TEXT_COLS = ["raw_row_number", "location", "geocode_source", "county_name", "neighborhood", "beat", "district", "subdistrict",
             "division", "subdivision", "police_grid_number", "precinct", "region", "reporting_area", "sector", "subsector",
             "substation", "service_area", "zone", "subject_race", "subject_sex", "officer_id_hash", "officer_race", "officer_sex",
             "officer_assignment", "department_id", "department_name", "unit", "type", "disposition", "violation", "outcome",
             "search_basis", "reason_for_arrest", "reason_for_frisk", "reason_for_search", "reason_for_stop", "use_of_force_description",
             "use_of_force_reason", "vehicle_color", "vehicle_make", "vehicle_model", "vehicle_type", "vehicle_registration_state", "notes"]
STANDARD = ["date", "time"] + TEXT_COLS + sorted(INT_COLS) + sorted(DOUBLE_COLS) + sorted(BOOL_COLS)

TABLE_DESCRIPTIONS = {
    "stops": "One row per police stop (traffic and pedestrian) from every Stanford Open Policing Project location, 2000s-2020s: "
             "the project's standardized columns (date, time, place, subject demographics, outcome, search, contraband, vehicle) "
             "typed, plus each location's raw_* source columns as text; location_id/state/city say where a row came from",
    "locations": "One row per source file: state, city or statewide, release date, rows loaded, observed first/last stop dates, "
                 "the data readme's stated coverage and data notes",
}
JOIN_HINTS = {
    "location_id": "Source location (state_city or state_statewide); joins stops to locations",
    "raw_row_number": "Row number(s) in the project's raw extract for the location (pipe-joined when rows were merged)",
    "officer_id_hash": "Hashed officer identifier, consistent within a location only",
}


def col_type(c: str) -> str:
    if c == "date":
        return "DATE"
    if c == "time":
        return "TIME"
    if c in BOOL_COLS:
        return "BOOLEAN"
    if c in INT_COLS:
        return "INTEGER"
    if c in DOUBLE_COLS:
        return "DOUBLE"
    return "VARCHAR"


def cast(c: str) -> str:
    raw = f'NULLIF(NULLIF("{c}", \'NA\'), \'\')'
    t = col_type(c)
    if t == "DATE":
        return f"TRY_STRPTIME({raw}, '%Y-%m-%d')::DATE AS {c}"
    if t == "TIME":
        return f"TRY_CAST({raw} AS TIME) AS {c}"
    if t == "BOOLEAN":
        return f"CASE {raw} WHEN 'TRUE' THEN TRUE WHEN 'FALSE' THEN FALSE END AS {c}"
    if t == "INTEGER":
        return f"TRY_CAST(TRY_CAST({raw} AS DOUBLE) AS INTEGER) AS {c}"
    if t == "DOUBLE":
        return f"TRY_CAST({raw} AS DOUBLE) AS {c}"
    return f"{raw} AS {c}"


def file_meta(z: Path) -> dict:
    m = re.match(r"^([a-z0-9]+)_([a-z]{2})_(.+)_(\d{4})_(\d{2})_(\d{2})\.csv\.zip$", z.name)
    druid, state, city, y, mo, d = m.groups()
    return {"location_id": f"{state}_{city}", "state": state.upper(), "city": None if city == "statewide" else city,
            "statewide": city == "statewide", "release_date": f"{y}-{mo}-{d}", "druid": druid, "source_file": z.name}


def readme_entry(meta: dict) -> dict | None:
    def norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    for loc in README_LOCATIONS:
        if loc["state"] == meta["state"] and norm(loc["city"]) == norm(meta["city"] or "statewide"):
            return loc
    return None


def load_file(con, z: Path, first: bool) -> dict:
    meta = file_meta(z)
    TMP.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(z) as zf:
        member = [m for m in zf.namelist() if m.endswith(".csv")][0]
        zf.extract(member, TMP)
    csv = TMP / member
    # the files are R write.csv output: comma-delimited, double-quoted where needed. The
    # dialect is given explicitly because an unquoted apostrophe in a vehicle model
    # ('RIO in tx_austin) made the sniffer pick ' as the quote character.
    con.execute(f"CREATE OR REPLACE TABLE _raw AS SELECT * FROM read_csv('{csv}', all_varchar=true, header=true, sample_size=-1, "
                f"delim=',', quote='\"', escape='\"', ignore_errors=false, max_line_size=1048576)")
    header = [r[0] for r in con.execute("DESCRIBE _raw").fetchall()]
    unknown = [h for h in header if h not in STANDARD and not h.startswith("raw_")]
    if unknown:
        raise RuntimeError(f"{z.name}: columns outside the standardized set that are not raw_*: {unknown}")
    if first:
        cols = ", ".join(f"{c} {col_type(c)}" for c in STANDARD)
        con.execute(f"CREATE TABLE stops (location_id VARCHAR, state VARCHAR, city VARCHAR, {cols})")
    # DuckDB column names are case-insensitive and a few locations vary the case of their
    # raw_* headers (raw_Race vs raw_race), so raw_* columns are stored lower-case
    have = {r[0].lower() for r in con.execute("DESCRIBE stops").fetchall()}
    target = {}
    for h in header:
        t = h if h in STANDARD else h.lower()
        while t in target.values():
            t += "_"
        target[h] = t
        if h.startswith("raw_") and t not in have:
            con.execute(f'ALTER TABLE stops ADD COLUMN "{t}" VARCHAR')
            have.add(t)
    exprs = [f"'{meta['location_id']}' AS location_id", f"'{meta['state']}' AS state",
             ("NULL" if meta["city"] is None else f"'{meta['city']}'") + " AS city"]
    for h in header:
        exprs.append(cast(h) if h in STANDARD else f'NULLIF(NULLIF("{h}", \'NA\'), \'\') AS "{target[h]}"')
    con.execute(f"INSERT INTO stops BY NAME SELECT {', '.join(exprs)} FROM _raw")
    n, bad_dates, dmin, dmax = con.execute(
        "SELECT COUNT(*), COUNT(*) FILTER (WHERE date <> 'NA' AND date <> '' AND TRY_STRPTIME(date, '%Y-%m-%d') IS NULL), "
        "MIN(TRY_STRPTIME(date, '%Y-%m-%d'))::DATE, MAX(TRY_STRPTIME(date, '%Y-%m-%d'))::DATE FROM _raw").fetchone()
    con.execute("DROP TABLE _raw")
    csv.unlink()
    rd = readme_entry(meta)
    meta.update({"rows": n, "unparsed_dates": bad_dates, "first_stop": dmin, "last_stop": dmax,
                 "readme_coverage": "; ".join(f"{a} to {b}" for a, b in rd["ranges"]) if rd else None,
                 "readme_notes": "\n".join(rd["notes"]) if rd else None,
                 "raw_columns": ", ".join(target[h] for h in header if h.startswith("raw_")) or None})
    return meta


def run_validation(con, expected_files: int) -> int:
    ck = Checker("Validation")
    ck.query(con, f"{expected_files} locations loaded", "SELECT COUNT(*) FROM locations", lambda n: n == expected_files, str)
    ck.query(con, "stops non-empty per location", "SELECT MIN(rows) FROM locations", lambda n: n > 1000, lambda n: f"min {n:,}")
    ck.query(con, "stops total matches locations", "SELECT (SELECT COUNT(*) FROM stops) = (SELECT SUM(rows) FROM locations)", lambda v: v, str)
    ck.query(con, "dates parsed (unparsed < 0.1% overall)", "SELECT SUM(unparsed_dates) * 1.0 / SUM(rows) FROM locations", lambda v: v < 0.001, lambda v: f"{v:.4%}")
    ck.query(con, "date populated (> 99%)", "SELECT COUNT(date) * 1.0 / COUNT(*) FROM stops", lambda v: v > 0.99, lambda v: f"{v:.2%}")
    ck.query(con, "stop dates outside 1990-2024 are rare (< 1%)", "SELECT COUNT(*) FILTER (WHERE date < '1990-01-01' OR date > '2024-12-31') * 1.0 / COUNT(*) FROM stops",
             lambda v: v < 0.01, lambda v: f"{v:.3%}")
    ck.query(con, "type values are vehicular/pedestrian/NULL", "SELECT COUNT(*) FROM stops WHERE type NOT IN ('vehicular', 'pedestrian')", lambda n: n == 0, str)
    ck.query(con, "subject_race values are the project's categories",
             "SELECT COUNT(DISTINCT subject_race) FROM stops WHERE subject_race NOT IN ('white','black','hispanic','asian/pacific islander','other','unknown')", lambda n: n == 0, str)
    ck.query(con, "observed first stop on/after the readme coverage start (>= 80% of locations)",
             "SELECT AVG(CASE WHEN first_stop >= LEFT(readme_coverage, 10)::DATE - INTERVAL 31 DAY THEN 1 ELSE 0 END) FROM locations WHERE readme_coverage IS NOT NULL",
             lambda v: v >= 0.8, lambda v: f"{v:.0%}")
    ck.query(con, "every location has a readme section", "SELECT COUNT(*) FROM locations WHERE readme_coverage IS NULL", lambda n: n == 0, str)
    ck.query(con, "v_stops_by_year has a row per location-year", "SELECT COUNT(*) >= (SELECT COUNT(*) FROM locations) FROM v_stops_by_year", lambda v: v, str)
    return ck.report()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path(DEFAULT_OUTPUT))
    ap.add_argument("--only", nargs="*", help="location ids to load (e.g. az_mesa ct_hartford)")
    a = ap.parse_args()
    t0 = time.time()
    files = sorted(RAW.glob("*.csv.zip"))
    if a.only:
        files = [f for f in files if file_meta(f)["location_id"] in set(a.only)]
    if not files:
        sys.exit("no input files (run ./download_data.sh)")
    con = connect(a.output, fresh=True, memory_limit="4GB", threads=2)
    metas = []
    for i, z in enumerate(files):
        t1 = time.time()
        m = load_file(con, z, first=(i == 0))
        metas.append(m)
        print(f"  [{i + 1}/{len(files)}] {m['location_id']}: {m['rows']:,} rows, {m['first_stop']} .. {m['last_stop']} ({time.time() - t1:.0f}s)", flush=True)
        if i % 10 == 9:
            con.execute("CHECKPOINT")
    con.execute("CREATE TABLE locations (location_id VARCHAR, state VARCHAR, city VARCHAR, statewide BOOLEAN, release_date DATE, druid VARCHAR, "
                "source_file VARCHAR, rows BIGINT, unparsed_dates BIGINT, first_stop DATE, last_stop DATE, readme_coverage VARCHAR, "
                "readme_notes VARCHAR, raw_columns VARCHAR)")
    for m in metas:
        con.execute("INSERT INTO locations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [m["location_id"], m["state"], m["city"], m["statewide"], m["release_date"], m["druid"], m["source_file"], m["rows"],
                     m["unparsed_dates"], m["first_stop"], m["last_stop"], m["readme_coverage"], m["readme_notes"], m["raw_columns"]])
    con.execute("""
        CREATE VIEW v_stops_by_year AS
        SELECT location_id, state, city, EXTRACT(YEAR FROM date) AS year, COUNT(*) AS stops,
               COUNT(*) FILTER (WHERE search_conducted) AS searches,
               COUNT(*) FILTER (WHERE contraband_found) AS contraband_found,
               COUNT(*) FILTER (WHERE arrest_made) AS arrests,
               COUNT(*) FILTER (WHERE citation_issued) AS citations,
               COUNT(*) FILTER (WHERE warning_issued) AS warnings
        FROM stops WHERE date IS NOT NULL GROUP BY 1, 2, 3, 4""")
    print("\nMetadata + dictionary")
    ensure_metadata(con, descriptions=TABLE_DESCRIPTIONS, tables=["stops", "locations"], source_url=SOURCE_URL,
                    license="ODC-By 1.0 (Stanford Open Policing Project)", replace=True)
    build_columns_table(con, join_hints=JOIN_HINTS, tables=["stops", "locations", "v_stops_by_year"])
    export_dictionary(con, Path("DICTIONARY.md"), title="open-policing Data Dictionary",
                      intro=[f"Source: [Stanford Open Policing Project standardized data]({SOURCE_URL}); column definitions in `docs/data_readme.md`.",
                             "Columns named raw_* are location-specific source fields kept as text; the readme's per-location sections explain them.",
                             "`v_stops_by_year` counts stops, searches, contraband hits, arrests, citations and warnings per location and year."],
                      style="registry", tables=["stops", "locations", "v_stops_by_year"])
    con.execute("CHECKPOINT")
    failures = run_validation(con, len(files))
    con.close()
    print(f"\nBUILD DONE in {(time.time() - t0) / 60:.1f} min; {len(files)} locations, {sum(m['rows'] for m in metas):,} stops; "
          f"{a.output.stat().st_size / 1024**3:.2f} GB")
    if failures:
        print(f"BUILD FAILED: {failures} check(s) failed -- do not publish this file")
        sys.exit(1)


if __name__ == "__main__":
    main()
