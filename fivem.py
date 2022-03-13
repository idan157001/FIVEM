import asyncio
import os
import json
import time
from datetime import datetime,date
import discord
from discord.ext import commands,tasks
from json import JSONDecodeError
import aiohttp
import random
#
from firebase import FireBase_DB as DB
from core import Server_info
#

client = commands.Bot(command_prefix='f!')
client.remove_command('help')
DEV = "Flash_Bot"


    
@client.event
async def on_guild_remove(guild):
    servers = 0
    for _ in client.guilds:
        servers+= 1

    DB(guild.id).del_server()
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Servers:{servers}")) 
    
@client.event
async def on_guild_join(guild):
    global flash
    db = DB(guild.id)   
         
    db.add_new_server(guild.name)
       
    servers = 0
    for _ in client.guilds:
        servers+= 1
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Servers:{servers}")) 
    try:
        config = await guild.create_text_channel(name="・flash_bot") # text channel
        flash = await guild.create_voice_channel(name="・Flash_Bot") # voice channel
        db.update_by_data({"v_channel":f"{flash.id}"})
        x = guild.me.guild_permissions
        if x.manage_channels == True and x.send_messages == True  and x.read_messages == True  and x.view_channel == True and x.manage_messages == True:
            pass
        else:
            print("dont have permission")
        embed = discord.Embed(title=f'Thanks for inviting me to your server!',description="I am FiveM bot\n I am here to help you with FiveM status\n\
                                                                                            This is FiveM Status project that we developed for FiveM players\n\
                                                                                            Have Fun ;)\n\
                                                                                            It should be noted that this is **Beta Project**\n\
                                                                                            This Project Developed By **Idan#8461**",timestamp=datetime.utcnow(), color=84848)
        
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/803961555267485736/931623750175187054/unknown.png")
        embed.set_footer(text=f'Flash_Bot Beta Project')
        await voice_connect()
        await config.send(embed=embed)
        await help(config)
        await config.set_permissions(guild.default_role, view_channel=False)
        

    except commands.errors.CommandInvokeError:
        await config.send("Missing Permissions")
    except Exception as e:
        pass

@client.command()
@commands.has_permissions(administrator = True)
async def help(ctx):
    embed = discord.Embed(title=f'Fivem Status',timestamp=datetime.utcnow(), color=84848)
    embed.add_field(name="**f!start**", value="Select Channels", inline=False)
    embed.add_field(name="**Information**", value="``f!config``\n``f!config info``\n``f!config title``\n``f!config ip``\n``f!config icon``", inline=False)
    embed.set_footer(text=f'{DEV} | Last Updated:')
    await ctx.send(embed=embed)


@client.event
async def on_ready():
    await voice_connect()
    servers = 0
    for _ in client.guilds:
        servers+= 1
        
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Servers:{servers}"))
    print('Connected')
    await asyncio.sleep(3)    
    while True:
        
        for guild in client.guilds:
            guild = guild
            guild_id = guild.id
        
            try:   
                db = DB(guild_id)

                info_channels = db.channels_id_info
                title_name,icon,IP = db.config_info
                server = Server_info(IP)
                req_json,max_players = await server.send_request()

           
               
                if info_channels[0] is not None and len(info_channels[0])  > 5 and len(info_channels[1]) > 5:
                
                    channel0,channel1,msg0,msg1=info_channels 

                    channel = guild.get_channel(int(channel0)) #ID of channel
                    msg = await channel.fetch_message(int(msg0)) #ID of the message

                    information_channel = guild.get_channel(int(channel1)) #ID of channel
                    information_msg = await information_channel.fetch_message(int(msg1)) #ID of the 
                    
                    if req_json is None: 
                            try:
                                #Offline
                                embed = discord.Embed(title="``👥`` ``Players: [0/0]``\n``🔴`` ``Status`` - Server Offline ",description="", colour=discord.Colour.red(),timestamp=datetime.utcnow())
                                embed.set_thumbnail(url=f"{icon}")
                                embed.set_author(name =f"{title_name}", icon_url=f"{icon}")
                                embed.set_footer(text=f'{DEV} | Last Updated:', icon_url=f"{icon}")
                                await msg.edit(embed=embed)
                                

                                #################################
                                embed = discord.Embed(title=f"**{title_name} information**", colour=discord.Colour.red(),timestamp=datetime.utcnow())
                                embed.set_thumbnail(url=f"{icon}")
                                embed.set_footer(text=f'{DEV} | Last Updated:', icon_url=f"{icon}")
                                embed.add_field(name=f"``🔴`` ``Status``\n``👥`` ``Players: Server Offline ``", value=f"``🌐`` ``IP-{IP}``\n  ")
                                await information_msg.edit(embed=embed)
                            except discord.errors.NotFound:
                                pass
                            except discord.errors.HTTPException:
                                #await msg.channel.send("Config Icon Is Wrong\nChanged to Default!")
                                db.update_by_data({"icon":""})#config icon error change it do default ""
                            except Exception as e:
                                pass
                    
                        
                    else:
                        try:
                            
                            
                            #Online
                        
                            id,name,dis,players_length = server.build_form(req_json)
                            
                            if id == "None":
                                TITLE = f"{title_name}\n ``👥`` ``Players`` - ``{players_length}/{max_players}``\n ``👽`` `` Space``   - ``0% `` \n ``⚪`` ``Status``   - ``Server is empty``" # SERVER OPEN WITH 0 PLAYERS
                               
                            else:
                                space = server.caculate_space(players_length,max_players)
                                TITLE = f"``👥``  ``Players`` - ``[{players_length}/{max_players}]``\n``👽``  `` Space`` -  ``{space}%`` \n``🟢``  ``Status`` -  ``ONLINE`` " # SERVER ONLINE WITH PLAYERS 
                                
                            
                            #await guild.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"🐌[{players_length}/{max_players}] ({guild.member_count})"))
                            embed = discord.Embed(title=TITLE, colour=discord.Colour.green(), timestamp=datetime.utcnow())
                            embed.set_footer(text=f'{DEV} | Last Updated:', icon_url=f"{icon}")
                            embed.set_author(name =f"{title_name}", icon_url=f"{icon}")
                            embed.set_thumbnail(url=f"{icon}")

                            embed.add_field(name="[💳ID] ", value=id,inline=True)
                            embed.add_field(name="[👥Name]", value=name,inline=True)
                            embed.add_field(name="[💻 Discord ]", value=dis,inline=True)
                            embed.set_thumbnail(url=f"{icon}")
                            embed.set_footer(text=f'{DEV} | Last Updated:', icon_url=f"{icon}")
                            
                            await msg.edit(embed=embed)


                            #########################
                            embed = discord.Embed(title=f"Status Information", colour=discord.Colour.green(), timestamp=datetime.utcnow())
                            embed.add_field(name=f"``🟢`` ``Status``\n``👥`` ``Players: [{players_length}/{max_players}]``\n``📉`` ``Empty Slots: [{int(max_players)-int(players_length)}]``", value=f"``🌐`` ``IP- {IP}``  ")
                            embed.set_author(name =f"{title_name}", icon_url=f"{icon}")
                            embed.set_thumbnail(url=f"{icon}")
                            embed.set_footer(text=f'{DEV} | Last Updated:', icon_url=f"{icon}")
                            await information_msg.edit(embed=embed)
                        except discord.errors.NotFound:
                            pass
                        except discord.errors.HTTPException:
                            #await msg.channel.send("Config Icon Is Wrong\n\nChanged to Default!")
                            db.update_by_data({"icon":""})#config icon error change it do default ""
                            await asyncio.sleep(2)
                        except Exception as e:
                            pass

                #
                else:
                    pass
            
            except Exception as e:
                print(e)
@client.command()
@commands.has_permissions(administrator = True)
async def start(ctx):
    ch_id = ctx.message.channel.id
    channel0 = client.get_channel(ch_id)
    db = DB(ctx.guild.id)
    

    def check(message):
        return message

    async def channel0(ctx):
        await ctx.send("Pick Channel for Status #<channel>")
        channel0 = await client.wait_for("message",check=check)
        if channel0.channel_mentions != []:
            channel0 = channel0.channel_mentions[0].id
            return str(channel0)
        else:
            await ctx.send("Could not found this channel\nTry again")
            return None

    async def channel1(ctx):
        await ctx.send("Pick Channel for ON/OFF #<channel>")
        channel1 = await client.wait_for("message",check=check)
        if channel1.channel_mentions != []:
            channel1 = channel1.channel_mentions[0].id
            return str(channel1)
        else:
            await ctx.send("Could not found this channel\nTry again")
            return None
        
    c0 = await channel0(ctx)
    if c0 is not None and len(c0) > 5:    
        c1 = await channel1(ctx)
        if c1 is not None:
            chann0 = ctx.guild.get_channel(int(c0))
            chann1 = ctx.guild.get_channel(int(c1))
            msg0 = await chann0.send(".")
            msg1 = await chann1.send(".")
            data = {"channel_id0":c0,"msg0":msg0.id,"msg1":msg1.id,"channel_id1":c1}
            db.update_by_data(data)
            await ctx.send("Updated",delete_after=2)
    
    

@start.error        
async def start(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error,commands.errors.CommandInvokeError):
        await ctx.send("Missing Permissions")
    else:
        await ctx.send("Something went wrong")



 


@client.command()
@commands.has_permissions(administrator = True)
async def config(ctx,info):
    db = DB(ctx.message.guild.id)

    messages = ["I Updated your data 😉","Your data has been updated","Successfully updated","Got it 😉"]
    updated = random.choice(messages)
    def check(message):
        if message.content not in ["Enter Status Title","Enter Status Icon","Enter Status IP"]:
            return message

    guild = ctx.message.guild.id
    
    if info.lower() == "title":
        await ctx.send("Enter Status Title")
        title = await client.wait_for("message",check=check)
        if title.content == "None" or title.content == 'none':
            data = {"title":""}
        else:
            data = {"title":title.content}
        db.update_by_data(data)
        await ctx.send(f"{updated}",delete_after=2)

    elif info.lower() == "icon":
        await ctx.send("Enter Status Icon")
        icon = await client.wait_for("message",check=check)
        if icon.content.lower() == "none":
            data = {"icon":""}
        elif icon.content.startswith("http") is not True:
            await ctx.send("Icon Is Wrong")
            data = {"icon":""}
            return
        else:
            data = {"icon":icon.content}
        db.update_by_data(data)
        await ctx.send(f"{updated}",delete_after=2)

    elif info.lower() == "ip":
        await ctx.send("Enter Status IP")
        ip = await client.wait_for("message",check=check)
        data = {"ip":ip.content}
        db.update_by_data(data)
        await ctx.send(f"{updated}",delete_after=2)
    if info.lower() =="info":
        try:
            data = db.info_by_data({"title":"","ip":"","icon":""})

            embed = discord.Embed(title="Config",description="", colour=discord.Colour.red())
            embed.add_field(name="**Title**",value=f"``{data['title']  if len(data['title']) >= 1 else 'None'}``",inline=False)
            embed.add_field(name="**Ip**",value=f"``{data['ip']  if len(data['ip']) >= 1 else 'None'}``",inline=False)
            embed.add_field(name="**Icon**",value=f"``{data['icon']  if len(data['icon']) >= 1 else 'None'}``",inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Something went wrong")
@config.error        
async def config_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        db = DB(ctx.guild.id)
        data = db.info_by_data({"title":"","ip":"","icon":""})
        
        embed = discord.Embed(title="Config",description="", colour=discord.Colour.red())
        embed.add_field(name="f!config title",value=f"Title of the server",inline=False)
        embed.add_field(name="f!config ip",value=f"ip of the server",inline=False)
        embed.add_field(name="f!config icon",value=f"icon of the server",inline=False)
        await ctx.send(embed=embed)
    else:
        pass

@client.event    
async def on_command_error(ctx,error):
    if isinstance(error,discord.errors.Forbidden):
        await ctx.send("I dont have the permission to do that")
    pass

@client.command()
@commands.has_permissions(administrator = True)  
async def leave(ctx,id):
    if ctx.author.id == 353898849334460417:
        try:
            await client.get_guild(int(id)).leave()
            await ctx.send("Just Left ;)",delete_after=3)
        except:pass


async def voice_connect():
    for guild in client.guilds:
        try: 
            db = DB(guild.id)
            voice_id = db.info_by_data({"v_channel":""})
            if voice_id["v_channel"] != "":
                c = guild.get_channel(int(voice_id["v_channel"])) 
                connected = (discord.utils.get(client.voice_clients, guild=guild))
                if connected is None:
                    await c.connect()
                    
                else:
                    if connected.channel.id != int(voice_id["v_channel"]):
                        await connected.disconnect()
                        await asyncio.sleep(2)
                        await c.connect()
               
        except Exception as e:
            pass


TOKEN = os.getenv("TOKEN")
client.run(TOKEN)

