# Unit 4 after assessment

Evidence: [after report](run_2026-10-10_151811_after.md) and [after JSON](run_2026-10-10_151811_after.json). This review was prepared with AI assistance from the saved output and is available for the student to inspect.

The only agent behavior change is the clothing-type filter in `tools.py::search_listings`. Comparison of the saved before and after records confirms the same scenario definitions, queries, wardrobes and selected listing dictionaries. Caching was off; all 25 trials and 35 requests completed without crashes.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops with guidance | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Each request keeps its own selected item | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card reports listing details correctly | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Outfit advice does not invent ownership | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

## Control flow and state

- Criterion 1: all five requests called MCP search, suggest_outfit and create_fit_card successfully, and returned non-empty cards.
- Criterion 2: all five requests recorded only MCP search, with empty results and a message naming words, size and budget as things to change.
- Criterion 3: all five sequences selected lst_002 → none → lst_004. For each matching request, the actual full item inputs to both later tools equal the session's selected item and first result. Every empty request left selected_item, outfit_suggestion and fit_card null and called neither later tool. The comparisons used complete dictionaries, not only IDs.

## Criterion 4 — manual caption review

| Try | Selected item | Caption facts checked | Result |
|---|---|---|---|
| 1 | lst_002 butterfly baby tee | Identifies the tee, $18.0, depop | PASS |
| 2 | lst_004 track jacket | Identifies the jacket, $45.00, Poshmark; lightweight/layering matches source | PASS |
| 3 | lst_005 corduroy wide-leg pants | Identifies the pants, $32.0, Depop | PASS |
| 4 | lst_019 platform sneakers | Identifies white chunky platform sneakers, $48.0, poshmark | PASS |
| 5 | lst_007 denim jacket | Identifies the Wrangler denim jacket, $42.0, Poshmark; vintage matches its style tags | PASS |

All five outfit suggestions and captions are non-empty. None of the selected-item details stated in these captions contradict the listing. Equivalent price formatting and platform capitalization are allowed by the original criterion.

## Criterion 5 — manual ownership review

| Try | Wardrobe | Review | Result |
|---|---|---|---|
| 1 | Full example | All referenced owned pieces are present; the silver necklace is labeled Addition in an outfit suggestion, not described as owned. | PASS |
| 2 | Full example | Wardrobe Pieces lists supplied items; the silver necklace is a Suggested Addition. | PASS |
| 3 | Only w_001 jeans | Your jeans refers to the supplied jeans; white leather sneakers are a Suggested addition. | PASS |
| 4 | Only w_001 jeans | Uses the supplied jeans; white leather sneakers are a Suggested Addition. | PASS |
| 5 | Empty | Both combinations use Add to introduce new pieces; no ownership claims. | PASS |

These are judgments about ownership, not an automatic match of exact phrases. In try 1, Addition is less explicit than Suggested Addition, but it appears as advice and does not claim the necklace is in the wardrobe. All five responses contain styling advice.

## Comparison

Each original criterion scored 5/5 both before and after. The measured benefit is instead in the [fixed supplementary search test](search_type_comparison.md): 0/5 to 5/5, with 21 wrong-type occurrences reduced to zero and all previously returned valid items preserved. Model wording varies between runs, but these results do not establish a model-quality improvement or universal reliability.
