"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import json
import re

import config
from generate import generate
from utils.data_loader import load_listings

_STOPWORDS = {
    "a", "an", "and", "the", "for",
    "with", "under", "over", "in", "of",
}


def _keywords(text: str) -> set[str]:
    """Lowercase words worth matching on, stopwords removed."""
    words = re.findall(r"[a-z0-9']+", (text or "").lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1}


def _size_tokens(size: str) -> set[str]:
    cleaned = re.sub(r"\([^)]*\)", " ", size or "")
    parts = [p.strip().upper() for p in cleaned.split("/")]
    return {p for p in parts if p}


def _size_matches(wanted: str, listing_size: str) -> bool:
    if not wanted:
        return True

    listing_tokens = _size_tokens(listing_size)

    if any(token.startswith("ONE SIZE") for token in listing_tokens):
        return True

    return bool(_size_tokens(wanted) & listing_tokens)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

_CLOTHING_TYPES = {
    "jacket": {"jacket", "jackets", "bomber", "bombers", "windbreaker",
               "windbreakers", "blazer", "blazers", "shacket", "shackets"},
    "tee": {"tee", "tees", "tshirt", "tshirts"},
    "sneaker": {"sneaker", "sneakers", "trainer", "trainers"},
}


def _clothing_types(text: str) -> set[str]:
    """Recognize three supported type families, including common aliases."""
    normalized = re.sub(r"\bt[ -]shirts?\b", "tee", (text or "").lower())
    words = _keywords(normalized)
    return {kind for kind, aliases in _CLOTHING_TYPES.items() if words & aliases}


def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    Recognized jacket, tee and sneaker terms also filter by the listing title's
    clothing family. Other queries keep the existing keyword matching behavior.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    wanted_keywords = _keywords(description)
    if not wanted_keywords:
        return []
    wanted_types = _clothing_types(description)

    ranked = []
    for listing in load_listings():
        # Titles identify the item itself; descriptions can mention other
        # clothes as styling suggestions. Untyped searches retain old behavior.
        if wanted_types and not wanted_types & _clothing_types(listing["title"]):
            continue
        if max_price is not None and listing["price"] > max_price:
            continue
        if size is not None and not _size_matches(size, listing["size"]):
            continue

        searchable_text = " ".join(
            [listing["title"], listing["description"], *listing["style_tags"]]
        )
        score = len(wanted_keywords & _keywords(searchable_text))
        if score:
            ranked.append((score, listing))

    # Python's sort is stable, so tied results retain their order in the file.
    ranked.sort(key=lambda result: result[0], reverse=True)
    return [listing for _, listing in ranked[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    items = wardrobe.get("items") or []
    item_details = {
        "title": new_item["title"],
        "description": new_item["description"],
        "category": new_item["category"],
        "colors": new_item["colors"],
        "style_tags": new_item["style_tags"],
    }

    if items:
        prompt = (
            "Suggest one or two outfits for the new item below using pieces "
            "from this user's wardrobe. Name the wardrobe pieces you choose "
            "and briefly explain why they work together. You may suggest an "
            "additional piece, but present it as something the user could add.\n\n"
            f"New item: {json.dumps(item_details, ensure_ascii=False)}\n"
            f"Wardrobe items: {json.dumps(items, ensure_ascii=False)}"
        )
    else:
        prompt = (
            "The user has no saved wardrobe items. Suggest one or two general "
            "ways to style the new item. Describe other pieces as options the "
            "user could add, never as clothes they already own.\n\n"
            f"New item: {json.dumps(item_details, ensure_ascii=False)}"
        )

    response = generate(
        prompt,
        system=(
            "You are a clothing stylist. Use only the supplied item and "
            "wardrobe details. Keep the advice brief and specific. Do not "
            "claim the user owns a piece unless it appears in their wardrobe."
        ),
    ).strip()
    if response:
        return response

    return (
        f"You could style {new_item['title']} with complementary basics."
        if not items else
        f"Try styling {new_item['title']} with one of the listed wardrobe pieces."
    )


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "I couldn't create a fit card because no outfit suggestion was provided."

    item_details = {
        "title": new_item["title"],
        "description": new_item["description"],
        "price": new_item["price"],
        "platform": new_item["platform"],
        "colors": new_item["colors"],
        "style_tags": new_item["style_tags"],
    }
    if new_item.get("brand"):
        item_details["brand"] = new_item["brand"]

    prompt = (
        "Write a caption someone might post about this thrift find and outfit. "
        "Use two to four sentences. Name the item, state its price and "
        "platform exactly once each, and describe the outfit's vibe. "
        "Use only the supplied facts; do not invent a brand or other details. "
        "Return only the caption, without a heading or bullet points.\n\n"
        f"Listing: {json.dumps(item_details, ensure_ascii=False)}\n"
        f"Outfit suggestion: {outfit.strip()}"
    )
    response = generate(
        prompt,
        system="You write short, accurate social captions from supplied listing details.",
    ).strip()
    return response or "I couldn't create a fit card because the model returned no text."
