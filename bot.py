import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- DISCORD SETUP ----------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

USER_MAP = {
    "643833470329552896": "Cat",
    "364035221458255873": "Alex",
    "467843817513680896": "Amos",
    "461691395208380426": "Raymond",
    "1101971726973284373": "Annika",
    "447831993229639690": "Allen",
    "990791466458677289": "Chelsy",
    "733710117509398600": "Sora", 
    "583952488277868549": "Joyce",
    "704803971369533522": "Chris",
    "698735433646866504": "Peyton", 
    "879062143113261127": "Jayden",
    "374691703703076874": "Brad",
    "332158564418322433": "Sean",
    "710585332361461891": "Laura",
}

# ---------------- GOOGLE SHEETS SETUP ----------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

SHEET_ID = "1hkRisUFg4xvku6xsom9opi6YezMQQKG-7bDrNud-k-A"
sheet = client.open_by_key(SHEET_ID).sheet1


# ---------------- HELPERS ----------------

def get_name(member: discord.Member):
    return USER_MAP[str(member.id)]


def find_row(name):
    data = sheet.get_all_values()
    for i, row in enumerate(data, start=1):
        if row and row[0] == name:
            return i
    return None


def ensure_user(member: discord.Member):
    name = get_name(member)
    row = find_row(name)

    if row is None:
        sheet.append_row([name, 0, 0])


# ---------------- COMMANDS ----------------

@bot.command()
async def sniped(ctx, user: discord.Member):
    ensure_user(ctx.author)
    ensure_user(user)

    shooter_name = get_name(ctx.author)
    target_name = get_name(user)

    shooter_row = find_row(shooter_name)
    target_row = find_row(target_name)

    if shooter_row is None or target_row is None:
        await ctx.send("❌ User not found in sheet.")
        return

    shooter_sniped = int(sheet.cell(shooter_row, 2).value or 0)
    sheet.update_cell(shooter_row, 2, shooter_sniped + 1)

    target_got = int(sheet.cell(target_row, 3).value or 0)
    sheet.update_cell(target_row, 3, target_got + 1)

    await ctx.send(f"📸 {shooter_name} sniped {target_name}!")


@bot.command()
async def revoke(ctx, user: discord.Member, kind: str):
    ensure_user(user)

    name = get_name(user)
    row = find_row(name)

    if row is None:
        await ctx.send("User not found.")
        return

    if kind.lower() == "snipe":
        col = 2
    elif kind.lower() in ["gotsniped", "got"]:
        col = 3
    else:
        await ctx.send("Use `snipe` or `gotsniped`")
        return

    current = int(sheet.cell(row, col).value or 0)
    sheet.update_cell(row, col, max(0, current - 1))

    await ctx.send(f"🔁 Revoked {kind} from {user.mention}")


@bot.command()
async def stats(ctx, user: discord.Member = None):
    user = user or ctx.author

    name = get_name(user)

    ensure_user(user)
    row = find_row(name)

    if row is None:
        await ctx.send("User not found.")
        return

    sniped = sheet.cell(row, 2).value
    got = sheet.cell(row, 3).value

    await ctx.send(
        f"📊 Stats for {name}\n"
        f"Sniped: {sniped}\n"
        f"Got Sniped: {got}"
    )
    

@bot.command()
async def leaderboard(ctx):
    data = sheet.get_all_values()[1:]  # skip header if you have one

    leaderboard_sniped = []
    leaderboard_got = []

    for row in data:
        if len(row) < 3:
            continue

        name = row[0]
        try:
            sniped = int(row[1])
        except:
            sniped = 0

        try:
            got = int(row[2])
        except:
            got = 0

        leaderboard_sniped.append((name, sniped))
        leaderboard_got.append((name, got))

    leaderboard_sniped.sort(key=lambda x: x[1], reverse=True)
    leaderboard_got.sort(key=lambda x: x[1], reverse=True)

    top_sniped = "\n".join(
        [f"{i+1}. {name} — {val}" for i, (name, val) in enumerate(leaderboard_sniped[:10])]
    )

    top_got = "\n".join(
        [f"{i+1}. {name} — {val}" for i, (name, val) in enumerate(leaderboard_got[:10])]
    )

    await ctx.send(
        "🏆 **SNIPE LEADERBOARD** 🏆\n\n"
        "📸 Most Snipes:\n"
        f"{top_sniped}\n\n"
        "🎯 Most Times Sniped:\n"
        f"{top_got}"
    )


# ---------------- RUN BOT ----------------
bot.run(os.getenv("DISCORD_TOKEN"))