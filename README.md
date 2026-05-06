# Test Data Management

Utilities for generating realistic Salesforce Sales Cloud test data for development, demos, QA, sandboxes, and integration testing.

## Overview

This repository currently includes a Python-based Salesforce test data generator that can create related sample records for common Sales Cloud objects:

- Accounts
- Contacts
- Opportunities
- Quotes
- Orders
- Order Items

The generated records preserve simple parent-child relationships, such as Contacts and Opportunities belonging to Accounts, Quotes referencing Opportunities, Orders referencing Quotes, and Order Items referencing Orders.

> **Note:** The generated data is synthetic and intended for testing only. Review and adapt the fields before importing into a real Salesforce org.

## Repository contents

| File | Purpose |
| --- | --- |
| `salesforce_test_data_generator.py` | Main CLI utility for generating Salesforce-style test data. |
| `main_version.py` | Version/reference script. |
| `pr_version.py` | Version/reference script. |

## Requirements

- Python 3.8+
- No external Python packages are required; the generator uses only the Python standard library.

## Quick start

Clone the repository:

```bash
git clone https://github.com/openautonomyx/test-data-management.git
cd test-data-management
```

Generate CSV files with the default settings:

```bash
python salesforce_test_data_generator.py --output ./out
```

Generate both CSV and JSON output with a reproducible random seed:

```bash
python salesforce_test_data_generator.py --accounts 50 --format both --output ./out --seed 42
```

## Output files

When using CSV output, the generator creates one file per object in the selected output directory:

```text
out/
├── Accounts.csv
├── Contacts.csv
├── Opportunities.csv
├── Quotes.csv
├── Orders.csv
└── OrderItems.csv
```

When using JSON output, the generator writes a single `salesforce_test_data.json` file containing all generated objects.

## CLI options

| Option | Default | Description |
| --- | ---: | --- |
| `--accounts` | `50` | Number of Account records to generate. |
| `--contacts-total` | unset | Total number of Contact records to distribute across Accounts. |
| `--contacts-per-account` | `2-4` | Random Contact count range per Account when `--contacts-total` is not set. |
| `--opportunities-total` | unset | Total number of Opportunity records to distribute across Accounts. |
| `--opportunities-per-account` | `1-3` | Random Opportunity count range per Account when `--opportunities-total` is not set. |
| `--opp-amount-min` | `5000` | Minimum Opportunity amount. |
| `--opp-amount-max` | `500000` | Maximum Opportunity amount. |
| `--opp-stages` | unset | Comma-separated Opportunity stage list to use instead of the built-in stage list. |
| `--format` | `csv` | Output format: `csv`, `json`, or `both`. |
| `--output` | `.` | Output directory for CSV files. For JSON-only output, this is the output file path. |
| `--no-contacts` | `false` | Skip Contact generation. |
| `--no-opportunities` | `false` | Skip Opportunity generation. |
| `--no-quotes` | `false` | Skip Quote generation. |
| `--no-orders` | `false` | Skip Order and Order Item generation. |
| `--seed` | unset | Random seed for reproducible output. |

## Examples

Generate 100 Accounts with 300 Contacts and 200 Opportunities:

```bash
python salesforce_test_data_generator.py \
  --accounts 100 \
  --contacts-total 300 \
  --opportunities-total 200 \
  --format csv \
  --output ./out
```

Generate demo data using selected Opportunity stages:

```bash
python salesforce_test_data_generator.py \
  --accounts 25 \
  --opp-stages "Prospecting,Qualification,Closed Won" \
  --format both \
  --output ./demo-data \
  --seed 123
```

Generate Accounts and Contacts only:

```bash
python salesforce_test_data_generator.py \
  --accounts 50 \
  --no-opportunities \
  --no-quotes \
  --no-orders \
  --output ./accounts-contacts
```

## Salesforce import order

If you import the generated CSV files into Salesforce, import parent records before child records:

1. `Accounts.csv`
2. `Contacts.csv`
3. `Opportunities.csv`
4. `Quotes.csv`
5. `Orders.csv`
6. `OrderItems.csv`

The generated IDs are synthetic Salesforce-style IDs for test linking. Depending on your import tool and Salesforce org configuration, you may need to map these values to external ID fields instead of native Salesforce `Id` fields.

## Data model notes

- Contacts reference Accounts through `AccountId`.
- Opportunities reference Accounts through `AccountId`.
- Quotes reference Opportunities through `OpportunityId`.
- Orders reference Quotes through `QuoteId`.
- Order Items reference Orders through `OrderId`.
- Opportunity probability is derived from the selected stage when the stage exists in the built-in probability map.

## Development

Run the generator directly while iterating:

```bash
python salesforce_test_data_generator.py --format both --output ./tmp --seed 1
```

Because the project currently uses only the Python standard library, no dependency installation step is required.

## Contributing

Contributions are welcome. Useful improvements include:

- Additional Salesforce objects and relationships
- Configurable field schemas
- More realistic address and company data
- Validation helpers for import order and required fields
- Unit tests for deterministic generation with seeded runs

## License

No license file is currently included. Add a license before distributing or reusing this project outside internal testing workflows.
