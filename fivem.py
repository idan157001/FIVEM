import asyncio
from requests.exceptions import ConnectionError
import os
import json
import time
from datetime import datetime,date
import discord
from discord.ext import commands,tasks
import requests
from json import JSONDecodeError
from firebase import *
class Server_info():
    def __init__(self,ip):
        self.ip = ip

    def send_request(self):
        try:
            req_players = (requests.get(f'http://{self.ip}/players.json')).json()
            req_server_info = (requests.get(f'http://{self.ip}/info.json')).json()
            if req_server_info:
                
                for item in req_server_info:
                    if item == 'vars':
                        max_players = req_server_info['vars']['sv_maxClients']
            
                return req_players,max_players
        except ConnectionError:
            return None,None
        except JSONDecodeError:
            return None,None
        except Exception as e:
            return None,None
            

    def build_form(self,req_json):
        info = {"id":[],"name":[],"dis":[]}
        f_id,f_name,f_dis = "","",""
        p = list()
        final = ""

        if req_json == []:
            return "None","None","None","0"

        for item in req_json:
            id = item['id']
            name = (item['name'])
            ping = (item['ping'])
            for i in item['identifiers']:
                if 'discord' in i:
                    dis_id = str(i).split(':')[1]
                    
                    discord = f'<@{dis_id}>'

            p.append(f'{id}: {name} {discord} ')
        
        sort = sorted(p,key=lambda x:int(x.split(':')[0]))
        for i in sort:
            info["id"].append(i.split(':')[0])
            info["name"].append(i.split(':')[1].split("<")[0])
            info["dis"].append(i.split()[-1])

        for i in info["id"]:
            t = len(f"**{i}**\n")
            if len(f_id)+t < 1024:
                f_id+= f"**{i}**\n"
            else:
                break

        for i in info["name"]:
            if len(f_name)+len(f"{i}\n") < 1024:
                f_name+=f"{i}\n"
            else:
                break
        for i in info["dis"]:
            if len(f_dis)+len(f"{i}\n") < 1024:
                f_dis+=f"{i}\n"
            else:
                break

        
        length = len(sort)
        return f_id,f_name,f_dis,length
        
    def caculate_space(self,players_length,max_players):
        try:
            players_length,max_players = int(players_length),int(max_players)
            precent = (round((players_length/max_players)*100))
            return precent
        except:
            pass


client = commands.Bot(command_prefix='-')


@tasks.loop(seconds=5.0)
async def update_new():
    for guild in client.guilds:
      create_table(guild.id,guild.name)
    
    
    

    
            
@client.event
async def on_ready():
    update_new.start()
    print('Connected')
    await asyncio.sleep(3)
    DEV = "Idan#8461"
    
    while True:
        for guild in client.guilds:
            guild = guild
            guild_id = guild.id
            
            try:
                     
                info_channels= get_status_info(guild_id)
                title_name,icon,IP = get_information(guild_id)
                server = Server_info(IP)
                req_json,max_players = server.send_request()[0],server.send_request()[1]

           
               
                if info_channels[0] is not None and len(info_channels[0])  > 5 and len(info_channels[1]) > 5:
                
                    channel0,channel1,msg0,msg1=get_status_info(guild_id) #stopped here work need to use -channel before 

                    channel = guild.get_channel(int(channel0)) #ID of channel
                    msg = await channel.fetch_message(int(msg0)) #ID of the message

                    information_channel = guild.get_channel(int(channel1)) #ID of channel
                    information_msg = await information_channel.fetch_message(int(msg1)) #ID of the 
                    
                    if req_json is None: 
                            try:
                                #Offline
                                #await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"yy"))
                                #await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=f"🐌[OFF] xx")) 
                                embed = discord.Embed(title="``👥`` ``Players: [0/0]``\n``🔴`` ``Status`` - Server Offline ",description="", colour=discord.Colour.red(),timestamp=datetime.utcnow())
                                embed.set_thumbnail(url=f"{icon}")
                                embed.set_author(name =f"{title_name}", icon_url=f"{icon}")
                                embed.set_footer(text=f'{DEV} | Last Updated: Today ·', icon_url=f"{icon}")
                                await msg.edit(embed=embed)
                                

                                ##################################
                                embed = discord.Embed(title=f"**{title_name} information**", colour=discord.Colour.red())
                                embed.set_thumbnail(url=f"{icon}")
                                embed.set_footer(text=f'{DEV} | Last Updated: Today ·', icon_url=f"{icon}")
                                embed.add_field(name=f"``🔴`` ``Status``\n``👥`` ``Players: Server Offline ``", value=f"``🌐`` ``IP-❌``\n  ")
                                await information_msg.edit(embed=embed)
                            except discord.errors.NotFound:
                                print(1)
                            except discord.errors.HTTPException:
                                await msg.channel.send("Config Icon Is Wrong\nChanged to Default!")
                                update_by_data(guild.id,{"icon":""})#config icon error change it do default ""
                            except Exception as e:
                                raise e
                    
                        
                    else:
                        try:
                            
                            space = server.caculate_space(server.build_form(req_json)[3],max_players)
                            #Online
                        
                            id,name,dis,players_length = server.build_form(req_json)
                            if id == "None":
                                TITLE = f"{title_name}\n ``👥`` ``Players`` - ``{players_length}/{max_players}``\n ``👽`` `` Space``   - ``{space}% `` \n ``⚪`` ``Status``   - ``Server is empty``" # SERVER OPEN WITH 0 PLAYERS
                               
                            else:
                                TITLE = f"``👥``  ``Players`` - ``[{players_length}/{max_players}]``\n``👽``  `` Space`` -  ``{space}%`` \n``🟢``  ``Status`` -  ``ONLINE`` " # SERVER ONLINE WITH PLAYERS 
                                
                            
                            #await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"xxxxx)"))
                            #await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"🐌[{players_length}/{max_players}] ({guild.member_count})"))
                            embed = discord.Embed(title=TITLE, colour=discord.Colour.green(), timestamp=datetime.utcnow())
                            embed.set_footer(text=f'{DEV} | Last Updated: Today ·', icon_url=f"{icon}")
                            embed.set_author(name =f"{title_name}", icon_url=f"{icon}")
                            embed.set_thumbnail(url=f"{icon}")

                            embed.add_field(name="[💳ID] ", value=id,inline=True)
                            embed.add_field(name="[👥Name]", value=name,inline=True)
                            embed.add_field(name="[💻 Discord ]", value=dis,inline=True)
                            embed.set_thumbnail(url=f"{icon}")
                            embed.set_footer(text=f'{DEV} | Last Updated: Today ·', icon_url=f"{icon}")
                            
                            await msg.edit(embed=embed)


                            #########################
                            embed = discord.Embed(title=f"{title_name} Status Information", colour=discord.Colour.green(), timestamp=datetime.utcnow())
                            embed.add_field(name=f"``🟢`` ``Status``\n``👥`` ``Players: [{players_length}/{max_players}]``", value=f"``🌐`` ``IP-Soon..``  ")
                            embed.set_author(name =f"{title_name}", icon_url=f"{icon}")
                            embed.set_thumbnail(url=f"{icon}")
                            embed.set_footer(text=f'{DEV} | Last Updated: Today ·', icon_url=f"{icon}")
                            await information_msg.edit(embed=embed)
                        except discord.errors.NotFound:
                            print(1)
                        except discord.errors.HTTPException:
                            await msg.channel.send("Config Icon Is Wrong\n\nChanged to Default!")
                            update_by_data(guild.id,{"icon":""})#config icon error change it do default ""
                            await asyncio.sleep(3)
                        except Exception as e:
                            print(0)

                
                else:
                    pass
                    await asyncio.sleep(2)
            except Exception as e:
                raise e
@client.command()
@commands.has_permissions(administrator = True)
async def start(ctx):
    ch_id = ctx.message.channel.id
    channel0 = client.get_channel(ch_id)
    

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
            update_by_data(ctx.guild.id,data)
            await ctx.send("Updated",delete_after=2)
    
    #status_update(ctx.message.guild.id,channel0.id,msg0.id,msg1.id)

"""@start.error        
async def config_error(ctx: commands.Context, error: commands.CommandError):
    await ctx.send("x")"""



    
            
      
    
@client.command()
@commands.has_permissions(administrator = True)
async def say(ctx,*,msg):
    await ctx.message.delete()
    await ctx.send(f'{msg}')

@client.command()
@commands.has_permissions(administrator = True)
async def config(ctx,info):
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
        update_by_data(guild,data)
        await ctx.send("Updated!")

    elif info.lower() == "icon":
        await ctx.send("Enter Status Icon")
        icon = await client.wait_for("message",check=check)
        if icon.content == "None" or icon.content == 'none':
            data = {"icon":""}
        elif icon.content.startswith("http") is not True:
            await ctx.send("Icon Is Wrong")
            data = {"icon":""}
            return
        else:
            data = {"icon":icon.content}
        update_by_data(guild,data)
        await ctx.send("Updated!")

    elif info.lower() == "ip":
        await ctx.send("Enter Status IP")
        ip = await client.wait_for("message",check=check)
        data = {"ip":ip.content}
        update_by_data(guild,data)
        await ctx.send("Updated!")
    if info.lower() =="info":
        try:
            data = get_info_by_data(ctx.guild.id,{"title":"","ip":"","icon":""})

            embed = discord.Embed(title="Config",description="", colour=discord.Colour.red())
            embed.add_field(name="-config title",value=f"{data['title']  if len(data['title']) >= 1 else 'None'}",inline=False)
            embed.add_field(name="-config ip",value=f"``{data['ip']  if len(data['ip']) >= 1 else 'None'}``",inline=False)
            embed.add_field(name="-config icon",value=f"{data['icon']  if len(data['icon']) >= 1 else 'None'}",inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Something went wrong")
@config.error        
async def config_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        data = get_info_by_data(ctx.guild.id,{"title":"","ip":"","icon":""})
        
        embed = discord.Embed(title="Config",description="", colour=discord.Colour.red())
        embed.add_field(name="-config title",value=f"Title of the server",inline=False)
        embed.add_field(name="-config ip",value=f"ip of the server",inline=False)
        embed.add_field(name="-config icon",value=f"icon of the server",inline=False)
        await ctx.send(embed=embed)
    else:
        pass
    

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)

