from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def load_data():
    games = pd.read_csv(DATA / "games.csv", keep_default_na=False)
    sources = pd.read_csv(DATA / "sources.csv", keep_default_na=False)
    claims = pd.read_csv(DATA / "claims.csv", keep_default_na=False)
    framework = pd.read_csv(DATA / "outcome_framework.csv", keep_default_na=False)
    return games, sources, claims, framework

def validate(games, sources, claims, framework):
    errors = []
    required = {
        "games": (games, ["game_id", "title", "release_year", "genre", "working_outcome"]),
        "sources": (sources, ["source_id", "game_id", "source_title", "url", "confidence"]),
        "claims": (claims, ["claim_id", "game_id", "claim_text", "source_ids", "status"]),
        "framework": (framework, ["outcome_category", "definition", "evidence_required"]),
    }
    for label, (df, cols) in required.items():
        missing_cols = [c for c in cols if c not in df.columns]
        if missing_cols:
            errors.append(f"{label}: missing columns {missing_cols}")
        if df.empty:
            errors.append(f"{label}: file has no rows")
    if "game_id" in games.columns:
        if games["game_id"].duplicated().any():
            errors.append("games.csv contains duplicate game_id values")
        years = pd.to_numeric(games["release_year"], errors="coerce")
        if years.isna().any() or not years.between(1970, 2026).all():
            errors.append("games.csv has invalid release_year values (expected 1970–2026)")
    if "source_id" in sources.columns and sources["source_id"].duplicated().any():
        errors.append("sources.csv contains duplicate source_id values")
    if "claim_id" in claims.columns and claims["claim_id"].duplicated().any():
        errors.append("claims.csv contains duplicate claim_id values")

    game_ids = set(games.get("game_id", []))
    if "game_id" in sources.columns:
        unknown = sorted(set(sources["game_id"]) - game_ids)
        if unknown:
            errors.append(f"sources.csv contains unknown game_id values: {unknown}")
    if "game_id" in claims.columns:
        unknown = sorted(set(claims["game_id"]) - game_ids)
        if unknown:
            errors.append(f"claims.csv contains unknown game_id values: {unknown}")

    source_ids = set(sources.get("source_id", []))
    if "source_ids" in claims.columns:
        for _, row in claims.iterrows():
            for sid in [s.strip() for s in str(row["source_ids"]).split(";") if s.strip()]:
                if sid not in source_ids:
                    errors.append(f"{row['claim_id']} references missing source_id {sid}")

    if errors:
        print("VALIDATION: ISSUES FOUND")
        for error in errors:
            print(" -", error)
    else:
        print("VALIDATION: PASS — IDs, required columns, years, and references look consistent.")

    print("\nData sizes")
    print(f"Games: {len(games)}")
    print(f"Sources: {len(sources)}")
    print(f"Claims: {len(claims)}")
    print(f"Outcome framework categories: {len(framework)}")
    return errors


def validate_annual_sales():
    """Validate the annual-sales research file and its source references."""
    file_path = DATA / "annual_sales_2025_evidence.csv"
    source_file = DATA / "annual_sales_sources.csv"
    report_path = OUT / "annual_sales_2025_validation.txt"

    required_columns = [
        "calendar_year",
        "game_title",
        "publisher",
        "platform_scope",
        "geographic_scope",
        "sales_metric",
        "annual_sales_value_usd",
        "annual_rank",
        "sales_period",
        "source_id",
        "evidence_status",
        "limitations",
    ]

    issues = []
    notes = []
    df = None

    # Check that the research file exists.
    if not file_path.exists():
        issues.append(
            "Research file not found: data/annual_sales_2025_evidence.csv"
        )
    else:
        df = pd.read_csv(file_path, keep_default_na=False)

        missing_columns = [
            col for col in required_columns if col not in df.columns
        ]

        if missing_columns:
            issues.append(f"Missing required columns: {missing_columns}")

        if df.empty:
            issues.append("The annual-sales research file has no rows.")

        if "calendar_year" in df.columns:
            years = pd.to_numeric(df["calendar_year"], errors="coerce")
            if years.isna().any() or not years.eq(2025).all():
                issues.append(
                    "The 2025 pilot file should contain only year 2025."
                )

        if "game_title" in df.columns:
            if df["game_title"].astype(str).str.strip().eq("").any():
                issues.append("One or more rows have a blank game title.")

        if "source_id" in df.columns:
            if df["source_id"].astype(str).str.strip().eq("").any():
                issues.append("One or more rows have a blank source_id.")

        # Dollar amounts may remain blank if the source does not provide them.
        if "annual_sales_value_usd" in df.columns:
            values = df["annual_sales_value_usd"].astype(str).str.strip()
            supplied_values = values[values.ne("")]
            numeric_values = pd.to_numeric(
                supplied_values.str.replace(",", "", regex=False)
                .str.replace("$", "", regex=False),
                errors="coerce",
            )

            if numeric_values.isna().any():
                issues.append("A supplied dollar-sales value is not numeric.")

            if (numeric_values < 0).any():
                issues.append("Dollar-sales values cannot be negative.")

            blank_count = int(values.eq("").sum())
            notes.append(
                f"{blank_count} rows have blank dollar-sales values. "
                "Blanks are allowed when exact values are unavailable."
            )

        # Supplied ranks must be positive whole numbers.
        if "annual_rank" in df.columns:
            ranks = df["annual_rank"].astype(str).str.strip()
            supplied_ranks = ranks[ranks.ne("")]
            numeric_ranks = pd.to_numeric(supplied_ranks, errors="coerce")

            if (
                numeric_ranks.isna().any()
                or (numeric_ranks <= 0).any()
                or (numeric_ranks % 1 != 0).any()
            ):
                issues.append(
                    "Supplied annual ranks must be positive whole numbers."
                )

        # Flag U.S. evidence that lacks an explicit scope limitation.
        if {"geographic_scope", "limitations"}.issubset(df.columns):
            for _, row in df.iterrows():
                scope = str(row["geographic_scope"]).strip().lower()
                limitation = str(row["limitations"]).strip().lower()

                if scope in {"united states", "us", "u.s."}:
                    if "not global" not in limitation:
                        notes.append(
                            f"Review geographic limitation for "
                            f"{row['game_title']}: U.S. evidence must not "
                            "be presented as global."
                        )

        # Check research source IDs against the source register.
        if not source_file.exists():
            issues.append(
                "Source register not found: data/annual_sales_sources.csv"
            )
        else:
            source_df = pd.read_csv(source_file, keep_default_na=False)

            if "source_id" not in source_df.columns:
                issues.append(
                    "annual_sales_sources.csv is missing source_id."
                )
            elif "source_id" in df.columns:
                known_source_ids = set(
                    source_df["source_id"].astype(str).str.strip()
                )

                for _, row in df.iterrows():
                    sid = str(row["source_id"]).strip()
                    if sid and sid not in known_source_ids:
                        issues.append(
                            f"{row.get('game_title', 'Unknown game')}: "
                            f"source_id {sid} is not in "
                            "annual_sales_sources.csv."
                        )

    # Write a report even if the research file is missing.
    status = "ISSUES FOUND" if issues else "STRUCTURE CHECK PASSED"

    lines = [
        "ANNUAL SALES RESEARCH VALIDATION",
        "Pilot year: 2025",
        f"Research file: {file_path}",
        "",
        f"STATUS: {status}",
        "",
        "Issues:",
    ]

    lines.extend(
        [f"- {item}" for item in issues] or ["- None detected."]
    )
    lines.extend(["", "Research notes:"])
    lines.extend([f"- {item}" for item in notes] or ["- None."])

    if df is not None:
        lines.extend([
            "",
            f"Rows: {len(df)}",
            "Structural validation does not independently verify rankings.",
        ])

    report_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\nAnnual-sales research validation:")
    print(f"STATUS: {status}")
    print(f"Report written to {report_path.relative_to(ROOT)}")

    for issue in issues:
        print(" -", issue)

    for note in notes:
        print(" NOTE:", note)

    return issues

def make_outputs(games):
    years = pd.to_numeric(games["release_year"], errors="coerce")
    by_year = years.value_counts().sort_index().rename_axis("release_year").reset_index(name="candidate_count")
    by_year.to_csv(OUT / "games_by_year.csv", index=False)

    outcomes = games["working_outcome"].value_counts().rename_axis("working_outcome").reset_index(name="game_count")
    outcomes.to_csv(OUT / "outcome_counts.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.hist(years.dropna(), bins=range(2008, 2028), edgecolor="black")
    plt.title("Candidate games by release year")
    plt.xlabel("Release year")
    plt.ylabel("Number of candidate entries")
    plt.tight_layout()
    plt.savefig(OUT / "games_by_year.png", dpi=160)
    plt.close()

    plt.figure(figsize=(11, 6))
    outcomes = outcomes.sort_values("game_count", ascending=True)
    plt.barh(outcomes["working_outcome"], outcomes["game_count"])
    plt.title("Working classifications in candidate inventory")
    plt.xlabel("Number of games")
    plt.ylabel("Working classification")
    plt.tight_layout()
    plt.savefig(OUT / "working_outcomes.png", dpi=160)
    plt.close()


def main():
    games, sources, claims, framework = load_data()

    errors = validate(games, sources, claims, framework)
    annual_sales_errors = validate_annual_sales()

    make_outputs(games)

    print("\nGames by working classification:")
    print(games["working_outcome"].value_counts().to_string())
    print("\nFiles written to outputs/")

    if errors:
        raise SystemExit(
            "\nFix the validation issues above before treating outputs as final."
        )

    if annual_sales_errors:
        print(
            "\nAnnual-sales research needs attention. "
            "See outputs/annual_sales_2025_validation.txt"
        )


if __name__ == "__main__":
    main()

