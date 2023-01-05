import discord
import mysql.connector
import random

mydb = mysql.connector.connect(host="localhost", user="root", passwd="2I8AUUD5", database="AIME")
mycursor = mydb.cursor()
command = "Select problem from AIME_Problems where problemid={}"
randomcmd = "Select problem from AIME_Problems where id={}"
randomcmd2 = "Select problemid from AIME_Problems where id={}"
answercmd = "Select answer from AIME_Problems where problemid={}"
file_template = "/Users/kedarvernekar/MathBot/Problem Pictures/{}.png"
prefix = '!'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await problem(message)
    await answer(message)

async def problem(message):
    messagecontent = message.content
    if messagecontent == "!random":
        num = random.randint(1, 30)
        mycursor.execute(randomcmd2.format(num))
        myresult = mycursor.fetchall()
        for row in myresult:
            mycursor.execute(command.format(*row))
            myresult1 = mycursor.fetchall()
            for row1 in myresult1:
                await message.channel.send(*row1)
                await message.channel.send(file=discord.File(file_template.format(*row)))



    else:
        try:
            mycursor.execute(command.format(messagecontent))
            myresult = mycursor.fetchall()
            for row in myresult:
                await message.channel.send(*row)
                await message.channel.send(file=discord.File(file_template.format(messagecontent)))
        except:
            pass

async def answer(message):
    messagecontent = message.content
    if messagecontent.startswith("!answer"):
        answer_form = messagecontent[8:].split()
        mycursor.execute(answercmd.format(int(answer_form[0])))
        myresult = mycursor.fetchall()
        for row in myresult:
            if int(answer_form[1]) == int(*row):
                await message.channel.send("Correct!")
            else:
                await message.channel.send("Incorrect!")





client.run('MTAyNTgxOTY2MzQ3ODgxNjc3OA.GA_asR.iWKY_T3K9G00ptBIo5Cidh6B8hXrYQUUmskxAs')
