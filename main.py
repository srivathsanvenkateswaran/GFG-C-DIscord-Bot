import discord
import os

client = discord.Client()

def get_curr():
    with open('curr.txt', 'r') as c:
        curr = int(c.read())
    return curr

def update_curr(curr):
    with open('curr.txt', 'w') as c:
        c.write(str(curr))

def check_time():
    import time

    modification_time = os.path.getmtime('link.txt')
    mt = time.ctime(modification_time)
    time_obj = time.strptime(mt)
    modification_stamp = time.strftime("%d", time_obj)

    current_time = time.time()
    ct = time.ctime(current_time)
    time_obj = time.strptime(ct)
    current_stamp = time.strftime("%d", time_obj)

    return modification_stamp != current_stamp
    # return True

def read_data_from_file():
    with open('link.txt', 'r') as l:
        LINES = l.readlines()
    return LINES


def get_item(curr):
    LINES = read_data_from_file()
    TODAY = LINES[curr].split('$')
    update_curr(curr+1)
    message = f'Article number: {curr + 1}\n\nTopic: {TODAY[0]}\n\nLink: {TODAY[1]}\n\n@everyone'
    return message


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.help'):
        reply = '.help -> Help\n.link -> To get today\'s links\n.next -> To get the Article Number of next article.'
        await message.channel.send(reply)

    if message.content.startswith('.link'):
        if check_time():
            curr = get_curr()
            for i in range(0, 4):
                reply = get_item(curr+i)
                await message.channel.send(reply)
        else:
            await message.channel.send('Today\'s links has been already posted!!!')
    
    if message.content.startswith('.next'):
        await message.channel.send(f'Next article is Article Number {get_curr()+1}')


        

client.run('YOUR TOKEN HERE')
