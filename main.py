import os
import discord
from discord.ext import commands
from discord.ui import View, Button
from keep_alive import keep_alive

# Remplace avec les vrais IDs
LOG_CHANNEL_ID = 1363681263281770526
ROLE_IDS_TO_MENTION = [
    1363698665239089245,  # Rôle 1
    1363700530442145842,  # Rôle 2
    1364015052121964576   # Rôle 3
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class BCButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ RAS", style=discord.ButtonStyle.success, custom_id="btn_ras")
    async def ras(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_report(interaction, "✅ Rien à signaler", alert=False)

    @discord.ui.button(label="⚠️ N°1", style=discord.ButtonStyle.danger, custom_id="btn_1")
    async def danger1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_report(interaction, "⚠️ N°1 - Assaut en cours (Wither)", alert=True)

    async def send_report(self, interaction: discord.Interaction, message: str, alert: bool):
        user = interaction.user.name
        role_mentions = " ".join([f"<@&{role_id}>" for role_id in ROLE_IDS_TO_MENTION]) if alert else ""
        full_message = f"**{message}**\n🔍 Vérifiée par **{user}**\n{role_mentions}"

        # Supprime l'affichage de message dans le salon d'origine
        await interaction.response.defer(ephemeral=True)  # juste pour dire que le bouton a été cliqué

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(full_message)


@bot.command(name="bcpanel")
async def send_buttons(ctx):
    embed = discord.Embed(title="Interface BC", color=discord.Color.dark_gray())
    embed.description = (
        "*Différents boutons sont disponibles lors des rondes autour de la base claim,*\n"
        "*veuillez sélectionner un bouton une fois que vous avez fait le tour de la base claim.*\n\n"
        "[**Liste des boutons**](https://google.com) :\n\n"
        "✅ **RAS - Rien à signaler.**\n"
        "⚠️ **N°1 - Assaut en cours (Wither) ping everyone automatiquement**\n"
        "*Un message s'affichera dans le channel ci-dessous lorsque vous aurez sélectionné l’un des boutons.*"
    )
    await ctx.send(embed=embed, view=BCButtons())


# Démarrage
keep_alive()
bot.run(os.getenv("TOKEN"))