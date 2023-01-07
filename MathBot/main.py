import discord
import mysql.connector
import random

mydb = mysql.connector.connect(host="localhost", user="root", passwd="database_password", database="database_name")
mycursor = mydb.cursor()
command = "Select problem from database_name where problemid={}"
randomcmd = "Select problem from database_name where id={}"
randomcmd2 = "Select problemid from database_name where id={}"
answercmd = "Select answer from database_name where problemid={}"
file_template = "[path]{}.png"
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
    await help(message)

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
                
async def help(message):
    messagecontent = message.content
    if messagecontent.startswith("!help"):
        await message.channel.send("Use this bot to fetch past American Invitational Mathematics Exam problems from 2022 to practice for the exam!")
        await message.channel.send("To select a specific problem, you must type in its problem id.")
        await message.channel.send("The id is formed by getting the year of release(i.e 2022), the version(AIME I/II), and the problem number(i.e #13).")
        await message.channel.send("If one wants to find the the problem labeled 2022 AIME II Problem 7, then the id will simply be 202227. 2022 is the year of release, 2 is the version, and 7 is the problem number.")
        await message.channel.send("If one wants a random problem, simply type in **!random** and the bot will spew a randomly picked problem.")
        await message.channel.send("If one wants to check/find the answer to their problem, simply type in **!answer [problem id] [answer]**(with spaces) and the bot will reply by responding whether it is incorrect or correct.")
        await message.channel.send("More functions will be coming to this bot, like the addition of more problems and the '!test' command, which will give the user a 15-problem randomly generated test.")






client.run('token')
