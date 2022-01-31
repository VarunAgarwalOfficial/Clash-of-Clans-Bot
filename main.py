token = 'OTMyODg3NTA1MTg1OTUxNzk0.YeZhMQ.FDIAs5EEa_osoFoiK2Mh3oTP4i0'

import discord
import json
import random
import os
import time



client = discord.Client()

with open("base_array.json", "r") as f:
    base_array = json.load(f)["arr"]
print(len(base_array))
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!base'):
        bases = random.choice(base_array)
        await message.channel.send("Video Title : " + bases["title"].split("|")[1] + os.linesep + os.linesep)
        base_images = bases["imgs"]
        bases_txt = os.linesep.join(bases["bases"][0].split("\n"))
        # bases_txt = bases["bases"][0].split("\n")

        # first_half = bases_txt[:len(bases_txt)//2]
        # second_half = bases_txt[len(bases_txt)//2:]
        # await message.channel.send(os.linesep.join(first_half))
        # await message.channel.send(os.linesep.join(second_half))

        for i , image in enumerate(base_images):
            st_index = bases_txt.find(str(i+1)+":")
            end_index = bases_txt.find(str(i+2)+":")

            await message.channel.send(bases_txt[st_index:end_index])
            await message.channel.send(f"https://raw.githubusercontent.com/agarwalvarun1/clash_youtube/master/images/{image}")
            
            time.sleep(1)

client.run(token)
