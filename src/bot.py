from pathlib import Path

import disnake as ds
from disnake.ext import commands

from config import token

VERSION = "3.2.2026_1"

intents = ds.Intents.all()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    help_command=None,
    intents=intents,
    test_guilds=[1171730226741522432],
)



@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")


@bot.event
async def on_member_join(member):
    role = ds.utils.get(member.guild.roles, id=1201612717878935732)
    channel = bot.get_channel(1171730227173523476)  # member.guild.system_channel

    embed = ds.Embed(
        title="Новый участник!",
        description=f"{member.name}",
        color=0xffffff
    )

    await member.add_roles(role)
    if channel is not None:
        await channel.send(embed=embed)


# Загружаем матерные слова из файлов
def load_censored_words():
    censored = set()
    data_dir = Path(__file__).resolve().parent.parent / "data"
    try:
        with (data_dir / "swear-words-english.txt").open(
            "r",
            encoding="utf-8",
        ) as eng_file:
            for line in eng_file:
                word = line.strip()
                if word:
                    censored.add(word.lower())
    except FileNotFoundError:
        print("Файл swear-words-english.txt не найден.")

    try:
        with (data_dir / "swear-words-russian.txt").open(
            "r",
            encoding="utf-8",
        ) as rus_file:
            for line in rus_file:
                word = line.strip()
                if word:
                    censored.add(word.lower())
    except FileNotFoundError:
        print("Файл swear-words-russian.txt не найден.")

    return list(censored)


CENSORED_WORDS = load_censored_words()


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    message_content = message.content.lower().split()
    if any(word in CENSORED_WORDS for word in message_content):
        try:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} не выражайся так, будь культурным!"
            )
        except ds.Forbidden:
            await message.channel.send(
                f"{message.author.mention} не выражайся так, будь культурным!"
            )
        return

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для данной команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=ds.Embed(
            description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}`({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
        ))


# Команда для исключения пользователя
@bot.command(name="кик", administrator=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: ds.Member, *, reason="Нарушение правил."):
    await member.kick(reason=reason)


# Команда для бана пользователя
@bot.command(name="бан", administrator=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: ds.Member, *, reason="Нарушение правил."):
    await member.ban(reason=reason)


@bot.command()
async def data(ctx, * args):
    await ctx.reply(args)


@bot.command(name="пинг")
async def ping(ctx):
    latency_ms = round(bot.latency * 1000)
    await ctx.send(f"Pong! {latency_ms}ms")


@bot.command(name="версия")
async def version(ctx):
    await ctx.send(f"Версия бота: {VERSION}")


@bot.command(name="помощь")
async def help_command(ctx):
    await ctx.send(
        "Команды: !пинг, !версия, !помощь, !сумма <num1> <num2>, /calc"
    )


@bot.command(name="сумма", usage="sum <num1> <num2>")
async def sum_numbers(ctx, num1, num2):
    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        await ctx.send("Error")
        return
    result = num1 + num2
    await ctx.send(result)


@bot.slash_command(description="Обычный калькулятор")
async def calc(inter, a: int, oper: str, b: int):
    if oper == "+":
        result = a + b
    elif oper == "-":
        result = a - b
    elif oper == "*":
        result = a * b
    elif oper == "/":
        if b == 0:
            await inter.send("Ошибка: деление на ноль.")
            return
        result = a / b
    elif oper == "**":
        result = a ** b
    else:
        result = "Неверный оператор. Error 001"

    await inter.send(str(result))

bot.run(token)
