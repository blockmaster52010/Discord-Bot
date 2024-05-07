import discord
from discord.ext import commands
import random as random_mod

intents = discord.Intents.all()
intents.members = True
intents.guilds = True

client = commands.Bot(intents=intents, command_prefix=";")
client.remove_command("help")

@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity=discord.Game("Waiting For Command."))

@client.command()
async def add(ctx, a, b):
    await ctx.send(f"{float(a) + float(b)}")
    
@client.command()
async def subtract(ctx, a, b):
    await ctx.send(f"{float(a) - float(b)}")

@client.command()
async def mutiply(ctx, a, b):
    await ctx.send(f"{float(a) * float(b)}")

@client.command()
async def divide(ctx, a, b):
    await ctx.send(f"{float(a) / float(b)}")

@client.command()
async def random(ctx):
    await ctx.send(f"{random_mod.random()}")

@client.command()
async def remap(ctx, start, stop, new_start, new_stop, value):
    start, stop, new_start, new_stop, value = float(start), float(stop), float(new_start), float(new_stop), float(value)
    da = abs(start - stop)
    db = abs(new_start - new_stop)
    value *= db/da
    value += new_start - start 
    await ctx.send(f"{value}")

@client.command()
async def get_role(ctx):
    role = discord.utils.get(ctx.author.guild.roles, name="Member")
    await ctx.author.add_roles(role)

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Guest")
    channel = client.get_channel(<id>)
    await channel.send(f"Hello, {member.mention}!")
    await member.add_roles(role)



client.run("<token>")
