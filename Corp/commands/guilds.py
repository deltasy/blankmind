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

reason_opts = {"Inatividade": 0, "Mal desempenho": 1, "Quebrando salas": 2, "Trollando": 3}
reasons = ["Inatividade", "Mal desempenho", "Quebrando salas", "Trollando"]

color_opts = {"Azul": 0x008bFF, "Verde": 0x10FF00, "Vermelho": 0xFF2626, "Amarelo":  0xF4FF00, "Branco": 0xFFFFFF}

global upgrades, upcosts
upgrades = ['', '# ⏫ Upgrade para **Nível 2**?\n> A guilda <@&REPGUILD> desbloqueará as seguintes melhorias:\n- :speech_balloon: **Chat de guilda**\n- <:guild_member:1217871413617229914> **+1 Vaga**\n\n:credit_card: **O upgrade custará 50.0 <:blank:1124439750208655500> do cofre da guilda**']
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
    nome = com.Param(max_length=35),
    cor = com.Param(max_length=10),
    símbolo: com.option_enum(simbol_opts) = 0
  ): 
    """
    Custa 100 𝔅 ➔ 👥 Crie sua própria guilda: Um super grupo de estudo em conjunto!
    Parameters
    ----------
    nome: O nome da sua guilda
    cor: Escolha entre: Azul, Verde, Vermelho, Amarelo, Branco
    símbolo: O emoji que representa sua guilda
    """
	  
    guild = inter.guild
    uid = inter.author.id
    suid = str(uid)

    símbolo = simbols[símbolo]

    try:
      cor = color_opts[cor.capitalize()]
    except:
      return await inter.response.send_message(f'"{cor}" não é uma cor válida dentre as disponíveis **(Azul, Verde, Vermelho, Amarelo, Branco)**', ephemeral=True)

    udata = udb.find_one({'uid': uid, 'blanks': {'$gte': 100}})

    if not udata: 
      return await inter.response.send_message('Você não tem blanks o suficiente. Vaza, POBRE', ephemeral=True)

    elif not bool(re.match(r'^[a-zA-ZÀ-ÖØ-öø-ÿ\s]+$', nome)):
      return await inter.response.send_message(f'**Nome de guilda inválido**\n> Inclua apenas letras; nada de números e caracteres especiais.', ephemeral=True)

    uguild = None
    try:
      uguild = udb.find_one({'ugid': udata['guild']})
    except: pass

    if uguild:
      return await inter.response.send_message(f'Você já participa da guilda "**{uguild["guild_name"]}**"', ephemeral=True)

    role = await guild.create_role(name=f'{símbolo} ' + nome + ' (Nv1)', color=disnake.Color(cor))
    await inter.author.add_roles(role)
    
    udb.insert_one({
      'ugid': uid,
      'guild_name': nome.capitalize(), 
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
      description=f'# A guilda __{nome}__ foi fundada com sucesso.\n> Você recebeu o cargo <@&{role.id}>. Marque esse cargo sempre que quiser chamar os membros da guilda. **Sua sala privada estará sempre aberta para eles.**\n▬▬▬▬▬▬▬▬▬▬▬▬\n{newBlank([udata["blanks"] - 100, 100], "g")}',
      colour=disnake.Color(cor)
    )

    return await inter.response.send_message(embed=embed)

  @sguild.sub_command(name="invite")
  async def sbinvite(
    inter = disnake.ApplicationCommandInteraction,
    usuário = com.Param(max_length=100)
  ): 
    """
    👑 Para líderes (Custa 5 𝔅) ➔ ➕ Convide um usuário para sua guilda
    Parameters
    ----------
    usuário: EX: @fulano
    """

    try:
      udata = udb.find_one({'uid': inter.author.id})
      have_guild = udata['guild']
    except:
      return await inter.response.send_message('Você nem tem guilda...', ephemeral=True)
    
    uguild = udb.find_one({'ugid': inter.author.id})
    mlimit = 10 + (uguild["level"] - 1)

    if udata['blanks'] < 5:
      return await inter.response.send_message('Você não tem blanks o suficiente. Vaza, POBRE', ephemeral=True)
	  
    elif not uguild: 
      return await inter.response.send_message('**Apenas o dono da sua guilda pode criar convites**', ephemeral=True)

    elif len(uguild['guild_members']) >= mlimit:
      return await inter.response.send_message(f'**Sua guilda está cheia. O limite atual é de {mlimit} membros**\n- Aumente o nível da guilda com </guild upgrade:1233220536780324864> para aumentar o limite', ephemeral=True)
	  
    elif usuário.count('<@') > 1:
      return await inter.response.send_message('**Você só pode convidar um usuário por vez**', ephemeral=True)

    cuid = int(usuário.replace(">", "").replace("<", "").replace("@", ""))

    if inter.author.id == cuid:
      return await inter.response.send_message('Você não pode se autoconvidar né, gênio.', ephemeral=True)

    guild = inter.guild

    valid_cuid = guild.get_member(cuid)
    
    if not valid_cuid:
      return await inter.response.send_message('**Convide um usuário válido!**', ephemeral=True)

    try:
      has_guild = udb.find_one({'uid': cuid})['guild']
      return await inter.response.send_message(f'Esse usuário já faz parte de uma guilda', ephemeral=True)
    except: pass

    embed = disnake.Embed(
      description=f"{inter.author.mention} o convidou para entrar na guilda **{uguild['guild_name']}**\n▬▬▬▬▬▬▬▬▬▬▬▬\n{newBlank([udata['blanks'] - 5, 5], 'g')}",
      colour=0x000080
    )

    udb.update_one({'uid': inter.author.id}, {'$inc': {'blanks': -5}})

    try: await namedisplay(inter.author)
    except: pass
    
    await inter.response.send_message(f'<@{cuid}>', embed=embed, components=[disnake.ui.Button(label='👥 Entrar na guilda', style=disnake.ButtonStyle.primary, custom_id=f"enterguild.{cuid}.by.{inter.author.id}")])

  @sguild.sub_command(name="kick")
  async def sbkick(
    inter = disnake.ApplicationCommandInteraction,
    usuário = com.Param(max_length=100),
    motivo: com.option_enum(reason_opts) = None
  ): 
    """
    👑 Para líderes ➔ ❌ Expulse um usuário de sua guilda
    Parameters
    ----------
    usuário: EX: @fulano
    motivo: Escolha uma justificativa
    """
    try:
      udata = udb.find_one({'uid': inter.author.id})
      have_guild = udata['guild']
    except:
      return await inter.response.send_message('Você nem tem guilda...', ephemeral=True)
    
    uguild = udb.find_one({'ugid': inter.author.id})

    if not uguild: 
      return await inter.response.send_message('**Apenas o dono da sua guilda pode expulsar membros**', ephemeral=True)
	  
    elif usuário.count('<@') > 1:
      return await inter.response.send_message('**Você só pode convidar um usuário por vez**', ephemeral=True)

    cuid = int(usuário.replace(">", "").replace("<", "").replace("@", ""))

    if inter.author.id == cuid:
      return await inter.response.send_message('Você não pode se autokickar né, gênio.', ephemeral=True)

    guild = inter.guild

    valid_cuid = guild.get_member(cuid)
    inyour_guild = uguild['guild_members']
    
    if not valid_cuid:
      return await inter.response.send_message('**Convide um usuário válido!**', ephemeral=True)
    elif cuid not in uguild['guild_members']:
      return await inter.response.send_message('**Esse usuário não está na sua guilda.**', ephemeral=True)

    embed = disnake.Embed(
      description=f"<a:heartbreak:1219782670062452736> Você foi expulso da guilda **{uguild['guild_name']}**",
      colour=0xed3325
    )

    try: embed.description += f'\n▬▬▬▬▬▬▬▬▬▬▬▬\n## Motivo:\n> {reasons[motivo]}'
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
    confirmar = com.Param(max_length=3)
  ): 
    """
    Saia de sua guilda
    Parameters
    ----------
    confirmar: Digite "sim" para confirmar.
    """
    if 1126331167084388372 != inter.channel.id:  await inter.response.send_message(f"**Utilize esse comando só no canal <#{1126331167084388372}>**!", ephemeral=True)
	  
    if confirmar.lower() != 'sim': return await inter.response.send_message('Confirmação inválida. Você deve digitar "**sim**" para prosseguir com a ação', ephemeral=True)
	  
    try:
      udata = udb.find_one({'uid': inter.author.id})
      have_guild = udata['guild']
      uguild = udb.find_one({'ugid': udata['guild']})
    except:
      return await inter.response.send_message('Você nem tem guilda...', ephemeral=True)

    svguild = getSv('guild')
    guild_role = svguild.get_role(uguild['guild_role'])
    await inter.author.remove_roles(guild_role)

    if uguild['ugid'] == inter.author.id: # O lider da guilda saiu.
      if len(uguild['guild_members']) == 1:
        await guild_role.delete()

        udb.delete_one({'ugid': udata['guild']})
        new_leader = f"\n> O último membro saiu. A guilda foi desfeita."

      else:
        set_owner = uguild['guild_members'][1]
        udb.update_one({'ugid': udata['guild']}, {'$set': {'ugid': set_owner, 'guild_owner': set_owner}, '$pull': {'guild_members': inter.author.id}, '$unset': {f'bank.contributors.{inter.author.id}': 1}})
        udb.update_many({'guild': inter.author.id}, {'$set': {'guild': set_owner}})
		  
        new_leader = f"\n> A posse da guilda irá para o membro mais antigo. O novo líder da guilda agora é <@{set_owner}>"		  

      icon_display = '# <:guild_owner:1217871403538321428>'

		
    else:
      udb.update_one({'ugid': udata['guild']}, {'$pull': {'guild_members': inter.author.id}, '$unset': {f'bank.contributors.{inter.author.id}': 1}})
      icon_display, new_leader = '<:guild_member:1217871413617229914>', ''

    embed = disnake.Embed(
      description=f"{icon_display} {inter.author.mention} saiu da guilda **{uguild['guild_name']}**{new_leader}",
      colour=0xed3325
    )
	  
    udb.update_one({'uid': inter.author.id}, {'$unset': {'guild': 1}})

    await inter.response.send_message(embed=embed)




  @sguild.sub_command(name="stats")
  async def sbstats(
    inter = disnake.ApplicationCommandInteraction,
  ): 
    """
    👀 Veja as estatísticas de sua guilda
    """
    try:
      udata = udb.find_one({'uid': inter.author.id})
      has_guild = udata['guild']
    except:
      return await inter.response.send_message('Você nem tem guilda...', ephemeral=True)

    guild = udb.find_one({'ugid': has_guild})
	  
    svguild = getSv('guild')
	  
    grole = svguild.get_role(guild['guild_role'])
	  

    contributors = sorted(guild["bank"]["contributors"], key=lambda uid: guild["bank"]["contributors"][str(uid)])[::-1]
   
    contributors = '\n'.join([f'**`{i + 1}.`** {"<:guild_owner:1217871403538321428>" if int(uid) == guild["ugid"] else "<:guild_member:1217871413617229914>"} <@{uid}> **{round(guild["bank"]["contributors"][uid], 1)}** <:blank:1124439750208655500>' for i, uid in enumerate(contributors)])


    embed = disnake.Embed(
      description=f'# <@&{guild["guild_role"]}>\n> **Fundada <t:{int((guild["was_born"] + timedelta(hours=3)).timestamp())}:R>**\n> **{len(guild["guild_members"])}/{10 + (guild["level"] - 1)} Membros**\n\n## <:guildvault:1233430694231932959> **Cofre:** {round(guild["bank"]["blanks"], 1)} <:blank:1124439750208655500>\n\n## Maiores contribuidores\n{contributors}',
      colour = grole.colour
    )

    return await inter.response.send_message(embed=embed)



  @sguild.sub_command(name="upgrade")
  async def sbview(
    inter = disnake.ApplicationCommandInteraction,
  ): 
    """
    👑 Para líderes ➔ ⏫ Aumente o nível da sua guilda
    """
    try:
      udata = udb.find_one({'uid': inter.author.id})
      have_guild = udata['guild']
    except:
      return await inter.response.send_message('Você nem tem guilda...', ephemeral=True)
	  
    
    uguild = udb.find_one({'ugid': inter.author.id})

    if not uguild: 
      return await inter.response.send_message('**Apenas o dono da sua guilda pode fazê-la subir de nível**', ephemeral=True)
    elif uguild["level"] == 2:
      return await inter.response.send_message('**Sua guilda está no nível máximo.**', ephemeral=True)


    embed = disnake.Embed(
      description=upgrades[uguild["level"]].replace("REPGUILD", str(uguild["guild_role"])),
      colour=0xFFFFFF
	)

    await inter.response.send_message(embed=embed,components=[disnake.ui.Button(label='Upgrade!', emoji='🆙', style=disnake.ButtonStyle.primary, custom_id=f"upgradeguild.{inter.author.id}.{upcosts[uguild['level']]}")])






