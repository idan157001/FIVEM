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
firebaseConfig = {
    "apiKey": "AIzaSyBi5lCG1nrj6Q6wsYp8jid4eGrKjpay-1w",
    "authDomain": "developmentfivemx-fef16.firebaseapp.com",
    "databaseURL": "https://developmentfivemx-fef16-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "developmentfivemx-fef16",
    "storageBucket": "developmentfivemx-fef16.appspot.com",
    "messagingSenderId": "646628019661",
    "appId": "1:646628019661:web:e60edb1dd0edf077b70884",
    "databaseURL": "https://developmentfivemx-fef16-default-rtdb.europe-west1.firebasedatabase.app/u99zXqOp6tYDd370gzvKrgmUz742"
  }
email = "idanalbam1@gmail.com"
password = "admin123"
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


create_table("698299485570203658","idan")