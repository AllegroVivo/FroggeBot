from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import (
        Position, 
        Requirement, 
        TUser,
        Availability, 
        Qualification, 
        Training,
        SignUpMessage,
        ProfilePersonality,
        ProfileImages,
        ProfileDetails,
        ProfileAtAGlance,
        AdditionalImage,
        UserConfiguration,
        UserDetails,
    )
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater(DBWorkerBranch):
    """A utility class for updating records in the database."""

    def _update_profile_details(self, details: ProfileDetails) -> None:
        
        self.execute(
            "UPDATE details SET char_name = %s, url = %s, color = %s, jobs = %s, "
            "rates = %s, post_url = %s WHERE _id = %s;",
            details.name, details.url, 
            details.color.value if details.color is not None else None,
            details.jobs, details.rates, details.post_url, details.profile_id
        )
    
################################################################################    
    def _update_profile_ataglance(self, aag: ProfileAtAGlance) -> None:
        
        gender = race = clan = orientation = None
        if aag.gender is not None:
            gender = aag.gender if isinstance(aag.gender, str) else aag.gender.value
        if aag.race is not None:
            race = aag.race if isinstance(aag.race, str) else aag.race.value
        if aag.clan is not None:
            clan = aag.clan if isinstance(aag.clan, str) else aag.clan.value
        if aag.orientation is not None:
            orientation = (
                aag.orientation if isinstance(aag.orientation, str) 
                else aag.orientation.value
            )
        
        self.execute(
            "UPDATE ataglance SET gender = %s, pronouns = %s, race = %s, "
            "clan = %s, orientation = %s, height = %s, age = %s, mare = %s "
            "WHERE _id = %s;",
            str(gender), [p.value for p in aag.pronouns], str(race), 
            str(clan), str(orientation), aag.height, str(aag.age), str(aag.mare), 
            aag.profile_id
        )
       
################################################################################ 
    def _update_profile_personality(self, personality: ProfilePersonality) -> None:
        
        self.execute(
            "UPDATE personality SET likes = %s, dislikes = %s, personality = %s, "
            "aboutme = %s WHERE _id = %s;",
            personality.likes, personality.dislikes, personality.personality,
            personality.aboutme, personality.profile_id
        )
        
################################################################################
    def _update_profile_images(self, images: ProfileImages) -> None:
        
        self.execute(
            "UPDATE images SET thumbnail = %s, main_image = %s WHERE _id = %s;",
            images.thumbnail, images.main_image, images.profile_id
        )
    
################################################################################        
    def _update_profile_additional_image(self, image: AdditionalImage) -> None:
        
        self.execute(
            "UPDATE additional_images SET url = %s, caption = %s "
            "WHERE _id = %s;",
            image.url, image.caption, image.id
        )
    
################################################################################
    
    profile_details     = _update_profile_details
    profile_ataglance   = _update_profile_ataglance
    profile_personality = _update_profile_personality
    profile_images      = _update_profile_images
    profile_addl_image  = _update_profile_additional_image
    
################################################################################
    