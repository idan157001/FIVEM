import pyrebase
import os
from datetime import datetime,date
from discord.ext import commands,tasks



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
class FireBase_DB:
  def __init__(self,guild_id: int):
    self.guild_id = str(guild_id)

  def channels_id_info(self):
    """Getting Channel/Messages ID's from db """
    data = db.child("Servers").child(self.guild_id).get()
    data = data.val()
    return data["channel_id0"],data["channel_id1"],data["msg0"],data["msg1"]
  ##
  def add_new_server(self,server_name):
    """Adding new server to db initilize attributes """

    data = {"title":"","icon":"","ip":"","server_name":server_name,"channel_id0":"","channel_id1":"","msg0":"","msg1":"","v_channel":""}
    guild_obj = db.child("Servers").child(self.guild_id).get()
    if guild_obj.val() is None:
      db.child("Servers").child(self.guild_id).set(data)
##
  def update_by_data(self,data):
    db.child("Servers").child(self.guild_id).update(data)
##
  def info_by_data(self,information):
    data = db.child("Servers").child(self.guild_id).get()
    db_keys = data.val()
    for key in db_keys:
      for item in information:
        if key == item:
          information[item] = data[key]
    return information
##
  def status_update(self,channel0,msg0,msg1): # NOT USED NEED TO CHECK
    self.guild_id,channel0,msg0,msg1 = str(self.guild_id),str(channel0),str(msg0),str(msg1)
    data = {"channel_id0":channel0,"msg0":msg0,"msg1":msg1}
    db.child("Servers").child(self.guild_id).update(data)
##
  def config_info(self):
    data = db.child("Servers").child(self.guild_id).get()
    data = data.val()
    return data["title"],data["icon"],data["ip"]
##
  def del_server(self):
    db.child("Servers").child(self.guild_id).remove()


