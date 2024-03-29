from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Tuple

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("DatabaseLoader",)

################################################################################
class DatabaseLoader(DBWorkerBranch):
    """A utility class for loading data from the database."""

    def load_all(self) -> Dict[str, Any]:
        """Performs all sub-loaders and returns a dictionary of their results."""

        return {
            "bot_config": self._load_bot_config(),
            "profiles" : self._load_profiles(),
            "additional_images" : self._load_additional_images()
        }

################################################################################
    def _load_bot_config(self) -> Tuple[Any, ...]:
        
        self.execute("SELECT * FROM bot_config;")
        return self.fetchall()
        
################################################################################
    def _load_profiles(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM profile_master;")
        return self.fetchall()

################################################################################
    def _load_additional_images(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM additional_images;")
        return self.fetchall()
    
################################################################################
