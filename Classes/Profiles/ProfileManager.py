from __future__ import annotations
import json
from discord import User, Interaction, Attachment, TextChannel
from typing import TYPE_CHECKING, List, Optional, Any, Tuple, Dict

from .Profile import Profile
from Utilities import InvalidFileTypeError, CorruptedFileError, InvalidOperationError

if TYPE_CHECKING:
    from Classes import GuildData, FroggeBot
################################################################################

__all__ = ("ProfileManager",)

################################################################################
class ProfileManager:
    
    __slots__ = (
        "_state",
        "_profiles"
    )
    
################################################################################
    def __init__(self, guild: GuildData) -> None:
        
        self._state: GuildData = guild
        self._profiles: List[Profile] = []
    
################################################################################
    async def _load_all(self, payload: Dict[str, Any]) -> None:
        
        profiles = []
        for p in payload["profiles"]:       
            profile = await Profile.load(self, p)
            if profile is not None:  # None when user not found.
                profiles.append(profile)
                
        self._profiles = profiles
        
################################################################################    
    def __getitem__(self, user_id: int) -> Optional[Profile]:
        
        for p in self._profiles:
            if p.user.id == user_id:
                return p
    
################################################################################
    @property
    def bot(self) -> FroggeBot:
        
        return self._state.bot
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._state.parent.id
    
################################################################################
    def create_profile(self, user: User) -> Profile:
        
        # Just double checking we don't add an extra record.
        profile = self[user.id]
        if profile is not None:
            return profile
        
        profile = Profile.new(self, user)
        self._profiles.append(profile)
        
        return profile
    
################################################################################
    async def import_profile(self, interaction: Interaction, data: Attachment, channel: TextChannel) -> None:
        
        if not data.filename == "profile.json":
            error = InvalidFileTypeError("profile.json")
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        try:
            payload = json.loads(await data.read())
        except json.JSONDecodeError:
            error = CorruptedFileError("profile.json")
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if payload["guild_id"] == self.guild_id:
            error = InvalidOperationError("Importing a profile into the same server")
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await interaction.response.defer()
        
        profile = Profile.from_dict(self, interaction.user, payload)
        profile.update_all()
        self._profiles.append(profile)
        
        await profile.post(interaction, channel)        
    
################################################################################
    