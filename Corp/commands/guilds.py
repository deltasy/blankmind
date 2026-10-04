import disnake
from disnake.ext import commands as com
from traceback import format_exc as error
from disnake import utils as Dutils
from datetime import datetime, timedelta
import re

from functions.page1 import namedisplay, newBlank, getSv
from mongo import udb

global simbol_opts, simbols, color_opts, reason_opts, reasons
simbol_opts = {"👥": 0, "📚": 1, "🧐": 2, "🔥": 3, "💣": 4, "🎩": 5}
simbols = ["👥", "📚", "🧐", "🔥", "💣", "🎩"]

reason_opts = {"Inactivity": 0, "Poor performance": 1, "Breaking rooms": 2, "Trolling": 3}
reasons = ["Inactivity", "Poor performance", "Breaking rooms", "Trolling"]

color_opts = {"Blue": 0x008bFF, "Green": 0x10FF00, "Red": 0xFF2626, "Yellow":  0xF4FF00, "White": 0xFFFFFF}

global upgrades, upcosts
upgrades = ['', '# ⏫ Upgrade to **Level 2**?\n> The guild <@&REPGUILD> will unlock the following improvements:\n- :speech_balloon: **Guild chat**\n- <:guild_member:1217871413617229914> **+1 Slot**\n\n:credit_card: **The upgrade will cost 50.0 <:blank:1124439750208655500> from the guild vault**']
upcosts = [0, 50, -1]

def command(client):
  @client.slash_command(name="guild")
  async def sguild(
    inter = disnake.ApplicationCommandInteraction,
  ):
    pass

  @sguild.sub_command(name="create")
  async def sbcreate(
    inter = disnake.ApplicationCommandInteraction,
    name = com.Param(max_length=35),
    color = com.Param(max_length=10),
    symbol: com.option_enum(simbol_opts) = 0
  ): 
    """
    Costs 100 𝔅 ➔ 👥 Create your own guild: A super joint study group!
    Parameters
    ----------
    name: The name of your guild
    color: Choose between: Blue, Green, Red, Yellow, White
    symbol: The emoji that represents your guild
    """
	  
    guild = inter.guild
    uid = inter.author.id
    suid = str(uid)

    symbol = simbols[symbol]

    try:
      color = color_opts[color.capitalize()]
    except:
      return await inter.response.send_message(f'"{color}" is not a valid color among the available ones **(Blue, Green, Red, Yellow, White)**', ephemeral=True)

    udata = udb.find_one({'uid': uid, 'blanks': {'$gte': 100}})

    if not udata: 
      return await inter.response.send_message('You don\'t have enough blanks. Get out, POOR', ephemeral=True)

    elif not bool(re.match(r'^[a-zA-ZÀ-ÖØ-öø-ÿ\s]+$', name)):
      return await inter.response.send_message(f'**Invalid guild name**\n> Include only letters; no numbers or special characters.', ephemeral=True)

    uguild = None
    try:
      uguild = udb.find_one({'ugid': udata['guild']})
    except: pass

    if uguild:
      return await inter.response.send_message(f'You are already in the guild "**{uguild["guild_name"]}**"', ephemeral=True)

    role = await guild.create_role(name=f'{symbol} ' + name + ' (Lv1)', color=disnake.Color(color))
    await inter.author.add_roles(role)
    
    udb.insert_one({
      'ugid': uid,
      'guild_name': name.capitalize(), 
      'guild_members': [
        uid
      ],
      'guild_owner': uid,
      'was_born': datetime.now() - timedelta(hours=3),
      'guild_role': role.id,
      'bank': {
        'blanks': 0,
        'contributors': {
          str(uid): 0
		}
	  },
      'level': 1
    })
    udb.update_one({'uid': uid}, {'$set': {'guild': uid}, '$inc': {'blanks': -100}})

    try: await namedisplay(uid)
    except: pass


    embed = disnake.Embed(
      description=f'# The guild __{name}__ was successfully founded.\n> You received the role <@&{role.id}>. Mention this role whenever you want to call guild members. **Your private room will always be open for them.**\n▬▬▬▬▬▬▬▬▬▬▬▬\n{newBlank([udata["blanks"] - 100, 100], "g")}',
      colour=disnake.Color(color)
    )

    return await inter.response.send_message(embed=embed)

  @sguild.sub_command(name="invite")
  async def sbinvite(
    inter = disnake.ApplicationCommandInteraction,
    user = com.Param(max_length=100)
  ): 
    """
    👑 For leaders (Costs 5 𝔅) ➔ ➕ Invite a user to your guild
    Parameters
    ----------
    user: EX: @user
    """

    try:
      udata = udb.find_one({'uid': inter.author.id})
      have_guild = udata['guild']
    except:
      return await inter.response.send_message('You don\'t even have a guild...', ephemeral=True)
    
    uguild = udb.find_one({'ugid': inter.author.id})
    mlimit = 10 + (uguild["level"] - 1)

    if udata['blanks'] < 5:
      return await inter.response.send_message('You don\'t have enough blanks. Get out, POOR', ephemeral=True)
	  
    elif not uguild: 
      return await inter.response.send_message('**Only the guild owner can create invites**', ephemeral=True)

    elif len(uguild['guild_members']) >= mlimit:
      return await inter.response.send_message(f'**Your guild is full. The current limit is {mlimit} members**\n- Upgrade the guild level with </guild upgrade:1233220536780324864> to increase the limit', ephemeral=True)
	  
    elif user.count('<@') > 1:
      return await inter.response.send_message('**You can only invite one user at a time**', ephemeral=True)

    cuid = int(user.replace(">", "").replace("<", "").replace("@", ""))

    if inter.author.id == cuid:
      return await inter.response.send_message('You can\'t invite yourself, genius.', ephemeral=True)

    guild = inter.guild

    valid_cuid = guild.get_member(cuid)
    
    if not valid_cuid:
      return await inter.response.send_message('**Invite a valid user!**', ephemeral=True)

    try:
      has_guild = udb.find_one({'uid': cuid})['guild']
      return await inter.response.send_message(f'This user is already part of a guild', ephemeral=True)
    except: pass

    embed = disnake.Embed(
      description=f"{inter.author.mention} invited you to join the guild **{uguild['guild_name']}**\n▬▬▬▬▬▬▬▬▬▬▬▬\n{newBlank([udata['blanks'] - 5, 5], 'g')}",
      colour=0x000080
    )

    udb.update_one({'uid': inter.author.id}, {'$inc': {'blanks': -5}})

    try: await namedisplay(inter.author)
    except: pass
    
    await inter.response.send_message(f'<@{cuid}>', embed=embed, components=[disnake.ui.Button(label='👥 Join guild', style=disnake.ButtonStyle.primary, custom_id=f"enterguild.{cuid}.by.{inter.author.id}")])

  @sguild.sub_command(name="kick")
  async def sbkick(
    inter = disnake.ApplicationCommandInteraction,
    user = com.Param(max_length=100),
    reason: com.option_enum(reason_opts) = None
  ): 
    """
    👑 For leaders ➔ ❌ Kick a user from your guild
    Parameters
    ----------
    user: EX: @user
    reason: Choose a justification
    """
    try:
      udata = udb.find_one({'uid': inter.author.id})
      have_guild = udata['guild']
    except:
      return await inter.response.send_message('You don\'t even have a guild...', ephemeral=True)
    
    uguild = udb.find_one({'ugid': inter.author.id})

    if not uguild: 
      return await inter.response.send_message('**Only the guild owner can kick members**', ephemeral=True)
	  
    elif user.count('<@') > 1:
      return await inter.response.send_message('**You can only invite one user at a time**', ephemeral=True)

    cuid = int(user.replace(">", "").replace("<", "").replace("@", ""))

    if inter.author.id == cuid:
      return await inter.response.send_message('You can\'t kick yourself, genius.', ephemeral=True)

    guild = inter.guild

    valid_cuid = guild.get_member(cuid)
    inyour_guild = uguild['guild_members']
    
    if not valid_cuid:
      return await inter.response.send_message('**Invite a valid user!**', ephemeral=True)
    elif cuid not in uguild['guild_members']:
      return await inter.response.send_message('**This user is not in your guild.**', ephemeral=True)

    embed = disnake.Embed(
      description=f"<a:heartbreak:1219782670062452736> You were kicked from the guild **{uguild['guild_name']}**",
      colour=0xed3325
    )

    try: embed.description += f'\n▬▬▬▬▬▬▬▬▬▬▬▬\n## Reason:\n> {reasons[reason]}'
    except: pass

    udb.update_one({'ugid': inter.author.id}, {'$pull': {'guild_members': cuid}, '$unset': {f'bank.contributors.{cuid}': 1}})
    udb.update_one({'uid': cuid}, {'$unset': {'guild': 1}})

    svguild = getSv('guild')
    guild_role = svguild.get_role(uguild["guild_role"])
    await valid_cuid.remove_roles(guild_role)

    await inter.response.send_message(f'<@{cuid}>', embed=embed)

  @sguild.sub_command(name="leave")
  async def sbleave(
    inter = disnake.ApplicationCommandInteraction,
    confirm = com.Param(max_length=3)
  ): 
    """
    Leave your guild
    Parameters
    ----------
    confirm: Type "yes" to confirm.
    """
    if 1126331167084388372 != inter.channel.id:  return await inter.response.send_message(f"**Use this command only in the channel <#{1126331167084388372}>**!", ephemeral=True)
	  
    if confirm.lower() != 'yes': return await inter.response.send_message('Invalid confirmation. You must type "**yes**" to proceed with the action', ephemeral=True)
	  
    try:
      udata = udb.find_one({'uid': inter.author.id})
      have_guild = udata['guild']
      uguild = udb.find_one({'ugid': udata['guild']})
    except:
      return await inter.response.send_message('You don\'t even have a guild...', ephemeral=True)

    svguild = getSv('guild')
    guild_role = svguild.get_role(uguild['guild_role'])
    await inter.author.remove_roles(guild_role)

    if uguild['ugid'] == inter.author.id: # O lider da guilda saiu.
      if len(uguild['guild_members']) == 1:
        await guild_role.delete()

        udb.delete_one({'ugid': udata['guild']})
        new_leader = f"\n> The last member left. The guild has been disbanded."

      else:
        set_owner = uguild['guild_members'][1]
        udb.update_one({'ugid': udata['guild']}, {'$set': {'ugid': set_owner, 'guild_owner': set_owner}, '$pull': {'guild_members': inter.author.id}, '$unset': {f'bank.contributors.{inter.author.id}': 1}})
        udb.update_many({'guild': inter.author.id}, {'$set': {'guild': set_owner}})
		  
        new_leader = f"\n> The guild ownership will go to the oldest member. The new guild leader is now <@{set_owner}>"		  

      icon_display = '# <:guild_owner:1217871403538321428>'

		
    else:
      udb.update_one({'ugid': udata['guild']}, {'$pull': {'guild_members': inter.author.id}, '$unset': {f'bank.contributors.{inter.author.id}': 1}})
      icon_display, new_leader = '<:guild_member:1217871413617229914>', ''

    embed = disnake.Embed(
      description=f"{icon_display} {inter.author.mention} left the guild **{uguild['guild_name']}**{new_leader}",
      colour=0xed3325
    )
	  
    udb.update_one({'uid': inter.author.id}, {'$unset': {'guild': 1}})

    await inter.response.send_message(embed=embed)




  @sguild.sub_command(name="stats")
  async def sbstats(
    inter = disnake.ApplicationCommandInteraction,
  ): 
    """
    👀 View your guild's statistics
    """
    try:
      udata = udb.find_one({'uid': inter.author.id})
      has_guild = udata['guild']
    except:
      return await inter.response.send_message('You don\'t even have a guild...', ephemeral=True)

    guild = udb.find_one({'ugid': has_guild})
	  
    svguild = getSv('guild')
	  
    grole = svguild.get_role(guild['guild_role'])
	  

    contributors = sorted(guild["bank"]["contributors"], key=lambda uid: guild["bank"]["contributors"][str(uid)])[::-1]
   
    contributors = '\n'.join([f'**`{i + 1}.`** {"<:guild_owner:1217871403538321428>" if int(uid) == guild["ugid"] else "<:guild_member:1217871413617229914>"} <@{uid}> **{round(guild["bank"]["contributors"][uid], 1)}** <:blank:1124439750208655500>' for i, uid in enumerate(contributors)])


    embed = disnake.Embed(
      description=f'# <@&{guild["guild_role"]}>\n> **Founded <t:{int((guild["was_born"] + timedelta(hours=3)).timestamp())}:R>**\n> **{len(guild["guild_members"])}/{10 + (guild["level"] - 1)} Members**\n\n## <:guildvault:1233430694231932959> **Vault:** {round(guild["bank"]["blanks"], 1)} <:blank:1124439750208655500>\n\n## Top contributors\n{contributors}',
      colour = grole.colour
    )

    return await inter.response.send_message(embed=embed)



  @sguild.sub_command(name="upgrade")
  async def sbview(
    inter = disnake.ApplicationCommandInteraction,
  ): 
    """
    👑 For leaders ➔ ⏫ Upgrade your guild's level
    """
    try:
      udata = udb.find_one({'uid': inter.author.id})
      have_guild = udata['guild']
    except:
      return await inter.response.send_message('You don\'t even have a guild...', ephemeral=True)
	  
    
    uguild = udb.find_one({'ugid': inter.author.id})

    if not uguild: 
      return await inter.response.send_message('**Only the owner of your guild can upgrade it**', ephemeral=True)
    elif uguild["level"] == 2:
      return await inter.response.send_message('**Your guild is at maximum level.**', ephemeral=True)


    embed = disnake.Embed(
      description=upgrades[uguild["level"]].replace("REPGUILD", str(uguild["guild_role"])),
      colour=0xFFFFFF
	)

    await inter.response.send_message(embed=embed,components=[disnake.ui.Button(label='Upgrade!', emoji='🆙', style=disnake.ButtonStyle.primary, custom_id=f"upgradeguild.{inter.author.id}.{upcosts[uguild['level']]}")])






