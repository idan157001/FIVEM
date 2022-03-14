from app.fivem import client
import os

if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    client.run(TOKEN)