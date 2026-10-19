# Game Industry Outcomes Research (2008–2026)

## Overview

This project investigates commercial performance, development practices, launch outcomes, and player reception across the video game industry. It examines both commercially successful releases and games associated with commercial underperformance, troubled launches, operational difficulties, or significant changes in their post-launch trajectory.

The project uses a structured, evidence-based research process to distinguish documented outcomes from estimates, incomplete evidence, and interpretations.

**Research period:** 2008–2026  
**Project status:** Active research and data validation  
**Data status:** Working classifications; conclusions remain subject to source verification

## Research Objectives

The project aims to:

- Examine the relationship between commercial expectations and reported outcomes.
- Compare publisher statements, financial disclosures, sales rankings, and other available commercial evidence.
- Analyze critical reception and player perception without treating either as a direct proxy for sales or profitability.
- Investigate development practices, launch conditions, post-launch support, and operational decisions where reliable evidence is available.
- Evaluate the effects of platform availability, subscription services, and changing distribution models.
- Identify recurring patterns while accounting for differences in genre, budget, business model, release year, and available evidence.

The research does not assume that negative reception causes commercial failure, that positive reception guarantees commercial success, or that a successful launch establishes long-term profitability.

## Scope and Methodology

The dataset is a research inventory, not a verified list of the best-selling game for every year from 2008 through 2026.

It includes commercial benchmarks, franchise comparisons, troubled launches, recovery cases, and other examples selected for investigation. Inclusion in the dataset does not imply that a game's classification has been conclusively established.

Annual sales comparisons must identify the relevant:

- Calendar year and reporting period
- Geographic market
- Platform coverage
- Sales or revenue metric
- Ranking methodology
- Source and publication date

For example, a U.S. annual full-game dollar-sales ranking cannot establish a worldwide unit-sales ranking. Lifetime sales, annual sales, sell-through, sell-in, revenue, profitability, player counts, and engagement are distinct measures and must not be substituted for one another.

**2026 findings are provisional** because the calendar year is incomplete.

## Evidence Standards

The project distinguishes among:

1. **Documented facts:** Information directly supported by an identifiable source.
2. **Publisher-reported results:** Figures and statements released by a publisher or platform holder.
3. **Independent reporting:** Findings reported by identifiable journalists, analysts, or research organizations.
4. **Estimates and forecasts:** Values or expectations that are not confirmed actual results.
5. **Research interpretations:** Conclusions drawn from the available evidence.
6. **Unresolved questions:** Issues for which the current source set is insufficient.

Publisher statements are attributed to their origin. Analyst forecasts are not treated as publisher targets, and estimates are not presented as confirmed figures.

The absence of publicly available financial information does not establish that a game was unprofitable.

## Project Structure

- `data/games.csv` — Candidate games, release years, research roles, and working classifications.
- `data/sources.csv` — Source register, publication details, URLs, supported claims, and confidence assessments.
- `data/claims.csv` — Atomic research claims linked to source IDs, with evidence types, status, and limitations.
- `data/outcome_framework.csv` — Outcome categories, definitions, and minimum evidence requirements.
- `data/annual_sales_2025_evidence.csv` — Structured annual-sales evidence with geographic and metric scope.
- `data/annual_sales_sources.csv` — Sources used for annual-sales research.
- `src/analyze.py` — Data validation, summaries, and chart generation.
- `research/` — Methodology, case-study notes, and research logs.
- `outputs/` — Generated tables, charts, and validation reports.
- `notebooks/` — Workspace for exploratory analysis.

Generated files may be refreshed by running the analysis script. Source data and research notes remain the primary records for documenting evidence.

## Validation and Analysis

The Python analysis script checks data structure and relationships, including required columns, unique identifiers, valid years, and references between games, sources, and claims. It generates summary tables and visualizations to support further investigation.

Passing structural validation means the data is internally consistent according to the implemented checks. It does **not** establish that every source is accurate, every claim is sufficiently supported, or every working classification is correct.

Annual-sales validation similarly checks the consistency of the recorded data; rankings and figures must still be checked against their cited sources and stated scope.

## Reproducibility

The project uses Python and a virtual environment for dependency management.

From the project root:

```powershell
python -m pip install -r requirements.txt
python src/analyze.py
```

If using a virtual environment on Windows, activate it first:

```powershell
.\.venv\Scripts\Activate.ps1
```

The generated outputs are written to `outputs/`.

The repository is maintained in Git so that changes to the dataset, research methodology, source register, and analysis code can be tracked over time.

## Current Limitations

- Some working classifications remain unresolved pending source review.
- Public reporting may not disclose title-specific budgets, internal targets, lifetime unit sales, or profitability.
- Annual sales rankings vary by geography, platform coverage, metric, and reporting organization.
- Publisher-reported engagement figures do not independently establish commercial profitability.
- Subscription distribution complicates direct comparisons with traditional premium sales.
- Critical and player-review aggregates can vary by platform, date, sample, and review methodology.
- Industry-wide patterns require comparable evidence across multiple games, not isolated examples.

## Future Development

Planned improvements include a local data-management application for browsing and editing records, managing source-to-claim relationships, identifying missing evidence, and exploring the dataset through interactive visualizations.

The application will build on the existing research files and validation rules rather than replace the evidence base.

## Research Principle

**Classifications are hypotheses until supported by sufficient evidence.** The objective is not to prove that a predetermined set of games failed or succeeded, but to determine what the available evidence supports, what remains uncertain, and which explanations survive comparison with alternative interpretations.
