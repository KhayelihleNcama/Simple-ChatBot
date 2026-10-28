# Data Redundancy Removal System

A cloud-based pipeline that validates incoming data, classifies it as **unique**, **redundant** or **false positive**, and appends only verified, unique records to the database.

## Why this project

Duplicate records waste storage, slow queries and corrupt reports. Simple exact-match checks miss messy near-duplicates ("J. Smith, 12 Main St" vs "John Smith, 12 Main Street") and can wrongly reject look-alike records that are genuinely different. This system handles both cases.

## Features

- Schema and format validation (required fields, emails, phones, dates)
- Normalization (case, whitespace, abbreviations, date formats)
- Fast exact-match detection using SHA-256 fingerprints
- Fuzzy matching (Jaro-Winkler / Levenshtein) across multiple fields
- Three-way classification with a manual-review queue for uncertain matches
- Database-level unique constraint, so duplicates are blocked even under concurrent writes
- Audit log of every accepted, rejected and quarantined record, with reasons

## Classification

| Class | Meaning | Action |
|---|---|---|
| Unique | No match found | Insert |
| Redundant | Same real-world record | Reject, log |
| False positive | Looked like a duplicate but is distinct | Insert |
| Uncertain | Score in the gray zone | Quarantine for review |

Default thresholds: score > 0.95 redundant, < 0.70 unique, between goes to review. These are configurable and were tuned using the evaluation below.

## Architecture

```
Upload / API -> Queue -> Validation + Dedup workers -> Database
                                  |                        |
                           Quarantine table          Audit log
```

Stack (edit to match yours): Python, AWS (SQS, Lambda or containers, RDS PostgreSQL).

## Getting started

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
cp .env.example .env      # add your database credentials
python -m app.main
```

## Usage

```bash
curl -X POST http://localhost:8000/records \
  -H "Content-Type: application/json" \
  -d '{"name": "John Smith", "address": "12 Main Street", "email": "john@example.com"}'
```

Example response:

```json
{ "status": "rejected", "class": "redundant", "matched_id": 4821, "score": 0.97 }
```

## Evaluation

Tested on a synthetic dataset of 10,000 records containing exact duplicates, messy near-duplicates and look-alike non-duplicates.

| Metric | Result |
|---|---|
| Precision | _fill in_ |
| Recall | _fill in_ |
| F1 score | _fill in_ |
| Concurrency test (50 parallel identical requests) | _1 row stored_ |

Also include: a threshold-versus-accuracy graph and a confusion matrix.

## Project structure

```
app/          validation, normalization, matching, classification
db/           schema and migrations
tests/        unit, accuracy and concurrency tests
data/         sample and synthetic datasets
docs/         diagrams and report
```

## Roadmap

- Blocking/indexing to speed up fuzzy matching on very large datasets
- Reviewer dashboard for the quarantine queue
- Bloom filter pre-check for faster rejection

## License

MIT