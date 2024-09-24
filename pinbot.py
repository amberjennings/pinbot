#!/usr/bin/python3

import discord
import yaml

# Adjust this value to change how many reactions are needed to pin
THRESHHOLD = 2

# Change this emote to set what is used to pin messages
EMOTE = "📌"

intents = discord.Intents.default()

intents.messages = True
intents.reactions = True
intents.message_content = True

bot = discord.Bot(intents=intents)

with open("rb.yaml", "r") as yaml_file:
	cfg = yaml.safe_load(yaml_file)
	token = cfg["token"]
	channel_id = int(cfg["channel"])

@bot.event
async def on_ready():
	global channel
	channel = bot.get_channel(channel_id)
	print(channel)
	print(f"Logged in as {bot.user} and ready!")

@bot.command(description="ping")
async def ping(ctx):
	await ctx.respond(f"pong! took {round(bot.latency * 1000, 3)}ms")

@bot.event
async def on_reaction_add(reaction, user):
	if user.bot:
		return

	if reaction.emoji == EMOTE and reaction.count == THRESHHOLD:
		message = reaction.message

		print(f"---\nMessage ID: {message.id}")
		print(f"Author UID: {message.author.id}")
		print(f"Author username: {message.author}")
		print(f"Content: {message.content}")
		print(f"Attachments: {message.attachments}\n")

		embed = discord.Embed(
			title = f"Original Message: {message.jump_url}",
			description = message.content,
			color=discord.Color.green(),
		).set_author(name=f"{message.author.nick if message.author.nick \
			     is not None else message.author.display_name} - ({message.author.name})", \
			     icon_url=message.author.avatar.url)

		if message.attachments:
			embed = embed.set_image(url=message.attachments[0].url)

		await channel.send(embed=embed)

bot.run(token)
