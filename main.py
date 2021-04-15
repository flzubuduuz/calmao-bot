#1. ESENCIALES
#libraries y weas para que funcione el bot
import discord
import os
import json
from discord.ext import commands
from keep_alive import keep_alive
bot = commands.Bot(command_prefix=['%calmaobot ','%cb '])
bot.remove_command('help')


#2. CARGAR .JSONS
#count
count_file = open("count.json", "r")
count = json.load(count_file)
count_file.close()

#names
names_file = open("names.json", "r")
names = json.load(names_file)
names_file.close()


#3. DEFINICIONES
#numbers
numbers = {
  "0": ":zero:",
  "1": ":one:",
  "2": ":two:",
  "3": ":three:",
  "4": ":four:",
  "5": ":five:",
  "6": ":six:",
  "7": ":seven:",
  "8": ":eight:",
  "9": ":nine:"
}

#digits
def digits(x):
  return str(x).zfill(2)

#first
def first(x):
  sorted_count = sorted(count.items(), key=lambda z: z[1], reverse=True)
  t = ""
  
  if x < 10:
    for y in range(1,x+1):
      t += numbers[str(y)] + ' ' + names[sorted_count[y][0]] + ': ' + str(sorted_count[y][1]) + '\n'

  else:
    for y in range(1,x+1):
      t += numbers[digits(y)[0]] + numbers[digits(y)[1]] + ' ' + names[sorted_count[y][0]] + ': ' + str(sorted_count[y][1]) + '\n'

  return t

#embeds
help_embed=discord.Embed(title="Hola! Aquí hay una lista de comandos disponibles:", color=0xf40101)
help_embed.add_field(name="%calmaobot check @usuario", value="Muestra el puntaje del usuario (si no pones usuario, muestra tu propio puntaje).", inline=False)
help_embed.add_field(name="%calmaobot total", value="Muestra el total de calmaos en el server.", inline=False)
help_embed.add_field(name="%calmaobot top", value="Muestra las 5 personas más calmadas del server.", inline=False)
help_embed.add_field(name="%calmaobot all", value="Muestra todas las personas calmadas del server, hasta un máximo de 50.", inline=False)
help_embed.add_field(name="%calmaobot help", value="Muestra este mensaje de ayuda!", inline=False)
help_embed.add_field(name="\u200B", value="PD: puedes usar **%cb** en vez de **%calmaobot** si así lo prefieres.", inline=False)
help_embed.add_field(name="\u200B", value="\u200B", inline=False)
help_embed.add_field(name="¿Qué es este bot?", value='Gracias por preguntar! calmao bot cuenta la cantidad de veces que cada usuario ha dicho "calmao" en el server. Intenta no hacer spam de la palabra, para poder ver quién es, verdaderamente, el más calmao del server.', inline=False)
help_embed.add_field(name="\u200B", value="by flzubuduuz. [Repositorio.](https://github.com/flzubuduuz/calmao-bot)", inline=False)

error_embed=discord.Embed(title="El comando que has escrito no existe :(", description="Utiliza **%calmaobot help** para mostrar los comandos disponibles.\n_Recuerda también siempre escribir los comandos en minúsculas._", color=0xf40101)


#4. INICIO
#pone el status y conecta el bot
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='%calmaobot help'))
  print('{0.user} is up and running'.format(bot))


#5. ON MESSAGE
#para sumar puntos si hay calmaos
@bot.event
async def on_message(message):
  await bot.process_commands(message)
  
  #msgcount: cantidad de "calmaos" descontando menciones al bot
  
  msgcount = str(message.content).lower().count("calmao") - str(message.content).lower().count("calmaobot") - str(message.content).lower().count("calmao bot") - str(message.content).lower().count("calmao-bot")

  if msgcount > 0 and message.author.bot==False:
    
    #suma puntos al counter total
    if not "ccounter" in count: count["ccounter"]=0
    count["ccounter"] = count["ccounter"] + msgcount

    #suma puntos al usuario
    if str(message.author.id) in count:
      count[str(message.author.id)] = count[str(message.author.id)] + msgcount
    else:
      count[str(message.author.id)] = msgcount

    #agrega/cambia nombre de usuario
    if not names[str(message.author.id)] == str(message.author.name):
      names[str(message.author.id)] = str(message.author.name)

      #modifica los .json
      names_file = open("names.json", "w")
      json.dump(names, names_file)
      names_file.close()

    count_file = open("count.json", "w")
    json.dump(count, count_file)
    count_file.close()

    return


#6. COMANDOS
#check
@bot.command()
async def check(ctx, users: commands.Greedy[discord.User]):

  userlist = []
  for user in users:
    userlist.append(user.id)
    userlist.append(user.name)
  
  #si hay mas de una mención
  if len(userlist) > 2:
    await ctx.send(':no_entry: **Solo puedes mencionar a una persona por mensaje.**')
    return

  #si no hay menciones, agrega autor a la lista
  if not userlist:
    userlist.append(ctx.message.author.id)
    userlist.append(ctx.message.author.name)

  #easter egg
  if userlist[0] == bot.user.id:
    await ctx.send('Calmao puntos de calmao bot: 2̵̢̗̯̼̝̠̦̹͍̥̪̍̐̓̿̃̒͆̔̎̈͌͌͆͝7̵̘͉̲̬̗̭̓́̽̔̄́1̷̛̘̩̮̤̝̿́͑̄͝8̶̢̦̫̹͈̬́͋͂̔͗̊̉͆̒͑́͘͘͘͠͝2̷̢͈͙̬̜͈̼̤͋̋̃͊̆̌̈́̾̒̆͗̚͝8̶͖̰̣̾̽̃͋͊̿̎͐̕1̴̤̠͎̙̭̉͋͗͛̍͗̈́̕8̸̡̢̦̬̜̗̈́̇̈́̈́̇͊̽͆̋͝͠͠2̶̛͔̓̅̚8̷̧̡̡̧̺̣̤̗͕̬͎̎̊͐̊͑̎͗̌̉̆̍̕̕4̷̛͕̮͓̈́́́̽̂͑5̶̮͔͔̯̲̫̻̻̮͓̳̼̗̙̩̣͚͑̓̀̀͒9̸̨̹̟̘̣͉̺͖̦̥̥̃͛͊̓͗͛͒͂̆͌̏̾͒͂͜͝͠͠0̷͉̹̦͛͌̽́̾͊͒̆̏̍̀̐̄͆ͅ4̵̲̖͇͋͑͜5̶̢̧̩̩̮̯͚͈͎̼̹͎͔͎̓̄͗̽̌̔̿̈̀̑̅̀͐́̿͝͝')
    return

  #si la persona tiene puntos
  if str(userlist[0]) in count:
    await ctx.send('Calmao puntos de ' + userlist[1] + ': ' + str(count[str(userlist[0])]))
    return

  #si no tiene puntos
  await ctx.send('Calmao puntos de ' + userlist[1] + ': 0 \n:(')

#total
@bot.command()
async def total(ctx):
  await ctx.send('**TOTAL DE CALMAO PUNTOS DEL SERVER:  **' + str(count["ccounter"]))

#top
@bot.command()
async def top(ctx):
  if len(names) < 5:
    await ctx.send(':no_entry: Todavía no hay 5 personas calmadas como para hacer el top, pero puedes usar **%calmaobot all** para mostrar todas las personas calmadas que hay hasta ahora.')
    return
  await ctx.send(':trophy: **TOP 5 PERSONAS MAS CALMADAS DEL SERVER** :trophy: \n\n' + first(5))

#all
@bot.command()
async def all(ctx):
  if len(names) > 50:
    await ctx.send('_Hay ' + str(len(names)) + ' personas calmadas, por lo que solo se muestran las primeras 50._ \n\n:loudspeaker: **TODAS LAS PERSONAS CALMADAS DEL SERVER** :loudspeaker: \n\n' + first(50))
    return
  await ctx.send(':loudspeaker: **TODAS LAS PERSONAS CALMADAS DEL SERVER** :loudspeaker: \n\n' + first(len(names)))

#help
@bot.command()
async def help(ctx):
  await ctx.send(embed=help_embed)

#error
@bot.event
async def on_command_error(ctx, error):
  print(error)
  if isinstance(error, commands.CommandNotFound):
    await ctx.send(embed=error_embed)


#7. FIN
#pingea al bot
keep_alive()

#token
bot.run(os.getenv('TOKEN'))