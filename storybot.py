import discord
import openai
import os
from discord.ext import commands

# API keys and bot initialization
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("STORYBOT")
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='story', help="Uses OpenAI to write an open-ended story with the prompt given.\nUsage: !story <prompt>\nNote: text-davinci-002 is a text-completion engine, which means sometimes it will read a prompt as a sentence to finish.\nIf this happens unintentionally, use a period at the end of your prompt.")
async def write_story(ctx):
    message = ctx.message.content[7:] # strip !story from the message
    message = "Write a story where the prompt is: " + message # text-davinci-002 needs to be nudged a bit. this ensures the prompt is a story
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message,
            temperature=1,
            max_tokens=3900,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
    except openai.error.InvalidRequestError: # openAI has a token limit set by max_tokens, and lengthy prompts will exceed this limit
        await ctx.reply("Prompt is too long, try reducing it!")

    try:
        await ctx.reply(response["choices"][0]["text"]) # subscript the response body to get the text
    except discord.ext.commands.errors.CommandInvokeError as e: # in case of Discord error
        print(e)
        await ctx.reply("Discord's API failed somewhere, try again.")

@bot.command(name='2sh', help="Uses OpenAI to write a two-sentence horror story with the prompt given.\nUsage: !2sh <prompt>")
async def two_sentence_horror(ctx):
    message = ctx.message.content[5:] # strip !2sh from the message
    message = f"Topic: Breakfast\nTwo-Sentence Horror Story: He always stops crying when I pour the milk on his cereal. I just have to remember not to let him see his face on the carton.\n    \nTopic: {message}\nTwo-Sentence Horror Story:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message,
            temperature=0.8,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
    except openai.error.InvalidRequestError: # openAI has a token limit set by max_tokens, and lengthy prompts will exceed this limit
        await ctx.reply("Prompt is too long, try reducing it!")

    try:
        await ctx.reply(response["choices"][0]["text"]) # subscript the response body to get the text
    except discord.ext.commands.errors.CommandInvokeError as e: # in case of Discord error
        print(e)
        await ctx.reply("Discord's API failed somewhere, try again.")

bot.run(TOKEN)
