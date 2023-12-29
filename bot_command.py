from tools import *
from tools import *
from discord.ext import commands
import sqlite3
from macro import *
from tools import is_channel
import threading
import discord

def great_spirit_command(bot, intents):

    @bot.command()          #bot say coucou
    async def coucou(ctx):
        if (is_channel(ctx) == True):
            await ctx.channel.send("Coucou !")

    @bot.command()                  #write the message of the user
    async def say(ctx, *text):
        if (is_channel(ctx) == True):
            await ctx.send(" ".join(text))

    @bot.command()              #all information on the serveur
    async def serveurinfo(ctx):
        if (is_channel(ctx) == True):
            server = ctx.guild
            numberoftextchanel = len(server.text_channels)
            numbervoicechannels = len(server.voice_channels)
            serverdescription = server.description
            numberofperson = server.member_count
            server_name = server.name
            message = f"le serveur **{server_name}** contient {numberofperson} personnes.\n\
La description du serveur {serverdescription}.\n ce serveur possède {numberoftextchanel} \
salons ecrit ainsi que {numbervoicechannels} vocaux"
            await ctx.send(message)

    @bot.event  #message hello new member
    async def on_member_join(member):
        general_channel = bot.get_channel(989089726743060480)
        general_channel.send(f"Bienvenue sur le serveur {member.display_name}, Identification obligatoire (nom, prénom, totem, premiere lettre de ton adjectif, id)")

    @bot.command()
    @commands.has_any_role("Grand Sachem (H)", "Grand Sachem Suprême (H)")
    async def plumerie(ctx):
        if is_channel(ctx):
            GM_id = 0
            sorcier_name = 0
            date = 0
            code_postal = 0
            lieux = ""
            dure = ""
            vp = 0
            my_timeout = 40

            def check(message):
                return message.author == ctx.message.author and ctx.message.channel == message.channel

            def checkemodji(reaction, user):
                return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

            message = await ctx.send("Vous avez demandé d'organiser une plumerie. En déclarent vous acceptez d'être Grand Manitou. Veuillez valider en réagissant avec 'valide'.")
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=my_timeout, check=checkemodji)
                if reaction.emoji == "✅":
                    GM_id = user.id
                    await ctx.send(f"Le Grand Manitou a été validé se sera {user}!")

                    message = await ctx.send("Quel est le totem du sorcier ?")
                    sorcier_name = await bot.wait_for("message", timeout=my_timeout, check=check)
                    sorcier_name = sorcier_name.content
                    await ctx.send(f"Le Sorcier a été validé se sera {sorcier_name}!")

                    await ctx.send(f"Quel jour commencera la plumerie AAAA-MM-DD")
                    date = await bot.wait_for("message", timeout=my_timeout, check=check)
                    date = date.content

                    await ctx.send(f"Quel est le code postal de l'endroit où la plumerie va se dérouler ?")
                    code_postal = await bot.wait_for("message", timeout=my_timeout, check=check)
                    code_postal = int(code_postal.content)

                    await ctx.send(f"Quel est le nom de l'endroit où la plumerie va se dérouler ?")
                    lieux = await bot.wait_for("message", timeout=my_timeout, check=check)
                    lieux = lieux.content

                    await ctx.send(f"Combien de temps va durer la plumerie Xh ?")
                    dure = await bot.wait_for("message", timeout=my_timeout, check=check)
                    dure = dure.content

                    await ctx.send(f"Combien de visages pâles vont être présents ?")
                    vp = await bot.wait_for("message", timeout=my_timeout, check=check)
                    vp = int(vp.content)

                    try:
                        con = sqlite3.connect("plumeries.db")
                        cur = con.cursor()
                        cur.execute(f"INSERT INTO informations (date, grand_manitou, sorcier, code_postal, lieux, duree, visage_pale) VALUES\
                            ('{date}', '{GM_id}', '{sorcier_name}', {code_postal}, '{lieux}', '{dure}', {vp});")
                        con.commit()
                        cur.close()
                        await ctx.send("Déclaration Validée ! ✅")
                    except Exception as e:
                        print(e)
                        await ctx.send(ERROR_MESSAGE_PLUMERIE)
                    name_gm = await ctx.bot.fetch_user(GM_id)
                    channel = bot.get_channel(CHANNEL_ANNONCES)
                    message = await channel.send(f"🪶 @everyone,\nUne plumerie a été validée et sera organisée par:\nLe Grand Sachem {name_gm}\nLe sorcier {sorcier_name}\nElle aura lieu le {date} à {lieux} ({code_postal}).\nSa durée sera de {dure} heures et {vp} visages pâles seront présents.\nSi vous serez présent, merci de réagir avec ✅ sous ce message, ou avec ❌ pour non.\n\nPour que la plumerie soit validée, un autre sachem doit également approuver ce message. 🪶")
                    await message.add_reaction("✅")
                    await message.add_reaction("❌")
                else:
                    await ctx.send(ERROR_MESSAGE_PLUMERIE)
            except Exception as e:
                print(e)
                await ctx.send(ERROR_MESSAGE_PLUMERIE)


    @bot.command(name='test')
    async def test(ctx):
        # Trouver le canal 'test' par son ID
        channel_test = bot.get_channel(CHANNEL_TEST)
        ROLE_NAME = "test"
        
        # Créer le rôle 'test' s'il n'existe pas
        role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
        if role is None:
            role = await ctx.guild.create_role(name=ROLE_NAME)
        
        # Envoyer un message dans le canal 'test'
        message = await channel_test.send(f"Réagissez avec ✅ pour obtenir le rôle '{ROLE_NAME}'.")
        
        # Attendre la réaction de l'utilisateur
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        
        reaction, user = await bot.wait_for('reaction_add', check=check)
        
        # Assigner le rôle au membre
        await ctx.author.add_roles(role)
        
        # Envoyer un message de confirmation
        await channel_test.send(f"Rôle '{ROLE_NAME}' attribué à {ctx.author.mention}.")
        
        # Créer un thread avec le nom du rôle
        thread_name = f"{ROLE_NAME}_thread"
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        thread_channel = await ctx.guild.create_text_channel(name=thread_name, overwrites=overwrites)
        
        # Envoyer un message dans le thread
        await thread_channel.send(f"Bienvenue dans le thread pour le rôle '{ROLE_NAME}'!")



    return 0
