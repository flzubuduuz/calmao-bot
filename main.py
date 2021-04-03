#Libraries y weas pa que funcione el bot#
import os
import json
from keep_alive import keep_alive
import discord
client = discord.Client()
intents = discord.Intents.default()
intents.members = True

#Abre el archivo con la cuenta actual y lo guarda#
a_file = open("count.json", "r")
json_object = json.load(a_file)
a_file.close()
print(json_object)

#Abre el archivo con los nombres y los guarda#
b_file = open("names.json", "r")
json_names = json.load(b_file)
b_file.close()
print(json_names)

#Embed#
embed=discord.Embed(title="El comando que has enviado no existe.", description="Aquí hay una lista de comandos disponibles (siempre deben ir en minúsculas):", color=0xf40101)
embed.add_field(name="%calmaobot check @usuario", value="Muestra el puntaje del usuario (si no pones usuario, muestra tu propio puntaje).", inline=False)
embed.add_field(name="%calmaobot total", value="Muestra el total de calmaos en el server.", inline=False)
embed.add_field(name="%calmaobot top", value="Muestra las 5 personas más calmadas del server.", inline=False)
embed.add_field(name="¿Qué es este bot?", value='Gracias por preguntar! calmao bot cuenta la cantidad de veces que cada usuario ha dicho "calmao" en el server. Intenta no hacer spam de la palabra, para poder ver quién es, verdaderamente, el mas calmao del server.', inline=False)
embed.add_field(name="\u200B", value="by flzubuduuz. [Repositorio.](https://github.com/flzubuduuz/calmao-bot)", inline=False)

#Pone el status y conecta el bot#
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='%calmaobot'))
    print('{0.user} is up and running'.format(client))

#Para cada mensaje del server se activa esto#
@client.event
async def on_message(message):
    #Salta mensajes si son del mismo bot#
    if message.author == client.user:
      return

    #easter egg#
    if message.content.startswith("%calmaobot check") and len(message.mentions)==1 and message.mentions[0].id==client.user.id:
      await message.channel.send('Calmao puntos de calmao bot: 2̵̢̗̯̼̝̠̦̹͍̥̪̍̐̓̿̃̒͆̔̎̈͌͌͆͝7̵̘͉̲̬̗̭̓́̽̔̄́1̷̛̘̩̮̤̝̿́͑̄͝8̶̢̦̫̹͈̬́͋͂̔͗̊̉͆̒͑́͘͘͘͠͝2̷̢͈͙̬̜͈̼̤͋̋̃͊̆̌̈́̾̒̆͗̚͝8̶͖̰̣̾̽̃͋͊̿̎͐̕1̴̤̠͎̙̭̉͋͗͛̍͗̈́̕8̸̡̢̦̬̜̗̈́̇̈́̈́̇͊̽͆̋͝͠͠2̶̛͔̓̅̚8̷̧̡̡̧̺̣̤̗͕̬͎̎̊͐̊͑̎͗̌̉̆̍̕̕4̷̛͕̮͓̈́́́̽̂͑5̶̮͔͔̯̲̫̻̻̮͓̳̼̗̙̩̣͚͑̓̀̀͒9̸̨̹̟̘̣͉̺͖̦̥̥̃͛͊̓͗͛͒͂̆͌̏̾͒͂͜͝͠͠0̷͉̹̦͛͌̽́̾͊͒̆̏̍̀̐̄͆ͅ4̵̲̖͇͋͑͜5̶̢̧̩̩̮̯͚͈͎̼̹͎͔͎̓̄͗̽̌̔̿̈̀̑̅̀͐́̿͝͝')
      return

    #calmaobot check#
    if message.content.startswith("%calmaobot check"):
      if len(message.mentions) == 1:
        if str(message.mentions[0].id) in json_object:
          await message.channel.send('Calmao puntos de ' + message.mentions[0].name + ': ' + str(json_object[str(message.mentions[0].id)]))
          return
        await message.channel.send('Calmao puntos de ' + message.mentions[0].name + ': 0 \n:(')
        return
      if len(message.mentions) > 1:
        await message.channel.send(':no_entry: **Solo puedes mencionar a una persona por mensaje.**')
        return
      if str(message.author.id) in json_object:
        await message.channel.send('Calmao puntos de ' + message.author.name + ': ' + str(json_object[str(message.author.id)]))
        return
      await message.channel.send('Calmao puntos de ' + message.author.name + ': 0 \n:(')
      return
    
    #calmaobot total#
    if message.content.startswith("%calmaobot total"):
      await message.channel.send('**TOTAL DE CALMAO PUNTOS DEL SERVER:  **' + str(json_object["ccounter"]))
      return

    #calmaobot top#
    if message.content.startswith("%calmaobot top"):
      sorted_object = sorted(json_object.items(), key=lambda x: x[1], reverse=True)
      await message.channel.send(':trophy: **TOP 5 PERSONAS MAS CALMADAS DEL SERVER** :trophy: \n\n:one: ' + str(json_names[sorted_object[1][0]]) + ': ' + str(sorted_object[1][1]) + '\n:two: '  + str(json_names[sorted_object[2][0]]) + ': ' + str(sorted_object[2][1]) + '\n:three: '  + str(json_names[sorted_object[3][0]]) + ': ' + str(sorted_object[3][1]) + '\n:four: '  + str(json_names[sorted_object[4][0]]) + ': ' + str(sorted_object[4][1]) + '\n:five: '  + str(json_names[sorted_object[5][0]]) + ': ' + str(sorted_object[5][1]))
      return

    #Activa mensaje de ayuda#
    if message.content.startswith('%calmaobot'):
      channel = message.channel
      await channel.send(embed=embed)
      return

    #Salta el mensaje si habla de calmaobot#
    if "calmaobot" in message.content.lower() or "calmao bot" in message.content.lower():
      return

    #Si encuentra un calmao#
    if "calmao" in message.content.lower():

      #Agrega 1 al contador total#
      json_object["ccounter"] = json_object["ccounter"]+1

      #Actualiza los nombres y counters individuales#
      if str(message.author.id) in json_object:
        json_object[str(message.author.id)] = json_object[str(message.author.id)]+1
      else:
        json_object[str(message.author.id)] = 1

      json_names[str(message.author.id)] = str(message.author.name)

      a_file = open("count.json", "w")
      json.dump(json_object, a_file)
      a_file.close()

      b_file = open("names.json", "w")
      json.dump(json_names, b_file)
      b_file.close()
        
#Pingea al bot#
keep_alive()

#Token para identificar al bot#
client.run(os.getenv('TOKEN'))