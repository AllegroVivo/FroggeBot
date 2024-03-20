from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("DatabaseInserter",)

################################################################################
class DatabaseInserter(DBWorkerBranch):
    """A utility class for inserting new records into the database."""

    def _add_guild(self, guild_id: int) -> None:
        
        self.execute(
            "INSERT INTO bot_config (guild_id) VALUES (%s) "
            "ON CONFLICT DO NOTHING;",
            guild_id
        )
        
################################################################################
    def _add_profile(self, guild_id: int, user_id: int) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO profiles (_id, guild_id, user_id) VALUES (%s, %s, %s);",
            new_id, guild_id, user_id
        )
        self.execute("INSERT INTO details (_id) VALUES (%s);", new_id)
        self.execute("INSERT INTO ataglance (_id) VALUES (%s);", new_id)
        self.execute("INSERT INTO personality (_id) VALUES (%s);", new_id)
        self.execute("INSERT INTO images (_id) VALUES (%s);", new_id)
        
        return new_id
    
################################################################################
    def _add_additional_image(self, profile_id: str, url: str, caption: Optional[str]) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO additional_images (_id, profile_id, url, caption) "
            "VALUES (%s, %s, %s, %s);",
            new_id, profile_id, url, caption
        )
        
        return new_id

################################################################################

    guild           = _add_guild
    profile         = _add_profile
    addl_image      = _add_additional_image
    
################################################################################
    