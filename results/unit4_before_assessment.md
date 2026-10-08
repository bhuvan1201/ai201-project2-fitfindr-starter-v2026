# Unit 4 baseline assessment

Evidence: [raw report](run_2026-10-08_004633_before.md) and [full JSON](run_2026-10-08_004633_before.json). No criteria or agent behavior were changed for this baseline. The review below was prepared with AI assistance from the recorded output; it is available for the student to inspect.

The recorder in `run_eval.py::run_once` wraps the real tool calls and copies their inputs at entry. It delegates to the actual MCP client and model tools. It does not supply fake responses. Each criterion has five trials; each state trial includes three requests.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops with guidance | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Each request keeps its own selected item | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card reports listing details correctly | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Outfit advice does not invent ownership | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

## 1. Full path

In tries 1–5, the recorded call order is search_listings (via MCP), suggest_outfit, create_fit_card. Each call returned, each session has no error, and each fit card is non-empty. This measures completion, not whether search found the best possible tee.

## 2. Empty branch

In tries 1–5, search returned [], neither later tool was called, and the returned message suggested broader search words, a different size, or a higher budget. The message is pasted in README.

## 3. State isolation

Full dictionary equality was checked against the saved JSON, not just matching IDs. For each matching request, suggest_outfit's first positional argument and create_fit_card's second positional argument equal both session.selected_item and session.search_results[0]. For each middle request, selected_item, outfit_suggestion and fit_card are null and the sole call is search.

| Try | Selected IDs in request order | Full item equality | Empty state and no later calls |
|---|---|---|---|
| 1 | lst_002 → none → lst_004 | PASS | PASS |
| 2 | lst_002 → none → lst_004 | PASS | PASS |
| 3 | lst_002 → none → lst_004 | PASS | PASS |
| 4 | lst_002 → none → lst_004 | PASS | PASS |
| 5 | lst_002 → none → lst_004 | PASS | PASS |

## 4. Caption facts — manual review

| Try | Selected item | Expected price/platform | Review |
|---|---|---|---|
| 1 | lst_002, butterfly baby tee | $18 / depop | Identifies the tee and gives both facts correctly. |
| 2 | lst_004, 90s track jacket | $45 / poshmark | Identifies the jacket and gives both facts correctly. |
| 3 | lst_005, corduroy wide-leg pants | $32 / depop | Identifies the pants and gives both facts correctly. |
| 4 | lst_019, platform sneakers | $48 / poshmark | Gives both facts; white chunky soles and Velcro straps match the source. |
| 5 | lst_007, cropped light-wash denim jacket | $42 / poshmark | Gives both facts; Wrangler, cropped light wash and structured shoulders match. |

All five outfit suggestions and captions are non-empty. Title rewording, service capitalization and equivalent numeric price formatting are allowed by the original criterion. No stated selected-item detail contradicts the source.

## 5. Ownership — manual review

| Try | Supplied wardrobe | Review |
|---|---|---|
| 1 | All ten example items | Chosen wardrobe pieces exist. Necklace and baseball cap are marked suggested additions. |
| 2 | All ten example items | Chosen wardrobe pieces exist. The extra white t-shirt is an optional addition. |
| 3 | Only w_001 jeans | Uses those jeans; white sneakers are a Suggested Addition. |
| 4 | Only w_001 jeans | Uses those jeans; white canvas sneakers are a Suggested Addition. |
| 5 | Empty | Gives general combinations using Pair, Add and Layer; does not claim those clothes are already owned. |

All five responses contain styling advice. The selected jacket is supplied separately and does not count as invented wardrobe ownership.

## Limits of this result

These are passes on the chosen cases, not proof of general reliability. The same small data set and familiar phrases were used. Criteria 1–3 mostly test completion and deterministic control flow; they do not require the highest-ranked listing to be the best interpretation of a user's request. Broader diagnosis and any proposed improvement belong in Milestone 4, after reviewing this baseline.
