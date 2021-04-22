#1. ESENCIALES
import os
import asyncio
from replit import db
from datetime import datetime
from dateutil import parser
from keep_alive import keep_alive

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix=['%calmaobot ','%cb '])
bot.remove_command('help')





#2. DEFINICIONES

#wordcount
def wordcount(message, count, words, subtract):

  wordcount = 0
  if subtract == True:
    for word in words:
      wordcount -= str(message.content).lower().count(word)
  else:
    for word in words:
      wordcount += str(message.content).lower().count(word)
  return wordcount

#msgcount
def msgcount(message, count, words, subtract = False):
  userid = str(message.author.id)
  serverid = str(message.guild.id)

  if message.author.bot == True:
    return

  if message.content.startswith('%calmaobot') or message.content.startswith('%cb'):
    return
  
  msgcount = wordcount(message, count, words, subtract)
  if msgcount > 0 or msgcount < 0:
      
    if userid in db[serverid]["counts"][count]:
      db[serverid]["counts"][count][userid] += msgcount
    else: db[serverid]["counts"][count][userid] = msgcount
        
    if not userid in db[serverid]["names"] or db[serverid]["names"][userid] != message.author.name:
      db[serverid]["names"][userid] = message.author.name

#parse
def parse(str):
  return parser.parse(str, dayfirst = True)

#countercheck
async def countercheck(ctx, name):
  if len(db[str(ctx.guild.id)]["counts"]) == 0:
    await ctx.send(embed = nocounts_embed)
    return False
  if not name in db[str(ctx.guild.id)]["counts"]:
    await ctx.send(embed = countdoesntexist_embed)
    return False

#check
async def check(ctx, count, user):
  userid = str(user.id)
  
  if userid in db[str(ctx.guild.id)]["counts"][count]:
    points =  str(db[str(ctx.guild.id)]["counts"][count][userid])
  else: points = "0\n:("

  await ctx.send(count + " puntos de " + user.name + ": " + points)

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
def first(ctx, count, n):
  sorted_count = sorted(db[str(ctx.guild.id)]["counts"][count].items(), key=lambda x: x[1], reverse=True)
  t = ""
  
  if n < 10:
    for x in range(0, n):
      t += numbers[str(x+1)] + ' ' + db[str(ctx.guild.id)]["names"][sorted_count[x][0]] + ': ' + str(sorted_count[x][1]) + '\n'

  else:
    for x in range(0, n):
      t += numbers[digits(x+1)[0]] + numbers[digits(x+1)[1]] + ' ' + db[str(ctx.guild.id)]["names"][sorted_count[x][0]] + ': ' + str(sorted_count[x][1]) + '\n'

  return t

#total
def total(ctx, count):
    total = 0
    for user in db[str(ctx.guild.id)]["counts"][count]:
        total += db[str(ctx.guild.id)]["counts"][count][user]
    return str(total)





#3. INICIO
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='%calmaobot help'))
  print('{0.user} is up and running'.format(bot))





#4. ON MESSAGE (SUMAR PUNTOS)
@bot.event
async def on_message(message):
  await bot.process_commands(message)

  if str(message.guild.id) in db:
    for count in db[str(message.guild.id)]["counts"]:
      msgcount(message, count, db[str(message.guild.id)]["words"][count])

@bot.event
async def on_message_delete(message):
  await bot.process_commands(message)

  if str(message.guild.id) in db:
    for count in db[str(message.guild.id)]["counts"]:
      msgcount(message, count, db[str(message.guild.id)]["words"][count], subtract = True)





#5. COMANDOS

#%cb create
@bot.command()
@has_permissions(manage_messages=True)
async def create(ctx, name: str, date: str, *terms):

  if str(ctx.guild.id) in db and name in db[str(ctx.guild.id)]["counts"]:
    await ctx.send(embed = usedname_embed)
    return

  if len(ctx.message.content) > 1000:
    await ctx.send(embed = toolong_embed)
    return

  if date != "none" and date != "all":
    try: date = parse(date)
    except:
      await ctx.send(embed = parsingerror_embed)
      return

  if date == "none":
    datestr = "momento en el que se agregue el contador"
  if date == "all":
    datestr = "inicio del servidor"
  if date != "none" and date != "all": datestr = date.strftime("%d/%m/%Y")
  
  sure_embed = discord.Embed(title="Estás a punto de agregar un nuevo contador!", description= "Se llamará **" + name + "** y contará las siguientes palabras o frases:\n- " + "\n- ".join(terms) + "\na partir del **" + datestr + "**.\n\nSi está todo bien, reacciona con un 👍 para agregar el contador.\n_Este comando expirará en 30 segundos._", color=0xff0000)

  suremsg = await ctx.send(embed = sure_embed)
  suremsg
  await suremsg.add_reaction('👍')

  def check(reaction, user):
    return user == ctx.message.author and str(reaction.emoji) == '👍'

  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
  except asyncio.TimeoutError:
    await ctx.send("⏱ **El comando ha expirado.**", reference = suremsg)
    return
  else: pass

  if date == "all":
    date = parse("13/05/2015")

  if not str(ctx.guild.id) in db:
    db[str(ctx.guild.id)] = {"words": {}, "names": {}, "counts":{}}

  db[str(ctx.guild.id)]["words"][name] = list(terms)
  db[str(ctx.guild.id)]["counts"][name] = {}

  done_embed = discord.Embed(title="Todo listo!", description="El contador **" + name + "** ha sido creado y está listo para usarse.", color=0xff0000)

  if date != "none":
    await ctx.send(embed = readinghistory_embed)
    for channel in ctx.guild.text_channels:
      print("STARTING " + channel.name)
      try: messages = await channel.history(limit = None, after = date).flatten()
      except: continue
      else:
        print("RETRIEVED " + channel.name)
        for message in messages:
          print(message.content)
          msgcount(message, name, list(terms))
        print("FINISHED " + channel.name)

  await ctx.send(embed = done_embed)

#%cb delete
@bot.command()
@has_permissions(manage_messages=True)
async def delete(ctx, name: str):

  if await countercheck(ctx, name) == False:
    return
  
  deletesure_embed = discord.Embed(title="Estás a punto de eliminar un contador!", description= "El contador **" + name + "** será eliminado **permanentemente**. \n\nSi estás seguro, reacciona con un 👍 para eliminar el contador.\n_Este comando expirará en 30 segundos._", color=0xff0000)

  suremsg = await ctx.send(embed = deletesure_embed)
  suremsg
  await suremsg.add_reaction('👍')

  def check(reaction, user):
    return user == ctx.message.author and str(reaction.emoji) == '👍'

  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
  except asyncio.TimeoutError:
    await ctx.send("⏱ **El comando ha expirado.**", reference = suremsg)
    return
  else: pass

  del db[str(ctx.guild.id)]["words"][name]
  del db[str(ctx.guild.id)]["counts"][name]

  if db[str(ctx.guild.id)]["counts"] == {}:
    del db[str(ctx.guild.id)]

  deletedone_embed = discord.Embed(title="Todo listo!", description="El contador **" + name + "** ha sido eliminado.", color=0xff0000)

  await ctx.send(embed = deletedone_embed)

#%cb check
@bot.command(name="check")
async def _check(ctx, count: str, users: commands.Greedy[discord.User]):

  if await countercheck(ctx, count) == False:
    return

  if len(list(users)) > 1:
    await ctx.send(embed = toomanyusers_embed)
    return
    
  if len(list(users)) == 0:
    await check(ctx, count, ctx.message.author)
    return

  if users[0] == bot.user:
    await ctx.send(count + ' puntos de calmao bot: 2̵̢̗̯̼̝̠̦̹͍̥̪̍̐̓̿̃̒͆̔̎̈͌͌͆͝7̵̘͉̲̬̗̭̓́̽̔̄́1̷̛̘̩̮̤̝̿́͑̄͝8̶̢̦̫̹͈̬́͋͂̔͗̊̉͆̒͑́͘͘͘͠͝2̷̢͈͙̬̜͈̼̤͋̋̃͊̆̌̈́̾̒̆͗̚͝8̶͖̰̣̾̽̃͋͊̿̎͐̕1̴̤̠͎̙̭̉͋͗͛̍͗̈́̕8̸̡̢̦̬̜̗̈́̇̈́̈́̇͊̽͆̋͝͠͠2̶̛͔̓̅̚8̷̧̡̡̧̺̣̤̗͕̬͎̎̊͐̊͑̎͗̌̉̆̍̕̕4̷̛͕̮͓̈́́́̽̂͑5̶̮͔͔̯̲̫̻̻̮͓̳̼̗̙̩̣͚͑̓̀̀͒9̸̨̹̟̘̣͉̺͖̦̥̥̃͛͊̓͗͛͒͂̆͌̏̾͒͂͜͝͠͠0̷͉̹̦͛͌̽́̾͊͒̆̏̍̀̐̄͆ͅ4̵̲̖͇͋͑͜5̶̢̧̩̩̮̯͚͈͎̼̹͎͔͎̓̄͗̽̌̔̿̈̀̑̅̀͐́̿͝͝')
    return

  await check(ctx, count, users[0])

#%cb top
@bot.command(name = "top")
async def _top(ctx, count: str):

  if await countercheck(ctx, count) == False:
    return

  n = min(len(db[str(ctx.guild.id)]["counts"][count]), 5)
  if n < 5: footnote = "_Hay menos de 5 usuarios con puntaje, por lo que la lista muestra a todos los usuarios._\n\n"
  else: footnote = ""

  await ctx.send(footnote + "🏆 **TOP " + str(n) + " CON MÁS " + count.upper() + " PUNTOS DEL SERVER** 🏆\n\n" + first(ctx, count, n))

#%cb all
@bot.command(name = "all")
async def _all(ctx, count: str):

  if await countercheck(ctx, count) == False:
    return

  n = min(len(db[str(ctx.guild.id)]["counts"][count]), 50)
  if n > 50: footnote = "_Hay más de 50 usuarios con puntaje, por lo que la lista solo muestra a los primeros 50._\n\n"
  else: footnote = ""

  all_embed = discord.Embed(title="📣 TODOS LOS USUARIOS CON " + count.upper() + " PUNTOS DEL SERVER 📣", description=footnote + first(ctx, count, n), color=0xff0000)

  await ctx.send(embed = all_embed)

#%cb total
@bot.command(name = "total")
async def _total(ctx, count: str):

  if await countercheck(ctx, count) == False:
    return
    
  await ctx.send("**TOTAL DE " + count.upper() + " PUNTOS DE " + ctx.guild.name.upper() + ": **" + total(ctx, count))

#%cb counters
@bot.command()
async def counters(ctx):
  if not str(ctx.guild.id) in db:
    await ctx.send(embed = nocounts_embed)
    return
  else:
    if len(db[str(ctx.guild.id)]["counts"]) == 0:
      await ctx.send(embed = nocounts_embed)
      return

  counters_embed = discord.Embed(title="Lista de contadores actualmente activos:", description="- " + "\n- ".join(db[str(ctx.guild.id)]["counts"]), color=0xff0000)

  await ctx.send(embed = counters_embed)

#%cb help
@bot.command()
async def help(ctx):
  await ctx.send(embed = help_embed)

#%cb admin
@bot.command()
@has_permissions(manage_messages=True)
async def admin(ctx):
  await ctx.send(embed = admin_embed)





#6. ERRORES / SERVER LEAVE
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, MissingPermissions):
    await ctx.send(embed= nopermissions_embed)
    return
  if isinstance(error, commands.CommandNotFound):
    await ctx.send(embed= nocommand_embed)
    return
  if isinstance(error, commands.CommandError):
    await ctx.send(embed = badarguments_embed)
    return
  else:
    print(error)
    await ctx.send(embed =unknownerror_embed)

@bot.event
async def on_guild_remove(guild):
  del db[str(guild.id)]





#7. EMBEDS

nocounts_embed = discord.Embed(title="El server no tiene ningún contador!", description="Si tienes el permiso de **Administrar mensajes**, puedes utilizar **%calmaobot admin** para ver cómo crear un contador nuevo.", color=0xff0000)

countdoesntexist_embed = discord.Embed(title="No existen contadores con ese nombre:(", description="Puedes utilizar **%calmaobot counters** para ver los contadores que tiene actualmente el server.", color=0xff0000)

usedname_embed = discord.Embed(title="Ya existe un contador con este nombre!", description="Puedes usar **%calmaobot counters** para revisar los contadores actualmente activos.", color=0xff0000)

toolong_embed = discord.Embed(title="El nombre del contador es muy largo!", description="¿En serio necesitas más de mil caracteres?", color=0xff0000)

parsingerror_embed = discord.Embed(title="Hubo un error procesando la fecha escrita.", description="Revisa si el formato es el adecuado **(dd/mm/yyyy)**.", color=0xff0000)

readinghistory_embed = discord.Embed(title="Leyendo la historia de mensajes...", description="El contador está siendo actualizado. Esto podría tomar varios minutos (dependiendo de la cantidad de mensajes que tenga que leer), por lo que se recomienda dejar al bot tranquilo hasta que indique que haya terminado. Puede que algunos mensajes enviados en este período no sean contados adecuadamente.", color=0xff0000)

toomanyusers_embed = discord.Embed(title="🚫 No puedes etiquetar a más de un usuario!", color=0xff0000)

nocommand_embed = discord.Embed(title="El comando que has escrito no existe:(", description="Usa **%calmaobot help** para ver la lista de comandos disponibles.", color=0xff0000)

nopermissions_embed = discord.Embed(title="No tienes permisos para ejecutar ese comando.", description="Necesitas el permiso de **Administrar mensajes** para acceder al comando.", color=0xff0000)

badarguments_embed = discord.Embed(title="Los argumentos del comando están equivocados.", description="Revisa bien que hayas escrito todo como corresponde. Recuerda utilizar **%calmaobot help** si necesitas ayuda.", color=0xff0000)

unknownerror_embed = discord.Embed(title="Ha ocurrido un error desconocido:(", description="🤖🔧 No está claro qué ha pasado, pero estamos trabajando para usted.", color=0xff0000)

help_embed = discord.Embed(title="Hola! Aquí hay una lista de comandos disponibles:", description="_Nota: si tienes el permiso de **Administrar mensajes** y quieres ver cómo crear o borrar contadores, escribe_ **%calmaobot admin**.",  color=0xf40101)
help_embed.add_field(name="%calmaobot counters", value="Muestra los nombres de todos los contadores actualmente activos en el server.", inline=False)
help_embed.add_field(name="%calmaobot check _contador_ @usuario", value="Muestra el puntaje del usuario (si no pones usuario, muestra tu propio puntaje).", inline=False)
help_embed.add_field(name="%calmaobot total _contador_", value="Muestra la suma de todos los puntajes en el server.", inline=False)
help_embed.add_field(name="%calmaobot top _contador_", value="Muestra las 5 personas con mayor puntaje del server.", inline=False)
help_embed.add_field(name="%calmaobot all", value="Muestra todas las personas con puntaje del server, hasta un máximo de 50.", inline=False)
help_embed.add_field(name="%calmaobot help", value="Muestra este mensaje de ayuda!", inline=False)
help_embed.add_field(name="\u200B", value="PD: puedes usar **%cb** en vez de **%calmaobot** si así lo prefieres.", inline=False)
help_embed.add_field(name="\u200B", value="by flzubuduuz. [Repositorio.](https://github.com/flzubuduuz/calmao-bot)", inline=False)

admin_embed = discord.Embed(title="Hola! Aquí hay una lista de comandos para administrar los contadores:", color=0xf40101)
admin_embed.add_field(name='%calmaobot create _nombre_ _fecha_ "frase1" "frase2" ...', value="Crea un contador con las siguientes características:\n_-  Nombre:_ es fuertemente recomendado que sea **una** sola palabra y que esté en **minúsculas**, para que sea más fácil referirse al contador en los comandos.\n_-  Fecha:_ la fecha a partir de la cual el contador empezará a leer mensajes. Debe ser escrita en formato **_dd/mm/yyyy_**. Escribe **_all_** si quieres que cuente todos los mensajes de la historia del server, y **_none_** si quieres que comience a contar en el momento de la creación del bot.\n_-  Frases:_ las palabras o frases que va a contar el bot, no son case-sensitive. Deben ir entre comillas y separadas por espacios.", inline=False)
admin_embed.add_field(name="%calmaobot delete _contador_", value="Elimina permanentemente el contador con el nombre ingresado.", inline=False)
admin_embed.add_field(name="%calmaobot admin", value="Muestra este mensaje de ayuda!", inline=False)
admin_embed.add_field(name="\u200B", value="PD: puedes usar **%cb** en vez de **%calmaobot** si así lo prefieres.", inline=False)





#8. FIN
#pingea al bot
keep_alive()

#token
bot.run(os.environ['TOKEN'])