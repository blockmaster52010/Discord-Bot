import sqlite3 as sql
import discord
from discord.ext import commands
import random as random_mod
from PIL import Image, ImageDraw, ImageFont
import os

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

@client.event
async def on_member_join(member):
    name: str = member.name
    conn = sql.connect("bot_memory.db")
    cursor = conn.cursor()
    if len(cursor.execute("SELECT * FROM Rock_Paper_Scissors WHERE User = ?", (name,)).fetchall()) > 0:
         cursor.execute("DELETE FROM Rock_Paper_Scissors WHERE User = ?", (name,))
    cursor.execute(f"INSERT INTO Rock_Paper_Scissors (User, Wins, Losses) VALUES (?,?,?)", (name, 0, 0))
    role = discord.utils.get(member.guild.roles, name="Guest")
    channel = client.get_channel(1235728615329628205)
    await channel.send(f"Hello, {member.mention}!")
    await member.add_roles(role)
    conn.commit()
    conn.close()

@client.command()
async def RPS(ctx, pick):
    name = ctx.author.name
    conn = sql.connect("bot_memory.db")
    await ctx.send(rock_paper_scissors(pick, conn, name))
    conn.commit()
    conn.close()
    

@client.command()
async def dice(ctx, sides: str, winning_number: str):
    text_choice: list[str] = ["You Lose!", "You Win!"]
    number = random_mod.randint(1, int(sides))
    await ctx.send(f"Winning Side: {int(winning_number)} \nYour Side: {number} \n{text_choice[int(number == int(winning_number))]}")
    
@client.command()
async def create_image(ctx):
    image = Image.new("RGB", (600, 400), color='white')
    draw = ImageDraw.Draw(image)
    draw.ellipse((300, 200), (55, 255, 100))
    img_path = 'white.png'
    image.save(img_path)
    await ctx.send(file=discord.File(img_path))
    os.remove(img_path)

@client.command()
async def image(ctx):
    embed = discord.Embed(title="Heres Your Image")
    embed.set_image(url="https://m.media-amazon.com/images/I/71nwE3uVB7L._AC_UY1000_.jpg")
    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if message.content.lower() == "pls kick me":
        await message.author.kick(reason="you asked")
    await client.process_commands(message)


@client.command()
async def get_role(ctx):
    name = ctx.author.name
    conn = sql.connect("bot_memory.db")
    cursor = conn.cursor()
    role = discord.utils.get(ctx.author.guild.roles, name="Member")
    if cursor.execute("SELECT Wins FROM Rock_Paper_Scissors WHERE User = ?", (name,)).fetchall()[0][0] >= 20:
        await ctx.author.add_roles(role)

def rock_paper_scissors(pick: str, conn, name) -> str:
    pick.lower()
    table = {
        "rock": 0,
        "paper": 1,
        "scissors": 2
    }
    reverse = ["rock", "paper", "scissors"]
    winning_type = ["Tie", "Bot wins", "Player wins"]
    player = table[pick]
    bot = random_mod.randint(0,2)
    match player:
        case 0:
            match bot:
                case 0:
                    winner =  0
                case 1:
                    winner = 1
                case 2:
                    winner = 2
        case 1:
            match bot:
                case 0:
                    winner = 2
                case 1:
                    winner = 0
                case 2:
                    winner = 1
        case 2:
            match bot:
                case 0:
                    winner = 1
                case 1:
                    winner = 2
                case 2:
                    winner = 0
    
    cursor = conn.cursor()
    if winner == 1:
        cursor.execute("UPDATE Rock_Paper_Scissors SET Losses = Losses + ? WHERE User = ?", (1, name))
    elif winner == 2:
        cursor.execute("UPDATE Rock_Paper_Scissors SET Wins = Wins + ? WHERE User = ?", (1, name))
    return f"Player Choice: {pick} \nBot Choice: {reverse[bot]} \nOutcome: {winning_type[winner]}"

client.run("<token>")
