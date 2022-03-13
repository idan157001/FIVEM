import pyrebase
from requests.exceptions import ConnectionError
import os
import json
import time
from datetime import datetime,date
import discord
from discord.ext import commands,tasks
import requests
from json import JSONDecodeError


apiKey = os.getenv("apiKey")
appId = os.getenv("appId")
authDomain = os.getenv("authDomain")
databaseURL =os.getenv("databaseURL")
email = os.getenv("email")
messagingSenderId = os.getenv("messagingSenderId")
password = os.getenv("password")
projectId = os.getenv("projectId")
storageBucket = os.getenv("storageBucket")

firebaseConfig = {
    "apiKey": apiKey,
    "authDomain": authDomain,
    "databaseURL": databaseURL,
    "projectId": projectId,
    "storageBucket": storageBucket,
    "messagingSenderId": messagingSenderId,
    "appId": appId,
    "databaseURL": databaseURL
  }
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

x = auth.sign_in_with_email_and_password(email,password)



############

def get_status_info(guild_id):
  data = db.child("Servers").child(guild_id).get()
  data = data.val()
  return data["channel_id0"],data["channel_id1"],data["msg0"],data["msg1"]

def create_table(guild_id,server_name):
  guild_id = str(guild_id)
  data = {"title":"","icon":"","ip":"","server_name":server_name,"channel_id0":"","channel_id1":"","msg0":"","msg1":"","v_channel":""}
  
  guild_obj = db.child("Servers").child(guild_id).get()
  if guild_obj.val() is None:
    db.child("Servers").child(guild_id).set(data)

def update_by_data(guild_id,data):
  db.child("Servers").child(guild_id).update(data)

def get_info_by_data(guild_id,info):
  data = db.child("Servers").child(guild_id).get()
  data = data.val()
  for key in data:
    for i in info:
      if key == i:
        info[i] = data[key]
  return info

def status_update(guild_id,channel0,msg0,msg1):
  guild_id,channel0,msg0,msg1 = str(guild_id),str(channel0),str(msg0),str(msg1)
  data = {"channel_id0":channel0,"msg0":msg0,"msg1":msg1}
  db.child("Servers").child(guild_id).update(data)

def get_information(guild_id):
  data = db.child("Servers").child(guild_id).get()
  data = data.val()
  return data["title"],data["icon"],data["ip"]

def del_db(guild_id):
  db.child("Servers").child(guild_id).remove()


