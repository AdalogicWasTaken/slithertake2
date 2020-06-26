#The bot is actually named Slither but im too lazy to change the file name
import os

import yaml
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
from discord.ext.commands import bot
import re
import shutil
from discord.utils import get
from PyDictionary import PyDictionary
import typing
from discord.ext.commands import Bot, has_permissions, CheckFailure

dictionary=PyDictionary()

def timeout():
    future = datetime.now() + timedelta(seconds=20)
    while True:
        if datetime.now() == future:
            channel = int(726218132032585749)
            await channel.send("Yikes")
        else:
            pass

TOKEN = 'NzIyNTc1NzAwNzMyNjc0MTEx.Xup5YQ.84dqnKZngB1g7Suak_w1GHIvVEc'

bot = commands.Bot(command_prefix ='s.')
bot.guild_id = 0
bot.log_enable = False

#on ready message, setup activity
@bot.event
async def on_ready():
    print("Connected to Discord")
    with open (r'C:\Users\Cindyarta\PycharmProjects\assimilate\guilds.yaml', 'w') as file:
        yaml.dump(['Guild Info And log Channel ID'], file)
    with open (r'C:\Users\Cindyarta\PycharmProjects\assimilate\mail.yaml', 'w') as file:
        yaml.dump(['Mail Setup'], file)
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\roles.yaml', 'w') as file:
        yaml.dump(['self roles'], file)
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\suggestions.yaml', 'w') as file:
        yaml.dump(['suggestions'], file)
    await bot.change_presence(activity=discord.Game(name="s.commands"))
    timeout()
    for guild in bot.guilds:
        break

#commands command
@bot.command()
async def commands(ctx):
    await ctx.send("```s.log <channel>``` \n*Administrator command only:* Used to assign the log channel. \n\n```s.recover <channel> <number of days> <user (optional)>``` \nRecovers the message history of the specified channel within the past number of days specified. If a user is specified, Slither will only include messages made by that user \n\n```s.members <total/online>``` \nReturns number of members total/currently online in the server \n\n```s.mail_setup <channel> <role> <ping/noping>``` \n*Administrator command only:* Sets up an Inbox for the command ``s.mail_send``, as well as what role can reply to mail. If ping is enabled, Slither will ping the role specified whenever a new mail is sent to Inbox \n\n```s.mail_send <message>``` \nMails a message to Inbox \n\n```s.mail_respond <receiver> <message>``` \nResponds to mail sent by a user. *Only members with the role specified in* ``s.mail_setup`` *can use this command* \n\n```s.define <word>``` sends the definition(s) of a word \n\n```s.selfrole_add <role>``` \n*Administrator command only:* Adds a role to ``s.selfrole`` \n\n```s.selfrole <role``` \nAssigns you a role \n\n```s.selfrole_remove <role>``` \n*Administrator command only:* Removes a role from ``s.selfrole`` \n\n```s.suggest <message>``` \n\nSends a suggestion to the owner of this bot")

#log command
@bot.command()
@has_permissions(administrator=True)
async def log(ctx, channel):
    with open (r'C:\Users\Cindyarta\PycharmProjects\assimilate\guilds.yaml', 'r+') as file:
        bot.channelid = re.sub('<', '', re.sub('>', '', re.sub('#', '', channel)))
        bot.channelname = bot.get_channel(int(bot.channelid))
        if bot.channelname != None:
            bot.guildinfo = None
            print(bot.guildinfo)
            bot.guildinfo = yaml.load(file, Loader=yaml.FullLoader)
            file.close()
            with open (r'C:\Users\Cindyarta\PycharmProjects\assimilate\guilds.yaml', 'w') as file:
                bot.guildinfo.append(ctx.message.guild.id)
                bot.guildinfo.append(int(bot.channelid))
                yaml.dump(bot.guildinfo, file)
            await ctx.send("" + str(channel) + " has been chosen as the log channel.")
            bot.log_enable = True
        else:
            await ctx.send("Invalid channel name. Please try again")
@log.error
async def log_error(ctx, error):
    if isinstance(error, CheckFailure):
        ctx.send("Sorry, only members with the permission ``administrator`` can use this command.")

#log messages
@bot.event
async def on_message(message):
    await bot.wait_until_ready()
    await bot.process_commands(message)
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\guilds.yaml', 'r+') as file:
        if message.author != bot.user:
            bot.findlog_channel = yaml.load(file, Loader=yaml.FullLoader)
            bot.findlog_channel.reverse()
            bot.findguild_id = bot.findlog_channel.index(int(message.guild.id))
            bot.logchannel = bot.findlog_channel[(bot.findguild_id - 1)]
            channel = bot.get_channel(bot.logchannel)
            if channel != None:
                await channel.send("Message posted by " + str(message.author) + " in " + str(message.channel) + ": \"" + message.content + "\" \nTime posted: " + str(datetime.now()) + "\n.\n.\n.")

#log message deletes
@bot.event
async def on_message_delete(message):
    await bot.wait_until_ready()
    await bot.process_commands(message)
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\guilds.yaml', 'r+') as file:
        if bot.log_enable == True and message.author != bot.user:
            bot.findlog_channel = yaml.load(file, Loader=yaml.FullLoader)
            bot.findlog_channel.reverse()
            bot.findguild_id = bot.findlog_channel.index(int(message.guild.id))
            bot.logchannel = bot.findlog_channel[(bot.findguild_id - 1)]
            channel = bot.get_channel(bot.logchannel)
            if channel != None:
                await channel.send("Message *DELETED* by " + str(message.author) + " in " + str(message.channel) + ": \"" + message.content + "\" \nTime deleted: " + str(datetime.now()) + "\n.\n.\n.")

#log message edits
@bot.event
async def on_message_edit(before, after):
    await bot.wait_until_ready()
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\guilds.yaml', 'r+') as file:
        if bot.log_enable == True and after.author != bot.user:
            bot.findlog_channel = yaml.load(file, Loader=yaml.FullLoader)
            bot.findlog_channel.reverse()
            bot.findguild_id = bot.findlog_channel.index(int(before.guild.id))
            bot.logchannel = bot.findlog_channel[(bot.findguild_id - 1)]
            channel = bot.get_channel(bot.logchannel)
            if channel != None:
                await channel.send("Message *EDITED* by " + str(after.author) + " in " + str(after.channel) + " (original author: " + str(before.author) + "). \nBEFORE: \"" + before.content + " \" \nAFTER: \"" + after.content + "\" \nTime edited: " + str(datetime.now()) + "\n.\n.\n.")

#recover command
@bot.command()
async def recover(ctx, channelid, num, user: typing.Optional[str] = None):
    await bot.wait_until_ready()
    days_ = 0
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\recover.txt', 'a+', encoding="utf-8") as text:
        if user != None:
            print(user)
            user2 = re.sub('<', '', re.sub('>', '', re.sub('!', '', re.sub('@', '', user))))
            userid = bot.get_user(int(user2))
            print(user2)
            print(userid)
        channelid2 = re.sub('<', '', re.sub('>', '', re.sub('#', '', channelid)))
        channel = bot.get_channel(int(channelid2))
        days_ = int(num)
        if days_ > 7:
            await ctx.send("Sorry, the max amount of days is ``7``.")
        elif days_ <= 7:
            await ctx.send("This might take a moment...")
            daylimit = datetime.now() - timedelta(days=days_)
            history = await channel.history(limit=None, after=daylimit, oldest_first=True).flatten()
            print(f"Message history of {channel} (from OLDEST to NEWEST) \n.\n.", sep="\n\n", file=text)
            for i in history:
                if user == None:
                    print("\"" + i.clean_content + "\" (Author: " + str(i.author) + " || posted at " + str(i.created_at) + ")\n.\n.\n.", sep="\n\n", file=text)
                if user != None:
                    if i.author == userid:
                        print("\"" + i.clean_content + "\" (Author: " + str(i.author) + " || posted at " + str(i.created_at) + ")\n.\n.\n.", sep="\n\n", file=text)
            shutil.copyfile(r'C:\Users\Cindyarta\PycharmProjects\assimilate\recover.txt', r'C:\Users\Cindyarta\PycharmProjects\assimilate\file%s.txt' % ctx.message.guild.id)
            text.truncate(0)
            text.close()
            await ctx.send(content="Here you go:", file=discord.File(r'C:\Users\Cindyarta\PycharmProjects\assimilate\file%s.txt' % ctx.message.guild.id))
            os.remove(r'C:\Users\Cindyarta\PycharmProjects\assimilate\file%s.txt' % ctx.message.guild.id)

#members command
@bot.command()
async def members(ctx, type):
    num = 0
    if str(type) == "total":
        for member in ctx.guild.members:
            if not member.bot:
                num = num + 1
    if str(type) == "online":
        for online in ctx.guild.members:
            if not online.bot and online.status != discord.Status.offline:
                num = num + 1
    if str(type) == "total":
        await ctx.send("``" + str(num) + "`` members total in this server.")
    if str(type) == "online":
        await ctx.send("``" + str(num) + "`` members online in this server.")

#mail inbox setup command
@bot.command()
@has_permissions(administrator=True)
async def mail_setup(ctx, channel, role, ping):
    with open (r'C:\Users\Cindyarta\PycharmProjects\assimilate\mail.yaml', 'r+') as file:
        bot.channelidmail = re.sub('<', '', re.sub('>', '', re.sub('#', '', channel)))
        bot.roleidmail = re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))
        bot.channelnamemail = bot.get_channel(int(bot.channelidmail))
        if bot.channelnamemail != None and bot.roleidmail != None and ping == "ping" or ping == "noping":
            bot.guildinfomail = None
            print(bot.roleidmail)
            bot.guildinfomail = yaml.load(file, Loader=yaml.FullLoader)
            print(bot.guildinfomail)
            print(yaml.load(file, Loader=yaml.FullLoader))
            file.close()
            with open (r'C:\Users\Cindyarta\PycharmProjects\assimilate\mail.yaml', 'w') as file:
                bot.guildinfomail.append(ctx.message.guild.id)
                bot.guildinfomail.append(int(bot.channelidmail))
                bot.guildinfomail.append(int(bot.roleidmail))
                bot.guildinfomail.append(str(ping))
                yaml.dump(bot.guildinfomail, file)
            await ctx.send("Alright. Mailbox setup complete.")
            bot.mail_enable = True
        else:
            await ctx.send("Invalid command. Please try again")
@mail_setup.error
async def mail_setup_error(ctx, error):
    if isinstance(error, CheckFailure):
        ctx.send("Sorry, only members with the permission ``administrator`` can use this command.")


#mail send command
@bot.command()
async def mail_send(ctx, *message):
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\mail.yaml', 'r+') as file:
        if ctx.author != bot.user:
            findlog_channel = yaml.load(file, Loader=yaml.FullLoader)
            for i in findlog_channel:
                if i == ctx.message.guild.id:
                    findlog_channel.reverse()
                    findguild_id = findlog_channel.index(int(ctx.message.guild.id))
                    logchannel = findlog_channel[(findguild_id - 1)]
                    roleid = findlog_channel[(findguild_id - 2)]
                    channel = bot.get_channel(logchannel)
                    if (" ".join(message[:])) != None:
                        await ctx.send("Message sent to mailbox. Thank you")
                        if findlog_channel[(findguild_id - 3)] == "ping":
                            rolemention = get(ctx.guild.roles, id=roleid)
                            await channel.send(rolemention.mention + " Mail sent by " + str(ctx.message.author) + ": \n\n\"" + (" ".join(message[:])) + "\"\n.\n.\n.")
                        else:
                            await channel.send("Mail sent by " + str(ctx.message.author) + ": \n\n\"" + (" ".join(message[:] )) + "\"\n.\n.\n.")

#mail respond command
@bot.command()
async def mail_respond(ctx, address, *message):
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\mail.yaml', 'r+') as file:
        if ctx.author != bot.user:
            findlog_channel = yaml.load(file, Loader=yaml.FullLoader)
            for i in findlog_channel:
                if i == ctx.message.guild.id:
                    findlog_channel.reverse()
                    findguild_id = findlog_channel.index(int(ctx.message.guild.id))
                    roleid = findlog_channel[(findguild_id - 2)]
                    if (" ".join(message[:])) != None:
                        if get(ctx.guild.roles, id=roleid) in ctx.author.roles:
                            userid = re.sub('<', '', re.sub('>', '', re.sub('!', '', re.sub('@', '', address))))
                            print(userid)
                            user = bot.get_user(int(userid))
                            print(user)
                            await ctx.send("Message response DMed to user.")
                            await user.send("Response to your mail sent by " + str(ctx.message.author) + " in " + str(bot.get_guild(ctx.message.guild.id)) + ": \n\n\"" + (" ".join(message[:])) + "\"\n.\n.\n.")

#define command
@bot.command()
async def define(ctx, word):
    definition = dictionary.meaning(str(word))
    if definition != None:
        for dict in definition.keys():
            grammar = str(dict)
            await ctx.send("\n ``" + grammar.upper() + ":``\n\n" + ".\n".join(definition[dict]) + ".")
    else:
        await ctx.send(f"\"{word}\" not found in dictionary. Check if it is spelled correctly")

#selfrole add command
@bot.command()
@has_permissions(administrator=True)
async def selfrole_add(ctx, role):
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\roles.yaml', 'r+') as file:
        rolelist = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\roles.yaml', 'w') as file:
        if int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))) not in rolelist:
            rolelist.append(int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))))
            yaml.dump(rolelist, file)
            await ctx.send("Role has been added to your self roles list.")
        elif int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))) in rolelist:
            yaml.dump(rolelist, file)
            await ctx.send("Role already exists in my self roles list. Please specify a different role")
@selfrole_add.error
async def selfrole_add_error(ctx, error):
    if isinstance(error, CheckFailure):
        ctx.send("Sorry, only members with the permission ``administrator`` can use this command.")

#selfrole assign command
@bot.command()
async def selfrole(ctx, role):
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\roles.yaml', 'r+') as file:
        rolelist = yaml.load(file, Loader=yaml.FullLoader)
        if int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))) in rolelist:
            user = ctx.message.author
            if get(ctx.guild.roles, id=int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role)))))) not in ctx.author.roles:
                print("adding role")
                await user.add_roles(get(ctx.guild.roles, id=int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role)))))))
                await ctx.send("You have been assigned: " + str(get(ctx.guild.roles, id=int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))))))
            elif get(ctx.guild.roles, id=int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role)))))) in ctx.author.roles:
                print("removing role")
                await user.remove_roles(get(ctx.guild.roles, id=int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role)))))))
                await ctx.send("Role removed.")
        if int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))) not in rolelist:
            await ctx.send("Role was not found in your server's list of roles allowed. Contact you server admin if you believe this is a mistake")

#selfrole remove command
@bot.command()
@has_permissions(administrator=True)
async def selfrole_remove(ctx, role):
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\roles.yaml', 'r+') as file:
        rolelist = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\roles.yaml', 'w') as file:
        if int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))) in rolelist:
            del rolelist[rolelist.index(int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))))]
            yaml.dump(rolelist, file)
            await ctx.send("Role removed from your self role list.")
        elif int(re.sub('<', '', re.sub('>', '', re.sub('&', '', re.sub('@', '', role))))) not in rolelist:
            yaml.dump(rolelist, file)
            await ctx.send("Role not found in my self roles list. Please specify a different role")
@selfrole_remove.error
async def selfrole_remove_error(ctx, error):
    if isinstance(error, CheckFailure):
        ctx.send("Sorry, only members with the permission ``administrator`` can use this command.")

#suggestions command
@bot.command()
async def suggest(ctx, *message):
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\suggestions.yaml', 'r+') as file:
        list = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    with open(r'C:\Users\Cindyarta\PycharmProjects\assimilate\suggestions.yaml', 'w') as file:
        list.append(' '.join(message[:]))
        yaml.dump(list, file)
        await ctx.send("Suggestion sent. Thank you")



bot.run(TOKEN)
