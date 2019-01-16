import discord
from discord.ext import commands
import config

client = commands.Bot(command_prefix = '^')

# general information message, ids of nations servers, general information channel in ff, nation names to search, business channel in nations, economy channel in ff, state-owned business channel, flag filepath, government channel in ff
bornholm = [''' 
Name: Danish Coalition
Population: {}
Name of the Navy: Danish Navy
Navy prefix: KDM
Types of ships used in the Navy: Type 45  Destroyer class, Skjold-class Corvette
Natural resources: Lumber, Iron, Fish
Server: discord.gg/5NxJEMv
Flag:
''', '491724729120587807', '517377372023160853', ['bornholm', 'danish coalition', 'denmark', 'ronne', 'nexo', 'gudhjem'],'491729812017119242', '517377269774286848', '516303631054536724', r'C:\DiscordBot\flags\bornholm.png', '517365042572951592']
# general information message, ids of nations servers, general information channel in ff, economy message, business channel in nations, economy channel in ff, flag filepath, government channel in ff
wolin = ['''
Name: Nordic Council
Population: {}
Name of the Navy: Union Naval Forces
Navy prefix: NV, NTV, NNV, NES, NNAV, WNS
Types of ships used in the Navy: Type 45 Daring-class Destroyer, Visby-Class Corvette, Trafalgar-Class Submarine, Lublin-Class Landing Ship
Natural resources: Wood, Gravel, Sand, Fish
Server: discord.gg/5rreNdC
Flag:
''', '491710737698521090', '517378401569472522', ['wolin','nordic council'], '491712695561748500', '517378474420207626', '', r'C:\DiscordBot\flags\wolin.png', '517378435283288065']

eire = ['''
Name: An tAontas Farraige na hÉire
Population: {}
Name of the Navy: An Tseirbhís Chabhlaigh
Navy prefix: LÉ
Types of ships used in the Navy: Centaur-Class Aircraft Carrier, Eithne-Class OPV, Trafalgar-Class Submarine
Natural resources: Fish
Server: discord.gg/YpefrTz
Flag:
''', '491717783281991682', '517387950799978497', ['eire', 'an taontas farraige na héire', 'ireland', 'haulbowline'], '491722236391063577', '517388033071513601', '', r'C:\DiscordBot\flags\eire.jpg', '517388011307139094']

testing = ['''
Name: Testing Nation
Population: {}
Name of the Navy: Testing Navy
Navy prefix: TN
Types of ships used in the Navy: Ship
Natural resources: Test
Server: Test
Flag:
''', '501645038204223489', '531730954385883137', ['bornholm', 'danish coalition', 'denmark', 'ronne', 'nexo', 'gudhjem'],'531091793006297088', '531730969204621325', '', r'C:\DiscordBot\flags\test.png', '532837222920093697']

nations = [bornholm]

@client.event
async def on_ready():
    print('Bot is ready.')



async def isMessage(channelID): #checks whether there are any messages in the channel, if not returns false, if yes returns the id of the message
    channel = client.get_channel(channelID)
    messages = 0
    messageID = ''
    async for x in client.logs_from(channel):
        messages = messages + 1
        messageID = x.id
    if messages == 0:
        return False
    else:
        return messageID

# what to post, where to post, is flag present, flag file path
async def postMessage(message, channelID, flag=False, flagPath=''):
    if await isMessage(channelID) == False:
        if flag==True:
            await client.send_file(client.get_channel(channelID), flagPath, content=message)
        else:
            await client.send_message(client.get_channel(channelID), message)
        #await client.send_file(client.get_channel(channelID), flag, content=generalInformation)
    else:
        editChannel = client.get_channel(channelID) # gets the channel using Channel ID
        editMessage = await client.get_message(editChannel, await isMessage(channelID)) # gets a specific message using channel and message id
        await client.edit_message(editMessage, message) #edits the specific message from editMessage to the second argument

#@client.command()  #which server to count in and in what channel to post, channelID, flagPath
async def generalInformation(generalMessage, serverID): #counts people with Citizen role and/or edits a specific message to the number of Citizens in a general information form
    citizens = 0
    server = client.get_server(serverID)
    for member in server.members:
        for role in member.roles:
            if role.name == 'Citizen':
                citizens = citizens + 1
        generalInformation = generalMessage.format(citizens)
    return generalInformation
    '''    
    if await isMessage(channelID) == False:
        #await client.send_message(client.get_channel(channelID), generalInformation)
        await client.send_file(client.get_channel(channelID), flagPath, content=generalInformation)
        #await client.send_file(client.get_channel(channelID), flag, content=generalInformation)
    else:
        editChannel = client.get_channel(channelID) # gets the channel using Channel ID
        editMessage = await client.get_message(editChannel, await isMessage(channelID)) # gets a specific message using channel and message id
        await client.edit_message(editMessage, generalInformation) #edits the specific message from editMessage to the second argument
    '''

async def countUnemployment(serverID): # counts a the number of people with only Citizen role in the server
    citizens = 0
    unemployed = 0
    server = client.get_server(serverID)
    for member in server.members:
        rolesNumber = 0
        permit = False
        ensign = False
        for role in member.roles:
            rolesNumber = rolesNumber + 1
            if role.name == 'Citizen':
                citizens = citizens + 1
            if 'Permit' in role.name:
                permit = True
            if 'Ensign' in role.name:
                ensign = True
        if (role.name == 'Citizen' and rolesNumber == 2) or ((role.name == 'Citizen' and permit == True) and rolesNumber == 3) or ((role.name == 'Citizen' and ensign == True) and rolesNumber == 3):
                unemployed = unemployed + 1
    unemployment = int(round((unemployed/citizens)*100))
    return str(unemployment)

#@client.command() # which server to count unemployment from, country reference, from where to look for Businesses, where to post, additional business channel e.g. state-owned
async def updateBusinesses(serverID, location, businessChannelID, additionalBusinessChannelID):
    channel = client.get_channel(businessChannelID) # gets the channel using ID
    businesses = [] # an array for to store the discord links of businesses
    async for x in client.logs_from(channel): # for loop through all messages in a channel, only discord links added to businesses
        located = False
        for y in x.content.split():
            y = y.lower()
            for l in location:
                if l in y:
                    for y in x.content.split():
                        if 'https://discord.gg/' in y:
                            businesses.append(y)
                            located = True
                            break
            if located:
                break
    unemployment = await countUnemployment(serverID)
    economy = '''
Unemployment rate (not accurate): {}%
List of businesses stationed in this nation:
'''.format(unemployment)
    for b in businesses: # iteration through businesses array to change economy into a nicer form with new lines
        economy = economy + b + "\n"
    if additionalBusinessChannelID != '':
        channel = client.get_channel(additionalBusinessChannelID)
        async for x in client.logs_from(channel): # for loop through all messages in a channel, only discord links added to businesses
            located = False
            for y in x.content.split():
                y = y.lower()
                for l in location:
                    if l in y:
                        for y in x.content.split():
                            if 'https://discord.gg/' in y:
                                businesses.append(y)
                                located = True
                                break
                if located:
                    break
        for b in businesses: # iteration through businesses array to change economy into a nicer form with new lines
            economy = economy + b + "\n"
    return economy
    '''        
    if await isMessage(channelID):
        editChannel = client.get_channel(channelID) # gets the channel using Channel ID
        editMessage = await client.get_message(editChannel, await isMessage(channelID))
        await client.edit_message(editMessage, economy) #edits the specific message from editMessage to the second argument
    else:
        await client.send_message(client.get_channel(channelID), economy) # sends economy string in a nice form to the specific channel
'''


# which server to check, which server to post in FF
async def lookupGovernment(serverID):
    governmentRoles = ['secretary', 'department', 'minister', 'president', 'taoiseach', 'teachtaí']
    unsortedPositions = []
    unsortedMembers = []
    governmentPositions = []
    governmentMembers = []
    #eire = False
    server = client.get_server(serverID)
    for member in server.members: # checks each member
        for role in member.roles: # checks each role of a member
            for r in role.name.split(): # checks each word in the role name of a member
                for government in governmentRoles: # compares each word to the 
                    r = r.lower()
                    #if 'teachtaí dála' in r:
                     #   eire = True
                      #  unsortedMembers.append(member.name)
                    #else: #'teachtaí dála'
                    if government in r:
                        unsortedPositions.append(role.name)
                        unsortedMembers.append(member.display_name)
    vicePresident = False
    for p in unsortedPositions:
        u = p.lower()
        if ('president' in u and 'vice' not in u) or ('taoiseach' in u):
            governmentPositions.insert(0, unsortedPositions[unsortedPositions.index(p)])
            governmentMembers.insert(0, unsortedMembers[unsortedPositions.index(p)])
            #governmentMembers.insert(position, governmentMembers[governmentPositions.index(p)])
        elif ('vice' in u and 'secretary' not in u):
            governmentPositions.insert(0, unsortedPositions[unsortedPositions.index(p)])
            governmentMembers.insert(0, unsortedMembers[unsortedPositions.index(p)] + '\n')
            vicePresident = True
        elif ('secretary' in u) or ('minister' in u) or ('department' in u) or ('teachtaí dála' in u):
            governmentPositions.append(unsortedPositions[unsortedPositions.index(p)])
            governmentMembers.append(unsortedMembers[unsortedPositions.index(p)])
    if vicePresident == False:
        governmentMembers[0] = governmentMembers[0] + '\n'
    governmentMessage = ''
    for g in governmentMembers:
        governmentMessage = governmentMessage + governmentPositions[governmentMembers.index(g)] + ': ' + g + '\n'
    return governmentMessage
    '''
    if await isMessage(channelID):
        editChannel = client.get_channel(channelID) # gets the channel using Channel ID
        editMessage = await client.get_message(editChannel, await isMessage(channelID))
        await client.edit_message(editMessage, governmentMessage) #edits the specific message from editMessage to the second argument
    else:
        await client.send_message(client.get_channel(channelID), governmentMessage)
    '''




@client.command(pass_context=True)
async def ud(ctx): # uses all data collecting functions to update the data
    if ctx.message.author.id == '226682765465223178':    
        for nation in nations:
            await postMessage(await generalInformation(nation[0], nation[1]), nation[2], True, nation[7])
            await postMessage(await updateBusinesses(nation[1], nation[3], nation[4], nation[6]), nation[5])
            await postMessage(await lookupGovernment(nation[1]), nation[8])
    else:
        await client.send_message(ctx.message.channel, 'You do not have permission to run this command')

'''
@client.command(pass_context=True)
async def pd(ctx, request, country):
    if request.lower() == 'general':
        if country.lower() == 'bornholm':
            selected = bornholm
        if country.lower() == 'wolin':
            selected = wolin
        if country.lower() == 'eire':
            selected = eire
        await client.send_message(ctx.message.author, await generalInformation(selected[0], selected[1]))
    elif request.lower() == 'government':
        if country.lower() == 'bornholm':
            selected = bornholm
        if country.lower() == 'wolin':
            selected = wolin
        if country.lower() == 'eire':
            selected = eire
        await client.send_message(ctx.message.author, await lookupGovernment(selected[1]))
    elif request.lower() == 'economy':
        if country.lower() == 'bornholm':
            selected = bornholm
        if country.lower() == 'wolin':
            selected = wolin
        if country.lower() == 'eire':
            selected = eire
        await client.send_message(ctx.message.author, await updateBusinesses(selected[1], selected[3], selected[4], selected[6]))
    elif request=='' or country=''
        await client.send_message(ctx.message.author,
        '''
'''
It appears that you have used the command incorrectly, please use the following format:

^pd (what information you want to use) (information about which country)

**Types of information**:
-general
-economy
-government

**Countries**:
-wolin
-bornholm
-eire

'''


client.run(config.TOKEN)