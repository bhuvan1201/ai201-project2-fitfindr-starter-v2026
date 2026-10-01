# Milestone 1 — Read the data and run the starter

## What I noticed in the data

I read the first six listings using `python app.py listings --full -n 6` and checked the fields using `python app.py fields`.

A listing has these fields: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

- The title, description, and style tags contain words I can use to match a search. Size and price can narrow the results.
- Sizes use different formats, such as `M`, `S/M`, `XL (oversized)`, and `W30 L30`. I will need to decide how size matching works when I specify the search tool.
- Some listings have `brand: null`, so a fit card should not invent a brand.
- Listing `lst_006` is a vintage-style graphic tee priced at $24, with size L. It fits the description and budget in the starter query, which does not specify a size.

## Wardrobe structure

A wardrobe item has `id`, `name`, `category`, `colors`, `style_tags`, and `notes`. The wardrobe stores these items in an `items` list.

The empty example in `data/wardrobe_schema.json` is:

```json
"empty_wardrobe": {
  "_note": "Use this as the starting template for a new user with no wardrobe entered yet.",
  "items": []
}
```

An empty list means the user has no saved wardrobe items. In that case, `suggest_outfit` should give general advice without claiming the user owns particular clothes.

## Starter run

I ran `python app.py examples` to see the suggested queries, then ran this query:

```text
$ python app.py ask 'vintage graphic tee under $30'

  The planning loop isn't built yet — see the TODO in agent.py.

0 model calls this session
```

This is the expected starting result. The command runs, but the planning loop still needs to be implemented.
