# Game Industry Outcomes Research (2008–2026)

This is a clean replacement starter project. Copy the project files into your existing VS Code project folder or open this folder directly in VS Code.

## Important scope note
This is a **candidate inventory**, not a verified list of the best-selling game in every year from 2008 through 2026. The inventory combines commercial benchmarks, franchise comparisons, recovery cases, and operational failures. To claim a yearly best-seller, you must choose one consistent metric and geography (for example, U.S. full-game dollar sales from a named annual chart, or global lifetime units) and source each year consistently.

2026 is incomplete. Treat all 2026 findings as provisional.

## Folder layout
- `data/games.csv`: candidate games and working classifications
- `data/sources.csv`: source register and evidence notes
- `data/claims.csv`: atomic claims linked to source IDs
- `data/outcome_framework.csv`: definitions and minimum evidence requirements
- `src/analyze.py`: loads, validates, and summarizes the data
- `outputs/`: generated summaries and charts
- `research/methodology.md`: research rules

## Setup in VS Code
1. Open this project folder in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment if needed:
   - Windows: `py -m venv .venv`
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
4. Install dependencies: `python -m pip install -r requirements.txt`
5. Run: `python src/analyze.py`

If you already have Python and a virtual environment, activate it and install the requirements. Do not keep two different copies of the same project open accidentally.

## What the script does
- Checks required columns, unique IDs, missing values, invalid years, and unmatched game/source/claim IDs.
- Prints basic summaries.
- Writes `outputs/games_by_year.csv` and `outputs/outcome_counts.csv`.
- Creates `outputs/games_by_year.png` and `outputs/working_outcomes.png`.

## Research discipline
Working classifications are hypotheses for organizing research, not final conclusions. Keep confirmed facts, publisher-reported figures, analyst estimates, and your own interpretation distinct. Negative reviews or online controversy alone do not prove a commercial failure.
