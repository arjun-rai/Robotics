import discord
from discord.ext import commands
intents = discord.Intents.all()
intents.message_content = True
# set up the bot and components
bot = commands.Bot(command_prefix='!', intents=intents)
# define a function to create a new channel for a question
async def create_question_channel(guild, question_author, question):
    category = discord.utils.get(guild.categories, name='Questions')
    archive_category = discord.utils.get(guild.categories, name='archive')
    answered = discord.utils.get(guild.channels, name='answered')
    channel_name = f'{question}'
    overwrites = {
        guild.get_role(1103828941300568134): discord.PermissionOverwrite(send_messages=False),
        question_author: discord.PermissionOverwrite(send_messages=True)
    }
    channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
    

    async def close_channel():
        await channel.edit(category=archive_category)

    # class LinkButton(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    #     @discord.ui.button(label="Link", style=discord.ButtonStyle.primary)
    #     async def button_callback(self, interaction,button):
    #         await interaction.response.send_message(channel.jump_url, ephemeral=True)
    class ClosingButton(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
        @discord.ui.button(label="Close", style=discord.ButtonStyle.primary)
        async def button_callback(self, interaction,button):
            await close_channel()
            await interaction.response.edit_message(content=f'Question from {question_author.mention}: {question}', view=None)
            await answered.send(f'{question} {channel.jump_url}')
            # await interaction.response.send_message("Closing Q&A, Moving to Archive!", ephemeral=True)

            

    closingButtonInstance = ClosingButton()
    message = await channel.send(f'Question from {question_author.mention}: {question}', view=closingButtonInstance)
    
    # wait for the button to be clicked and call the close_channel function
    # while True:
    #     try:
    #         button_ctx = await bot.wait_for('button_click', timeout=300, check=lambda b: b.message.id == message.id)
    #     except:
    #         break
    #     if button_ctx.component.id == 'close_button':
    #         await close_channel(button_ctx)
    #         break



# define the on_ready event
@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready.')

# define the on_message event
@bot.event
async def on_message(message):
    # ignore messages from the bot itself
    if message.author == bot.user:
        return

    # check if the message is a question
    if message.content.startswith('?'):
        question = message.content[1:]
        channel = await create_question_channel(message.guild, message.author, question)

    await bot.process_commands(message)

# run the bot
bot.run('MTEwMzg1MTY3MzUzMDY4MzQ2Mg.Gql-HK.FvLLqh64Nb3SvAaXiChOVNyOzWdsp0cQn1RLew')