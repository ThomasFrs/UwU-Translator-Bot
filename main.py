# i've made everything here so please don't accuse me of stealing code
# though it's pretty shitty so idk why you would do that lol

import discord
from datetime import datetime
import text_translator as tt
import media_retriever as mr
import os
import json
from pathlib import Path


bot_prefix = "^^"
client = discord.Client(
    activity=discord.Game(
        name=(
            "%scommands" %
            bot_prefix)))
start_time = datetime.now()


def get_tokens():
    current_working_file = str(Path(__file__).parent.resolve())
    if os.path.exists(current_working_file + "/config.json"):
        with open(current_working_file + "/config.json") as file:
            config_data = json.load(file)
    else:
        config_template = {"discord_token": "", "api_key": ""}
        with open(current_working_file + "/config.json", "w+") as file:
            json.dump(config_template, file)

    return config_data["discord_token"], config_data["api_key"]


@client.event
async def on_ready():
    print(
        tt.text_translation("I have logged in as"),
        "{0.user}".format(client))


@client.event
async def on_message(message):
    if message.author != client.user:
        # prints out every message
        print(
            "%s (%s, %s, %s, %s)" %
            (datetime.now().strftime("%H:%M:%S"),
             message.guild.name,
             message.channel.name,
             message.author.name,
             message.content))

        # useful commands
        # detects if there any uwu or owo in the message
        if any(elt in message.content for elt in tt.list_permutations("uwu")) or any(
                elt in message.content for elt in tt.list_permutations("owo")):
            translation = tt.text_translation(message.content)
            print("\tIdentified uwu/owo in content")
            print("\tSent translation: %s" % (translation))
            await message.channel.send(translation)

        # says and translates a given message
        elif message.content.startswith(bot_prefix + "say"):
            translation = tt.text_translation(
                message.content[len(bot_prefix) + 4:])
            print("\tIdentified %ssay command" % bot_prefix)
            print("\tDeleted message from %s" % message.author.name)
            await message.delete()
            print("\tSent translation: %s" % (translation))
            await message.channel.send(translation)

        elif message.content.startswith(bot_prefix + "gif"):
            gif_url = mr.retrieve_gif("owo", 20, api_key)
            print("\tIdentified %sgif command" % bot_prefix)
            print("\tSent gif: %s" % (gif_url))
            await message.channel.send(gif_url)

        elif message.content.startswith(bot_prefix + "cpasta"):
            copypasta_translation = tt.text_translation(
                mr.retrieve_copypasta("copypastas.txt"))
            print("\tIdentified %scpasta command" % bot_prefix)
            print("\tSent copypasta: %s" % (copypasta_translation))
            await message.channel.send(copypasta_translation)

        # hidden commands
        elif message.content.startswith(bot_prefix + "stats"):
            uptime = datetime.now() - start_time
            print("\tIdentified %sstats command" % bot_prefix)
            print("\tDeleted message from %s" % message.author.name)
            await message.delete()
            print("Uptime: %s\nServers: %s" %
                  (uptime, str(len(client.guilds))))
            await message.channel.send("Uptime: %s\nServers: %s" % (uptime, str(len(client.guilds))))

        elif message.content.startswith(bot_prefix + "read"):
            print("\tIdentified %sread command" % bot_prefix)
            print("\tDeleted message from %s" % message.author.name)
            await message.delete()
            try:
                reading = mr.retrieve_text(
                    message.content[len(bot_prefix) + 5:])
                print("\tSent %s" % message.content[len(bot_prefix) + 5:])
                await message.channel.send(tt.text_translation(reading))
            except BaseException:
                print("\tCould not send %s" %
                      message.content[len(bot_prefix) + 5:])

        # useless commands
        elif message.content.startswith(bot_prefix + "whoru"):
            print("\tIdentified %swhoru command" % bot_prefix)
            await message.channel.send(tt.text_translation("Hello! My name is ") + "{0.user}".format(client))
            await message.channel.send(tt.text_translation("My pronouns are (NVIDIA GeForce RTX 2060 Intel Core i5-10400F CPU 16.0GB RAM/ them)."))
            await message.channel.send(tt.text_translation("My main purpose is to translate your text into its something very UwU."))
            await message.channel.send(tt.text_translation("I have been created by Anne Frs in only one day! Which probably explains why my organism\nis a complete mess and I can't do much :("))

        elif message.content.startswith(bot_prefix + "commands"):
            print("\tIdentified %scommands command" % bot_prefix)
            await message.channel.send("*Prefix:* ``%s``\n*Commands:*\n``%swhoru``: I talk extensively about myself because I don't have a gf\n``%scommands``: I display this message once again, because why not\n``your_message containing uwu/owo``: I reply to your message and translate it into its UwU and OwO form\n``%ssay + your_message``: I delete your message and translate it into its UwU and OwO form\n``%sgif``: I post a random gif that is very much OwO\n``%scpasta``: I post a random copypasta that is very much OwO" % (bot_prefix, bot_prefix, bot_prefix, bot_prefix, bot_prefix, bot_prefix))  # bot_prefix


discord_token, api_key = get_tokens()
client.run(discord_token)
