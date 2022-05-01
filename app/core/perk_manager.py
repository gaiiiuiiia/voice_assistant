import logging

from app.core.perk_loader import PerkLoader

logger = logging.getLogger(__name__)


class PerkManager:
    def __init__(self, perk_loader: PerkLoader) -> None:
        self._perk_loader = perk_loader
        self._perks = self._perk_loader.load()

    def process(self, text: str) -> None:
        pass
