# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):

```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:

```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:

```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Tool Inventory

Your README submission must document each tool's name, inputs, and return value. **These must exactly match your actual function signatures in `tools.py`.** Your documented interfaces will be checked against your actual function signatures in `tools.py` — if the parameter count or types contradict what's in the code, you may not receive full credit for that tool.

1. search_listings(description: str, size: str | None = None, max_price: float | None = None,) -> list[dict].
   Filters the loaded_listings against the available input values and returns a list of matching listings.
2. suggest_outfit(new_item:dict,wardrobe:dict)->str
   From the selected new_item it suggests 1 outfit combination with your existing wardrobe if you have it, otherwise it just print out to the user a fallback message.
3. create_fit_card(outfit:str,new_item:dict)->str
   Describes the suggested outfit in a modern way to make it interesting. Returns a fit_card message.

---

## Interaction Walkthrough

User query: "I'm looking for a vintage graphic tee under $30."

Step 1 — Tool called:

- Tool: search_listings
- Input: description="vintage graphic tee", max_price=30
- Why this tool: The agent parses the query and calls this first to find matching listings from the dataset.
- Output: A ranked list of listings — top result is Graphic Tee — 2003 Tour Bootleg Style at $24.

Step 2 — Tool called:

- Tool: suggest_outfit
- Input: new_item=Graphic Tee listing, wardrobe=example wardrobe
- Why this tool: Called with the top listing and the user's wardrobe to generate a specific outfit pairing.
- Output: "Graphic Tee, baggy straight-leg jeans, black combat boots, brown leather belt. This outfit combines grunge and streetwear elements for a casual, edgy look."

Step 3 — Tool called:

- Tool: create_fit_card
- Input: outfit=outfit suggestion, new_item=Graphic Tee listing
- Why this tool: Called last to turn the outfit into a shareable Instagram-style caption.
- Output: "I'm obsessing over my new Graphic Tee — 2003 Tour Bootleg Style, it's the perfect addition for a laid-back grunge vibe. Paired with baggy jeans and combat boots, this look is giving me full Y2K nostalgia."

Final output to user: The fit card caption above is displayed in the "Your fit card" panel, alongside the listing details and outfit suggestion in their respective panels.

---

## Error Handling and Fail Points

<!-- For each tool, describe the specific failure mode and what your agent does in response.
     This maps to the error handling section of the rubric (F5-C1). -->

| Tool              | Failure mode                          | Agent response                                                                                                       |
| ----------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `search_listings` | No results match the query            | No matching items found! Try other styles, a different size, or a higher budget.                                     |
| `suggest_outfit`  | Wardrobe is empty                     | No worries! Let's start building a wardrobe for you.<br />The chosen Y2K Baby Tee — Butterfly Print is a good start! |
| `create_fit_card` | Outfit input is missing or incomplete | How do you like, Y2K Baby Tee — Butterfly Print?                                                                     |

---

## Spec Reflection

<!-- Answer both questions with at least 2–3 sentences each. -->

**One way planning.md helped during implementation:** Planning.md helped me stay on top of what I want Claude to help me implement and remaining strict on thought out scenarios rather than facing an error and having to go with anything Claude is suggesting.

**One divergence from your spec, and why:** No significant divergence, used what spec suggested.

---

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.
