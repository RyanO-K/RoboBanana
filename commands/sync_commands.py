import datetime
import subprocess
import time
from discord import Interaction, app_commands, Client
from config import YAMLConfig as Config
from util.sync_utils import SyncUtils
import logging
from discord.app_commands.errors import AppCommandError, CheckFailure

LOG = logging.getLogger(__name__)

UPTIME_START_TIME = 0.0

MOD_ROLE = os.getenv("ROLES_MOD")
CHAT_MOD_ROLE = os.getenv("ROLES_CMCHATMODERATOR")
TRUSTWORTHY = os.getenv("ROLES_TRUSTWORTHY")
# these are hardcoded until raze to radiant is over, or config file changes are allowed
# for testing on own setup, these need to be changed to your appropriate IDs
# HIDDEN_MOD_ROLE should be 1040337265790042172 when committing and refers to the Mod (Role Hidden)
# STAFF_DEVELOPER_ROLE should be 1226317841272279131 when committing and refers to the Staff Developer role
HIDDEN_MOD_ROLE = os.getenv("ROLES_HIDDENMOD")
STAFF_DEVELOPER_ROLE = os.getenv("ROLES_STAFFDEV")


@app_commands.guild_only()
class SyncCommands(app_commands.Group, name="sync"):
    def __init__(self, tree: app_commands.CommandTree, client: Client) -> None:
        super().__init__()
        self.tree = tree
        self.client = client

    async def on_error(self, interaction: Interaction, error: AppCommandError):
        if isinstance(error, CheckFailure):
            return await interaction.response.send_message(
                "Failed to perform command - please verify permissions.", ephemeral=True
            )
        logging.error(error)
        return await super().on_error(interaction, error)

    @app_commands.command(name="sync")
    @app_commands.checks.has_any_role(MOD_ROLE, HIDDEN_MOD_ROLE, STAFF_DEVELOPER_ROLE)
    async def sync(self, interaction: Interaction) -> None:
        """Manually sync slash commands to guild"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            logging.info(
                f"Command sync started by {interaction.user.name} ({interaction.user.id})"
            )
            guild = interaction.guild
            self.tree.clear_commands(guild=guild)
            SyncUtils.add_commands_to_tree(self.tree, self.client, override=True)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            await interaction.followup.send("Commands synced", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Command sync failed: {e}", ephemeral=True)
            logging.info(f"Command sync failed: {e}")

    @app_commands.command(name="info")
    @app_commands.checks.has_any_role(
        MOD_ROLE, HIDDEN_MOD_ROLE, CHAT_MOD_ROLE, STAFF_DEVELOPER_ROLE
    )
    async def info(self, interaction: Interaction) -> None:
        """Display info on current bot uptime and commit hash"""
        uptime = str(
            datetime.timedelta(seconds=int(round(time.time() - UPTIME_START_TIME)))
        )

        hash = "Unavailable"
        try:
            hash = get_git_revision_short_hash()
        except Exception as e:
            LOG.error(f"Unable to get commit hash: {e}")

        message = f"Current bot uptime: {uptime} | Current bot commit hash: {hash}"
        await interaction.response.send_message(message, ephemeral=True)


def get_git_revision_short_hash() -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .decode("ascii")
        .strip()
    )
