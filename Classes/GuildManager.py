from __future__ import annotations

from discord import Guild
from typing import TYPE_CHECKING, List

from .GuildData import GuildData

if TYPE_CHECKING:
    from Classes import FroggeBot
################################################################################

__all__ = ("GuildManager",)

################################################################################
class GuildManager:
    """A class for managing bot-specific guild data and settings."""

    __slots__ = (
        "_state",
        "_fguilds"
    )
    
################################################################################
    def __init__(self, bot: FroggeBot):
        
        self._state: FroggeBot = bot
        self._fguilds: List[GuildData] = []
    
################################################################################
    def __getitem__(self, guild_id: int) -> GuildData:
        
        for frogge in self._fguilds:
            if frogge.guild_id == guild_id:
                return frogge
    
################################################################################    
    @property
    def fguilds(self) -> List[GuildData]:
        
        return self._fguilds
    
################################################################################
    def add_new_guild(self, guild: Guild) -> None:
        
        g = self[guild.id]
        if g is None:
            self._fguilds.append(GuildData.new(self._state, guild))
        
################################################################################
    def add_guild_data(self, guild: Guild) -> None:

        g = self[guild.id]
        if g is None:
            self._fguilds.append(GuildData(self._state, guild))

################################################################################
