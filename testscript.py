# Бот на disnake
import disnake
import disnake as ds
from disnake.ext import commands

from testdatabot import token

intents = ds.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!",help_command=None ,intents=disnake.Intents.all(), test_guilds=[1171730226741522432])



@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")


@bot.event
async def on_member_join(member):
    role = ds.utils.get(member.guild.roles, id=1201612717878935732)
    channel = bot.get_channel(1171730227173523476) #member.guild.system_channel

    embed = ds.Embed(
        title="Новый участник!",
        description=f"{member.name}",
        color=0xffffff
    )

    await member.add_roles(role)
    await channel.send(embed=embed)


# Загружаем матерные слова из файлов
def load_censored_words():
    censored = set()
    try:
        with open("swear-words-english.txt", "r", encoding="utf-8") as eng_file:
            for line in eng_file:
                word = line.strip()
                if word:
                    censored.add(word.lower())
    except FileNotFoundError:
        print("Файл swear-words-english.txt не найден.")

    try:
        with open("swear-words-russian.txt", "r", encoding="utf-8") as rus_file:
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
    await bot.process_commands(message)

    message_content = message.content.lower().split()
    for word in message_content:
        if word in CENSORED_WORDS:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention} не выражайся так, будь культурным!")
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


#Команда для исключения пользователя
@bot.command(name="кик", administrator=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: ds.Member, *, reason="Нарушение правил."):
    await member.kick(reason=reason)


#Команда для бана пользователя
@bot.command(name="бан", administrator=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: ds.Member, *, reason="Нарушение правил."):
    await member.ban(reason=reason)


@bot.command(name="жумайсынба")
async def zhumaisinba(ctx):
    await ctx.reply(f"Шампунь ЖУМАЙСЫНБА, скажи перхоти, я еб@л негров!")


@bot.command()
async def data(ctx, * args):
    await ctx.reply(args)


@bot.command(name="сумма", usage="sum <num1> <num2>")
async def sum(ctx, num1, num2):
    try:
        num1 = float(num1)
        num2 = float(num2)
    except:
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
