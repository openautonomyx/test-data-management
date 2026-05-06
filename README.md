# Test Data Management

Generate synthetic Salesforce Sales Cloud test data for development, demos, QA, sandbox seeding, and integration testing.

The main utility in this repository is `salesforce_test_data_generator.py`, a zero-dependency Python CLI that creates related records for common Salesforce Sales Cloud objects and writes them to CSV, JSON, or both.

## What it generates

The generator creates synthetic records for:

- Accounts
- Contacts
- Opportunities
- Quotes
- Orders
- Order Items

The generated objects include simple relationships so records can be imported or tested together:

```text
Account
├── Contact
└── Opportunity
    └── Quote
        └── Order
            └── Order Item
```

> **Important:** This tool creates synthetic data for non-production use. Review generated fields, validation rules, required fields, and import mappings before loading data into any Salesforce org.

## Repository contents

| File | Purpose |
| --- | --- |
| `salesforce_test_data_generator.py` | Recommended CLI for generating Salesforce-style test data. |
| `main_version.py` | Earlier/reference version of the generator. |
| `pr_version.py` | Earlier/reference version of the generator. |

## Requirements

- Python 3.8 or later
- No third-party Python packages

## Quick start

Clone the repository:

```bash
git clone https://github.com/openautonomyx/test-data-management.git
cd test-data-management
```

Generate default CSV output:

```bash
python salesforce_test_data_generator.py --output ./out
```

Generate both CSV and JSON output with deterministic results:

```bash
python salesforce_test_data_generator.py \
  --accounts 50 \
  --format both \
  --output ./out \
  --seed 42
```

## Output

### CSV output

CSV mode writes one file per generated Salesforce object:

```text
out/
├── Accounts.csv
├── Contacts.csv
├── Opportunities.csv
├── Quotes.csv
├── Orders.csv
└── OrderItems.csv
```

### JSON output

JSON mode writes all generated objects into a single file:

```text
salesforce_test_data.json
```

When `--format both` is used, CSV files are written to the output directory and JSON is written to:

```text
<output>/salesforce_test_data.json
```

## CLI reference

| Option | Default | Description |
| --- | --- | --- |
| `--accounts` | `50` | Number of Account records to generate. |
| `--contacts-total` | unset | Total number of Contact records to distribute across generated Accounts. |
| `--contacts-per-account` | `2-4` | Range of Contacts per Account when `--contacts-total` is not provided. |
| `--opportunities-total` | unset | Total number of Opportunity records to distribute across generated Accounts. |
| `--opportunities-per-account` | `1-3` | Range of Opportunities per Account when `--opportunities-total` is not provided. |
| `--opp-amount-min` | `5000` | Minimum generated Opportunity amount. |
| `--opp-amount-max` | `500000` | Maximum generated Opportunity amount. |
| `--opp-stages` | unset | Comma-separated Opportunity stage list. Example: `Prospecting,Qualification,Closed Won`. |
| `--format` | `csv` | Output format: `csv`, `json`, or `both`. |
| `--output` | `.` | Output directory for CSV and `both` modes. In JSON-only mode, this is treated as the output JSON file path. |
| `--no-contacts` | `false` | Skip Contact generation. |
| `--no-opportunities` | `false` | Skip Opportunity generation. |
| `--no-quotes` | `false` | Skip Quote generation. |
| `--no-orders` | `false` | Skip Order and Order Item generation. |
| `--seed` | unset | Random seed for reproducible generated data. |

## Examples

Generate 100 Accounts, 300 Contacts, and 200 Opportunities:

```bash
python salesforce_test_data_generator.py \
  --accounts 100 \
  --contacts-total 300 \
  --opportunities-total 200 \
  --format csv \
  --output ./out
```

Generate a small demo dataset with selected Opportunity stages:

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

Generate JSON only:

```bash
python salesforce_test_data_generator.py \
  --accounts 10 \
  --format json \
  --output ./salesforce_test_data.json
```

## Salesforce import guidance

Import parent objects before child objects:

1. `Accounts.csv`
2. `Contacts.csv`
3. `Opportunities.csv`
4. `Quotes.csv`
5. `Orders.csv`
6. `OrderItems.csv`

The generated IDs are synthetic Salesforce-style identifiers. In many Salesforce import workflows, you should not map these values directly to native `Id` fields. Instead, consider mapping them to external ID fields and using those external IDs to maintain relationships during import.

Before importing, check your target org for:

- Required custom fields
- Validation rules
- Picklist restrictions
- Duplicate rules
- Record types
- Automation that may run on insert
- Object availability and enabled Salesforce features

## Data relationships

| Object | Relationship field | Parent object |
| --- | --- | --- |
| Contact | `AccountId` | Account |
| Opportunity | `AccountId` | Account |
| Quote | `OpportunityId` | Opportunity |
| Order | `QuoteId` | Quote |
| Order Item | `OrderId` | Order |

## Deterministic test data

Use `--seed` when you need repeatable output for tests, snapshots, demos, or CI workflows:

```bash
python salesforce_test_data_generator.py --accounts 20 --seed 2026 --output ./seeded-data
```

Running the same command with the same seed will produce the same randomized values for supported generation paths.

## Development

Run the generator locally:

```bash
python salesforce_test_data_generator.py --format both --output ./tmp --seed 1
```

Clean generated output:

```bash
rm -rf ./tmp ./out ./demo-data ./accounts-contacts
```

Because the project uses only the Python standard library, there is no dependency installation step.

## Suggested next improvements

- Add unit tests for deterministic seeded output
- Add schema configuration for custom Salesforce fields
- Add support for more Sales Cloud and Service Cloud objects
- Add configurable output prefixes and external ID field names
- Add sample import templates for Salesforce Data Loader
- Add CI checks for formatting and basic script execution

## License

No license file is currently included. Add a license before distributing or reusing this project outside internal testing workflows.
