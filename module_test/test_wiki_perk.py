import unittest

from app.perks.wikipedia_perk import WikipediaPerk


class TestWikiPerk(unittest.TestCase):

    def test_wiki_search(self) -> None:
        wiki_perk = WikipediaPerk()

        wiki_perk.wiki_search(query='ямакаси')

