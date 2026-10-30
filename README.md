# Kalshi Desk (paper-first PWA)
Live: https://owenpkemp-hub.github.io/kalshi-desk/

Mobile PWA that scans **real** Kalshi open markets and runs a 7-agent pipeline: Scout → Filter → Analyst → Judge → Sizer (¼-Kelly, 5%/position, 15% heat) → Risk → Logger. Paper trades, P&L, calibration and Brier-based go-live gate are stored in your browser (localStorage).

**Data:** Kalshi's public API rejects browser (CORS/Origin) requests, so `.github/workflows/snapshot.yml` runs `scripts/snapshot.py` every 15 min (GitHub cron, can lag) and commits `data/markets.json` (top 2,500 open markets with a two-sided book and activity, by 24h volume). The app tries the API directly first, then falls back to the snapshot. `liquidity` = top-of-book $ depth (the API no longer returns a liquidity field).

**Disclaimer:** Paper first. No guaranteed profit. The built-in "heuristic" fair value is not an edge; only your own probabilities count toward calibration. Not financial advice.
