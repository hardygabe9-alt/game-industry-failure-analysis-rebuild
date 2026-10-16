# Annual sales inventory: protocol and limitations

## Requested standard
- Geography: global
- Primary metric: annual dollar sales
- Coverage: broad inventory of major best-sellers per calendar year, 2008–2026

## Important availability constraint
A consistent, freely available public source that ranks individual games by global annual dollar sales across PC, console, and mobile for every year from 2008 through 2026 has not been established. Public sources often cover only one geography, selected platforms, retail-only or full-game spending, mobile estimates, or publisher-reported milestones. A lifetime copies-sold milestone cannot be substituted for annual revenue.

## Entry rules
1. Only enter `annual_sales_value_usd` when the source explicitly supports a global annual dollar-sales value for that game and calendar year.
2. Keep `annual_rank` blank unless the source gives a rank for the same metric, period, and geography.
3. Record platform scope (e.g., PC + console, mobile, all tracked platforms) and whether the source includes full-game sales, DLC, subscriptions, microtransactions, or mobile in-app purchases.
4. Preserve the original source's metric. Do not mix units sold, sell-in, sell-through, consumer spending, publisher net revenue, and estimated gross revenue.
5. A game can be included in the broader candidate inventory with `evidence_status` such as `Global annual dollar sales verified`, `Publisher-reported milestone only`, `Regional ranking only`, `Lifetime sales only`, or `Research needed`.
6. Do not treat regional charts as global evidence. For example, Circana U.S. rankings can be retained as regional cross-checks but must not fill the global annual sales field.
7. Keep 2026 provisional because the calendar year is incomplete.

## Current source leads
- Newzoo global market reports give useful global market and platform context, but do not by themselves supply a complete 2008–2026 title-by-title global annual dollar-sales ranking.
- Newzoo's commercial platform advertises game-level revenue data, but detailed access may require a paid product.
- Circana's public annual title rankings are useful for the U.S. market, not a substitute for global rankings.

## Recommended next research design
Maintain two separate but linked datasets:
- `annual_sales_inventory_template.csv`: global annual dollar-sales evidence only.
- The project's broader `games.csv`: candidate case studies and notable commercial/lifecycle outcomes, with evidence notes.

If global annual revenue is unavailable for a title, preserve the blank and document the evidence gap. Later, an explicitly separate comparison dataset may use global units sold or regional dollar-sales rankings, but those measures must not be merged into one numeric ranking.
