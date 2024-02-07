import discord
from discord.ext import commands, tasks
from discord.utils import get
import datetime
from datetime import date, datetime, timezone, timedelta
from decimal import Decimal
import random
import time
import json
from discord.ui import Button, View
# from discord import default_permissions
import mysql.connector
import asyncio
import pytz

def connect_to_database():
    mydb = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    return mydb

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

# Serveur Tag
TCOTLLF = [11111111111111111111111]

# client
client = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=intents,
)


## WEBHOOK ##


###### ACTIONS DES QUE LE BOT CHARGE #####

@client.event
async def on_ready():
    tigros = client.get_emoji(1072445715357368402)
    axodaft = client.get_emoji(1063028956833525760)
    panpan = client.get_emoji(1063029246731243540)
    ui = client.get_emoji(1063029071681966131)
    razeboom = client.get_emoji(1072445613922336859)
    client.add_view(RolesButtons())
    # Channel = client.get_channel(1063482256905207878)
    embed=discord.Embed(title="Choisis ton rôle ici !", description=f"Les rôles de jeux donnent accès aux salons appropriés pour discuter du jeu et proposer des parties pour jouer :\n \n{axodaft} <@&1063481817665126400> : Permet d'avoir excès également au server minecraft, ses logs et ses nouveautés !\n \n{tigros} <@&1063482059630313532> : Ce sont tout les jeux qui ne demandent aucun support ni investissement particulier, donc généralement des jeux sur navigateur (Skribbl, Gartic Phone, Code Name) et autres petits jeux moins cher que gratuit.\n \n{razeboom} <@&1063481986393579582> !\n \n{panpan} <@&1063481939115393044> !\n \nN'hésitez pas à proposer d'autres rôles potentiels {ui}.", color=0xFF5733)
    # await Channel.purge(limit=1)
    # MessageEmote = await Channel.send(embed=embed, view=RolesButtons())
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    

# Définition de la fonction d'insertion de données

def insert_user_data(user_id, name, score, daily, mute, server_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (id, name, score, daily, mute) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (user_id, name, score, daily, mute, server_id)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()

# Message de bienvenue

@client.event
async def on_member_join(member):
    channel = client.get_channel(1063024808738160731)
    ui = client.get_emoji(1063029071681966131)
    message = f"Bienvenue {member}, prends une chaise et un cookie et pose toi autour du feu {ui}"
    await channel.send(message)

# Whitelist checker quand une nouvelle personne arrive

    file = open("whitelist.json")
    data = json.load(file)
    file.close()
    list = data['whitelist']
    welcome = client.get_channel(1063024808738160731)
    if str(member.id) not in list:
        cpamwa = client.get_emoji(1063028855545274428)
        await member.send(f"Désolé, mais il semble que vous n'êtes pas whitelist sur ce serveur !{cpamwa} Demandez à un admin si le problème persiste.")
        await member.kick(reason = "Utilisateur n'est pas sur la Whitelist")
        await welcome.send(f"L'Utilisateur {member} a essayé de se connecter mais n'est pas autorisé (raison : non whitelist), J'ai donc kick {cpamwa}.")
    else:

        # CREER UNE NOUVELLE ENTREE EN BDD
        role_id = 1063384757871853598
        guild = member.guild
        role = get(guild.roles, id=role_id)
        await member.add_roles(role)
        user_id = member.id
        name = member.name
        score = 0
        daily = 0
        mute = 0
        server_id = 11111111111111111111
        insert_user_data(user_id, name, score, daily, mute, server_id)
    
    
# Message d'au revoir

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1063024808738160731)
    await channel.send(f"J'ai cru voir {member} prendre la direction de la sortie.")



##### ACTIONS DES QU'IL Y A UN MESSAGE ######

@client.event
async def on_message(message):


# Intervention aléatoire Lors des discutions

    if message.author != client.user:
        messageSplit = message.content.split(' ')
        messageEnd = messageSplit[len(messageSplit)-1].lower()
        if messageEnd == ('?'):
            messageEnd = messageSplit[len(messageSplit)-2].lower()
        if messageEnd == ('quoi') or messageEnd == ('pourquoi'):
                random_number = random.randint(1, 100)
                if random_number <= 10:
                    await message.reply("Feur !")


# GESTION DE LA Conversation avec le bot grace au @ / A rework

    # if "<@1063064988278861964>" in message.content:
    #     if message.author != client.user:
    #         if "bien jouer" in message.content.lower() or "bien joué" in message.content.lower():
    #             await message.channel.send("Merci !")
    #         elif "nez" in message.content.lower() and message.author.name == "romi'":
    #             await message.channel.send("Nez !")
    #         elif "crédit" in message.content.lower() and "?" in message.content.lower():
    #             randomMessagesList = [
    #                 "Essaye la commande /daily dans le channel #bot !",
    #                 "Ceux qui touchent leurs nez quand les chiffres sont égaux peuvent recevoir des cadeaux !",
    #                 "Parcipe à des évents ou gagne les c'est encore mieux",
    #                 "quand le serveur minecraft sera ouvert, tu pourras faire les succès"]
    #             await message.channel.send(random.choice(randomMessagesList))
    #         elif "ça va" in message.content.lower() and "?" in message.content.lower():
    #             randomMessagesList = [
    #                 "Ça va, Merci",
    #                 "Je ne suis pas doté d'humeurs, mais je suppose que si je suis fonctionnel, je peux répondre : oui"]
    #             await message.channel.send(random.choice(randomMessagesList))
    #         else:
    #             ui = client.get_emoji(1063029071681966131)
    #             amber = client.get_emoji(1072445642208714863)
    #             randomMessagesList = [
    #                 f"Bip Boup, Bip ? {ui}",
    #                 f"Kékiveu ? {ui}",
    #                 "Pas envie",
    #                 "Gné ?",
    #                 "Non, flemme",
    #                 f"Laisse moi tranquille {amber}",
    #                 "Pas compris"]
    #             await message.channel.send(random.choice(randomMessagesList))


# JEU DU NEZ DANS LE SALON NEZ

    if "Nez !" in message.content:
            if message.channel.name == "nez-👃" and message.author == client.user or message.channel.name == "testbot" and message.author == client.user:
                await asyncio.sleep(60)
                random_number = random.uniform(0.5, 2)
                print(f"random number : {random_number}")
                responses = []
                responded_users = set()
                async for msg in message.channel.history(limit=10):
                    if "nez" in msg.content.lower() and msg.author != client.user and (datetime.now(pytz.utc) - msg.created_at.replace(tzinfo=pytz.utc)) < timedelta(minutes=1):
                        responses.append((msg.author, msg.created_at))
                responses.sort(key=lambda x: x[1])
                for i, (author, created_at) in enumerate(responses):
                    if author.id in responded_users:
                            continue
                    responded_users.add(author.id)
                    score = await get_user_score(author.id)
                    credit = client.get_emoji(1087461478556237862)
                    multiplier = 1.5 if i == 0 else 1.0
                    credit_number = random_number * multiplier
                    credit_number = round(credit_number, 2)
                    print(f"gain : {author.name} = {credit_number} / base {multiplier}")
                    new_score = float(score) + random_number
                    await update_user_score(author.id, new_score)
                    await message.channel.send(f"{credit} {author.name} a gagné {credit_number} crédits {credit} !")



# FONCTION POUR GET LE SCORE EN BDD

async def get_user_score(user_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    sql = "SELECT score FROM users WHERE id = %s"
    mycursor.execute(sql, (user_id,))
    result = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if result:
        return result[0]
    else:
        return 0


# FONCTION POUR SET LE SCORE EN BDD

async def update_user_score(user_id, new_score):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    sql = "UPDATE users SET score = %s WHERE id = %s"
    val = (new_score, user_id)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()



# OBJET QUI VA GENERER LES BOUTONS POUR LA SELECTION DE ROLES

class RolesButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label='Minecaft',style=discord.ButtonStyle.green,emoji = '<:Axodaft:1063028956833525760>', custom_id='Minecraft')
    async def minecraft_button(self, button, interaction):
        custom_id = interaction.custom_id
        await interaction.response.defer()
        if custom_id == 'Minecraft':
            Role = discord.utils.get(interaction.user.guild.roles, id=1063481817665126400)
            await interaction.user.add_roles(Role)

    @discord.ui.button(label='Ptit Jeu',style=discord.ButtonStyle.blurple,emoji = '<:Tigros:1072445715357368402>', custom_id='PtitJeu')
    async def games_button(self, button, interaction):
        custom_id = interaction.custom_id
        await interaction.response.defer()
        if custom_id == 'PtitJeu':
            Role = discord.utils.get(interaction.user.guild.roles, id=1063482059630313532)
            await interaction.user.add_roles(Role)

    @discord.ui.button(label='Valorant',style=discord.ButtonStyle.red,emoji = '<:RazeBoom:1072445613922336859>', custom_id='Valorant')
    async def valorant_button(self, button, interaction):
        custom_id = interaction.custom_id
        await interaction.response.defer()
        if custom_id == 'Valorant':
            Role = discord.utils.get(interaction.user.guild.roles, id=1063481986393579582)
            await interaction.user.add_roles(Role)

    @discord.ui.button(label='League of Legends',style=discord.ButtonStyle.primary,emoji = '<:panpan:1063029246731243540>', custom_id='Lol')
    async def lol_button(self, button, interaction):
        custom_id = interaction.custom_id
        await interaction.response.defer()
        if custom_id == 'Lol':
            Role = discord.utils.get(interaction.user.guild.roles, id=1063481939115393044)
            await interaction.user.add_roles(Role)



# FONCTION QUI VA RECUPERER LES 10 MEILLEURS EN CREDITS

async def get_top_ten(server_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    sql = "SELECT name, score FROM users WHERE server_id = %s ORDER BY score DESC LIMIT 10"
    mycursor.execute(sql, (server_id,))
    results = mycursor.fetchall()

    top_ten = "```Rank   Pseudo            Score \n\n"
    rank = 1
    for row in results:
        top_ten += f"{rank:<6} {row[0]:<16} {row[1]:<5}\n"
        rank += 1
    top_ten += "```"
    mycursor.close()
    mydb.close()
    return top_ten


########## LES COMMANDES ICI ###############

# SET DE LA CLASSE POUR LES COMMANDES CLASSEMENT ET LEURS FONCTIONS
class Score(commands.Cog):
    def __init__(self, client):
        self.client = client
        
# COMMANDE POUR AFFICHER SON CLASSEMENT

    @client.slash_command(guild_ids=TCOTLLF, name="rank", description="Voir combien de crédits tu possèdes !")
    async def rank(ctx):
        if ctx.channel.name == ("bot-🦾"):
            user_id = ctx.author.id
            user_name = ctx.author.name
            avatar_url = ctx.author.avatar.url
            server_id = ctx.guild.id

            member = await ctx.guild.fetch_member(user_id)

            score = await get_user_score(user_id)
            position = await get_user_position(user_id, server_id)

            embed = discord.Embed(title=f"Profil de {user_name}", color=discord.Color.blue())
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="Crédits", value=score, inline=True)
            embed.add_field(name="Rank", value=position, inline=True)

            await ctx.respond(embed=embed)



# COMMANDE D'AFFICHAGE DU CLASSEMENT Général

    @client.slash_command(guild_ids=TCOTLLF, name="top", description="Voir le classement des plus riches du serveur")
    async def top(ctx):
        if ctx.channel.name == ("bot-🦾") or ctx.channel.name == ("testbot"):
            credit = client.get_emoji(1087461478556237862)
            server_id = ctx.guild.id
            user_name = ctx.author.name
            top_ten = await get_top_ten(server_id)
            user_id = ctx.author.id
            user_position = await get_user_position(user_id, server_id)
            user_score = await get_user_score(user_id)

            # Determine embed color based on user position
            if user_position == 1:
                color = discord.Color.gold()
                image = "https://i.imgur.com/xxxxxxxx.png"
            elif user_position <= 3:
                color = discord.Color.orange()
                image = "https://i.imgur.com/xxxxxxxx.png"
            else:
                color = discord.Color.green()
                image = "https://i.imgur.com/xxxxxxxx.png"

            embed = discord.Embed(title="Top Crédits 🏆", color=color)
            # embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_image(url=image)
            embed.add_field(name=f"Les Plus Riches {credit}", value=top_ten, inline=False)
            embed.add_field(name="Position :", value=f"{user_name}, tu es #{user_position} avec {user_score} crédits !", inline=False)

            member_count = ctx.guild.member_count - 1
            embed.set_footer(text=f"Classement basé sur {member_count} utilisateurs.")

            await ctx.respond(embed=embed)


# FONCTION POUR GET LE SCORE DE L'UTILISATEUR (OBJET SCORE)

async def get_user_score(user_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    sql = "SELECT score FROM users WHERE id = %s"
    mycursor.execute(sql, (user_id,))
    result = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if result:
        return result[0]
    else:
        return 0



# FONCTION POUR OPTENIR LE RANQ DE L'UTILISATEUR

async def get_user_position(user_id, server_id):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(*) FROM users WHERE server_id = %s AND score > (SELECT score FROM users WHERE id = %s)"
    mycursor.execute(sql, (server_id, user_id))
    result = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if result:
        return result[0] + 1
    else:
        return 0


# COMMANDE WHITELIST

@client.slash_command(guild_ids=TCOTLLF, name="whitelist", description="Add people to whitelist", default_permissions=False)
@discord.default_permissions(administrator=True)
async def whitelist(ctx, userid):
    file = open("whitelist.json")
    data = json.load(file)
    file.close()
    list = data['whitelist']
    if userid not in list:
        list.append(userid)
        newjson = {"whitelist": list}
        with open("whitelist.json", "w") as file:
            json.dump(newjson, file)
            await ctx.respond(content=f"Ajouté !", ephemeral=True)
    else:
        list.remove(userid)
        newjson = {"whitelist": list}
        with open("whitelist.json", "w") as file:
            json.dump(newjson, file)
            await ctx.respond(content=f"Suprimé !", ephemeral=True)




# COMMANDE CLEAR les derniers message d'un channel


@client.slash_command(guild_ids=TCOTLLF, name="clear", default_permissions=False)
@discord.default_permissions(administrator=True)
async def clear(ctx):
    await ctx.channel.purge(limit=100)
    await ctx.respond(content=f"Clear !", ephemeral=True)



# COMMANDE MUTE

@client.slash_command(guild_ids=TCOTLLF, name="mute", description="mute user", default_permissions=False)
@discord.default_permissions(administrator=True)
async def mute(ctx, user: discord.Member):
    role_id = 1063384200595644436
    guild = ctx.guild
    role = get(guild.roles, id=role_id)
    if role not in user.roles:
        await user.add_roles(role)
        await ctx.respond(f"{user.name} à été mute")
        role_id = 1063384757871853598
        role = get(guild.roles, id=role_id)
        await user.remove_roles(role)
    else:
        await user.remove_roles(role)
        role_id = 1063384757871853598
        role = get(guild.roles, id=role_id)
        await user.add_roles(role)
        await ctx.respond(f"{user.name} n'est plus mute")



# COMMANDE DAILY

@client.slash_command(guild_ids=TCOTLLF, name="daily", description="Gagner quelques crédit tous les jours")
async def daily(ctx):
    if ctx.channel.name == ("bot-🦾"):
        credit = client.get_emoji(1087461478556237862)
        mydb = connect_to_database()
        mycursor = mydb.cursor()
        sql = "SELECT score, daily FROM users WHERE id = %s"
        val = (ctx.user.id,)
        user_name = ctx.user.name
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result is not None:
            score, daily = result
            if daily == 0:
                random_number = random.randint(1,7)
                random_decim = random.randint(1,99)
                random_number = round(random_number * (random_decim / 100), 2)
                if random_number < 1:
                    await ctx.respond(f"Cheh, {user_name} a reçu {random_number} crédits {credit} !")
                elif random_number < 4:
                    random_number = round(random_number * 1.1, 2)
                    await ctx.respond(f"{user_name} a reçu {random_number} crédits {credit} !")
                elif random_number < 6:
                    random_number = round(random_number * 1.2, 2)
                    await ctx.respond(f"{credit} Bravo ! {user_name} a reçu {random_number} crédits {credit} !")
                elif random_number < 7:
                    random_number = round(random_number * 1.3, 2)
                    await ctx.respond(f"{credit} {user_name} a reçu un gros lot de {random_number} crédits {credit} !")
                else:
                    random_number = round(random_number * 1.5, 2)
                    await ctx.respond(f"{credit} WoW ,{user_name} a reçu le jackpot de {random_number} crédits {credit}!")
                new_score = Decimal(score) + Decimal(random_number)
                new_daily = 1
                sql = "UPDATE users SET score = %s, daily = %s WHERE id = %s"
                val = (new_score, new_daily, ctx.user.id)
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
                mydb.close()
            else:
                mycursor.close()
                mydb.close()
                return await ctx.respond("Vous avez déjà récupéré votre bonus quotidien aujourd'hui.")


#FONCTION RELOAD LE /DAILY


def update_daily():
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    sql = "UPDATE users SET daily = 0 WHERE daily = 1"
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()



# BOUCLE DES MINUTES


@tasks.loop(minutes=1)
async def loopMinutes():
    while True:
        now = datetime.now()
        if now.second == 0:
            if now.minute == now.hour:
                await nez(now.minute, now.hour, now)
        await asyncio.sleep(1)

async def nez(min, hour, mtn):
    if hour < 2 or hour > 8:
        if hour == min:
            random_number = random.randint(1, 100)
            print(f"nez probable : {random_number}")
            print(f"{mtn}")
            if random_number <= 35:
                channel = client.get_channel(1083679050280747018)
                await channel.send("Nez !")
    if hour == 0 and min == 0:
        update_daily()

loopMinutes.start()



# RUNNER

client.run('')