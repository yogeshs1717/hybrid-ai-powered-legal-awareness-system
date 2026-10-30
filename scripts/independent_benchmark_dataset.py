"""Independent 250-scenario testing benchmark dataset for LegalLens.

Strict 5 domains x 50 scenarios = 250 test cases.
"""

import json
from pathlib import Path

DOCS_JSON = Path(__file__).resolve().parents[1] / 'docs' / 'independent_benchmark_cases.json'
with open(DOCS_JSON, encoding='utf-8') as _f:
    BENCHMARK_250_CASES = json.load(_f)
