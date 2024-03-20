from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, Embed
from discord.ext.pages import Page, PageGroup, Paginator

from Assets import BotEmojis, BotImages
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import FroggeBot
################################################################################

__all__ = ("ProfileHelp",)
        
################################################################################
class ProfileHelp:
    
    __slots__ = (
        "_state",
    )
    
################################################################################
    def __init__(self, state: FroggeBot):
        
        self._state: FroggeBot = state
        
################################################################################
    @staticmethod
    async def menu(interaction: Interaction) -> None:
        
        pages = ProfileHelp._prepare_pages()
        frogginator = Paginator(
            pages=pages,
            show_menu=True, 
            menu_placeholder="Select a Command Category..."
        )
        await frogginator.respond(interaction)
    
################################################################################
    @staticmethod
    def _prepare_pages() -> List[PageGroup]:
        
        start_group = PageGroup(
            pages=[
                ProfileHelp._welcome_page(),
                ProfileHelp._preview_page(),
                ProfileHelp._import_page(),
                ProfileHelp._finalize_page()
            ], 
            label="Start & Other Commands",
            timeout=300.0
        )
        details_group = PageGroup(
            pages=[
                ProfileHelp._details_main_page(),
                ProfileHelp._name_page(),
                ProfileHelp._custom_url_page(),
                ProfileHelp._jobs_page(),
                ProfileHelp._accent_color_page(),
                ProfileHelp._rates_page()
            ],
            label="Profile Details",
            timeout=300.0
        )
        ataglance_group = PageGroup(
            pages=[
                ProfileHelp._ataglance_main_page(),
                ProfileHelp._gender_page(),
                ProfileHelp._race_page(),
                ProfileHelp._orientation_page(),
                ProfileHelp._height_page(),
                ProfileHelp._age_page(),
                ProfileHelp._mare_page()
            ],
            label="At A Glance",
            timeout=300.0
        )
        personality_group = PageGroup(
            pages=[
                ProfileHelp._personality_main_page(),
                ProfileHelp._likes_page(),
                ProfileHelp._dislikes_page(),
                ProfileHelp._personality_page(),
                ProfileHelp._aboutme_page()
            ],
            label="Personality",
            timeout=300.0
        )
        images_group = PageGroup(
            pages=[
                ProfileHelp._images_main_page(),
                ProfileHelp._thumbnail_page(),
                ProfileHelp._main_image_page(),
                ProfileHelp._additional_images_page()
            ],
            label="Images",
            timeout=300.0
        )
        
        return [
            start_group,
            details_group,
            ataglance_group,
            personality_group,
            images_group
        ]
    
################################################################################
    @staticmethod
    def _welcome_page() -> Page:
        
        embed = U.make_embed(
            title="Welcome to FroggeBot!",
            description=(
                "The bot that helps you create and manage your own personal "
                "FFXIV character profile.\n\n"

                "If you've reached this message, you're probably looking for "
                "help on how to use the bot! If you want the simple answer, "
                "just type `/profile` and the bot's various commands will be "
                "displayed for you to select from. You can pick any command "
                "to create a profile, and updating information to make a "
                "clean, unique, and personalized profile is easy!\n\n"

                "If you're looking for more detailed information on what each "
                "command does, you've come to the right place! Below is a "
                "selector with all the commands the bot has to offer, and "
                "by selecting one, you'll be provided a message with a general "
                "overview of that command and the ability to page through "
                "and get fine details on each element of that step in "
                "the process.\n\n"

                "If you're ready to get started, select a command from the "
                "dropdown menu below and let's get to work!"
            ),
            thumbnail_url=BotImages.FrogHeart
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _details_main_page() -> Page:
        
        embed = U.make_embed(
            title="Profile Details",
            description=(
                "The profile details command allows you to view and update "
                "the basic detail elements of your profile:\n\n"
                
                "* **Name**\n"
                "* **Custom URL**\n"
                "* **Jobs**\n"
                "* **Accent Color**\n"
                "* **Rates**\n\n"
                
                "*(All elements are optional, aside from your character's name.)*\n\n"
                
                "Use the buttons below to learn more about each element."
            )
        )
    
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _name_page() -> Page:
            
        embed = U.make_embed(
            title="Name",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"
                
                "The name element of your profile is the name of your FFXIV "
                "character. This is the only required element of a profile.\n\n"
                
                "Your character's name lives at the top of the profile, and is "
                "the first thing people will see when they view your profile. "
                "It's important to make sure your character's name is accurate "
                "and spelled correctly.\n\n"
                
                "Despite this being the only required element, it makes for a "
                "pretty boring profile if it's the only thing on there. So, "
                "let's make sure to fill out the rest of the profile as well!"
            ),
            thumbnail_url=BotImages.PH_CharName
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _custom_url_page() -> Page:
        
        embed = U.make_embed(
            title="Custom URL",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"
                
                "The custom URL element of your profile is a unique URL that "
                "is used as the underlying link for the title of your profile -"
                "your character name. This URL can be anything you like that "
                "relates to your character.\n\n"
                
                "The custom URL is a great way to share a personal Carrd site, "
                "a music playlist, or just a fun link that you think represents "
                "your character well. It's a great way to add a little extra "
                "flair to your profile!\n\n"
                
                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_CharName
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _jobs_page() -> Page:
            
        embed = U.make_embed(
            title="Jobs",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"
                
                "The jobs element of your profile is a list of the jobs that "
                "represents your character. They can be real, fake, RP, or "
                "otherwise. It's a great way to show off your character's "
                "abilities and lore.\n\n"
                
                "The jobs list is displayed in the top center of your "
                "profile, underneath your character name.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Jobs
        )
        
        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def _accent_color_page() -> Page:
            
        embed = U.make_embed(
            title="Accent Color",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"
                
                "The accent color element of your profile is the color strip "
                "located on the left-hand side of your profile. It's a "
                "great way to add a little extra flair to your profile and "
                "make it stand out.\n\n"
                
                "*(This element is optional.)*"
            ),
            thumbnail_url=BotImages.PH_AccentColor
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _rates_page() -> Page:
                
        embed = U.make_embed(
            title="Rates",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"
                
                "The rates element of your profile is a list of the rates you "
                "charge for various services. This can be anything from RP, "
                "commission, or other services you might offer.\n\n"
                
                "Some examples include:\n"
                "* Courtesan Services\n"
                "* GPose Photography Pricing\n"
                "* Website Design Rates\n"
                "* Etc...\n"
                
                "The rates list is displayed in the upper center of your "
                "profile, underneath the At A Glance section, but above your "
                "like and dislike lists.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Rates
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _ataglance_main_page() -> Page:
        
        embed = U.make_embed(
            title="Profile At a Glance",
            description=(
                "The profile at a glance command allows you to view and update "
                "the following demographic elements of your profile:\n\n"
                
                "* **Gender/Pronouns**\n"
                "* **Race/Clan**\n"
                "* **Sexual Orientation**\n"
                "* **Height**\n"
                "* **Age**\n"
                "* **Mare ID**\n"
                
                "*(All elements are optional.)*"
                
                "Use the buttons below to learn more about each element."
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _gender_page() -> Page:
        
        embed = U.make_embed(
            title="Gender/Pronouns",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "Your gender and pronouns are displayed in the upper portion "
                "of your main profile, in the At A Glance section.\n\n"
                
                "Your gender value is entirely customizable and not limited to "
                "the binary. You can use any term you like to represent your "
                "character's gender simply by selecting '`Custom`' from the "
                "dropdown menu.\n\n"
                
                "Please note that pronouns are __not__ customizable, and are "
                "limited to the options in the provided selector.\n\n"
                
                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Gender
        )
        
        return Page(embeds=[embed])
        
################################################################################
    @staticmethod
    def _race_page() -> Page:
        
        embed = U.make_embed(
            title="Race/Clan",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "Your race & clan are displayed in the upper portion "
                "of your main profile, in the At A Glance section.\n\n"
                
                "Your race and clan values are entirely customizable and not "
                "limited to the races/clans in FFXIV. You can use any term you "
                "like to represent your character's race and clan simply by "
                "selecting '`Custom`' from the dropdown menu.\n\n"
                
                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Race
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _orientation_page() -> Page:
        
        embed = U.make_embed(
            title="Sexual Orientation",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "Your character's orientation is displayed in the upper portion "
                "of your main profile, in the At A Glance section.\n\n"
                
                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Orientation
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _height_page() -> Page:
        
        embed = U.make_embed(
            title="Height",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "Your character's height is displayed in the upper portion "
                "of your main profile, in the At A Glance section.\n\n"
                
                "When entering your height ensure that you use the following "
                "format: `5' 7\"` or `5ft 7in`. This will ensure that your height "
                "is displayed correctly on your profile.\n\n"
                
                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Height
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _age_page() -> Page:
            
        embed = U.make_embed(
            title="Age",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "Your character's age is displayed in the upper portion "
                "of your main profile, in the At A Glance section.\n\n"
                
                "This can be a number or a text value.\n\n"
                
                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Age
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _mare_page() -> Page:
        
        embed = U.make_embed(
            title="Mare ID",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "Your character's Mare ID is displayed in the upper portion "
                "of your main profile, in the At A Glance section.\n\n"
                
                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Mare
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _personality_main_page() -> Page:
        
        embed = U.make_embed(
            title="Profile Personality",
            description=(
                "The profile personality command allows you to view and update "
                "the following personality-oriented elements of your profile:\n\n"
                
                "* **Likes**\n"
                "* **Dislikes**\n"
                "* **Personality**\n"
                "* **About Me**\n"
                
                "*(All elements are optional.)*"
                
                "Use the buttons below to learn more about each element."
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _likes_page() -> Page:
        
        embed = U.make_embed(
            title="Likes",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "The likes element of your profile is a list of things your "
                "character enjoys. It's a great way to show off your character's "
                "interests and hobbies.\n\n"
                
                "The likes list is displayed in the center of your "
                "profile, underneath your At A Glance and Rates sections.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Likes
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _dislikes_page() -> Page:
        
        embed = U.make_embed(
            title="Dislikes",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "The dislikes element of your profile is a list of things your "
                "character does not enjoy. It's a great way to show off your "
                "character's dislikes and pet peeves.\n\n"
                
                "The dislikes list is displayed in the center of your "
                "profile, underneath your At A Glance and Rates sections.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Dislikes
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _personality_page() -> Page:
        
        embed = U.make_embed(
            title="Personality",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "The personality element of your profile is a brief personality "
                "summary of your character. It's a great way to show off your "
                "character's quirks.\n\n"
                
                "The personality list is displayed in the center of your "
                "profile, underneath your Likes and Dislikes sections.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Personality
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _aboutme_page() -> Page:
        
        embed = U.make_embed(
            title="About Me",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "The about me element of your profile is a brief summary of "
                "your character. It's a great way to show off your character's "
                "lore and backstory.\n\n"
                
                "The about me page is displayed at the end of your profile as "
                "a separate embed to the main profile.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _images_main_page() -> Page:
        
        embed = U.make_embed(
            title="Profile Images",
            description=(
                "The profile images command allows you to view and update "
                "the following graphical elements of your profile:\n\n"
                
                "* **Thumbnail**\n"
                "* **Main Image**\n"
                "* **Additional Images**\n"
                
                "*(All elements are optional.)*"
                
                "Use the buttons below to learn more about each element."
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _thumbnail_page() -> Page:
        
        embed = U.make_embed(
            title="Thumbnail",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "The thumbnail element of your profile is a small image that "
                "represents your character. It's a great way to show off a "
                "profile pic or avatar.\n\n"
                
                "__**The recommended size for the thumbnail is at least "
                "512x512 pixels and preferably using a 1:1 aspect ratio.**__\n\n"
                
                "The thumbnail image is displayed in the upper right corner of "
                "your profile.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_Thumbnail
        )
        
        return Page(embeds=[embed])
        
################################################################################
    @staticmethod
    def _main_image_page() -> Page:
        
        embed = U.make_embed(
            title="Main Image",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "The main image element of your profile is a large image that "
                "represents your character. It's a great way to show off a "
                "profile pic or avatar.\n\n"
                
                "__**The recommended size for the main image is at least "
                "1024x768 pixels and preferably using a 16:9 aspect ratio.**__\n\n"
                
                "The main image is displayed at the bottom of your profile, "
                "after the list of additional images.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_MainImage
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _additional_images_page() -> Page:
        
        embed = U.make_embed(
            title="Additional Images",
            description=(
                "*(Click on the image to the right to view this element in the "
                "profile.)*\n\n"

                "The additional images element of your profile is a list of "
                "images that are great, and represent your character even further "
                "than the thumbnail and main image. It's a great way to show "
                "off all your other favorite gposes!.\n\n"
                
                "The additional images are displayed at the bottom of your profile, "
                "above the main image and below the personality section.\n\n"

                "*(This element is optional and won't appear if left empty.)*"
            ),
            thumbnail_url=BotImages.PH_AdditionalImages
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _preview_page() -> Page:
        
        embed = U.make_embed(
            title="Preview Profile",
            description=(
                "The preview profile command allows you to view a preview of "
                "your profile as it will appear when posted to a channel.\n\n"
                
                "This command is useful for checking your profile for any "
                "errors or issues before posting it to a channel."
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _import_page() -> Page:
        
        embed = U.make_embed(
            title="Import Profile",
            description=(
                "The import profile command allows you to import a profile "
                "from another server. This is useful when creating the same "
                "profile for yourself in multiple servers running FroggeBot.\n\n"
                
                "This command requires the Discord Message URL of the profile "
                "to be imported."
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    @staticmethod
    def _finalize_page() -> Page:
        
        embed = U.make_embed(
            title="Finalize Profile",
            description=(
                "The finalize profile command allows you to post your profile "
                "to a channel of your choosing, or to update an existing profile "
                "with new information.\n\n"
                
                "If you already have a profile, you can use this command to "
                "update the information on your profile without having to "
                "create a new post."
            )
        )
        
        return Page(embeds=[embed])
    
################################################################################
    
        