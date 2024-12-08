import discord
from discord.ext import commands
from datetime import datetime, timedelta

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='+', intents=intents)

service_start_times = {}
service_durations = {}

CHANNEL_ID_SPECIFIQUE = 1233012519719800865  # ID salon
ROLE_LSPD = "test"  # rôle

@bot.event
async def on_ready():
    print(f'{bot.user} est prêt et connecté.')

@bot.command(name='service')
async def service(ctx):
    user_id = ctx.author.id
    current_time = datetime.now()

    if user_id in service_start_times:
        embed = discord.Embed(
            title="⚠️ Erreur",
            description=f"{ctx.author.mention}, vous êtes déjà en service.",
            color=discord.Color.red()
        )
    else:
        service_start_times[user_id] = current_time
        embed = discord.Embed(
            title="✅ Début de service",
            description=f"{ctx.author.mention} est maintenant en service.\nHeure de début : {current_time.strftime('%H:%M:%S')}",
            color=discord.Color.green()
        )
    await ctx.send(embed=embed)

@bot.command(name='finservice')
async def fin_service(ctx):
    user_id = ctx.author.id
    if user_id not in service_start_times:
        embed = discord.Embed(
            title="⚠️ Erreur",
            description=f"{ctx.author.mention}, vous n'êtes pas en service.",
            color=discord.Color.red()
        )
    else:
        current_time = datetime.now()
        start_time = service_start_times.pop(user_id)
        duration = current_time - start_time

        if user_id not in service_durations:
            service_durations[user_id] = timedelta()
        service_durations[user_id] += duration

        embed = discord.Embed(
            title="📈 Fin de service",
            description=(
                f"{ctx.author.mention} a quitté le service.\n"
                f"Durée de cette session : {str(duration)}\n"
                f"Total aujourd'hui : {str(service_durations[user_id])}"
            ),
            color=discord.Color.blue()
        )
    await ctx.send(embed=embed)

@bot.command(name='temps_service')
async def temps_service(ctx):
    user_id = ctx.author.id
    if user_id in service_durations:
        total_duration = service_durations[user_id]
        embed = discord.Embed(
            title="⏳ Temps de service total",
            description=f"{ctx.author.mention}, votre temps total de service est de {str(total_duration)}.",
            color=discord.Color.purple()
        )
    else:
        embed = discord.Embed(
            title="⏳ Temps de service",
            description=f"{ctx.author.mention}, vous n'avez pas encore de temps de service enregistré.",
            color=discord.Color.purple()
        )
    await ctx.send(embed=embed)

@bot.command(name='renfort')
async def renfort(ctx, niveau: str):
    channel = bot.get_channel(CHANNEL_ID_SPECIFIQUE)
    role = discord.utils.get(ctx.guild.roles, name=ROLE_LSPD)

    if not role:
        embed = discord.Embed(
            title="⚠️ Erreur",
            description="Le rôle LSPD est introuvable.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title="🚨 Demande de renfort",
        description=(
            f"{ctx.author.mention} a demandé des renforts de niveau {niveau}.\n"
            f"{role.mention}, veuillez intervenir."
        ),
        color=discord.Color.red()
    )
    await channel.send(embed=embed)
    await ctx.send(f"{ctx.author.mention}, la demande de renfort a été envoyée avec succès.")

# Commande pour envoyer un message radio
@bot.command(name='radio')
async def radio(ctx, *, message: str):
    embed = discord.Embed(
        title="📻 Communication radio",
        description=f"{ctx.author.mention} : {message}",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

@bot.command(name='radio_alert')
async def radio_alert(ctx, *, message: str):
    embed = discord.Embed(
        title="🔊 Alerte radio",
        description=f"{ctx.author.mention} : {message}",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command(name='rapport')
async def rapport(ctx, *, contenu: str):
    channel = bot.get_channel(CHANNEL_ID_SPECIFIQUE)
    embed = discord.Embed(
        title="📝 Rapport de mission",
        description=f"Rapport soumis par {ctx.author.mention} :\n{contenu}",
        color=discord.Color.green()
    )
    await channel.send(embed=embed)
    await ctx.send(f"{ctx.author.mention}, votre rapport a été envoyé.")

# Lancement du bot
bot.run('token discord ')
