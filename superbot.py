import discord
import random
from discord.ext import commands
import requests


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
API_KEY = "2b350a87de1accceaaa66f9966efb1fe"


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

class CustomHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot

        embed = discord.Embed(title='Список команд', description='Список доступных команд', color=discord.Color.green())
        command_list = [f"`{command.name}` - {command.help or 'Описание отсутствует'}" for command in bot.commands]
        
        if command_list:
            embed.add_field(name="Команды", value='\n'.join(command_list), inline=False)
        else:
            embed.description = 'Нет доступных команд.'

        await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    """Начать тест"""
    questions = {
        "1. Как называется процесс увеличения температуры земной атмосферы?": "Глобальное потепление",
        "2. Что означает акроним ЧС?": "Чрезвычайная ситуация",
        "3. Какое действие может помочь уменьшить выбросы углекислого газа?": "Использование общественного транспорта",
        "4. Что является основной причиной глобального потепления?": "Выброс углекислого газа в атмосферу",
        "5. Какая основная экологическая проблема связана с уничтожением лесов?": "Вымирание видов",
        "6. Какое количество пластиковых отходов попадает в океаны ежегодно?": "500 тыс. пластикового мусора",
        "7. Что такое эффект парникового газа?": "Удерживание тепла в атмосфере",
        "8. Какие виды транспорта считаются наиболее экологичными?": "Электрокары и самокаты",
        "9. Какой вид энергии считается экологически чистым?": "Ветряная энергия",
        "10. Какое действие помогает уменьшить загрязнение воды?": "Утилизация и переработка отходов"
    }

    # Отправляем пользователю первый вопрос
    await ctx.send("Давайте начнем тест! Ответьте на следующие вопросы:")

    correct_answers = 0

    for question, correct_answer in questions.items():
        await ctx.send(question)
        try:
            answer = await bot.wait_for('message', timeout=30, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("Время вышло!")
            return

        if answer.content.lower() == correct_answer.lower():
            await ctx.send("Правильно!")
            correct_answers += 1
        else:
            await ctx.send(f"Неправильно. Правильный ответ: {correct_answer}")

    await ctx.send(f"Тест завершен! Вы ответили правильно на {correct_answers} из {len(questions)} вопросов.")



bot.help_command = CustomHelpCommand()
@bot.command()
async def info(ctx):
    """Команда для получения информации о глобальном потеплении"""
    additional_info = [
    "Глобальное потепление может привести к участию распространения инфекционных заболеваний.",
    "Одним из последствий глобального потепления является таяние ледников и айсбергов.",
    "Изменение климата может привести к снижению биоразнообразия и вымиранию многих видов животных.",
    "Глобальное потепление может вызвать повышение уровня мирового океана из-за таяния льдов и термического расширения воды.",
    "С увеличением температуры участились катастрофические погодные явления, такие как ураганы, засухи и наводнения.",
    "Кислотность океанов: Увеличение концентрации углекислого газа в атмосфере приводит к увеличению кислотности океанов. Это может негативно повлиять на морскую жизнь, включая коралловые рифы и различные виды морской фауны.",
    "Угроза экономике: Глобальное потепление может оказать серьезное воздействие на мировую экономику из-за повреждений инфраструктуры, потери рабочих мест и ухудшения условий для бизнеса.",
    "Необходимость совместных усилий: Решение проблемы глобального потепления требует совместных усилий и сотрудничества со стороны различных стран и международных организаций."
    ]
    await ctx.send(random.choice(additional_info))

@bot.command()
async def password(ctx, password_len: int = 8):
    '''Генератор пароля'''
    a = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ''
    
    if password_len <= 0:
        await ctx.send("Ошибка: 404 (необходимо написать положительное число, которое больше 0)")

    for i in range(password_len):
        password += random.choice(a)

    await ctx.send(password)



@bot.command()
async def links(ctx):
    """Команда для получения полезных источников"""
    links = [
        f"https://ru.wikipedia.org/wiki/%D0%93%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5_%D0%BF%D0%BE%D1%82%D0%B5%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5",
        "https://www.nationalgeographic.com/environment/article/global-warming-overview",
        "https://www.nationalgeographic.com/environment/article/global-warming-solutions",
        "https://earthobservatory.nasa.gov/features/GlobalWarming",
        "https://davidsuzuki.org/our-work/climate-solutions/?gclid=CP6eh4uc6a0CFQXCKgodETKn4g",
        "https://skepticalscience.com/",
        "https://wmo.int/",
        "https://www.c2es.org/",
        "https://science.nasa.gov/earth"
    ]
    await ctx.send(random.choice(links))

@bot.command()
async def weather(ctx, city):
    """Показывает текущую погоду в указанном городе"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Можно использовать "imperial" для температуры в Фаренгейтах
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        city_name = weather_data['name']
        
        message = f"Текущая погода в {city_name}: {temperature}°C, {description}"
        await ctx.send(message)
    else:
        await ctx.send("Не удалось получить данные о погоде. Пожалуйста, попробуйте позже.")


@bot.command()
async def solutions(ctx):
    """Команда для получения советов по борьбе с ГП"""
    advice = [
        "- Сокращение использования и выбросов ископаемых топлив",
        "- Переход на возобновляемые источники энергии",
        "- Энергоэффективность: улучшение изоляции зданий, использование энергоэффективных технологий",
        "- Поддержка и использование общественного транспорта или электромобилей",
        "- Энергоэффективность в домашних условиях:",
        "- Эффективное использование воды:",
        "- Уменьшение использования пластика:",
        "- Поддержка экологических инициатив:"

    ]
    await ctx.send(random.choice(advice))

@bot.command()
async def meme(ctx):
    """Статьи и мемы про экологию от Реддит сообщества"""
    subreddit = "ecology"
    url = f"https://www.reddit.com/r/{subreddit}/random.json"
    
    headers = {
        "User-Agent": "Discord bot by greenushtaf (Green Bot)"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        meme_url = data[0]['data']['children'][0]['data']['url']
        await ctx.send(meme_url)
    else:
        await ctx.send("ERROR404")

@bot.command()
async def voice(ctx, channel_name):
    """Создает голосовой канал"""
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    if not existing_channel:
        await guild.create_voice_channel(channel_name)
        await ctx.send(f"Голосовой канал {channel_name} успешно создан.")
    else:
        await ctx.send("Канал с таким именем уже существует.")


bot.run("MTEwOTM4MjcwMTMzMDQ4NTMyOA.GMpRYZ.3LF1uqaIvDuAJgdc9OETYWRyEio2dBp8_YZ0dQ")