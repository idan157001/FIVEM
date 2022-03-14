import requests
import aiohttp
import json




class Server_info():
    def __init__(self,ip):
        self.ip = ip

    async def send_request(self):
        x = [f'http://{self.ip}/players.json',f'http://{self.ip}/info.json']
        req_players,req_server_info= "",""
        try:
            async with aiohttp.ClientSession() as session:
                for i in x:  
                    async with session.get(i,timeout=1) as resp:
                        resp = await resp.read()
                        resp = json.loads(resp)
                        if i.endswith("players.json"):
                            req_players = resp
                        else:
                            req_server_info = resp
                            for item in req_server_info:
                                if item == 'vars':
                                    max_players = req_server_info['vars']['sv_maxClients']
            
            return req_players,max_players
                   
        
        
        except Exception as e:
            return None,None
            

    def build_form(self,req_json):
        info = {"id":[],"name":[],"dis":[]}
        f_id,f_name,f_dis = "","",""
        p = list()
        

        if req_json == []:
            return "None","None","None","0"

        for item in req_json:
            id = item['id']
            name = (item['name'])
            #ping = (item['ping'])
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

