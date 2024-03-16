from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict
from discord import Guild, User

from Classes.Profiles.ProfileManager import ProfileManager

if TYPE_CHECKING:
    from Classes import FroggeBot, Profile
################################################################################

__all__ = ("GuildData",)

################################################################################
class GuildData:
    """A container for bot-specific guild data and settings."""

    __slots__ = (
        "_state",
        "_parent",
        "_log",
        "_profile_mgr",
    )

################################################################################
    def __init__(self, bot: FroggeBot, parent: Guild):

        self._state: FroggeBot = bot
        self._parent: Guild = parent
        
        self._profile_mgr: ProfileManager = ProfileManager(self)

################################################################################
    async def load_all(self, data: Dict[str, Any]) -> None:
        
        await self._profile_mgr._load_all(data)
    
################################################################################
    @classmethod
    def new(cls, bot: FroggeBot, parent: Guild) -> GuildData:
        
        bot.database.insert.guild(parent.id)
        return cls(bot, parent)
    
################################################################################
    @property
    def bot(self) -> FroggeBot:
        
        return self._state
    
################################################################################
    @property
    def parent(self) -> Guild:
        
        return self._parent
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._parent.id
    
################################################################################
    @property
    def profile_manager(self) -> ProfileManager:

        return self._profile_mgr
    
################################################################################
    def get_profile(self, user: User) -> Profile:

        profile = self._profile_mgr[user.id]
        if profile is None:
            profile = self._profile_mgr.create_profile(user)
            
        return profile
    
################################################################################
