### Run Log — After

Three formal trials with unchanged code and criteria. Criteria 1, 3 and 4 share each trial's five measured outfit requests; the one warm-up attempt is excluded. Criterion 2 uses five hosted health requests per trial. Criterion 5 uses ten health requests per trial in an isolated local instance with an invalid log destination.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Hosted completion | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Recoverable health logs | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Response within 45 seconds | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Completed output and reported usage | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Visible logging failure | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

These counts check the stated response/log conditions; they do not judge outfit quality or establish accurate API billing.

**Criterion 1 — real output:** agent.py::run_agent, returned over HTTP by serve.py::ask.

```json
{
  "slot": 1,
  "passed": true,
  "client_response": {
    "timestamp": "2026-11-15T20:41:16.477387+00:00",
    "method": "POST",
    "url": "https://fitfindr-capstone.vercel.app/ask",
    "input": {
      "query": "90s track jacket in size M"
    },
    "http_status": 200,
    "response": {
      "error": null,
      "fit_card": "I am obsessed with this Champion 90s Track Jacket I found on Poshmark for $45.0! I styled it for a casual streetwear vibe using a white ribbed tank top, baggy dark wash straight-leg jeans, and chunky white sneakers.",
      "outfit_suggestion": "Here are two outfit suggestions using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers\n* **Why it works:** The white tank pairs effortlessly with the white sleeve stripes, while the baggy dark wash jeans and chunky sneakers lean into the 90s streetwear aesthetic of the jacket. \n\n**Outfit 2: Sporty Smart-Casual**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n* **Why it works:** Pairing the athletic navy-and-white jacket with tailored khaki trousers creates a high-low mix. The fitted white tank keeps the silhouette balanced against the wide-leg pants. *(Optional addition: A minimal silver chain necklace to tie the look together).*",
      "parsed": {
        "description": "90s track jacket in",
        "max_price": null,
        "size": "M"
      },
      "query": "90s track jacket in size M",
      "search_results": [
        {
          "brand": "Champion",
          "category": "outerwear",
          "colors": [
            "navy",
            "white"
          ],
          "condition": "excellent",
          "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
          "id": "lst_004",
          "platform": "poshmark",
          "price": 45.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "athletic",
            "streetwear"
          ],
          "title": "90s Track Jacket — Navy/White Stripe"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "black"
          ],
          "condition": "good",
          "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.",
          "id": "lst_022",
          "platform": "depop",
          "price": 75.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "leather",
            "classic",
            "grunge"
          ],
          "title": "90s Leather Bomber — Black"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "olive",
            "green"
          ],
          "condition": "excellent",
          "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.",
          "id": "lst_032",
          "platform": "poshmark",
          "price": 33.0,
          "size": "M/L",
          "style_tags": [
            "earth tones",
            "classic",
            "layering",
            "minimal"
          ],
          "title": "Shacket — Olive Canvas"
        }
      ],
      "selected_item": {
        "brand": "Champion",
        "category": "outerwear",
        "colors": [
          "navy",
          "white"
        ],
        "condition": "excellent",
        "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
        "id": "lst_004",
        "platform": "poshmark",
        "price": 45.0,
        "size": "M",
        "style_tags": [
          "90s",
          "vintage",
          "athletic",
          "streetwear"
        ],
        "title": "90s Track Jacket — Navy/White Stripe"
      },
      "wardrobe": {
        "items": [
          {
            "category": "bottoms",
            "colors": [
              "dark blue",
              "indigo"
            ],
            "id": "w_001",
            "name": "Baggy straight-leg jeans, dark wash",
            "notes": "High-waisted, sits above the hip",
            "style_tags": [
              "denim",
              "streetwear",
              "baggy"
            ]
          },
          {
            "category": "bottoms",
            "colors": [
              "khaki",
              "tan"
            ],
            "id": "w_002",
            "name": "Wide-leg khaki trousers",
            "notes": null,
            "style_tags": [
              "earth tones",
              "minimal",
              "wide-leg"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "white"
            ],
            "id": "w_003",
            "name": "White ribbed tank top",
            "notes": "Goes with everything",
            "style_tags": [
              "basics",
              "minimal",
              "fitted"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "grey",
              "charcoal"
            ],
            "id": "w_004",
            "name": "Oversized grey crewneck sweatshirt",
            "notes": "Really oversized — drops below the hip",
            "style_tags": [
              "oversized",
              "basics",
              "cozy"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "black"
            ],
            "id": "w_005",
            "name": "Black cropped zip hoodie",
            "notes": null,
            "style_tags": [
              "athletic",
              "streetwear",
              "cropped"
            ]
          },
          {
            "category": "outerwear",
            "colors": [
              "black"
            ],
            "id": "w_006",
            "name": "Vintage black denim jacket",
            "notes": "Slightly cropped",
            "style_tags": [
              "denim",
              "vintage",
              "classic"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "white"
            ],
            "id": "w_007",
            "name": "Chunky white sneakers",
            "notes": null,
            "style_tags": [
              "sneakers",
              "chunky",
              "streetwear"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "black"
            ],
            "id": "w_008",
            "name": "Black combat boots",
            "notes": "Lace-up, mid-ankle height",
            "style_tags": [
              "boots",
              "grunge",
              "classic"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "brown"
            ],
            "id": "w_009",
            "name": "Brown leather belt",
            "notes": null,
            "style_tags": [
              "classic",
              "earth tones",
              "accessories"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "black"
            ],
            "id": "w_010",
            "name": "Black crossbody bag",
            "notes": null,
            "style_tags": [
              "minimal",
              "accessories",
              "everyday"
            ]
          }
        ]
      }
    },
    "client_elapsed_ms": 2815.629,
    "request_id": "0c27498ecba24063a49160b75fc69bad",
    "run_log": "saved",
    "transport_error": null,
    "trial": 1,
    "kind": "ask",
    "slot": 1
  },
  "application_record": {
    "timestamp": "2026-11-15T20:41:16.689+00:00",
    "request_id": "0c27498ecba24063a49160b75fc69bad",
    "method": "POST",
    "path": "/ask",
    "input_format": "json",
    "input": {
      "query": "90s track jacket in size M"
    },
    "output_format": "json",
    "output": {
      "error": null,
      "fit_card": "I am obsessed with this Champion 90s Track Jacket I found on Poshmark for $45.0! I styled it for a casual streetwear vibe using a white ribbed tank top, baggy dark wash straight-leg jeans, and chunky white sneakers.",
      "outfit_suggestion": "Here are two outfit suggestions using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers\n* **Why it works:** The white tank pairs effortlessly with the white sleeve stripes, while the baggy dark wash jeans and chunky sneakers lean into the 90s streetwear aesthetic of the jacket. \n\n**Outfit 2: Sporty Smart-Casual**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n* **Why it works:** Pairing the athletic navy-and-white jacket with tailored khaki trousers creates a high-low mix. The fitted white tank keeps the silhouette balanced against the wide-leg pants. *(Optional addition: A minimal silver chain necklace to tie the look together).*",
      "parsed": {
        "description": "90s track jacket in",
        "max_price": null,
        "size": "M"
      },
      "query": "90s track jacket in size M",
      "search_results": [
        {
          "brand": "Champion",
          "category": "outerwear",
          "colors": [
            "navy",
            "white"
          ],
          "condition": "excellent",
          "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
          "id": "lst_004",
          "platform": "poshmark",
          "price": 45.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "athletic",
            "streetwear"
          ],
          "title": "90s Track Jacket — Navy/White Stripe"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "black"
          ],
          "condition": "good",
          "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.",
          "id": "lst_022",
          "platform": "depop",
          "price": 75.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "leather",
            "classic",
            "grunge"
          ],
          "title": "90s Leather Bomber — Black"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "olive",
            "green"
          ],
          "condition": "excellent",
          "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.",
          "id": "lst_032",
          "platform": "poshmark",
          "price": 33.0,
          "size": "M/L",
          "style_tags": [
            "earth tones",
            "classic",
            "layering",
            "minimal"
          ],
          "title": "Shacket — Olive Canvas"
        }
      ],
      "selected_item": {
        "brand": "Champion",
        "category": "outerwear",
        "colors": [
          "navy",
          "white"
        ],
        "condition": "excellent",
        "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
        "id": "lst_004",
        "platform": "poshmark",
        "price": 45.0,
        "size": "M",
        "style_tags": [
          "90s",
          "vintage",
          "athletic",
          "streetwear"
        ],
        "title": "90s Track Jacket — Navy/White Stripe"
      },
      "wardrobe": {
        "items": [
          {
            "category": "bottoms",
            "colors": [
              "dark blue",
              "indigo"
            ],
            "id": "w_001",
            "name": "Baggy straight-leg jeans, dark wash",
            "notes": "High-waisted, sits above the hip",
            "style_tags": [
              "denim",
              "streetwear",
              "baggy"
            ]
          },
          {
            "category": "bottoms",
            "colors": [
              "khaki",
              "tan"
            ],
            "id": "w_002",
            "name": "Wide-leg khaki trousers",
            "notes": null,
            "style_tags": [
              "earth tones",
              "minimal",
              "wide-leg"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "white"
            ],
            "id": "w_003",
            "name": "White ribbed tank top",
            "notes": "Goes with everything",
            "style_tags": [
              "basics",
              "minimal",
              "fitted"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "grey",
              "charcoal"
            ],
            "id": "w_004",
            "name": "Oversized grey crewneck sweatshirt",
            "notes": "Really oversized — drops below the hip",
            "style_tags": [
              "oversized",
              "basics",
              "cozy"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "black"
            ],
            "id": "w_005",
            "name": "Black cropped zip hoodie",
            "notes": null,
            "style_tags": [
              "athletic",
              "streetwear",
              "cropped"
            ]
          },
          {
            "category": "outerwear",
            "colors": [
              "black"
            ],
            "id": "w_006",
            "name": "Vintage black denim jacket",
            "notes": "Slightly cropped",
            "style_tags": [
              "denim",
              "vintage",
              "classic"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "white"
            ],
            "id": "w_007",
            "name": "Chunky white sneakers",
            "notes": null,
            "style_tags": [
              "sneakers",
              "chunky",
              "streetwear"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "black"
            ],
            "id": "w_008",
            "name": "Black combat boots",
            "notes": "Lace-up, mid-ankle height",
            "style_tags": [
              "boots",
              "grunge",
              "classic"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "brown"
            ],
            "id": "w_009",
            "name": "Brown leather belt",
            "notes": null,
            "style_tags": [
              "classic",
              "earth tones",
              "accessories"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "black"
            ],
            "id": "w_010",
            "name": "Black crossbody bag",
            "notes": null,
            "style_tags": [
              "minimal",
              "accessories",
              "everyday"
            ]
          }
        ]
      }
    },
    "status_code": 200,
    "outcome": "success",
    "error": null,
    "duration_ms": 2593.068,
    "queue_ms": 0.001,
    "agent_ms": 2592.371,
    "configured_model": "gemini-3.5-flash-lite",
    "cache_enabled": false,
    "model_usage": {
      "model_attempts": 2,
      "reported_prompt_tokens": 1121,
      "reported_output_tokens": 242,
      "reported_total_tokens": 1363
    }
  }
}
```

**Criterion 2 — real output:** serve.py::finish_request_record and run_log.py::append_record, recovered from Vercel runtime logs.

```json
{
  "slot": 1,
  "passed": true,
  "client_response": {
    "timestamp": "2026-11-15T20:42:10.477385+00:00",
    "method": "GET",
    "url": "https://fitfindr-capstone.vercel.app/health",
    "input": null,
    "http_status": 200,
    "response": {
      "status": "ok"
    },
    "client_elapsed_ms": 197.899,
    "request_id": "e1e94c0a0bc144d393f37d233d07ccb4",
    "run_log": "saved",
    "transport_error": null,
    "trial": 1,
    "kind": "health",
    "slot": 1
  },
  "application_record": {
    "timestamp": "2026-11-15T20:42:10.654+00:00",
    "request_id": "e1e94c0a0bc144d393f37d233d07ccb4",
    "method": "GET",
    "path": "/health",
    "input_format": "empty",
    "input": null,
    "output_format": "json",
    "output": {
      "status": "ok"
    },
    "status_code": 200,
    "outcome": "success",
    "error": null,
    "duration_ms": 0.262,
    "queue_ms": 0.0,
    "agent_ms": 0.0,
    "configured_model": "gemini-3.5-flash-lite",
    "cache_enabled": false,
    "model_usage": {
      "model_attempts": 0,
      "reported_prompt_tokens": 0,
      "reported_output_tokens": 0,
      "reported_total_tokens": 0
    }
  }
}
```

**Criterion 3 — real output:** tools/measure_capstone.py::request_once (monotonic client elapsed time).

```json
{
  "slot": 1,
  "passed": true,
  "client_response": {
    "timestamp": "2026-11-15T20:41:16.477387+00:00",
    "method": "POST",
    "url": "https://fitfindr-capstone.vercel.app/ask",
    "input": {
      "query": "90s track jacket in size M"
    },
    "http_status": 200,
    "response": {
      "error": null,
      "fit_card": "I am obsessed with this Champion 90s Track Jacket I found on Poshmark for $45.0! I styled it for a casual streetwear vibe using a white ribbed tank top, baggy dark wash straight-leg jeans, and chunky white sneakers.",
      "outfit_suggestion": "Here are two outfit suggestions using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers\n* **Why it works:** The white tank pairs effortlessly with the white sleeve stripes, while the baggy dark wash jeans and chunky sneakers lean into the 90s streetwear aesthetic of the jacket. \n\n**Outfit 2: Sporty Smart-Casual**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n* **Why it works:** Pairing the athletic navy-and-white jacket with tailored khaki trousers creates a high-low mix. The fitted white tank keeps the silhouette balanced against the wide-leg pants. *(Optional addition: A minimal silver chain necklace to tie the look together).*",
      "parsed": {
        "description": "90s track jacket in",
        "max_price": null,
        "size": "M"
      },
      "query": "90s track jacket in size M",
      "search_results": [
        {
          "brand": "Champion",
          "category": "outerwear",
          "colors": [
            "navy",
            "white"
          ],
          "condition": "excellent",
          "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
          "id": "lst_004",
          "platform": "poshmark",
          "price": 45.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "athletic",
            "streetwear"
          ],
          "title": "90s Track Jacket — Navy/White Stripe"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "black"
          ],
          "condition": "good",
          "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.",
          "id": "lst_022",
          "platform": "depop",
          "price": 75.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "leather",
            "classic",
            "grunge"
          ],
          "title": "90s Leather Bomber — Black"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "olive",
            "green"
          ],
          "condition": "excellent",
          "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.",
          "id": "lst_032",
          "platform": "poshmark",
          "price": 33.0,
          "size": "M/L",
          "style_tags": [
            "earth tones",
            "classic",
            "layering",
            "minimal"
          ],
          "title": "Shacket — Olive Canvas"
        }
      ],
      "selected_item": {
        "brand": "Champion",
        "category": "outerwear",
        "colors": [
          "navy",
          "white"
        ],
        "condition": "excellent",
        "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
        "id": "lst_004",
        "platform": "poshmark",
        "price": 45.0,
        "size": "M",
        "style_tags": [
          "90s",
          "vintage",
          "athletic",
          "streetwear"
        ],
        "title": "90s Track Jacket — Navy/White Stripe"
      },
      "wardrobe": {
        "items": [
          {
            "category": "bottoms",
            "colors": [
              "dark blue",
              "indigo"
            ],
            "id": "w_001",
            "name": "Baggy straight-leg jeans, dark wash",
            "notes": "High-waisted, sits above the hip",
            "style_tags": [
              "denim",
              "streetwear",
              "baggy"
            ]
          },
          {
            "category": "bottoms",
            "colors": [
              "khaki",
              "tan"
            ],
            "id": "w_002",
            "name": "Wide-leg khaki trousers",
            "notes": null,
            "style_tags": [
              "earth tones",
              "minimal",
              "wide-leg"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "white"
            ],
            "id": "w_003",
            "name": "White ribbed tank top",
            "notes": "Goes with everything",
            "style_tags": [
              "basics",
              "minimal",
              "fitted"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "grey",
              "charcoal"
            ],
            "id": "w_004",
            "name": "Oversized grey crewneck sweatshirt",
            "notes": "Really oversized — drops below the hip",
            "style_tags": [
              "oversized",
              "basics",
              "cozy"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "black"
            ],
            "id": "w_005",
            "name": "Black cropped zip hoodie",
            "notes": null,
            "style_tags": [
              "athletic",
              "streetwear",
              "cropped"
            ]
          },
          {
            "category": "outerwear",
            "colors": [
              "black"
            ],
            "id": "w_006",
            "name": "Vintage black denim jacket",
            "notes": "Slightly cropped",
            "style_tags": [
              "denim",
              "vintage",
              "classic"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "white"
            ],
            "id": "w_007",
            "name": "Chunky white sneakers",
            "notes": null,
            "style_tags": [
              "sneakers",
              "chunky",
              "streetwear"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "black"
            ],
            "id": "w_008",
            "name": "Black combat boots",
            "notes": "Lace-up, mid-ankle height",
            "style_tags": [
              "boots",
              "grunge",
              "classic"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "brown"
            ],
            "id": "w_009",
            "name": "Brown leather belt",
            "notes": null,
            "style_tags": [
              "classic",
              "earth tones",
              "accessories"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "black"
            ],
            "id": "w_010",
            "name": "Black crossbody bag",
            "notes": null,
            "style_tags": [
              "minimal",
              "accessories",
              "everyday"
            ]
          }
        ]
      }
    },
    "client_elapsed_ms": 2815.629,
    "request_id": "0c27498ecba24063a49160b75fc69bad",
    "run_log": "saved",
    "transport_error": null,
    "trial": 1,
    "kind": "ask",
    "slot": 1
  },
  "application_record": {
    "timestamp": "2026-11-15T20:41:16.689+00:00",
    "request_id": "0c27498ecba24063a49160b75fc69bad",
    "method": "POST",
    "path": "/ask",
    "input_format": "json",
    "input": {
      "query": "90s track jacket in size M"
    },
    "output_format": "json",
    "output": {
      "error": null,
      "fit_card": "I am obsessed with this Champion 90s Track Jacket I found on Poshmark for $45.0! I styled it for a casual streetwear vibe using a white ribbed tank top, baggy dark wash straight-leg jeans, and chunky white sneakers.",
      "outfit_suggestion": "Here are two outfit suggestions using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers\n* **Why it works:** The white tank pairs effortlessly with the white sleeve stripes, while the baggy dark wash jeans and chunky sneakers lean into the 90s streetwear aesthetic of the jacket. \n\n**Outfit 2: Sporty Smart-Casual**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n* **Why it works:** Pairing the athletic navy-and-white jacket with tailored khaki trousers creates a high-low mix. The fitted white tank keeps the silhouette balanced against the wide-leg pants. *(Optional addition: A minimal silver chain necklace to tie the look together).*",
      "parsed": {
        "description": "90s track jacket in",
        "max_price": null,
        "size": "M"
      },
      "query": "90s track jacket in size M",
      "search_results": [
        {
          "brand": "Champion",
          "category": "outerwear",
          "colors": [
            "navy",
            "white"
          ],
          "condition": "excellent",
          "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
          "id": "lst_004",
          "platform": "poshmark",
          "price": 45.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "athletic",
            "streetwear"
          ],
          "title": "90s Track Jacket — Navy/White Stripe"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "black"
          ],
          "condition": "good",
          "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.",
          "id": "lst_022",
          "platform": "depop",
          "price": 75.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "leather",
            "classic",
            "grunge"
          ],
          "title": "90s Leather Bomber — Black"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "olive",
            "green"
          ],
          "condition": "excellent",
          "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.",
          "id": "lst_032",
          "platform": "poshmark",
          "price": 33.0,
          "size": "M/L",
          "style_tags": [
            "earth tones",
            "classic",
            "layering",
            "minimal"
          ],
          "title": "Shacket — Olive Canvas"
        }
      ],
      "selected_item": {
        "brand": "Champion",
        "category": "outerwear",
        "colors": [
          "navy",
          "white"
        ],
        "condition": "excellent",
        "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
        "id": "lst_004",
        "platform": "poshmark",
        "price": 45.0,
        "size": "M",
        "style_tags": [
          "90s",
          "vintage",
          "athletic",
          "streetwear"
        ],
        "title": "90s Track Jacket — Navy/White Stripe"
      },
      "wardrobe": {
        "items": [
          {
            "category": "bottoms",
            "colors": [
              "dark blue",
              "indigo"
            ],
            "id": "w_001",
            "name": "Baggy straight-leg jeans, dark wash",
            "notes": "High-waisted, sits above the hip",
            "style_tags": [
              "denim",
              "streetwear",
              "baggy"
            ]
          },
          {
            "category": "bottoms",
            "colors": [
              "khaki",
              "tan"
            ],
            "id": "w_002",
            "name": "Wide-leg khaki trousers",
            "notes": null,
            "style_tags": [
              "earth tones",
              "minimal",
              "wide-leg"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "white"
            ],
            "id": "w_003",
            "name": "White ribbed tank top",
            "notes": "Goes with everything",
            "style_tags": [
              "basics",
              "minimal",
              "fitted"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "grey",
              "charcoal"
            ],
            "id": "w_004",
            "name": "Oversized grey crewneck sweatshirt",
            "notes": "Really oversized — drops below the hip",
            "style_tags": [
              "oversized",
              "basics",
              "cozy"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "black"
            ],
            "id": "w_005",
            "name": "Black cropped zip hoodie",
            "notes": null,
            "style_tags": [
              "athletic",
              "streetwear",
              "cropped"
            ]
          },
          {
            "category": "outerwear",
            "colors": [
              "black"
            ],
            "id": "w_006",
            "name": "Vintage black denim jacket",
            "notes": "Slightly cropped",
            "style_tags": [
              "denim",
              "vintage",
              "classic"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "white"
            ],
            "id": "w_007",
            "name": "Chunky white sneakers",
            "notes": null,
            "style_tags": [
              "sneakers",
              "chunky",
              "streetwear"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "black"
            ],
            "id": "w_008",
            "name": "Black combat boots",
            "notes": "Lace-up, mid-ankle height",
            "style_tags": [
              "boots",
              "grunge",
              "classic"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "brown"
            ],
            "id": "w_009",
            "name": "Brown leather belt",
            "notes": null,
            "style_tags": [
              "classic",
              "earth tones",
              "accessories"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "black"
            ],
            "id": "w_010",
            "name": "Black crossbody bag",
            "notes": null,
            "style_tags": [
              "minimal",
              "accessories",
              "everyday"
            ]
          }
        ]
      }
    },
    "status_code": 200,
    "outcome": "success",
    "error": null,
    "duration_ms": 2593.068,
    "queue_ms": 0.001,
    "agent_ms": 2592.371,
    "configured_model": "gemini-3.5-flash-lite",
    "cache_enabled": false,
    "model_usage": {
      "model_attempts": 2,
      "reported_prompt_tokens": 1121,
      "reported_output_tokens": 242,
      "reported_total_tokens": 1363
    }
  }
}
```

**Criterion 4 — real output:** serve.py::model_usage_snapshot and serve.py::finish_request_record.

```json
{
  "slot": 1,
  "passed": true,
  "client_response": {
    "timestamp": "2026-11-15T20:41:16.477387+00:00",
    "method": "POST",
    "url": "https://fitfindr-capstone.vercel.app/ask",
    "input": {
      "query": "90s track jacket in size M"
    },
    "http_status": 200,
    "response": {
      "error": null,
      "fit_card": "I am obsessed with this Champion 90s Track Jacket I found on Poshmark for $45.0! I styled it for a casual streetwear vibe using a white ribbed tank top, baggy dark wash straight-leg jeans, and chunky white sneakers.",
      "outfit_suggestion": "Here are two outfit suggestions using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers\n* **Why it works:** The white tank pairs effortlessly with the white sleeve stripes, while the baggy dark wash jeans and chunky sneakers lean into the 90s streetwear aesthetic of the jacket. \n\n**Outfit 2: Sporty Smart-Casual**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n* **Why it works:** Pairing the athletic navy-and-white jacket with tailored khaki trousers creates a high-low mix. The fitted white tank keeps the silhouette balanced against the wide-leg pants. *(Optional addition: A minimal silver chain necklace to tie the look together).*",
      "parsed": {
        "description": "90s track jacket in",
        "max_price": null,
        "size": "M"
      },
      "query": "90s track jacket in size M",
      "search_results": [
        {
          "brand": "Champion",
          "category": "outerwear",
          "colors": [
            "navy",
            "white"
          ],
          "condition": "excellent",
          "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
          "id": "lst_004",
          "platform": "poshmark",
          "price": 45.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "athletic",
            "streetwear"
          ],
          "title": "90s Track Jacket — Navy/White Stripe"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "black"
          ],
          "condition": "good",
          "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.",
          "id": "lst_022",
          "platform": "depop",
          "price": 75.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "leather",
            "classic",
            "grunge"
          ],
          "title": "90s Leather Bomber — Black"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "olive",
            "green"
          ],
          "condition": "excellent",
          "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.",
          "id": "lst_032",
          "platform": "poshmark",
          "price": 33.0,
          "size": "M/L",
          "style_tags": [
            "earth tones",
            "classic",
            "layering",
            "minimal"
          ],
          "title": "Shacket — Olive Canvas"
        }
      ],
      "selected_item": {
        "brand": "Champion",
        "category": "outerwear",
        "colors": [
          "navy",
          "white"
        ],
        "condition": "excellent",
        "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
        "id": "lst_004",
        "platform": "poshmark",
        "price": 45.0,
        "size": "M",
        "style_tags": [
          "90s",
          "vintage",
          "athletic",
          "streetwear"
        ],
        "title": "90s Track Jacket — Navy/White Stripe"
      },
      "wardrobe": {
        "items": [
          {
            "category": "bottoms",
            "colors": [
              "dark blue",
              "indigo"
            ],
            "id": "w_001",
            "name": "Baggy straight-leg jeans, dark wash",
            "notes": "High-waisted, sits above the hip",
            "style_tags": [
              "denim",
              "streetwear",
              "baggy"
            ]
          },
          {
            "category": "bottoms",
            "colors": [
              "khaki",
              "tan"
            ],
            "id": "w_002",
            "name": "Wide-leg khaki trousers",
            "notes": null,
            "style_tags": [
              "earth tones",
              "minimal",
              "wide-leg"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "white"
            ],
            "id": "w_003",
            "name": "White ribbed tank top",
            "notes": "Goes with everything",
            "style_tags": [
              "basics",
              "minimal",
              "fitted"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "grey",
              "charcoal"
            ],
            "id": "w_004",
            "name": "Oversized grey crewneck sweatshirt",
            "notes": "Really oversized — drops below the hip",
            "style_tags": [
              "oversized",
              "basics",
              "cozy"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "black"
            ],
            "id": "w_005",
            "name": "Black cropped zip hoodie",
            "notes": null,
            "style_tags": [
              "athletic",
              "streetwear",
              "cropped"
            ]
          },
          {
            "category": "outerwear",
            "colors": [
              "black"
            ],
            "id": "w_006",
            "name": "Vintage black denim jacket",
            "notes": "Slightly cropped",
            "style_tags": [
              "denim",
              "vintage",
              "classic"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "white"
            ],
            "id": "w_007",
            "name": "Chunky white sneakers",
            "notes": null,
            "style_tags": [
              "sneakers",
              "chunky",
              "streetwear"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "black"
            ],
            "id": "w_008",
            "name": "Black combat boots",
            "notes": "Lace-up, mid-ankle height",
            "style_tags": [
              "boots",
              "grunge",
              "classic"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "brown"
            ],
            "id": "w_009",
            "name": "Brown leather belt",
            "notes": null,
            "style_tags": [
              "classic",
              "earth tones",
              "accessories"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "black"
            ],
            "id": "w_010",
            "name": "Black crossbody bag",
            "notes": null,
            "style_tags": [
              "minimal",
              "accessories",
              "everyday"
            ]
          }
        ]
      }
    },
    "client_elapsed_ms": 2815.629,
    "request_id": "0c27498ecba24063a49160b75fc69bad",
    "run_log": "saved",
    "transport_error": null,
    "trial": 1,
    "kind": "ask",
    "slot": 1
  },
  "application_record": {
    "timestamp": "2026-11-15T20:41:16.689+00:00",
    "request_id": "0c27498ecba24063a49160b75fc69bad",
    "method": "POST",
    "path": "/ask",
    "input_format": "json",
    "input": {
      "query": "90s track jacket in size M"
    },
    "output_format": "json",
    "output": {
      "error": null,
      "fit_card": "I am obsessed with this Champion 90s Track Jacket I found on Poshmark for $45.0! I styled it for a casual streetwear vibe using a white ribbed tank top, baggy dark wash straight-leg jeans, and chunky white sneakers.",
      "outfit_suggestion": "Here are two outfit suggestions using your new track jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers\n* **Why it works:** The white tank pairs effortlessly with the white sleeve stripes, while the baggy dark wash jeans and chunky sneakers lean into the 90s streetwear aesthetic of the jacket. \n\n**Outfit 2: Sporty Smart-Casual**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n* **Why it works:** Pairing the athletic navy-and-white jacket with tailored khaki trousers creates a high-low mix. The fitted white tank keeps the silhouette balanced against the wide-leg pants. *(Optional addition: A minimal silver chain necklace to tie the look together).*",
      "parsed": {
        "description": "90s track jacket in",
        "max_price": null,
        "size": "M"
      },
      "query": "90s track jacket in size M",
      "search_results": [
        {
          "brand": "Champion",
          "category": "outerwear",
          "colors": [
            "navy",
            "white"
          ],
          "condition": "excellent",
          "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
          "id": "lst_004",
          "platform": "poshmark",
          "price": 45.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "athletic",
            "streetwear"
          ],
          "title": "90s Track Jacket — Navy/White Stripe"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "black"
          ],
          "condition": "good",
          "description": "Genuine leather bomber jacket. Classic 90s silhouette, slightly boxy. Ribbed collar, cuffs, and hem. Some creasing from age — adds character.",
          "id": "lst_022",
          "platform": "depop",
          "price": 75.0,
          "size": "M",
          "style_tags": [
            "90s",
            "vintage",
            "leather",
            "classic",
            "grunge"
          ],
          "title": "90s Leather Bomber — Black"
        },
        {
          "brand": null,
          "category": "outerwear",
          "colors": [
            "olive",
            "green"
          ],
          "condition": "excellent",
          "description": "Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.",
          "id": "lst_032",
          "platform": "poshmark",
          "price": 33.0,
          "size": "M/L",
          "style_tags": [
            "earth tones",
            "classic",
            "layering",
            "minimal"
          ],
          "title": "Shacket — Olive Canvas"
        }
      ],
      "selected_item": {
        "brand": "Champion",
        "category": "outerwear",
        "colors": [
          "navy",
          "white"
        ],
        "condition": "excellent",
        "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.",
        "id": "lst_004",
        "platform": "poshmark",
        "price": 45.0,
        "size": "M",
        "style_tags": [
          "90s",
          "vintage",
          "athletic",
          "streetwear"
        ],
        "title": "90s Track Jacket — Navy/White Stripe"
      },
      "wardrobe": {
        "items": [
          {
            "category": "bottoms",
            "colors": [
              "dark blue",
              "indigo"
            ],
            "id": "w_001",
            "name": "Baggy straight-leg jeans, dark wash",
            "notes": "High-waisted, sits above the hip",
            "style_tags": [
              "denim",
              "streetwear",
              "baggy"
            ]
          },
          {
            "category": "bottoms",
            "colors": [
              "khaki",
              "tan"
            ],
            "id": "w_002",
            "name": "Wide-leg khaki trousers",
            "notes": null,
            "style_tags": [
              "earth tones",
              "minimal",
              "wide-leg"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "white"
            ],
            "id": "w_003",
            "name": "White ribbed tank top",
            "notes": "Goes with everything",
            "style_tags": [
              "basics",
              "minimal",
              "fitted"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "grey",
              "charcoal"
            ],
            "id": "w_004",
            "name": "Oversized grey crewneck sweatshirt",
            "notes": "Really oversized — drops below the hip",
            "style_tags": [
              "oversized",
              "basics",
              "cozy"
            ]
          },
          {
            "category": "tops",
            "colors": [
              "black"
            ],
            "id": "w_005",
            "name": "Black cropped zip hoodie",
            "notes": null,
            "style_tags": [
              "athletic",
              "streetwear",
              "cropped"
            ]
          },
          {
            "category": "outerwear",
            "colors": [
              "black"
            ],
            "id": "w_006",
            "name": "Vintage black denim jacket",
            "notes": "Slightly cropped",
            "style_tags": [
              "denim",
              "vintage",
              "classic"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "white"
            ],
            "id": "w_007",
            "name": "Chunky white sneakers",
            "notes": null,
            "style_tags": [
              "sneakers",
              "chunky",
              "streetwear"
            ]
          },
          {
            "category": "shoes",
            "colors": [
              "black"
            ],
            "id": "w_008",
            "name": "Black combat boots",
            "notes": "Lace-up, mid-ankle height",
            "style_tags": [
              "boots",
              "grunge",
              "classic"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "brown"
            ],
            "id": "w_009",
            "name": "Brown leather belt",
            "notes": null,
            "style_tags": [
              "classic",
              "earth tones",
              "accessories"
            ]
          },
          {
            "category": "accessories",
            "colors": [
              "black"
            ],
            "id": "w_010",
            "name": "Black crossbody bag",
            "notes": null,
            "style_tags": [
              "minimal",
              "accessories",
              "everyday"
            ]
          }
        ]
      }
    },
    "status_code": 200,
    "outcome": "success",
    "error": null,
    "duration_ms": 2593.068,
    "queue_ms": 0.001,
    "agent_ms": 2592.371,
    "configured_model": "gemini-3.5-flash-lite",
    "cache_enabled": false,
    "model_usage": {
      "model_attempts": 2,
      "reported_prompt_tokens": 1121,
      "reported_output_tokens": 242,
      "reported_total_tokens": 1363
    }
  }
}
```

**Criterion 5 — real output:** serve.py::finish_request_record (failure header and stderr error), triggered by tools/evaluate_capstone.py::fault_trial.

```json
{
  "slot": 1,
  "passed": true,
  "client_response": {
    "timestamp": "2026-11-15T20:41:00.422825+00:00",
    "method": "GET",
    "url": "http://127.0.0.1:64873/health",
    "input": null,
    "http_status": 200,
    "response": {
      "status": "ok"
    },
    "client_elapsed_ms": 14.459,
    "request_id": "54791f214f2647ea8a92f6ab48e895a8",
    "run_log": "failed",
    "transport_error": null,
    "trial": 1,
    "kind": "logging_failure",
    "slot": 1
  },
  "stderr_lines": [
    "[2026-11-15 12:41:00,438] ERROR in serve: Could not save request 54791f214f2647ea8a92f6ab48e895a8: [Errno 17] File exists: '/var/folders/9g/v18s588943g4v58_2hbz9vyc0000gn/T/fitfindr-log-fault-y7wc1iuw/regular_file_not_directory'"
  ]
}
```

All responses, logs, stderr captures and per-request assessments remain in the trial folders. This report is a draft artifact; the README has not been edited.
