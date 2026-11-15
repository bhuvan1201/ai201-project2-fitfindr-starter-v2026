### Run Log — Before

Three formal trials with unchanged code and criteria. Criteria 1, 3 and 4 share each trial's five measured outfit requests; the one warm-up attempt is excluded. Criterion 2 uses five hosted health requests per trial. Criterion 5 uses ten health requests per trial in an isolated local instance with an invalid log destination.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Hosted completion | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Recoverable health logs | 5 of 5 | 5/5 | 0/5 | 0/5 | MISSED |
| 3. Response within 45 seconds | 4 of 5 | 5/5 | 4/5 | 4/5 | MET |
| 4. Completed output and reported usage | 5 of 5 | 5/5 | 4/5 | 4/5 | MISSED |
| 5. Visible logging failure | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

These counts check the stated response/log conditions; they do not judge outfit quality or establish accurate API billing.

**Criterion 1 — real output:** agent.py::run_agent, returned over HTTP by serve.py::ask.

```json
{
  "slot": 1,
  "passed": true,
  "client_response": {
    "timestamp": "2026-11-15T06:13:52.212324+00:00",
    "method": "POST",
    "url": "https://fitfindr-capstone.vercel.app/ask",
    "input": {
      "query": "90s track jacket in size M"
    },
    "http_status": 200,
    "response": {
      "error": null,
      "fit_card": "Scored this 90s Track Jacket for $45.0 on Poshmark! It's styled here in a relaxed 90s streetwear aesthetic with baggy dark-wash jeans and a white ribbed tank.",
      "outfit_suggestion": "Here are two outfits featuring your new 90s Track Jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers, Black crossbody bag\n* **Why it works:** The baggy dark-wash jeans and track jacket lean into a relaxed 90s streetwear aesthetic. Layering the white ribbed tank top underneath matches the white sleeve stripes, and the chunky white sneakers tie the athletic color scheme together. \n\n**Outfit 2: High-Low Mix**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n* **Why it works:** Pairing the sporty, retro track jacket with tailored wide-leg khaki trousers creates a cool contrast between athletic and smart-casual styles. The white ribbed tank keeps the base clean, while the white sneakers complement the jacket's detailing. *(You could add a simple silver chain necklace to finish the look.)*",
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
    "client_elapsed_ms": 17623.057,
    "request_id": "6ff0de72fd314ff98ab938d66e8c9306",
    "run_log": "saved",
    "transport_error": null,
    "trial": 1,
    "kind": "ask",
    "slot": 1
  },
  "application_record": {
    "timestamp": "2026-11-15T06:13:52.458+00:00",
    "request_id": "6ff0de72fd314ff98ab938d66e8c9306",
    "method": "POST",
    "path": "/ask",
    "input_format": "json",
    "input": {
      "query": "90s track jacket in size M"
    },
    "output_format": "json",
    "output": {
      "error": null,
      "fit_card": "Scored this 90s Track Jacket for $45.0 on Poshmark! It's styled here in a relaxed 90s streetwear aesthetic with baggy dark-wash jeans and a white ribbed tank.",
      "outfit_suggestion": "Here are two outfits featuring your new 90s Track Jacket:\n\n**Outfit 1: Casual Streetwear**\n* **Pieces:** 90s Track Jacket, Baggy straight-leg jeans (dark wash), White ribbed tank top, Chunky white sneakers, Black crossbody bag\n* **Why it works:** The baggy dark-wash jeans and track jacket lean into a relaxed 90s streetwear aesthetic. Layering the white ribbed tank top underneath matches the white sleeve stripes, and the chunky white sneakers tie the athletic color scheme together. \n\n**Outfit 2: High-Low Mix**\n* **Pieces:** 90s Track Jacket, Wide-leg khaki trousers, White ribbed tank top, Chunky white sneakers\n* **Why it works:** Pairing the sporty, retro track jacket with tailored wide-leg khaki trousers creates a cool contrast between athletic and smart-casual styles. The white ribbed tank keeps the base clean, while the white sneakers complement the jacket's detailing. *(You could add a simple silver chain necklace to finish the look.)*",
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
    "duration_ms": 17331.942,
    "queue_ms": 0.001,
    "agent_ms": 17331.401,
    "configured_model": "gemini-3.5-flash-lite",
    "cache_enabled": false,
    "model_usage": {
      "model_attempts": 2,
      "reported_prompt_tokens": 1151,
      "reported_output_tokens": 265,
      "reported_total_tokens": 1416
    }
  }
}
```

**Criterion 2 — real output:** serve.py::finish_request_record and run_log.py::append_record, recovered from Vercel runtime logs.

```json
{
  "slot": 1,
  "passed": false,
  "client_response": {
    "timestamp": "2026-11-15T06:18:49.726002+00:00",
    "method": "GET",
    "url": "https://fitfindr-capstone.vercel.app/health",
    "input": null,
    "http_status": 200,
    "response": {
      "status": "ok"
    },
    "client_elapsed_ms": 163.456,
    "request_id": "4712394962dc4a1bbdb86900f35cb949",
    "run_log": "saved",
    "transport_error": null,
    "trial": 2,
    "kind": "health",
    "slot": 1
  },
  "application_record": null
}
```

**Criterion 3 — real output:** tools/measure_capstone.py::request_once (monotonic client elapsed time).

```json
{
  "slot": 5,
  "passed": false,
  "client_response": {
    "timestamp": "2026-11-15T06:18:47.232283+00:00",
    "method": "POST",
    "url": "https://fitfindr-capstone.vercel.app/ask",
    "input": {
      "query": "90s track jacket in size M"
    },
    "http_status": 200,
    "response": {
      "error": null,
      "fit_card": "Scored this 90s Track Jacket for $45.0 on Poshmark! Paired with baggy jeans and chunky sneakers, it gives off the ultimate effortless streetwear vibe.",
      "outfit_suggestion": "Here are two outfits featuring your new 90s Track Jacket:\n\n**Outfit 1: Casual Streetwear**\n*   **Top:** White ribbed tank top\n*   **Bottoms:** Baggy straight-leg jeans, dark wash\n*   **Shoes:** Chunky white sneakers\n*   **Accessories:** Black crossbody bag\n*   *Why it works:* The fitted white tank balances the relaxed silhouette of the baggy dark wash jeans and lightweight track jacket. The chunky white sneakers tie in the white sleeve stripes for a cohesive, effortless 90s streetwear look. \n\n**Outfit 2: High-Low Contrast**\n*   **Bottoms:** Wide-leg khaki trousers\n*   **Shoes:** Black combat boots \n*   **Suggested Addition:** A simple silver chain necklace\n*   *Why it works:* Pairing the sporty, vintage track jacket with tailored wide-leg khaki trousers creates a stylish high-low mix. The edge of the black combat boots anchors the outfit and contrasts nicely with the lighter earth tones.",
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
    "client_elapsed_ms": 2491.448,
    "request_id": "8d250572059043068b24d54c2eb3090f",
    "run_log": "saved",
    "transport_error": null,
    "trial": 2,
    "kind": "ask",
    "slot": 5
  },
  "application_record": null
}
```

**Criterion 4 — real output:** serve.py::model_usage_snapshot and serve.py::finish_request_record.

```json
{
  "slot": 5,
  "passed": false,
  "client_response": {
    "timestamp": "2026-11-15T06:18:47.232283+00:00",
    "method": "POST",
    "url": "https://fitfindr-capstone.vercel.app/ask",
    "input": {
      "query": "90s track jacket in size M"
    },
    "http_status": 200,
    "response": {
      "error": null,
      "fit_card": "Scored this 90s Track Jacket for $45.0 on Poshmark! Paired with baggy jeans and chunky sneakers, it gives off the ultimate effortless streetwear vibe.",
      "outfit_suggestion": "Here are two outfits featuring your new 90s Track Jacket:\n\n**Outfit 1: Casual Streetwear**\n*   **Top:** White ribbed tank top\n*   **Bottoms:** Baggy straight-leg jeans, dark wash\n*   **Shoes:** Chunky white sneakers\n*   **Accessories:** Black crossbody bag\n*   *Why it works:* The fitted white tank balances the relaxed silhouette of the baggy dark wash jeans and lightweight track jacket. The chunky white sneakers tie in the white sleeve stripes for a cohesive, effortless 90s streetwear look. \n\n**Outfit 2: High-Low Contrast**\n*   **Bottoms:** Wide-leg khaki trousers\n*   **Shoes:** Black combat boots \n*   **Suggested Addition:** A simple silver chain necklace\n*   *Why it works:* Pairing the sporty, vintage track jacket with tailored wide-leg khaki trousers creates a stylish high-low mix. The edge of the black combat boots anchors the outfit and contrasts nicely with the lighter earth tones.",
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
    "client_elapsed_ms": 2491.448,
    "request_id": "8d250572059043068b24d54c2eb3090f",
    "run_log": "saved",
    "transport_error": null,
    "trial": 2,
    "kind": "ask",
    "slot": 5
  },
  "application_record": null
}
```

**Criterion 5 — real output:** serve.py::finish_request_record (failure header and stderr error), triggered by tools/evaluate_capstone.py::fault_trial.

```json
{
  "slot": 1,
  "passed": true,
  "client_response": {
    "timestamp": "2026-11-15T06:13:20.216779+00:00",
    "method": "GET",
    "url": "http://127.0.0.1:57069/health",
    "input": null,
    "http_status": 200,
    "response": {
      "status": "ok"
    },
    "client_elapsed_ms": 8.236,
    "request_id": "6089d619feb94d2abef3c1400ef4c19b",
    "run_log": "failed",
    "transport_error": null,
    "trial": 1,
    "kind": "logging_failure",
    "slot": 1
  },
  "stderr_lines": [
    "[2026-11-14 22:13:20,224] ERROR in serve: Could not save request 6089d619feb94d2abef3c1400ef4c19b: [Errno 17] File exists: '/var/folders/9g/v18s588943g4v58_2hbz9vyc0000gn/T/fitfindr-log-fault-uzbchkhd/regular_file_not_directory'"
  ]
}
```

All responses, logs, stderr captures and per-request assessments remain in the trial folders. This report is a draft artifact; the README has not been edited.
