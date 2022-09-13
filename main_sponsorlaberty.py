#from webserver import keep_alive
import sqlite3
import time
import discord
import asyncio
import os
from discord import Spotify
from discord.ext import commands
from asyncio import sleep
from datetime import datetime, date, time
from dislash import InteractionClient, Option, OptionType, Button, ButtonStyle, ActionRow

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="ll.",intents=discord.Intents.all())
bot.remove_command("help")
connection = sqlite3.connect('data/server.db')
cursor = connection.cursor()
inter_client = InteractionClient(bot)

@bot.event
async def on_ready():
	cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        warns INT,
    	voice_time INT
    )""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS sponsors (
        name TEXT,
        id INT,
        priority INT,
        uses_mute INT,
    	uses_ban INT,
    	uses_unmute INT,
    	uses_unban INT,
    	sp_date TEXT
    )""")
	for guild in bot.guilds:
		for member in guild.members:
			if cursor.execute(f"SELECT id FROM sponsors WHERE id = {member.id}").fetchone() is None:
				sp_date = datetime.now().strftime("%y%m%d%H%M")
				cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, '{sp_date}')")
				for r in member.roles:
					if r.id == 1005118227086573742 or r.id == 1001211749481070782:
						cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 1, 0, 0, 0, 0, '{sp_date}')")
					elif r.id == 1005512983436333076 or r.id == 1001211750965846026:
						cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 2, 0, 0, 0, 0, '{sp_date}')")
					elif r.id == 1005118220421828648 or r.id == 1001211752249315369:
						cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 3, 0, 0, 0, 0, '{sp_date}')")
					elif r.id == 1005118206681305108 or r.id == 1001211754073829547:
						cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 4, 0, 0, 0, 0, '{sp_date}')")
					else:
						cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, '{sp_date}')")
					if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
						date_sp = cursor.execute("SELECT sp_date FROM sponsors WHERE id = {}".format(member.id)).fetchone()[0]
						year = datetime.now().strftime("%y")
						mon = datetime.now().strftime("%m")
						month = int(mon)+1
						day = datetime.now().strftime("%d")
						hours = datetime.now().strftime("%H")
						minutes = datetime.now().strftime("%M")
						d = f"{year}{month}{day}{hours}{minutes}"
						if int(d) >= int(date_sp):
							if r.id == 1005118227086573742 or r.id == 1001211749481070782:
								cursor.execute("UPDATE sponsors SET uses_mute = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_ban = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_unmute = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_unban = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET sp_date = {} WHERE id = {}".format(d,member.id))
								await member.send("Вам снова доступны все функции спонсора!")
							elif r.id == 1005512983436333076 or r.id == 1001211750965846026:
								cursor.execute("UPDATE sponsors SET uses_mute = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_ban = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_unmute = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_unban = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET sp_date = {} WHERE id = {}".format(d,member.id))
								await member.send("Вам снова доступны все функции спонсора!")
							elif r.id == 1005118220421828648 or r.id == 1001211752249315369:
								cursor.execute("UPDATE sponsors SET uses_mute = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_ban = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_unmute = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_unban = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET sp_date = {} WHERE id = {}".format(d,member.id))
							elif r.id == 1005118206681305108 or r.id == 1001211754073829547:
								cursor.execute("UPDATE sponsors SET uses_mute = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_ban = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_unmute = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET uses_unban = 0 WHERE id = {}".format(member.id))
								cursor.execute("UPDATE sponsors SET sp_date = {} WHERE id = {}".format(d,member.id))
								await member.send("Вам снова доступны все функции спонсора!")
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0)")
				print(f"Пользователь {member} был записан в БД users")
			else:
				pass
			connection.commit()
	print("БОТ АКТИВЕН !")
	
@bot.listen()
async def on_ready():
    channel = bot.get_channel(1019150040335400962)
    while True:
        time.sleep(14400) 
        embed=discord.Embed(title=f"Внимание Стафф <@999016710990479480>,<@&999016710973689943> ,<@&999016710973689944>,<@&999016710973689942>, !!!", description="Используйте Команду: ``/up или /bump``", color=0x73d216)
        await channel.send(embed=embed)

@bot.event 
async def on_member_join(member):
	sp_date = datetime.now().strftime("%y%m%d%H%M")
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0)")
		print(f"Пользователь {member} был записан в БД users")
	else:
		pass
	if cursor.execute(f"SELECT id FROM sponsors WHERE id = {member.id}").fetchone() is None:
		for r in member.roles:
			if r.id == 1005118227086573742 or r.id == 1001211749481070782:
				cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 1, 0, 0, 0, 0, '{sp_date}')")
			elif r.id == 1005512983436333076 or r.id == 1001211750965846026:
				cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 2, 0, 0, 0, 0, '{sp_date}')")
			elif r.id == 1005118220421828648 or r.id == 1001211752249315369:
				cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 3, 0, 0, 0, 0, '{sp_date}')")
			elif r.id == 1005118206681305108 or r.id == 1001211754073829547:
				cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 4, 0, 0, 0, 0, '{sp_date}')")
			else:
				cursor.execute(f"INSERT INTO sponsors VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, '{sp_date}')")
	connection.commit()
@inter_client.slash_command(
    description="Посмотреть информацию",
    options=[
        Option("arg", "Введите о чем хотите посмотреть информацию",required=True),
	    Option("user", "Введите пользователя",OptionType.USER,required=False)
    ]
)
async def info(inter,arg,user=None):
	if arg == "user":
		if user is None:
			file = open(f"data/{inter.author.id}.txt","w")
			embed = discord.Embed(title=f":green_circle: Информация о {inter.author}",color=inter.author.color)
			embed.add_field(name="Полное имя",value=f"{inter.author}")
			embed.add_field(name="ID пользователя",value=f"{inter.author.id}")
			embed.add_field(name="Присоединился к серверу",value=f"""{inter.author.joined_at.strftime("%d.%m.%y")}""")
			embed.add_field(name="Аккаунт создан",value=f"""{inter.author.created_at.strftime("%d.%m.%y")}""")
			embed.add_field(name="Отображаемый цвет",value=f"{inter.author.color}")
			for role in inter.author.roles:
				if "everyone" in f"{role}":
					pass
				else:
					if role is None:
						file.write("Отсуствует")
					else:
						file.write(f" {role.mention} ")
					
			file.close()
			file = open(f"data/{inter.author.id}.txt","r")
			roles = file.read()
			activities = []
			for activity in inter.author.activities:
				if isinstance(activity, discord.CustomActivity):
					activities.append("**Custom Status**")
				if isinstance(activity, Spotify):
					activities.append("**Слушает** ***Spotify***")
			if roles == '':
				roles = "Отсуствует"
			else:
				roles = roles
			embed.add_field(name=f"Ролей ({len(inter.author.roles)-1})",value=f"{roles}")
			if len(inter.author.activities) == 0:
				pass
			else:
				if len(activities) == 2:
					a = f"{activities[0]}\n{activities[1]}"
				else:
					a = activities[0]
				embed.add_field(name=f"Активности ({len(inter.author.activities)})",value=f"{a}")
			embed.set_thumbnail(url=inter.author.avatar_url)
			await inter.reply(embed=embed)
		else:
			file = open(f"data/{user.id}.txt","w")
			embed = discord.Embed(title=f":green_circle: Информация о {user}",color=user.color)
			embed.add_field(name="Полное имя",value=f"{user}")
			embed.add_field(name="ID пользователя",value=f"{user.id}")
			embed.add_field(name="Присоединился к серверу",value=f"""{user.joined_at.strftime("%d.%m.%y")}""")
			embed.add_field(name="Аккаунт создан",value=f"""{user.created_at.strftime("%d.%m.%y")}""")
			embed.add_field(name="Отображаемый цвет",value=f"{user.color}")
			for role in user.roles:
				if "everyone" in f"{role}":
					pass
				else:
					if role is None:
						file.write("Отсуствует")
					else:
						file.write(f" {role.mention} ")
					
			file.close()
			file = open(f"data/{user.id}.txt","r")
			roles = file.read()
			activities = []
			for activity in user.activities:
				if isinstance(activity, discord.CustomActivity):
					activities.append("**Custom Status**")
				if isinstance(activity, Spotify):
					activities.append("**Слушает** ***Spotify***")
			if roles == '':
				roles = "Отсуствует"
			else:
				roles = roles
			embed.add_field(name=f"Ролей ({len(user.roles)-1})",value=f"{roles}")
			if len(user.activities) == 0:
				pass
			else:
				if len(activities) == 2:
					a = f"{activities[0]}\n{activities[1]}"
				else:
					a = activities[0]
				embed.add_field(name=f"Активности ({len(user.activities)})",value=f"{a}")
			embed.set_thumbnail(url=user.avatar_url)
			await inter.reply(embed=embed)
@inter_client.slash_command(description="Помощь по спонсорским командам")
async def sponsorhelp(inter):
	embed = discord.Embed(title=f"Помощь по командам",color=inter.author.color)
	embed.add_field(name="Мут",value="``/sponsormute [ник] [время (максимум 24h)] [причина]``")
	embed.add_field(name="Бан",value="``/sponsorban [ник] [время (максимум 24h)] [причина]``")
	embed.add_field(name="Размут",value="``/sponsorunmute [ник] [причина]``")
	embed.add_field(name="Разбан",value="``/sponsorunban [ник] [причина]``")
	embed.add_field(name="Создать персональную роль",value="``/role [название роли] [Цвет в HEX формате (необязательно)]``")
	embed.add_field(name="Удалить персональную роль",value="``/delrole [название роли]``")
	embed.add_field(name="Информация о пользователе",value="``/info user [ник (необязательно)]``")
	await inter.reply(embed=embed)

@inter_client.slash_command(
    description="Замутить пользователя на определенное время (платная функция)",
    options=[
        Option("user", "Введите пользователя которого хотите замутить",OptionType.USER,required=True),
        Option("time", "Введите время на которое хотите замутить пользователя",required=True),
        Option("reason", "Введите причину по которой хотите замутить пользователя",required=True)
    ]
)
async def sponsormute(inter, user, time, *, reason):
	access = False
	if os.path.exists(f"data/sponsors/{inter.author.id}.txt"):
		file = open(f"data/roles/{inter.author.id}.txt","r")
		f = file.read()
		for r in inter.author.roles:
			if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
				if f"{r.id}" in f"{f}":
					access = True
					sponsor_role = r.id
		file.close()
	else:
		file = open(f"data/roles/{inter.author.id}.txt","w")
		for r in inter.author.roles:
			if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
				file.write(str(r.id))
				access = True
				sponsor_role = r.id

		file.close()
	if access:
		for rr in user.roles:
			if rr == 1005118227086573742 or rr.id == 1005512983436333076 or rr.id == 1005118220421828648 or rr.id == 1005118206681305108 or rr.id == 1001211749481070782 or rr.id == 1001211750965846026 or rr.id == 1001211752249315369 or rr.id == 1001211754073829547:
				access = False
			else:
				access = True
		if access:
			mute_role = 1001096168039792700
			if sponsor_role == 1005118227086573742 or sponsor_role == 1001211749481070782:
				if cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 4:
					embed = discord.Embed(title=f"Мут",description=f'Вы уже потратили ``4`` мута, ждите следующего месяца.\nВы можете купить ***Основной спонсор*** и сможете мутить ``8`` раз',color=inter.author.color)
					await inter.send(embed = embed)
					print("Потрачено максимальное кол-во мутов")
				else:
					print(f"{inter.author} Удачный мут пользователя {user}")
					if "s" in time:
						if int(time[:-1]) > 86400:
							await inter.send("Максимальное время мута 24 часа!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` секунд по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]))
							await user.remove_roles(role)
					elif "m" in time:
						if int(time[:-1]) > 1440:
							await inter.send("Максимальное время мута 24 часа!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` минут по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60)
							await user.remove_roles(role)
					elif "h" in time:
						if int(time[:-1]) > 24:
							await inter.send("Максимальное время мута 24 часа!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` часов по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60 * 60)
							await user.remove_roles(role)
			elif sponsor_role == 1005512983436333076 or sponsor_role == 1001211750965846026:
				if cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 8:
					embed = discord.Embed(title=f"Мут",description=f'Вы уже потратили ``8`` мутов, ждите следующего месяца.\nВы можете купить ***Алмазный спонсор*** и сможете мутить ``15`` раз',color=inter.author.color)
					await inter.send(embed = embed)
				else:
					await inter.channel.purge(limit=1)
					if "s" in time:
						if int(time[:-1]) > 604800:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` секунд по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]))
							await user.remove_roles(role)
					elif "m" in time:
						if int(time[:-1]) > 10080:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` минут по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60)
							await user.remove_roles(role)
					elif "h" in time:
						if int(time[:-1]) > 168:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` часов по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60 * 60)
							await user.remove_roles(role)
					elif "d" in time:
						if int(time[:-1]) > 7:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` дней по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM users WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60 * 60 * 24)
							await user.remove_roles(role)
			elif sponsor_role == 1005118220421828648 or sponsor_role == 1001211752249315369:
				if cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 15:
					embed = discord.Embed(title=f"Мут",description=f'Вы уже потратили ``15`` мутов, ждите следующего месяца.\nВы можете купить ***Админ спонсор*** и сможете мутить ``20`` раз',color=inter.author.color)
					await inter.send(embed = embed)
				else:
					await inter.channel.purge(limit=1)
					if "s" in time:
						if int(time[:-1]) > 604800:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` секунд по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]))
							await user.remove_roles(role)
					elif "m" in time:
						if int(time[:-1]) > 10080:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` минут по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60)
							await user.remove_roles(role)
					elif "h" in time:
						if int(time[:-1]) > 168:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` часов по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60 * 60)
							await user.remove_roles(role)
					elif "d" in time:
						if int(time[:-1]) > 7:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` дней по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM users WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60 * 60 * 24)
							await user.remove_roles(role)
			elif sponsor_role == 1005118206681305108 or sponsor_role == 1001211754073829547:
				if cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 20:
					embed = discord.Embed(title=f"Мут",description=f'Вы уже потратили ``20`` мутов, ждите следующего месяца.',color=inter.author.color)
					await inter.send(embed = embed)
				else:
					await inter.channel.purge(limit=1)
					if "s" in time:
						if int(time[:-1]) > 604800:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` секунд по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]))
							await user.remove_roles(role)
					elif "m" in time:
						if int(time[:-1]) > 10080:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` минут по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60)
							await user.remove_roles(role)
					elif "h" in time:
						if int(time[:-1]) > 168:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` часов по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60 * 60)
							await user.remove_roles(role)		
					elif "d" in time:
						if int(time[:-1]) > 7:
							await inter.send("Максимальное время мута 7 дней!")
						else:
							role = user.guild.get_role(mute_role)
							embed = discord.Embed(title=f"Мут",description=f'Спонсор **{inter.author.name}** выдал мут **{user.name}** на ``{time[:-1]}`` дней по причине **{reason}**',color=user.color)
							await inter.send(embed=embed)
							await user.add_roles(role)
							await user.move_to(None)
							cursor.execute("UPDATE sponsors SET uses_mute = uses_mute + 1 WHERE id = {}".format(inter.author.id))
							connection.commit()	
							print(cursor.execute("SELECT uses_mute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
							await asyncio.sleep(int(time[:-1]) * 60 * 60 * 24)
							await user.remove_roles(role)	
		else:
			await inter.reply("Вы не можете мутить спонсоров!")
			print(f"Спонсор {inter.author} пытается замутить спонсора {user}")
	else:
		await inter.reply("Вы не спонсор!")
		print(f"Пользователь {inter.author} не имеет спонсорку поэтому не может мутить!")

@inter_client.slash_command(
    description="Размутить пользователя (платная функция)",
    options=[
        Option("user", "Введите пользователя которого хотите размутить",OptionType.USER,required=True),
        Option("reason", "Введите причину по которой хотите размутить пользователя",required=True)
    ]
)
async def sponsorunmute(inter,user:discord.Member,*,reason):
	access = False
	if os.path.exists(f"data/sponsors/{inter.author.id}.txt"):
		file = open(f"data/roles/{inter.author.id}.txt","r")
		f = file.read()
		for r in inter.author.roles:
			if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
				if f"{r.id}" in f"{f}":
					access = True
					sponsor_role = r.id
		file.close()
	else:
		file = open(f"data/roles/{inter.author.id}.txt","w")
		for r in inter.author.roles:
			if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
				file.write(str(r.id))
				access = True
				sponsor_role = r.id

		file.close()
	if access:
		mute_role = 1001096168039792700
		if sponsor_role == 1005118227086573742 or sponsor_role == 1001211749481070782:
			if cursor.execute("SELECT uses_unmute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 2:
				embed = discord.Embed(title=f"Размут",description=f'Вы уже потратили ``2`` размута, ждите следующего месяца.\nВы можете купить ***Основной спонсор*** и сможете размучивать ``5`` раз',color=inter.author.color)
				await inter.send(embed = embed)
			else:
				role = user.guild.get_role(mute_role)
				await user.remove_roles(role)
				embed = discord.Embed(title=f"Размут",description=f'Спонсор **{inter.author.name}** убрал мут **{user.name}** по причине **{reason}**',color=user.color)
				await inter.send(embed=embed)
				cursor.execute("UPDATE sponsors SET uses_unmute = uses_unmute + 1 WHERE id = {}".format(inter.author.id))
		elif sponsor_role == 1005512983436333076 or sponsor_role == 1001211750965846026:
			if cursor.execute("SELECT uses_unmute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 5:
				embed = discord.Embed(title=f"Размут",description=f'Вы уже потратили ``5`` размутов, ждите следующего месяца.\nВы можете купить ***Алмазный спонсор*** и сможете размучивать ``10`` раз',color=inter.author.color)
				await inter.send(embed = embed)
			else:
				role = user.guild.get_role(mute_role)
				await user.remove_roles(role)
				embed = discord.Embed(title=f"Размут",description=f'Спонсор **{inter.author.name}** убрал мут **{user.name}** по причине **{reason}**',color=user.color)
				await inter.send(embed=embed)
				cursor.execute("UPDATE sponsors SET uses_unmute = uses_unmute + 1 WHERE id = {}".format(inter.author.id))
		elif sponsor_role == 1005118220421828648 or sponsor_role == 1001211752249315369:
			if cursor.execute("SELECT uses_unmute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 10:
				embed = discord.Embed(title=f"Размут",description=f'Вы уже потратили ``10`` размутов, ждите следующего месяца.\nВы можете купить ***Админ спонсор*** и сможете размучивать ``15`` раз',color=inter.author.color)
				await inter.send(embed = embed)
			else:
				role = user.guild.get_role(mute_role)
				await user.remove_roles(role)
				embed = discord.Embed(title=f"Размут",description=f'Спонсор **{inter.author.name}** убрал мут **{user.name}** по причине **{reason}**',color=user.color)
				await inter.send(embed=embed)
				cursor.execute("UPDATE sponsors SET uses_unmute = uses_unmute + 1 WHERE id = {}".format(inter.author.id))
		elif sponsor_role == 1005118206681305108 or sponsor_role == 1001211754073829547:
			if cursor.execute("SELECT uses_unmute FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 15:
				embed = discord.Embed(title=f"Размут",description=f'Вы уже потратили ``15`` размутов, ждите следующего месяца.',color=inter.author.color)
				await inter.send(embed = embed)
			else:
				role = user.guild.get_role(mute_role)
				await user.remove_roles(role)
				embed = discord.Embed(title=f"Размут",description=f'Спонсор **{inter.author.name}** убрал мут **{user.name}** по причине **{reason}**',color=user.color)
				await inter.send(embed=embed)
				cursor.execute("UPDATE sponsors SET uses_unmute = uses_unmute + 1 WHERE id = {}".format(inter.author.id))

@inter_client.slash_command(
    description="Разбанить пользователя (платная функция)",
    options=[
        Option("user", "Введите пользователя которого хотите разбанить в формате: Никнейм#0000",required=True),
        Option("reason", "Введите причину по которой хотите разбанить пользователя",required=True)
    ]
)
async def sponsorunban(inter,user,*,reason):
	if os.path.exists(f"data/sponsors/{inter.author.id}.txt"):
		file = open(f"data/roles/{inter.author.id}.txt","r")
		f = file.read()
		for r in inter.author.roles:
			if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
				if f"{r.id}" in f"{f}":
					access = True
					sponsor_role = r.id
		file.close()
	else:
		file = open(f"data/roles/{inter.author.id}.txt","w")
		for r in inter.author.roles:
			if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
				file.write(str(r.id))
				access = True
				sponsor_role = r.id

		file.close()
	if access:
		await inter.channel.purge(limit=1)
		if sponsor_role == 1005118220421828648 or sponsor_role == 1001211749481070782:
			if cursor.execute("SELECT uses_unban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 1:
				embed = discord.Embed(title=f"Разбан",description=f'Вы уже потратили ``1`` разбан, ждите следующего месяца.\nВы можете купить ***Админ спонсор*** и сможете разбанивать ``2`` раза',color=inter.author.color)
				await inter.send(embed = embed)
			else:
				for ban_user in inter.guild.bans:
					if ban_user == user:
						await inter.guild.unban(user)
						print(f"{user} разбанен")
					else:
						await inter.send(f"{user} не найден в списке забаненых!")
				embed = discord.Embed(title=f"Разбан",description=f'Спонсор **{inter.author.name}** разбанил **{user.name}** по причине **{reason}**',color=user.color)
				await inter.send(embed=embed)
				cursor.execute("UPDATE sponsors SET uses_unban = uses_unban + 1 WHERE id = {}".format(inter.author.id))
		elif sponsor_role == 1005118206681305108 or sponsor_role == 1001211754073829547:
			if cursor.execute("SELECT uses_unban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] >= 2:
				embed = discord.Embed(title=f"Разбан",description=f'Вы уже потратили ``2`` разбана, ждите следующего месяца.',color=inter.author.color)
				await inter.send(embed = embed)
			else:
				for ban_user in inter.guild.bans:
					if ban_user == user:
						await inter.guild.unban(user)
						print(f"{user} разбанен")
					else:
						await inter.send(f"{user} не найден в списке забаненых!")
				embed = discord.Embed(title=f"Разбан",description=f'Спонсор **{inter.author.name}** разбанил **{user.name}** по причине **{reason}**',color=user.color)
				await inter.send(embed=embed)
				cursor.execute("UPDATE sponsors SET uses_unban = uses_unban + 1 WHERE id = {}".format(inter.author.id))

@inter_client.slash_command(
    description="Забанить пользователя на определенное время (платная функция)",
    options=[
        Option("user", "Введите пользователя которого хотите забанить",OptionType.USER,required=True),
        Option("time", "Введите время на которое хотите забанить пользователя",required=True),
        Option("reason", "Введите причину по которой хотите разбанить пользователя",required=True)
    ]
)
async def sponsorban(inter, user, time, *, reason):
	if os.path.exists(f"data/sponsors/{inter.author.id}.txt"):
		file = open(f"data/roles/{inter.author.id}.txt","r")
		f = file.read()
		for r in inter.author.roles:
			if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
				if f"{r.id}" in f"{f}":
					access = True
					sponsor_role = r.id
		file.close()
	else:
		file = open(f"data/roles/{inter.author.id}.txt","w")
		for r in inter.author.roles:
			if r.id == 1005118227086573742 or r.id == 1005512983436333076 or r.id == 1005118220421828648 or r.id == 1005118206681305108 or r.id == 1001211749481070782 or r.id == 1001211750965846026 or r.id == 1001211752249315369 or r.id == 1001211754073829547:
				file.write(str(r.id))
				access = True
				sponsor_role = r.id
		file.close()
	if access:
		for rr in user.roles:
			if rr == 1005118227086573742 or rr.id == 1005512983436333076 or rr.id == 1005118220421828648 or rr.id == 1005118206681305108 or rr.id == 1001211749481070782 or rr.id == 1001211750965846026 or rr.id == 1001211752249315369 or rr.id == 1001211754073829547:
				access = False
			else:
				access = True
		if access:
			for member in inter.guild.members:
				if member == user:
					for rr in user.roles:
						if rr == 1005118227086573742 or rr.id == 1005512983436333076 or rr.id == 1005118220421828648 or rr.id == 1005118206681305108 or rr.id == 1001211749481070782 or rr.id == 1001211750965846026 or rr.id == 1001211752249315369 or rr.id == 1001211754073829547:
							access = False
						else:
							access = True
					if access:
						if sponsor_role == 1005118220421828648 or sponsor_role == 1001211749481070782:
							if cursor.execute("SELECT uses_ban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] > 2:
								embed = discord.Embed(title=f"Бан",description=f'Вы уже потратили ``2`` бана, ждите следующего месяца.\nВы можете купить ***Админ спонсор*** и сможете банить ``3`` раза',color=inter.author.color)
								await inter.send(embed = embed)
							else:
								await inter.channel.purge(limit=1)
								if "s" in time:
									embed = discord.Embed(title=f"Бан",description=f'Спонсор **{inter.author.name}** выдал бан **{user.name}** на ``{time[:-1]}`` секунд по причине **{reason}**',color=user.color)
									await inter.send(embed=embed)
									await user.ban(reason=reason)
									cursor.execute("UPDATE sponsors SET uses_ban = uses_ban + 1 WHERE id = {}".format(inter.author.id))
									connection.commit()	
									print(cursor.execute("SELECT uses_ban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
									await asyncio.sleep(int(time[:-1]))
									await inter.guild.unban(user)
								elif "m" in time:
									embed = discord.Embed(title=f"Бан",description=f'Спонсор **{inter.author.name}** выдал бан **{user.name}** на ``{time[:-1]}`` минут по причине **{reason}**',color=user.color)
									await inter.send(embed=embed)
									await user.ban(reason=reason)
									cursor.execute("UPDATE sponsors SET uses_ban = uses_ban + 1 WHERE id = {}".format(inter.author.id))
									connection.commit()	
									print(cursor.execute("SELECT uses_ban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
									await asyncio.sleep(int(time[:-1])*60)
									await inter.guild.unban(user)
								elif "h" in time:
									embed = discord.Embed(title=f"Бан",description=f'Спонсор **{inter.author.name}** выдал бан **{user.name}** на ``{time[:-1]}`` часов по причине **{reason}**',color=user.color)
									await inter.send(embed=embed)
									await user.ban(reason=reason)
									cursor.execute("UPDATE sponsors SET uses_ban = uses_ban + 1 WHERE id = {}".format(inter.author.id))
									connection.commit()	
									print(cursor.execute("SELECT uses_ban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
									await asyncio.sleep(int(time[:-1])*60*60)
									await inter.guild.unban(user)
						elif sponsor_role == 1005118206681305108 or sponsor_role == 1001211754073829547:
							if cursor.execute("SELECT uses_ban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0] > 3:
								embed = discord.Embed(title=f"Бан",description=f'Вы уже потратили ``3`` бана, ждите следующего месяца.',color=inter.author.color)
								await inter.send(embed = embed)
							else:
								await inter.channel.purge(limit=1)
								if "s" in time:
									embed = discord.Embed(title=f"Бан",description=f'Спонсор **{inter.author.name}** выдал бан **{user.name}** на ``{time[:-1]}`` секунд по причине **{reason}**',color=user.color)
									await inter.send(embed=embed)
									await user.ban(reason=reason)
									cursor.execute("UPDATE sponsors SET uses_ban = uses_ban + 1 WHERE id = {}".format(inter.author.id))
									connection.commit()	
									print(cursor.execute("SELECT uses_ban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
									await asyncio.sleep(int(time[:-1]))
									await inter.guild.unban(user)
								elif "m" in time:
									embed = discord.Embed(title=f"Бан",description=f'Спонсор **{inter.author.name}** выдал бан **{user.name}** на ``{time[:-1]}`` минут по причине **{reason}**',color=user.color)
									await inter.send(embed=embed)
									await user.ban(reason=reason)
									cursor.execute("UPDATE sponsors SET uses_ban = uses_ban + 1 WHERE id = {}".format(inter.author.id))
									connection.commit()	
									print(cursor.execute("SELECT uses_ban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
									await asyncio.sleep(int(time[:-1])*60)
									await inter.guild.unban(user)
								elif "h" in time:
									embed = discord.Embed(title=f"Бан",description=f'Спонсор **{inter.author.name}** выдал бан **{user.name}** на ``{time[:-1]}`` часов по причине **{reason}**',color=user.color)
									await inter.send(embed=embed)
									await user.ban(reason=reason)
									cursor.execute("UPDATE sponsors SET uses_ban = uses_ban + 1 WHERE id = {}".format(inter.author.id))
									connection.commit()	
									print(cursor.execute("SELECT uses_ban FROM sponsors WHERE id = {}".format(inter.author.id)).fetchone()[0])
									await asyncio.sleep(int(time[:-1])*60*60)
									await inter.guild.unban(user)
					else:
						await inter.reply("Вы не можете банить спонсоров!")					
		else:
			await inter.reply("Вы не спонсор!")
def filewrite(file,value):
	file = open(file,"w")
	file.write(f"{value}")
	file.close()

@inter_client.slash_command(
    description="Создание кастомной роли (платная функция)",
    options=[
        Option("name", "Введите название роли",required=True),
        Option("color", "Введите код цвета в формате #HEX",required=False)
    ]
)
async def role(inter,name,color = None):
	interauthor = inter.author
	access = False
	if os.path.exists(f"data/sponsors/{inter.author.id}.txt"):
		file = open(f"data/roles/{inter.author.id}.txt","r")
		f = file.read()
		for r in inter.author.roles:
			if r.id == 1013552604871135282 or r.id == 1001211755415994449:
				if f"{r.id}" in f"{f}":
					access = True
		file.close()
	else:
		file = open(f"data/roles/{inter.author.id}.txt","w")
		for r in inter.author.roles:
			if r.id == 1013552604871135282 or r.id == 1001211755415994449:
				file.write(str(r.id))
				access = True
		file.close()
	if access:
		personal_role = 1013552604871135282
		if color is None:
			embed = discord.Embed(title="Создание персональной роли",description=f"\n\n    {name}    \n\n\n**Выберите цвет своей будущей роли**")
			row = ActionRow(
		        Button(
		            style=ButtonStyle.grey,
		            emoji='🔴',
		            custom_id="red"
		        ),
		        Button(
		            style=ButtonStyle.grey,
		            emoji='🔵',
		            custom_id="blurple"
		        ),
		        Button(
		            style=ButtonStyle.grey,
		            emoji='🟣',
		            custom_id="purple"
		        ),
		        Button(
		            style=ButtonStyle.grey,
		            emoji='🟢',
		            custom_id="green"
		        ),
		        Button(
		            style=ButtonStyle.blurple,
		            emoji='➡️',
		            custom_id="next"
		        )
		    )
			
			global msg
			msg = await inter.reply(embed=embed,components=[row])
			on_click = msg.create_click_listener(timeout=60)
			@on_click.matching_id("red")
			async def on_button(inter):
				if inter.author == interauthor:
					await inter.channel.purge(limit=1)
					color = discord.Colour.red()
					r = await inter.guild.create_role(name=name,color=color)
					await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=color))
					role = inter.author.guild.get_role(r.id)
					role2 = inter.author.guild.get_role(personal_role)
					await inter.author.remove_roles(role2)
					await inter.author.add_roles(role)
					filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
			@on_click.matching_id("blurple")
			async def on_button(inter):
				if inter.author == interauthor:
					await inter.channel.purge(limit=1)
					color = discord.Colour.blurple()    
					r = await inter.guild.create_role(name=name,color=color)
					await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=color))
					role = inter.author.guild.get_role(r.id)
					role2 = inter.author.guild.get_role(personal_role)
					await inter.author.remove_roles(role2)
					await inter.author.add_roles(role)
					filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
			@on_click.matching_id("purple")
			async def on_button(inter):
				if inter.author == interauthor:
					await inter.channel.purge(limit=1)
					color = discord.Colour.purple()  
					r = await inter.guild.create_role(name=name,color=color)
					await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=color))
					role = inter.author.guild.get_role(r.id)
					role2 = inter.author.guild.get_role(personal_role)
					await inter.author.remove_roles(role2)
					await inter.author.add_roles(role)
					filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
			@on_click.matching_id("green")
			async def on_button(inter):
				if inter.author == interauthor:
					await inter.channel.purge(limit=1)
					color = discord.Colour.green() 
					r = await inter.guild.create_role(name=name,color=color)
					await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=color))
					role = inter.author.guild.get_role(r.id)
					role2 = inter.author.guild.get_role(personal_role)
					await inter.author.remove_roles(role2)
					await inter.author.add_roles(role)
					filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
			@on_click.matching_id("next")
			async def on_button(inter):
				await page2()
			async def page1():
				embed = discord.Embed(title="Создание персональной роли",description=f"\n\n    {name}    \n\n\n**Выберите цвет своей будущей роли**")
				row = ActionRow(
			        Button(
			            style=ButtonStyle.grey,
			            emoji='🔴',
			            custom_id="red"
			        ),
			        Button(
			            style=ButtonStyle.grey,
			            emoji='🔵',
			            custom_id="blurple"
			        ),
			        Button(
			            style=ButtonStyle.grey,
			            emoji='🟣',
			            custom_id="purple"
			        ),
			        Button(
			            style=ButtonStyle.grey,
			            emoji='🟢',
			            custom_id="green"
			        ),
			        Button(
			            style=ButtonStyle.blurple,
			            emoji='➡️',
			            custom_id="next"
			        )
			    )
				global msg
				await msg.delete()
				msg = await inter.send(embed=embed, components=[row])
				on_click = msg.create_click_listener(timeout=60)
				@on_click.matching_id("red")
				async def on_button(inter):
					if inter.author == interauthor:
						await inter.channel.purge(limit=1)
						color = discord.Colour.red()
						r = await inter.guild.create_role(name=name,color=color)
						await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=color))
						role = inter.author.guild.get_role(r.id)
						role2 = inter.author.guild.get_role(personal_role)
						await inter.author.remove_roles(role2)
						await inter.author.add_roles(role)
						filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
				@on_click.matching_id("blurple")
				async def on_button(inter):
					if inter.author == interauthor:
						await inter.channel.purge(limit=1)
						color = discord.Colour.blurple()    
						r = await inter.guild.create_role(name=name,color=color)
						await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=color))
						role = inter.author.guild.get_role(r.id)
						role2 = inter.author.guild.get_role(personal_role)
						await inter.author.remove_roles(role2)
						await inter.author.add_roles(role)
						filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
				@on_click.matching_id("purple")
				async def on_button(inter):
					if inter.author == interauthor:
						await inter.channel.purge(limit=1)
						color = discord.Colour.purple()  
						r = await inter.guild.create_role(name=name,color=color)
						await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=color))
						role = inter.author.guild.get_role(r.id)
						role2 = inter.author.guild.get_role(personal_role)
						await inter.author.remove_roles(role2)
						await inter.author.add_roles(role)
						filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
				@on_click.matching_id("green")
				async def on_button(inter):
					if inter.author == interauthor:
						await inter.channel.purge(limit=1)
						color = discord.Colour.green() 
						r = await inter.guild.create_role(name=name,color=color)
						await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=color))
						role = inter.author.guild.get_role(r.id)
						role2 = inter.author.guild.get_role(personal_role)
						await inter.author.remove_roles(role2)
						await inter.author.add_roles(role)
						filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
				@on_click.matching_id("next")
				async def on_button(inter):
					await page2()
			async def page2():
				embed2 = discord.Embed(title="Создание персональной роли",description=f"\n\n    {name}    \n\n\n**Выберите цвет своей будущей роли**")
				row2 = ActionRow(
			        Button(
			            style=ButtonStyle.blurple,
			            emoji='⬅️',
			            custom_id="back"
			        ),
			        Button(
			            style=ButtonStyle.grey,
			            emoji='⚪',
			            custom_id="white"
			        ),
			        Button(
			            style=ButtonStyle.grey,
			            emoji='⚫',
			            custom_id="black"
			        ),
			        Button(
			            style=ButtonStyle.grey,
			            emoji='🟤',
			            custom_id="brown"
			        ),
			        Button(
			            style=ButtonStyle.grey,
			            emoji='🌺',
			            custom_id="pink"
			        )
			    )
				global msg
				await msg.delete()
				msg = await inter.send(embed=embed2,components=[row2])
				on_click = msg.create_click_listener(timeout=60)
				@on_click.matching_id("back")
				async def on_button(inter):
					await page1()	
				@on_click.matching_id("white")
				async def on_button(inter):
					if inter.author == interauthor:
						color = "#ffffff"
						sixteenIntegerHex = int(color.replace("#", ""), 16)
						readableHex = int(hex(sixteenIntegerHex), 0)
						await inter.channel.purge(limit=1)
						r = await inter.guild.create_role(name=name,color=readableHex)
						await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=readableHex))
						role = inter.author.guild.get_role(r.id)
						role2 = inter.author.guild.get_role(personal_role)
						await inter.author.remove_roles(role2)
						await inter.author.add_roles(role)
						filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
				@on_click.matching_id("black")
				async def on_button(inter):
					if inter.author == interauthor:
						color = "#000000"
						sixteenIntegerHex = int(color.replace("#", ""), 16)
						readableHex = int(hex(sixteenIntegerHex), 0)
						await inter.channel.purge(limit=1)
						r = await inter.guild.create_role(name=name,color=readableHex)
						await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=readableHex))
						role = inter.author.guild.get_role(r.id)
						role2 = inter.author.guild.get_role(personal_role)
						await inter.author.remove_roles(role2)
						await inter.author.add_roles(role)	
						filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
				@on_click.matching_id("brown")
				async def on_button(inter):
					if inter.author == interauthor:
						color = "#5e3a15"
						sixteenIntegerHex = int(color.replace("#", ""), 16)
						readableHex = int(hex(sixteenIntegerHex), 0)
						await inter.channel.purge(limit=1)
						r = await inter.guild.create_role(name=name,color=readableHex)
						await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=readableHex))
						role = inter.author.guild.get_role(r.id)
						role2 = inter.author.guild.get_role(personal_role)
						await inter.author.remove_roles(role2)
						await inter.author.add_roles(role)	
						filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
				@on_click.matching_id("pink")
				async def on_button(inter):
					if inter.author == interauthor:
						color = "#f213c2"
						sixteenIntegerHex = int(color.replace("#", ""), 16)
						readableHex = int(hex(sixteenIntegerHex), 0)
						await inter.channel.purge(limit=1)
						r = await inter.guild.create_role(name=name,color=readableHex)
						await inter.send(embed=discord.Embed(title="Создание персональной роли",description=f"\nВы создали роль {r.mention}",color=readableHex))
						role = inter.author.guild.get_role(r.id)
						role2 = inter.author.guild.get_role(personal_role)
						await inter.author.remove_roles(role2)
						await inter.author.add_roles(role)	
						filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
		else:
			sixteenIntegerHex = int(color.replace("#", ""), 16)
			readableHex = int(hex(sixteenIntegerHex), 0)
			role2 = inter.author.guild.get_role(personal_role)
			await inter.author.remove_roles(role2)
			r = await inter.guild.create_role(name=name,color=readableHex)
			role = inter.author.guild.get_role(r.id)
			embed = discord.Embed(title="Создание персональной роли",description=f"\n\n  Вы создали роль:  {name} с цветовым кодом: ``{color}``   \n\n",color=readableHex)
			await inter.author.add_roles(role)
			await inter.reply(embed=embed)
			filewrite(f"data/roles/{inter.author.id}.txt",f"{r.id}")
	else:
		await inter.reply(embed=discord.Embed(title="Персональная роль",description="Вы не купили эту услугу!",color=inter.author.color))

@inter_client.slash_command(
    description="Удаление кастомной роли (платная функция)",
    options=[
        Option("name", "Введите название роли которую хотите удалить",required=True)
    ]
)
async def delrole(inter,name):
	if os.path.exists(f"data/roles/{inter.author.id}.txt"):

		file = open(f"data/roles/{inter.author.id}.txt","r")
		f = file.read()
		access = False
		for r in inter.author.roles:
			if r.name == name:
				if f"{r.id}" in f"{f}":
					access = True
					id_role = r.id
		if access:
			personal_role = 1013552604871135282
			role = inter.author.guild.get_role(id_role)
			role2 = inter.author.guild.get_role(personal_role) 
			await role.delete()
			await inter.author.add_roles(role2)
			await inter.reply(embed=discord.Embed(title="Удаление кастомной роли",description=f"Вы успешно удалили кастомную роль ``@{name}``!\nВы можете создать ее снова с помощью команды **/role**",color=inter.author.color))
		else:
			await inter.reply("У вас нет прав/У вас нету этой роли")
		file.close()
	else:
		file = open(f"data/roles/{inter.author.id}.txt","w")
		file.close()
		await inter.reply("У вас нет прав или у вас нету этой роли!")

@inter_client.slash_command(
    description="Сообщить разработчику о ошибке/баге",
    options=[
        Option("message", "Введите название роли которую хотите удалить",required=True)
    ]
)
async def bug(inter,*,message):
	dev = bot.get_user(890649916135833600)
	await dev.send(f"Вам пришло сообщение о баге бота:\n ```{message}```\n **От** ***{inter.author}***")
	await dev.send(inter.author.id)
	await inter.reply("📨 *Сообщение отправлено*")

@bot.command()
async def reply(ctx,member:int,*,message):
	user = bot.get_user(member)
	await user.send(f"Разработчик бота **Laberty** ответил вам на ваше сообщение:\n```{message}```")

bot.run(TOKEN)