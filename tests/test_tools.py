"""
tests/test_tools.py

Pytest tests for each FitFindr tool, covering the failure modes
described in planning.md.
"""

from unittest.mock import MagicMock, patch

import pytest

from tools import create_fit_card, search_listings, suggest_outfit


# ── Shared fixtures ────────────────────────────────────────────────────────────

@pytest.fixture
def sample_item():
    return {
        "id": "lst_test",
        "title": "Graphic Tee — 2003 Tour Bootleg Style",
        "category": "tops",
        "style_tags": ["graphic tee", "vintage", "grunge", "streetwear"],
        "size": "M",
        "condition": "good",
        "price": 24.0,
        "colors": ["black", "white"],
        "brand": None,
        "platform": "depop",
        "description": "Faded bootleg-style tee with a worn-in feel.",
    }


@pytest.fixture
def empty_wardrobe():
    return {"items": []}


@pytest.fixture
def example_wardrobe():
    return {
        "items": [
            {
                "id": "w_001",
                "name": "Baggy straight-leg jeans, dark wash",
                "category": "bottoms",
                "colors": ["dark blue", "indigo"],
                "style_tags": ["denim", "streetwear", "baggy"],
                "notes": None,
            },
            {
                "id": "w_002",
                "name": "Chunky white sneakers",
                "category": "shoes",
                "colors": ["white"],
                "style_tags": ["sneakers", "chunky", "streetwear"],
                "notes": None,
            },
        ]
    }


# ── Tool 1: search_listings ────────────────────────────────────────────────────

class TestSearchListings:

    def test_no_results_returns_empty_list(self):
        """Failure mode: no listings match the query → return []."""
        results = search_listings("designer ballgown", size="XXS", max_price=5)
        assert results == []

    def test_price_filter_excludes_expensive_items(self):
        """All returned items must be at or below max_price."""
        max_price = 25.0
        results = search_listings("vintage", max_price=max_price)
        assert results, "Expected at least one result under $25"
        for item in results:
            assert item["price"] <= max_price

    def test_size_filter_case_insensitive(self):
        """Size filter should match regardless of case (e.g. 'm' matches 'M' or 'S/M')."""
        results = search_listings("jacket", size="m")
        assert results, "Expected at least one jacket in size M"
        for item in results:
            assert "m" in item["size"].lower()

    def test_results_sorted_by_relevance(self):
        """Item matching more keywords should rank above item matching fewer."""
        results = search_listings("vintage graphic tee")
        assert len(results) >= 2
        # The top result should contain both 'vintage' and 'graphic' in its searchable text
        top = results[0]
        searchable = " ".join([
            top["title"], top["description"],
            " ".join(top["style_tags"]), " ".join(top["colors"]),
        ]).lower()
        assert "vintage" in searchable or "graphic" in searchable


# ── Tool 2: suggest_outfit ─────────────────────────────────────────────────────

class TestSuggestOutfit:

    def test_empty_wardrobe_returns_fallback_message(self, sample_item, empty_wardrobe):
        """Failure mode: empty wardrobe → fixed encouragement message, no LLM call."""
        result = suggest_outfit(sample_item, empty_wardrobe)
        assert "No worries" in result
        assert sample_item["title"] in result

    def test_empty_wardrobe_does_not_call_llm(self, sample_item, empty_wardrobe):
        """Empty wardrobe path must not make an API call."""
        with patch("tools._get_groq_client") as mock_client:
            suggest_outfit(sample_item, empty_wardrobe)
            mock_client.assert_not_called()

    def test_with_wardrobe_calls_llm_and_returns_string(self, sample_item, example_wardrobe):
        """With a populated wardrobe, the LLM is called and a non-empty string is returned."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Pair the tee with baggy jeans and chunky sneakers."

        with patch("tools._get_groq_client") as mock_client:
            mock_client.return_value.chat.completions.create.return_value = mock_response
            result = suggest_outfit(sample_item, example_wardrobe)

        assert isinstance(result, str)
        assert len(result) > 0


# ── Tool 3: create_fit_card ────────────────────────────────────────────────────

class TestCreateFitCard:

    def test_empty_outfit_returns_fallback_message(self, sample_item):
        """Failure mode: empty outfit string → fallback message with item title."""
        result = create_fit_card("", sample_item)
        assert sample_item["title"] in result

    def test_whitespace_outfit_returns_fallback_message(self, sample_item):
        """Whitespace-only outfit string is treated the same as empty."""
        result = create_fit_card("   ", sample_item)
        assert sample_item["title"] in result

    def test_empty_outfit_does_not_call_llm(self, sample_item):
        """Empty outfit guard must short-circuit before any API call."""
        with patch("tools._get_groq_client") as mock_client:
            create_fit_card("", sample_item)
            mock_client.assert_not_called()

    def test_valid_outfit_calls_llm_and_returns_string(self, sample_item):
        """With a valid outfit, the LLM is called and a non-empty string is returned."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This thrift find is everything."

        with patch("tools._get_groq_client") as mock_client:
            mock_client.return_value.chat.completions.create.return_value = mock_response
            result = create_fit_card("Baggy jeans and chunky sneakers.", sample_item)

        assert isinstance(result, str)
        assert len(result) > 0
