from json import load as jload, dump as jdump
from disnake import Embed
import disnake
from random import randint
from traceback import format_exc as error
from datetime import datetime

from functions.page1 import newBlank, namedisplay, getSv

from mongo import udb

async def memberJoin(user, cInvites, cWelcome):
    if user.bot:
        rBot = cWelcome.guild.get_role(1111035491253497989)
        await user.add_roles(rBot)
        return
    
    guild = cInvites.guild

    with open('jsons/invites.json', 'r') as file:
        invs = jload(file)

    div1 = guild.get_role(1137200884137332849)
    div2 = guild.get_role(1138587258526638110)
    ini = guild.get_role(1093543202105077792)

    try:
        await user.add_roles(div1)
        await user.add_roles(div2)
        await user.add_roles(ini)
	
    except Exception as e:
        print(f"Erro ao adicionar papéis ao usuário: {e}")

    inviter = 0

    for inv in await guild.invites():
        icode, inviter = inv.code, inv.inviter.id

        try:
            stats = invs[icode]
        except:
            invs[icode] = [inviter, 0]
            stats = invs[icode]

        if stats[1] != inv.uses:
            invs[icode][1] = inv.uses

            if type(stats[0]) == str:  # Se for um convite customizado (Sem dono)
                welcome_sub = stats[0]
            else:
                try:
                    userinvites = sum(i[1] for i in invs.values() if i[0] == inviter)

                    invcount = f"{userinvites} invite"
                    if userinvites != 1:
                        invcount += "s"

                    blanks = udb.find_one({'uid': inviter})['blanks']
                    rew = 3.0
                    embed = Embed(
                        description=f'Você convidou {user.mention} e agora possui **{invcount}**)\n\n{newBlank([blanks, rew])}',
                        colour=0x0072DC
                    )

                    udb.update_one({'uid': inviter}, {'$inc': {'blanks': rew, 'timed.week.blank': rew, 'invites': 1}})

                    try:
                        await namedisplay(inviter)
                    except Exception as e:
                        print(f"Erro ao exibir o nome do usuário: {e}")

                    welcome_sub = f'✉️ Convidado por {inv.inviter}'

                    await cInvites.send(f'<@{inviter}>', embed=embed)
                except Exception as e:
                    print(f"Erro ao enviar mensagem de convite: {e}")

            with open('jsons/invites.json', 'w') as file:
                jdump(invs, file, indent=2)
            break

    embed = Embed(
        description=f'### <:joined:1219746985469411348> **Um novo desafiante surgiu**\n<@{user.id}>, Seja bem-vindo ao Blank Mind',
        color=0x33FF33,
    )

    try:
        embed.set_footer(text=welcome_sub)
    except Exception as e:
        embed.set_footer(text="🧭 Explorou e achou o servidor")

    try:
        imgprof = user.avatar.url
    except Exception as e:
        imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'

    try:
        embed.set_thumbnail(url=imgprof)
    except Exception as e:
        print(f"Erro ao definir a thumb do embed: {e}")

    try:
        embed.set_author(name=user.display_name.split(' ═ ')[0].capitalize())
        await cWelcome.send(embed=embed)
    except Exception as e:
        print(f"Erro ao enviar a mensagem de boas-vindas: {e}")

    try:
        udb.insert_one({
            'uid': user.id,
            'blanks': 0.0,
            'level': 1,
            'timed': {
                'week': {
                    'blank': 0,
                    'calls': 0
                }
            },
            'linked_stat': 100,
            'invites': 0,
            'invited_by': inviter,
        })
    except Exception as e:
        print(f"Erro ao inserir documento no banco de dados: {e}")

    try:

        embed3 = disnake.Embed(
          description='# Seja bem-vindo(a) ao **Blank Mind**, o servidor de estudos mais completo. Temos muitas mecânicas, então..\n\n# Esses 3 chats tirarão todas as suas dúvidas:\n## <#1138573291829858366>\n## <#1138573308837777568>\n## <#1138572804489490552>\n\n**Caso ainda possua dúvidas, use:** <#1238155003651166271>\n- Boa sorte, estudante!',
          colour=0x000000
        )

        await user.send(embed=embed3)

        
        with open('Blank Mind Universe.mp4', 'rb') as video:
          await user.send(file=disnake.File(video, filename='Blank Mind.mp4'))

        try:
            await namedisplay(user)
        except Exception as e:
            print(f"Erro ao exibir o nome do usuário: {e}")


    except Exception as e:
        print(f"Erro ao enviar mensagem privada para o usuário: {e}")