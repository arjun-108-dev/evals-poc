# Pass^k Reliability Failures

Generated automatically by `evaluator/analyze_passk.py`. All results below are from **real** model runs via Ollama (no synthetic data).

## Model ranking (by pass^K)

| Model | Size | pass^1 | pass^K | drop | always right | inconsistent | always wrong |
|-------|------|-------:|------:|-----:|-------------:|-------------:|-------------:|
| Qwen3 0.6B | 0.6B | 94% | 86% | 8pp | 129 | 18 | 3 |
| Qwen2.5 0.5B | 0.5B | 81% | 69% | 12pp | 104 | 24 | 22 |

## Qwen3 0.6B (0.6B)

- **pass^1**: 94.0%   **pass^K** (K=8): 86.0%   drop: 8.0pp
- Consistent (always right): **129/150** (86%)
- Inconsistent (right on some trials): **18/150**
- Incapable / always wrong: **3/150** (2%)

### Always wrong (3) - failed all 8 trials
- **n072** `send_message` (multi_arg/medium)
- **n110** `none` (should_not_call/hard)
- **n112** `none` (should_not_call/hard)

### Inconsistent (18) - right on some, wrong on some trials
- **n002** `get_weather` (should_call/easy): 7/8 trials correct
- **n015** `get_weather` (should_call/medium): 5/8 trials correct
- **n020** `get_weather` (should_call/hard): 2/8 trials correct
- **n027** `search_contacts` (should_call/easy): 7/8 trials correct
- **n063** `send_message` (multi_arg/easy): 6/8 trials correct
- **n066** `send_message` (multi_arg/medium): 7/8 trials correct
- **n068** `send_message` (multi_arg/medium): 1/8 trials correct
- **n074** `send_message` (multi_arg/medium): 2/8 trials correct
- **n075** `send_message` (multi_arg/medium): 3/8 trials correct
- **n083** `none` (should_not_call/easy): 7/8 trials correct
- **n085** `none` (should_not_call/easy): 7/8 trials correct
- **n103** `none` (should_not_call/medium): 7/8 trials correct
- **n106** `none` (should_not_call/hard): 3/8 trials correct
- **n113** `none` (should_not_call/hard): 2/8 trials correct
- **n115** `none` (should_not_call/hard): 7/8 trials correct
- **n132** `send_message` (edge_case/hard): 5/8 trials correct
- **n145** `send_message` (edge_case/hard): 7/8 trials correct
- **n150** `none` (edge_case/hard): 4/8 trials correct


## Qwen2.5 0.5B (0.5B)

- **pass^1**: 81.3%   **pass^K** (K=8): 69.3%   drop: 12.0pp
- Consistent (always right): **104/150** (69%)
- Inconsistent (right on some trials): **24/150**
- Incapable / always wrong: **22/150** (15%)

### Always wrong (22) - failed all 8 trials
- **n012** `get_weather` (should_call/medium)
- **n014** `get_weather` (should_call/medium)
- **n015** `get_weather` (should_call/medium)
- **n020** `get_weather` (should_call/hard)
- **n076** `send_message` (multi_arg/hard)
- **n086** `none` (should_not_call/easy)
- **n091** `none` (should_not_call/medium)
- **n092** `none` (should_not_call/medium)
- **n093** `none` (should_not_call/medium)
- **n095** `none` (should_not_call/medium)
- **n098** `none` (should_not_call/medium)
- **n100** `none` (should_not_call/medium)
- **n108** `none` (should_not_call/hard)
- **n109** `none` (should_not_call/hard)
- **n110** `none` (should_not_call/hard)
- **n111** `none` (should_not_call/hard)
- **n112** `none` (should_not_call/hard)
- **n113** `none` (should_not_call/hard)
- **n114** `none` (should_not_call/hard)
- **n127** `get_weather` (edge_case/hard)
- **n131** `send_message` (edge_case/hard)
- **n150** `none` (edge_case/hard)

### Inconsistent (24) - right on some, wrong on some trials
- **n016** `get_weather` (should_call/medium): 7/8 trials correct
- **n018** `get_weather` (should_call/medium): 6/8 trials correct
- **n022** `search_contacts` (should_call/easy): 7/8 trials correct
- **n062** `send_message` (multi_arg/easy): 7/8 trials correct
- **n066** `send_message` (multi_arg/medium): 7/8 trials correct
- **n068** `send_message` (multi_arg/medium): 5/8 trials correct
- **n081** `none` (should_not_call/easy): 2/8 trials correct
- **n082** `none` (should_not_call/easy): 1/8 trials correct
- **n083** `none` (should_not_call/easy): 6/8 trials correct
- **n085** `none` (should_not_call/easy): 5/8 trials correct
- **n087** `none` (should_not_call/easy): 1/8 trials correct
- **n089** `none` (should_not_call/easy): 1/8 trials correct
- **n090** `none` (should_not_call/easy): 7/8 trials correct
- **n096** `none` (should_not_call/medium): 4/8 trials correct
- **n097** `none` (should_not_call/medium): 3/8 trials correct
- **n099** `none` (should_not_call/medium): 1/8 trials correct
- **n101** `none` (should_not_call/medium): 2/8 trials correct
- **n102** `none` (should_not_call/medium): 3/8 trials correct
- **n103** `none` (should_not_call/medium): 1/8 trials correct
- **n104** `none` (should_not_call/medium): 3/8 trials correct
- **n106** `none` (should_not_call/hard): 1/8 trials correct
- **n107** `none` (should_not_call/hard): 3/8 trials correct
- **n115** `none` (should_not_call/hard): 2/8 trials correct
- **n142** `set_timer` (edge_case/hard): 7/8 trials correct

