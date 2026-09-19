# Coin Analyze

Coin Analyze is a Telegram bot that turns cryptocurrency market data into a
clear, plain-language analytics report.

A user can send the bot a coin name or ticker, such as `Bitcoin`, `BTC`, or
`ETH`, or upload a CSV containing OHLCV data. The bot validates the request,
obtains or cleans the market data, calculates performance and risk metrics, and
returns a concise report inside Telegram.

The project is currently in its foundation stage. The package structure and
development environment are ready; market-data ingestion, analytics, and the
Telegram interface are planned work.

## User experience

### Analyze a coin

```text
User: Analyze Ethereum

Bot:
Ethereum (ETH)
Period: Last 90 days
Currency: USD
Data source: ...

Performance
• Total return: ...
• Annualized volatility: ...
• Maximum drawdown: ...

Risk
• Sharpe ratio: ...
• Sortino ratio: ...
• Value at Risk: ...

Data checked at: ...
```

If a name or ticker could refer to more than one asset, the bot asks the user
to choose before continuing.

### Analyze an uploaded CSV

The user uploads a CSV with the following columns:

```csv
timestamp,open,high,low,close,volume
2026-01-01,93425.10,95110.00,92780.40,94890.20,18654.82
```

The bot checks the file before calculating anything. Invalid columns,
unparseable timestamps, non-numeric prices, duplicate rows, missing values, and
unsorted observations are reported clearly. A usable file produces the same
analytics report as the coin-name flow.

## Version 1 scope

Version 1 will:

- Accept a cryptocurrency name or ticker.
- Resolve ambiguous assets through a user choice.
- Fetch timestamped OHLCV data from a documented public source.
- Accept an OHLCV CSV upload.
- Normalize both input paths into one internal data format.
- Report data-quality problems before running calculations.
- Calculate simple, logarithmic, and cumulative returns.
- Calculate annualized volatility, maximum drawdown, CAGR, Sharpe ratio,
  Sortino ratio, and Value at Risk where the available data supports them.
- Return a readable plain-text report in Telegram.
- State the asset, quote currency, period, data source, and retrieval time.

## Outside Version 1

Version 1 will not:

- Accept voice notes, images, screenshots, or arbitrary documents.
- Generate charts.
- Execute trades or connect to an exchange account.
- Tell a user to buy or sell an asset.
- Present incomplete or unverified data as a reliable analysis.

## Design principles

- **One analytics engine:** API and CSV inputs produce the same normalized
  dataset and use the same calculations.
- **Clear provenance:** Every report identifies its asset, timeframe, currency,
  data source, and retrieval time.
- **Explain failure:** Invalid or insufficient data produces a useful message
  instead of a misleading result.
- **Telegram stays thin:** Telegram receives input and presents output; the
  Python package owns validation and calculations.
- **Test known answers:** Financial calculations are checked against small
  examples that can be verified by hand.
- **No hidden trading advice:** Reports describe measured performance and risk.

## Planned architecture

```text
Telegram interface
        │
        ▼
Request parser
   ┌────┴────┐
   ▼         ▼
Coin input   CSV upload
   │         │
   ▼         ▼
Market API   CSV loader
   └────┬────┘
        ▼
Validation and normalization
        │
        ▼
Quant analytics engine
        │
        ▼
Plain-text report formatter
        │
        ▼
Telegram response
```

The planned modules have these responsibilities:

| Area | Responsibility |
| --- | --- |
| Telegram interface | Receive messages and files, manage replies, and translate Telegram events into application requests. |
| Request parser | Determine whether the user supplied a coin request or CSV and extract the requested asset and period. |
| Coin resolver | Map names and tickers to an unambiguous market-data identifier. |
| Market-data client | Fetch OHLCV data and retain its source and retrieval metadata. |
| CSV loader | Read an uploaded file and convert it into the internal tabular format. |
| Validation | Enforce the required schema, types, chronological ordering, and data-quality rules. |
| Analytics | Calculate returns and risk metrics without depending on Telegram. |
| Report formatter | Convert analytics results and warnings into a concise Telegram message. |

## Development setup

### Requirements

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/)

Clone and prepare the project:

```bash
git clone git@github.com:jemmycodes/coin-analyze.git
cd coin-analyze
uv sync
```

Verify that the package imports from the project environment:

```bash
uv run python -c "import coin_analyze; print(coin_analyze.__file__)"
```

Run the test suite once real analytics tests are added:

```bash
uv run pytest
```

## Development plan

1. Define and validate the normalized OHLCV data contract.
2. Load and clean OHLCV CSV files.
3. Implement returns and known-answer tests.
4. Add coin resolution and public market-data ingestion.
5. Add risk and performance metrics incrementally.
6. Build the plain-text report formatter.
7. Connect the tested core to Telegram.
8. Test complete coin-name and CSV user journeys.

## Security and privacy

Telegram bot tokens and other credentials must be provided through environment
variables and must never be committed. Uploaded files should be processed only
for the requested analysis and should not be retained without an explicit
product requirement.

## License

No license has been selected yet.
