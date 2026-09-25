import disnake
from asyncio import sleep as asleep
import asyncio
from traceback import format_exc as error

from functions.page1 import getSv

global MPstate, avaible
MPstate = ['<:MPS_N:1230951538373951488><:MP_N:1230949545265987656><:MP_N:1230949545265987656><:MPE_N:1230960976816242728>', 
	     '<:MPS_L:1230951553825771520><:MP_N:1230949545265987656><:MP_N:1230949545265987656><:MPE_N:1230960976816242728>',
	     '<:MPS_M:1230951569512464384><:MP_M:1230949600798703729><:MP_N:1230949545265987656><:MPE_N:1230960976816242728>',
	     '<:MPS_H:1230951582368268319><:MP_H:1230949617668067379><:MP_H:1230949617668067379><:MPE_N:1230960976816242728>',
	     '<:MPS_F:1230955228954890442><:MP_F:1230954943180050604><:MP_F:1230954943180050604><:MPE_F:1230954925387681823>'
	    ]

avaible = [f'- **BLOQUEADOS**\n - <:MP_LOCK:1230985696353714237> :gear: **Comandos diversos**\n - <:MP_LOCK:1230985696353714237> :hourglass_flowing_sand: **Comandos de call**\n - <:MP_LOCK:1230985696353714237> :diamond_shape_with_a_dot_inside: **Comandos de guilda**', f'- **NOVO**\n - :new: :gear: **Comandos diversos** ➜ VBOT▬▬▬▬▬▬▬\n- **BLOQUEADOS**\n - <:MP_LOCK:1230985696353714237> :hourglass_flowing_sand: **Comandos de call**\n - <:MP_LOCK:1230985696353714237> :diamond_shape_with_a_dot_inside: **Comandos de guilda**', f'- :gear: **Comandos diversos** ➜ VBOT▬▬▬▬▬▬▬\n- **NOVO**\n - :new: :hourglass_flowing_sand: **Comandos de call** ➜ CBOT▬▬▬▬▬▬▬\n- **BLOQUEADO**\n - <:MP_LOCK:1230985696353714237> :diamond_shape_with_a_dot_inside: **Comandos de guilda**' ,f'- :gear: **Comandos diversos** ➜ VBOT- :hourglass_flowing_sand: **Comandos de call** ➜ CBOT- :diamond_shape_with_a_dot_inside: **Comandos de guilda** ➜ GBOT']


async def initial(bot, mode='cmds'):
  if mode == 'recruit':
    chat = getSv('cRecruit')
    await chat.purge(limit=None)
	  
    with open('pale_banner2.jpg', 'rb') as file: banner = disnake.File(file)
    await chat.send(file=banner)

    epale = disnake.PartialEmoji(animated=False, id='1232749831886209035', name='paleshield')
	  
    await chat.send("""
# <:paleshield:1232749831886209035> Pale Shield
- **Objetivo principal:** Debater sobre assuntos e possíveis melhorias, visando o futuro do servidor
- **Objetivo secundário:** Moderar o servidor e punir usuários mal intencionados 
- Não precisa ser muito ativo, mas não é permitido ser ocioso nas discussões da Pale
- **Só é possível existir 5 membros Pale Shield por vez. O menos útil entre esses 5 será deposto e outra pessoa (talvez você) assumirá o cargo**

# Candidatura
- O nível mínimo é <@&1143937396027699352>
- Sua única tarefa para ser aprovado é **me convencer**. Me diga seu diferencial e considere nossos objetivos.

# Você ganhará:
- Alto poder de decisão
- Poder de castigar e remover mensagens de usuários
- Capacidade de criar e comandar eventos ou outros projetos
- Ícone e cargo exclusivo
- Chats exclusivos

**`> Procuramos pessoas capazes e dedicadas <`**
""",components=[disnake.ui.Button(label="Quero me candidatar", emoji='🔰', style=disnake.ButtonStyle.danger, custom_id="palerequest")])

	
  elif mode == 'report':
     cReport = getSv('cReport')
	  
     roles = ["❔ Tirar dúvida", "🤖 Relatar bug", "🔰 Denunciar usuário"]
     dropdown = disnake.ui.Select(
       placeholder='Escolha uma ação',
       options=[disnake.SelectOption(label=role, value=role) for role in roles],
       custom_id='report',
       min_values=1,
       max_values=1
     )
      
     view2 = disnake.ui.View()
     view2.add_item(dropdown)

     embedesco = disnake.Embed(
       description="# 🔧・suporte\n### :ticket: **Um ticket de ajuda privado será criado e responderemos o seu chamado**",
       colour=0xFFFFFF
     )

     await cReport.purge(limit=2)
	  
     await cReport.send(embed=embedesco, view=view2)
	
  elif mode == 'cmds':
    chats = getSv(['cCommands_MPnull', 'cCommands_MPlow', 'cCommands_MPmed', 'cCommands'])

    emb1 = disnake.Embed(
      description=f'# :page_facing_up: COMANDOS DE RELATOR',
      colour = 0xFFFFFF
    )
    emb2 = disnake.Embed(
      description=f'## </mission set:1166864611199434895>\n> Ajuda a criar disciplina, fortalece o hábito de estudar e te ajuda a consolidar os conteúdos\n> Ao usá-lo, você ganha **10.0** <:blank:1124439750208655500> e se torna um **relator**, alguém que escreve relatórios sobre o que estudou/revisou no dia.\n\n> Se você já for um relator, usar esse comando atualizará seu horário de envio',
      colour = 0x33FF33
    )
    emb3 = disnake.Embed(
      description=f'## </mission send:1166864611199434895>\n> Envia seu relatório. Você só pode enviá-lo entre 1h antes e 1h depois do horário que você escolher.',
      colour = 0x33FF33
    )
    emb4 = disnake.Embed(
      description=f'## </mission giveup:1166864611199434895>\n> Faz você deixar de ser um relator\n> Você deixará de sofrer penalidades, mas não ganhará mais os <:blank:1124439750208655500> do relatório',
      colour = 0x33FF33
    )

    emb5 = disnake.Embed(
      description=f'# :chart_with_upwards_trend: COMANDOS ESTATÍSTICOS',
		colour = 0xFFFFFF		
    )
    emb6 = disnake.Embed(
      description=f'## </stats:1137464281756090511>\n> Mostra suas estatísticas, como **quantidade de blanks, tempo em calls, posição nos rankings, nível e guilda**. Se você for um **relator ou pesquisador**, esse comando mostrará dados adicionais',
		colour = 0x33FF33
    )
    emb7 = disnake.Embed(
      description=f'## </top:1137464281756090512>\n> Mostra o ranking dos 10 melhores membros e seu ranking comparado com eles. Também é possível escolher os top 10 baseado em alguma estatística específica',
		colour = 0x33FF33	
    )

    emb8 = disnake.Embed(
      description=f'# <a:cronocard:1142933723097084014> COMANDOS DE CARTAS',
        colour=0xFFFFFF	
    )
    emb9 = disnake.Embed(
      description=f'## </cronocard roll:1142940210649387018>  (Custa **1.5** <:blank:1124439750208655500>)\n> Procure por **cronocards**: cartas que simbolizam pessoas influentes ao longo da história, cada uma com um superpoder. Ao usar o comando, é possível uma carta de raridade aleatória baseada no quão forte é o superpoder da pessoa da carta:\n\n<:L1:1142498467818782831> **Lendária (1% de chance)**\n<:E1:1142498412391043076> Épica (4% de chance)\n<:R1:1142496422948786201> Rara (15% de chance)\n<:I1:1142495469717684236> Incomum (30% de chance)\n<:C1:1142494346696982650> Comum (50% de chance)\n\n> Se você optar por coletar a carta encontrada para sua coleção, a carta custará um certo número de <:blank:1124439750208655500> baseado em sua raridade. Você ganhará poder adquirindo cartas',
        colour=0x33FF33
    )
    emb10 = disnake.Embed(
      description=f'## </cronocard list:1142940210649387018>\n> Veja sua coleção de cartas e as cartas que você não encontrou',
        colour=0x33FF33
    )

    emb11 = disnake.Embed(
      colour=0xFFFFFF,
      description=f'# <:blank:1124439750208655500> <:blanks:1124438972144295936> <:blankbag:1124445117261037630> COMANDOS MONETÁRIOS'	
    )
    emb12 = disnake.Embed(
      colour=0x33FF33,
      description=f'## </blank pay:1198736232113504357>\n> Pague um usuário'
    )
    emb13 = disnake.Embed(
      colour=0x33FF33,
      description=f'## </blank loan:1198736232113504357>\n> Cria um contrato de empréstimo que ativa se o outro usuário concordar. O contrato faz você **X blanks** imediatamente a um usuário e, todo dia, durante **X dias**, o sistema te dará **Y blanks** desse usuário.\n\n> Se o usuário não pagar a dívida a tempo ou sair do server, **você receberá todo o valor restante que o usuário não pagou.** O contrato sempre garantirá o seu lucro.'
    )

    emb14 = disnake.Embed(
      colour=0xFFFFFF,
      description=f'# :boom: COMANDOS VARIADOS' 		
    )
    emb15 = disnake.Embed(
      colour=0x33FF33,
      description=f'## </namedisplay:1198342002778062950> (Custa **5.0** <:blank:1124439750208655500>)\n> Vincula ou desvincula uma estatística ao seu nome.\n\n**Exemplos:**\n> **Nome** ➜ Nome sem estatísticas (Desvinculado)\n> **Nome ═ 50.0 𝔅** ➜ Quantidade de blanks\n> **Nome ═ 100h** ➜ Quantidade de horas estudadas em calls'
    )
    emb16 = disnake.Embed(
      colour=0x33FF33,
      description=f'## </checklist:1138872920362471454>\n> Cria uma checklist automática. **Você pode separar a checklist em tópicos e em tarefas**. As tarefas só podem ser finalizadas em ordem e podem ser marcadas como **:green_square: Concluída** e **:red_square: Não concluída**.'
    )
    emb17 = disnake.Embed(
      colour=0x33FF33,
      description=f'## </searchbuddy:1221254411733696513>\n> Procure parceiros de estudo filtrando as características que você quiser\n\n- **Exemplos:**\n - *Idade: +18, xadrez* ➜ Todos com 18 anos pra cima que gostam de xadrez\n - *Idade: 20, faculdade* ➜ Todos com 20 anos que cursam a faculdade\n - *Idade: -17, xadrez, grupo, filosofia* ➜ Todos com 17 anos para baixo que querem participar de um grupo e gostam de filosofia'
    )




    embn1 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> :page_facing_up: COMANDOS DE RELATOR\n> Desbloqueia com um <@&1230869038402375751>',
      colour = 0xed3325
    )
    embn5 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> :chart_with_upwards_trend: COMANDOS ESTATÍSTICOS\n> Desbloqueia com um <@&1230869044190777437>',
      colour = 0xed3325
    )
    embn8 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> <a:cronocard:1142933723097084014> COMANDOS DE CARTAS\n> Desbloqueia com um <@&1230869044190777437>',
      colour = 0xed3325
    )
    embn11 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> <:blank:1124439750208655500> <:blanks:1124438972144295936> <:blankbag:1124445117261037630> COMANDOS MONETÁRIOS\n> Desbloqueia com um <@&1230869038402375751>',
      colour = 0xed3325
	)
    embn14 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> :boom: COMANDOS VARIADOS\n> Desbloqueia com um <@&1230869044190777437>', 	
      colour = 0xed3325
    )
	  



	  
    embl1 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> :page_facing_up: COMANDOS DE RELATOR\n> Desbloqueia com um <@&1230869038402375751>',
      colour = 0xed3325
    )

    embl5 = disnake.Embed(
      description=f'# :new: :chart_with_upwards_trend: COMANDOS ESTATÍSTICOS',
		colour = 0x8982C8	
    )
    embl6 = disnake.Embed(
      description=f'## :new: </stats:1137464281756090511>\n> Mostra suas estatísticas, como **quantidade de blanks, tempo em calls, posição nos rankings, nível e guilda**. Se você for um **relator ou pesquisador**, esse comando mostrará dados adicionais',
		colour = 0x8982C8
    )
    embl7 = disnake.Embed(
      description=f'## <:MP_LOCK:1230985696353714237> </top:1137464281756090512>',
		colour = 0xed3325
    )

    embl8 = disnake.Embed(
      description=f'# :new: <a:cronocard:1142933723097084014> COMANDOS DE CARTAS',
        colour=0x8982C8	
    )
    embl9 = disnake.Embed(
      description=f'## :new: </cronocard roll:1142940210649387018>  (Custa **1.5** <:blank:1124439750208655500>)\n> Procure por **cronocards**: cartas que simbolizam pessoas influentes ao longo da história, cada uma com um superpoder. Ao usar o comando, é possível uma carta de raridade aleatória baseada no quão forte é o superpoder da pessoa da carta:\n\n<:L1:1142498467818782831> **Lendária (1% de chance)**\n<:E1:1142498412391043076> Épica (4% de chance)\n<:R1:1142496422948786201> Rara (15% de chance)\n<:I1:1142495469717684236> Incomum (30% de chance)\n<:C1:1142494346696982650> Comum (50% de chance)\n\n> Se você optar por coletar a carta encontrada para sua coleção, a carta custará um certo número de <:blank:1124439750208655500> baseado em sua raridade. Você ganhará poder adquirindo cartas',
        colour=0x8982C8
    )
    embl10 = disnake.Embed(
      description=f'## :new: </cronocard list:1142940210649387018>\n> Veja sua coleção de cartas e as cartas que você não encontrou',
        colour=0x8982C8
    )

    embl11 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> <:blank:1124439750208655500> <:blanks:1124438972144295936> <:blankbag:1124445117261037630> COMANDOS MONETÁRIOS\n> Desbloqueia com um <@&1230869038402375751>',
      colour = 0xed3325
    )

    embl14 = disnake.Embed(
      colour=0x8982C8,
      description=f'# :new: :boom: COMANDOS VARIADOS' 		
    )
    embl15 = disnake.Embed(
      colour=0xed3325,
      description=f'## <:MP_LOCK:1230985696353714237> </namedisplay:1198342002778062950>'
    )
    embl16 = disnake.Embed(
      colour=0xed3325,
      description=f'## <:MP_LOCK:1230985696353714237> </checklist:1138872920362471454>'
    )
    embl17 = disnake.Embed(
      colour=0x8982C8,
      description=f'## :new: </searchbuddy:1221254411733696513>\n> Procure parceiros de estudo filtrando as características que você quiser\nExemplos:\n- *Idade: +18, xadrez* ➜ Todos com 18 anos pra cima que gostam de xadrez\n- *Idade: 20, faculdade* ➜ Todos com 20 anos que cursam a faculdade\n- *Idade: -17, xadrez, grupo, filosofia* ➜ Todos com 17 anos para baixo que querem participar de um grupo e gostam de filosofia'
    )






    embm1 = disnake.Embed(
      description=f'# :new: :page_facing_up: COMANDOS DE RELATOR',
      colour = 0x8982C8	
    )
    embm2 = disnake.Embed(
      description=f'## :new: </mission set:1166864611199434895>\n> Ajuda a criar disciplina, fortalece o hábito de estudar e te ajuda a consolidar os conteúdos\n> Ao usá-lo, você ganha **10.0** <:blank:1124439750208655500> e se torna um **relator**, alguém que escreve relatórios sobre o que estudou/revisou no dia.\n\n> Se você já for um relator, usar esse comando atualizará seu horário de envio',
      colour = 0x8982C8	
    )
    embm3 = disnake.Embed(
      description=f'## :new: </mission send:1166864611199434895>\n> Envia seu relatório. Você só pode enviá-lo entre 1h antes e 1h depois do horário que você escolher.',
      colour = 0x8982C8	
    )
    embm4 = disnake.Embed(
      description=f'## :new: </mission giveup:1166864611199434895>\n> Faz você deixar de ser um relator\n> Você deixará de sofrer penalidades, mas não ganhará mais os <:blank:1124439750208655500> do relatório',
      colour = 0x8982C8	
    )

    embm5 = disnake.Embed(
      description=f'# :chart_with_upwards_trend: COMANDOS ESTATÍSTICOS',
		colour = 0xFFFFFF			
    )
    embm6 = disnake.Embed(
      description=f'## </stats:1137464281756090511>\n> Mostra suas estatísticas, como **quantidade de blanks, tempo em calls, posição nos rankings, nível e guilda**. Se você for um **relator ou pesquisador**, esse comando mostrará dados adicionais',
		colour = 0x33FF33	
    )
    embm7 = disnake.Embed(
      description=f'## :new: </top:1137464281756090512>\n> Mostra o ranking dos 10 melhores membmros e seu ranking comparado com eles. Também é possível escolher os top 10 baseado em alguma estatística específica',
		colour = 0x8982C8		
    )

    embm8 = disnake.Embed(
      description=f'# <a:cronocard:1142933723097084014> COMANDOS DE CARTAS',
        colour=0xFFFFFF	
    )
    embm9 = disnake.Embed(
      description=f'## </cronocard roll:1142940210649387018>  (Custa **1.5** <:blank:1124439750208655500>)\n> Procure por **cronocards**: cartas que simbolizam pessoas influentes ao longo da história, cada uma com um superpoder. Ao usar o comando, é possível uma carta de raridade aleatória baseada no quão forte é o superpoder da pessoa da carta:\n\n<:L1:1142498467818782831> **Lendária (1% de chance)**\n<:E1:1142498412391043076> Épica (4% de chance)\n<:R1:1142496422948786201> Rara (15% de chance)\n<:I1:1142495469717684236> Incomum (30% de chance)\n<:C1:1142494346696982650> Comum (50% de chance)\n\n> Se você optar por coletar a carta encontrada para sua coleção, a carta custará um certo número de <:blank:1124439750208655500> baseado em sua raridade. Você ganhará poder adquirindo cartas',
        colour=0x33FF33
    )
    embm10 = disnake.Embed(
      description=f'## </cronocard list:1142940210649387018>\n> Veja sua coleção de cartas e as cartas que você não encontrou',
        colour=0x33FF33
    )

    embm11 = disnake.Embed(
      colour=0x8982C8,
      description=f'# :new: <:blank:1124439750208655500> <:blanks:1124438972144295936> <:blankbag:1124445117261037630> COMANDOS MONETÁRIOS'	
    )
    embm12 = disnake.Embed(
      colour=0x8982C8,
      description=f'## :new: </blank pay:1198736232113504357>\n> Pague um usuário'
    )
    embm13 = disnake.Embed(
      colour=0x8982C8,
      description=f'## :new: </blank loan:1198736232113504357>\n> Cria um contrato de empréstimo que ativa se o outro usuário concordar. O contrato faz você **X blanks** imediatamente a um usuário e, todo dia, durante **X dias**, o sistema te dará **Y blanks** desse usuário.\n\n> Se o usuário não pagar a dívida a tempo ou sair do server, **você receberá todo o valor restante que o usuário não pagou.** O contrato sempre garantirá o seu lucro.'
    )

    embm14 = disnake.Embed(
      colour=0xFFFFFF,
      description=f'# :boom: COMANDOS VARIADOS' 		
    )
    embm15 = disnake.Embed(
      colour=0xed3325,
      description=f'## <:MP_LOCK:1230985696353714237> </namedisplay:1198342002778062950>'
    )
    embm16 = disnake.Embed(
      colour=0xed3325,
      description=f'## <:MP_LOCK:1230985696353714237> </checklist:1138872920362471454>'
    )
    embm17 = disnake.Embed(
      colour=0x33FF33,
      description=f'## </searchbuddy:1221254411733696513>\n> Procure parceiros de estudo filtrando as características que você quiser\n\n- **Exemplos:**\n - *Idade: +18, xadrez* ➜ Todos com 18 anos pra cima que gostam de xadrez\n - *Idade: 20, faculdade* ➜ Todos com 20 anos que cursam a faculdade\n - *Idade: -17, xadrez, grupo, filosofia* ➜ Todos com 17 anos para baixo que querem participar de um grupo e gostam de filosofia'
    )



	  
    all_embeds = [
      [[embn1], [embn5], [embn8], [embn11], [embn14]],
      [[embl1], [embl5, embl6, embl7], [embl8, embl9, embl10], [embl11], [embl14, embl15, embl16, embl17]],
      [[embm1, embm2, embm3, embm4], [embm5, embm6, embm7], [embm8, embm9, embm10], [embm11, embm12, embm13], [embm14, embm15, embm16, embm17]],
      [[emb1, emb2, emb3, emb4], [emb5, emb6, emb7], [emb8, emb9, emb10], [emb11, emb12, emb13], [emb14, emb15, emb16, emb17]],
    ]

    async def multichat2(chat, aindex, this_embeds):
      try:
        await chat.purge(limit=1)
		  
        with open('divider_up.png', 'rb') as file: div_up = disnake.File(file)
        await chat.send(file=div_up)

        with open('void.gif', 'rb') as file: void = disnake.File(file)
        await chat.send(file=void)
		  
        for i, embeds in enumerate(this_embeds[aindex]): 
          try: await chat.send(embeds=embeds)
          except: 
            try: await chat.send(file=embeds)
            except: pass
				
          try: 
            if i + 1 < len(this_embeds[aindex]): await chat.send('‎\n\n‎')
          except: print(error())

        vbot, cbot, gbot = '', '', ''
        async for message in chat.history(limit=None):
          for attachment in message.attachments:
            if attachment.filename == 'void.gif': vbot = f'https://discord.com/channels/1091742896098660372/{chat.id}/{message.id}\n'
            elif attachment.filename == 'cronos.gif': cbot = f'https://discord.com/channels/1091742896098660372/{chat.id}/{message.id}\n'
            elif attachment.filename == 'corp.gif': gbot = f'https://discord.com/channels/1091742896098660372/{chat.id}/{message.id}'

        with open('divider_down.png', 'rb') as file: div_down = disnake.File(file)
        await chat.send(file=div_down)

        await chat.send("‎\n‎")
		  
        with open('comandos.gif', 'rb') as file: gif = disnake.File(file)
        await chat.send(file=gif)

        try: await chat.send(avaible[aindex].replace('VBOT', vbot).replace('CBOT', cbot).replace('GBOT', gbot))
        except: pass

      except: print(error())

    try: [asyncio.create_task(multichat2(chat, u, all_embeds)) for u, chat in enumerate(chats)]
    except: print(error())

	


	
  elif mode == 'marks':
    chat = await bot.fetch_channel(1137504108497080420)
    await chat.purge(limit=None)
    await chat.send("Você pode ler cada parte da enciclopédia como um livro, pois temos **marca página!\n\n> Salve os posts que parou reagindo com :bookmark:\n> Para desmarcar, é só retirar a reação do post**\n▬▬▬▬▬▬▬▬▬▬\n", components=[disnake.ui.Button(label="Suas marcações", style=disnake.ButtonStyle.success, custom_id="post_list")])





	

  elif mode == 'rules':
    chat = bot.get_channel(1127316885046837358)
    await chat.purge(limit=None)
    
    embed = disnake.Embed(
      title='Regras',
      description='Como usuário e membro deste servidor, é de suma importância a conformidade com as diretrizes do **[ToS](https://discord.com/terms#1)** e da **[Community guidelines](https://discord.com/guidelines)**.\n▬▬▬▬▬▬▬▬\n### :thumbsup: 1. Seja respeitoso\n> Mantenha o diálogo saudável. **Jamais** propague discursos odiosos, ameaças ou constrangimento\n\n# <a:ultrawarning:1220019342876348448> PROIBIÇÕES:\n### :warning: 2. Poluição de chat \n> Isso inclui flood, spam e utilizar nosso bot de maneira inadequada, fazendo-o enviar várias mensagens num curto espaço de tempo\n### :warning: 3. Autopromoção não autorizada de qualquer tipo\n> É altamente proibido qualquer tipo de divulgação que não tenha sido aprovada. Não divulgue na **DM** de usuários e não mande links de cursos/servidores sem antes consultar <@663525286784139274>\n### :warning: 4. Conteúdo inadequado (NSFW)\n> Inclui vídeos de caráter sexual, perturbador e qualquer tipo de mídia inadequada para menores\n### :warning: 5. Mencionar a staff desnecessariamente\n> Não mencione administradores várias vezes, apenas em situações de emergência, como usuários mal intencionados, raids, etc.',
      colour=0x7df9ff
	)
    embed.set_footer(text='Permanecer neste servidor deixa implicito que você concordou com todas as regras vigentes. Todas as regras estão sujeitas à mudanças.')
    await chat.send(embed=embed)
  elif mode == 'roles':
    try:
      chat = bot.get_channel(1138572804489490552)
      guild = chat.guild

      division = """
▬▬▬
▬▬▬▬▬
▬▬▬▬▬▬▬
▬▬▬▬▬▬▬
▬▬▬▬▬
▬▬▬
"""
		
      await chat.purge(limit=None)

      e = disnake.Embed(
        description='# :inbox_tray: CARGOS SELECIONÁVEIS',
        colour=0xFFFFFF
      )
      
      embedesco = disnake.Embed(
        description="## 🎓 Escolaridade\n<@&1115751360344887316>\n<@&1143697792158666856>\n<@&1115751063610470581>\n<@&1115751059692986608>\n<@&1115751050041888931>\n<@&1115750314679730207>",
        colour=guild.get_role(1115751360344887316).colour
      )
      roles = ["🎓 Faculdade", "🎓 Vestibulando", "🎓 3º ano", "🎓 2º ano", "🎓 1º ano", "🎓 Fundamental"]
      dropdown = disnake.ui.Select(
        placeholder='Seleção única',
        options=[disnake.SelectOption(label=role, value=role) for role in roles],
        custom_id='role_dropdown2',
        min_values=1,
        max_values=1
      )
      
      view2 = disnake.ui.View()
      view2.add_item(dropdown)

      sel = await chat.send(embed=e)
      await chat.send(embed=embedesco, view=view2)
		
      embedreg = disnake.Embed(
        description="## 🌐 Regionais\n<@&1205909270030454835>\n<@&1205908446231138396>\n<@&1205909274207723530>\n<@&1205909278607802479>\n<@&1205909753511804979>",
        colour=guild.get_role(1205909270030454835).colour
      )
      roles = ["🌐 Norte", "🌐 Nordeste", "🌐 Sul", "🌐 Sudeste", "🌐 Centro-Oeste"]
      dropdown = disnake.ui.Select(
        placeholder='Seleção única',
        options=[disnake.SelectOption(label=role, value=role) for role in roles],
        custom_id='role_dropdown4',
        min_values=1,
        max_values=1
      )

      view5 = disnake.ui.View()
      view5.add_item(dropdown)
		
      await chat.send(embed=embedreg, view=view5)

      embevest = disnake.Embed(
        description='## 🎯 Objetivos\n<@&1178025309589745665> ➜ **Exame Nacional do Ensino Médio**\n<@&1178026381586739211> ➜ **ENEM, USP, Unesp, Fuvest..**\n<@&1207455384671883395> ➜ **BACEN, ABIN, INSS, PF...**\n<@&1207455386874150963> ➜ **ITA, IME, EAM, EsPCEx...**\n<@&1238313392985608193> ➜ **OBI, OBF, OBM...**',
        colour=guild.get_role(1178025309589745665).colour
      )
      roles = ["🎯 ENEM", "🎯 Vestibular", "🎯 Concurso Público", "🎯 Concurso Militar", "🎯 Olimpíedas"]
      dropdown = disnake.ui.Select(
        placeholder='Multiseleção',
        options=[disnake.SelectOption(label=role, value=role) for role in roles],
        custom_id='role_dropdown3',
        min_values=0,
        max_values=len(roles)
      )

      view3 = disnake.ui.View()
      view3.add_item(dropdown)
		
      await chat.send(embed=embevest, view=view3)
		
      embednot = disnake.Embed(
        description="## 🔔 Notificáveis\n> Seja notificado em momentos específicos\n\n**<@&1162917883777663037> ➜ Atualizações importantes do server**\n<@&1112017303580708936> ➜ Hora de bumpar (impulsionar) o server\n<@&1138591176681869322> <@&1092918220400369775> ➜ Prazo de relatório quase acabando\n<@&1230693176839245846> ➜ Guildas procurando por novos membros\n<@&1230697271771922475> ➜ Algum evento especial em <#1230696631645765736>",
        colour=guild.get_role(1162917883777663037).colour
      )
      roles = ["🚨 Updates", "🚀 Bump", "📝 Relatórios", "💠 Guildas", "🎲 Minigames"]
      dropdown = disnake.ui.Select(
        placeholder='Multiseleção',
        options=[disnake.SelectOption(label=role, value=role) for role in roles],
        custom_id='role_dropdown1',
        min_values=0,
        max_values=len(roles)
      )
      
      view = disnake.ui.View()
      view.add_item(dropdown)
		
      await chat.send(embed=embednot, view=view)

      with open('divider_down.png', 'rb') as file: div_down = disnake.File(file)
      await chat.send(file=div_down)

      await chat.send("‎\n\n\n‎")	
		
      with open('divider_up.png', 'rb') as file: div_up = disnake.File(file)
      await chat.send(file=div_up)

      e = disnake.Embed(
        description='# :scroll: CARGOS CONDICIONAIS',
        colour=0xFFFFFF
      )
		
      cond = await chat.send(embed=e)
      embedniv = disnake.Embed(
        description='## ⏫ Obtiveís por nível\n> Acumule **horas em calls** para subir de nível!\n\n### <:SUPREMO:1231657119091134565> <@&1231649305362694216> ➜ O nível máximo, ocupado apenas pelos melhores dos melhores\n\n\n<:Lendaviva:1231657160455360532> <@&1199039648828235857>\n\n<:Mestre:1231657249693372624> <@&1168640140395163728>\n\n<:Insano:1231657289081946143> <@&1143937396027699352>\n\n<:Experiente:1231657323429363722> <@&1135629912770891816>\n\n<:Amador:1231657353242345542> <@&1132163320179339344>\n\n<:Ambicioso:1231657391620358265> <@&1122230870460342412>',
        colour=0x0072DC
      )
      await chat.send(embed=embedniv)
		
      embedother = disnake.Embed(
	    description='## 🗿 Situacionais\n<@&1092918220400369775> **+10.0** <:blank:1124439750208655500> ➜ Use o comando </mission set:1166864611199434895>\n\n<@&1174146227961614467> :lock: **+1.0 ~ 10.0** <:blank:1124439750208655500> ➜ Entre no chat <#1174127784189239377> (Só está disponível para quem tem o nível <@&1132163320179339344> para cima). **Escreva um artigo dentro desse chat sobre algum tema e, se esse artigo for aprovado, ele será enviado para a blankpédia e você ganhará o cargo**\n\n<@&1216770648010002482> ➜ Quando você entrar numa guilda, ganhará um cargo com o nome dessa guilda.\n\n<@&1216771400359219251> ➜ **Impulsione o servidor e crie seu próprio cargo**. Você pode escolher a cor, o nome e o ícone!',
          colour=0xffba3a
    )
      await chat.send(embed=embedother)
		
      with open('divider_down.png', 'rb') as file: div_down = disnake.File(file)
      await chat.send(file=div_down)
		
      await chat.send("‎\n\n\n‎")	
  
      with open('cargos.gif', 'rb') as file: cargos = disnake.File(file)
      await chat.send(file=cargos)

      await chat.send(f'- **Cargos selecionáveis** ➜ https://discord.com/channels/1091742896098660372/1138572804489490552/{sel.id}\n- **Cargos condicionais** ➜ https://discord.com/channels/1091742896098660372/1138572804489490552/{cond.id}')
		
    except: print(error())






	

	
  elif mode == 'chats':
    cuids = [1126227397663006813, 1124454684837564416, 1123770807592681565, 1093357243040276551, 1119381667363176518, 1126177822818435102, 1207442864477577257, 1134578673689821224, 1197315030341918761, 1137495923170230374, 1207834421273567254]
    categs = ['# ' + disnake.utils.get(getSv('guild').channels, id=cuid).name.split('═')[0] for cuid in cuids]


    
    emb1 = disnake.Embed(
      description=categs[0] + '\n> **Área inicial. Fique de olho em tudo que atualiza no server**',
      colour=0xffffff
    )
    emb2 = disnake.Embed(
      description='<#1127316885046837358> ➜ Regras gerais do server\n\n<#1100915945813319680> ➜ Avisos e melhorias do server\n\n▬▬▬▬▬▬▬\n\n:fog: <#1230914940437663786> ➜ Formas de ganhar mais MP\n\n:fog: <#1138573291829858366> ➜ Todos os chats do server\n\n:fog: <#1138573308837777568> ➜ Todos os comandos do server\n\n:fog: <#1138572804489490552> ➜ Todos os cargos do server. Veja e selecione seus cargos!\n\n▬▬▬▬▬▬▬\n\n<#1107757022503510147> ➜ Use os comandos dos nossos bots aqui!',
      colour=0x33FF33
    )

    emb3 = disnake.Embed(
      description=categs[1] + '\n> **Interaja com a galera e fique de boas**',
      colour=0xffffff
    )
    emb4 = disnake.Embed(
      description='<#1093630384174006282> ➜ Chat livre e sem tópico\n\n<#1126493560787714048> ➜ Desabafe aqui e se sinta mais leve\n\n<#1124455706309963817> ➜ Fale mais sobre você e se aproxime da galera\n\n<:private_text_channel:1216785798326910996>ﾠ **║:mortar_board:・chat acadêmico** ➜ Vá em <#1138572804489490552> para alterar\n\n<:private_text_channel:1216785798326910996>ﾠ **║:dart:・chats de vestibulares** ➜ Vá em <#1138572804489490552> para alterar\n\n<#1168716210565808220> ➜ Compartilhe vídeos e imagens\n\n<#1136343230217199787> ➜ Crie guerrinhas :cold_face:\n\n<#1124755293767749796> ➜ Compartilhe seus hobbies e encontre pessoas com gostos parecidos',
      colour=0x33FF33
    )
    
    emb5 = disnake.Embed(
      description=categs[2] + '\n> **Ajude nosso server a crescer! :sunglasses:**',
      colour=0xffffff
    )
    emb6 = disnake.Embed(
      description='<#1119719224160551063> **+3.0** <:blank:1124439750208655500> ➜ Convide pessoas. Esse chat mostrará quem você convidou e seu número de convites\n\n<#1112018256564326480> **+1.5** <:blank:1124439750208655500> ➜ Bumpe o server a cada 2 horas. Pegue o cargo de notificação para saber a hora de bumpar\n\n<#1123771863802335332> ➜ Dê ideias para o server. Elas serão votadas e consideradas',
      colour=0x33FF33
    )

    emb7 = disnake.Embed(
      description=categs[3] + '\n> **Estudo direcionado e áreas voltadas para a produtividade**',
      colour=0xffffff
    )
    emb8 = disnake.Embed(
      description='<#1124333630559367258> ➜ Espaço para postar links, ferramentas e estratégias focadas no estudo\n\n<#1141509793241108592> ➜ Tire suas dúvidas sobre questões ou conteúdos\n\n<#1126331167084388372> ➜ Entre em guildas ou forme grupinhos de estudo. Vocês poderão se juntar em calls. Use o comando </guild create:1220132312554147962> **(100 <:blank:1124439750208655500>)** para criar uma guilda ou o comando </guild invite:1220132312554147962> **(5 <:blank:1124439750208655500>)** para convidar pessoas para sua guilda\n\n<#1135738380555137084> ➜ Os relatórios que os relatores enviam ficam expostos aqui\n\n<#1119710450741940325> ➜ Crie checklists para melhorar seu direcionamento. Também é possível criar uma **checklist automática usando o comando** </checklist:1138872920362471454>\n\n<#1212500548520124447> ➜ Exiba seu domínio ou desdomínio de vocabulário em diferentes idiomas! Perfect',
      colour=0x33FF33
    )

    emb9 = disnake.Embed(
      description=categs[4] + '\n> **Acompanhe seu progresso e receba notificações específicas**',
      colour=0xffffff
    )
    emb10 = disnake.Embed(
      description='<#1157769760642171023> **+15.0** <:blank:1124439750208655500> ➜ Mostra os nobres da semana (Os usuários com maiores estatísticas). O 1º colocado é chamado de Rei e fica no topo dos cargos. No final da semana, o rei ganha **15 blanks**\n\n<#1202369082251280404> ➜ Mostre suas conquistas recentes para o server\n\n<#1133474876003459112> ➜ Seja notificado sobre subidas de nível, relatório próximo, etc.\n\n<#1119383275320909896> ➜ **O terror dos relatores**. Esse chat retira uma porcentagem dos **blanks** de quem não conseguiu enviar relatório no dia\n\n<#1109998084718612530> ➜ Acompanhe em tempo real há quanto tempo você está numa call de estudo. Assim que você entrar na call, vai começar a contar o tempo, e quando você sair, vai te dizer o tempo total que você esteve conectado',
      colour=0x33FF33
    )

    emb11 = disnake.Embed(
      description=categs[5] + '\n> **Estude em calls. Quanto mais tempo conectado, mais <:blank:1124439750208655500> você ganha!** Mas você deve ficar conectado por no mínimo **10 minutos** para ganhar recompensas',
      colour=0xffffff
    )
    emb12 = disnake.Embed(
      description='<#1133539336378396856>\n<#1133541164960714752>\n<#1133541192622157906>\n\n<#1207440546205929542>\n<#1207439560020197406>\n\n<#1110688647356895304> ➜ Quando você entrar aqui, a maioria dos chats vai sumir, tirando as distrações\n\n<#1137041362768900139> ➜ Estude enquanto curte uma musiquinha relaxante\n\n<#1136470255473000480> ➜ Você só consegue permanecer nesse canal se ativar a câmera ou compartilhar a tela! **Essa sala te dá mais blanks**\n\n<#1126180695019102208> ➜ Entre aqui para criar uma sala fechada só pra você. Convide seus amigos usando o comando </room:1126183220124323841>',
      colour=0x33FF33
	) 

    emb13 = disnake.Embed(
      description=categs[6] + '\n> **Abriga todas as salas privadas criadas pelos usuários**. Você só pode acessar essa área caso se conecte a <#1126180695019102208> ou seja convidado por alguém.\n\n> :fire: Característica geral das salas privadas: **A recompensa aumenta em 0.01 <:blank:1124439750208655500>/min para cada usuário conectado, mas se algum usuário sair da sala, ela será destruída e todos os outros usuários saírão**.',
      colour=0xffffff
    )
    emb14 = disnake.Embed(
      description='**<:private_voice_channel:1216789279523471390> 🔒 ⋯ Sala privada comum**\n\n**<:private_voice_channel:1216789279523471390> 🎯 ⋯ Sala de foco** ➜ **Surge quando um usuário no modo de foco (Ativável em </modelist:1225212116202684508>) cria uma sala**. A sala de foco deixam automaticamente todos que entrarem no modo focado\n\n**<:private_voice_channel:1216789279523471390> 🗻 ⋯ Caverna pessoal** ➜ Aparece sempre que um usuário no modo caverna (Ativável em </modelist:1225212116202684508>) cria uma sala privada. De todo o servidor, ele só pode ver a própria sala e não pode convidar ninguém.\n\n**<:private_voice_channel:1216789279523471390> 💠 ⋯ Sala de guilda** ➜ Surge quando alguém que possui guilda cria uma sala privada. Todos os membros dessa guilda podem se conectar mesmo que não tenham sido convidados; Não é possível ter mais de 1 sala da mesma guilda',
      colour=0x33FF33
    )

    emb15 = disnake.Embed(
      description=categs[7] + '\n> **Chats e calls normais para descansar e se divertir. As calls daqui não dão recompensas nem contabilizam o tempo.**',
      colour=0xffffff
    )
    emb16 = disnake.Embed(
      description='<#1230696631645765736> ➜ Esse pequeno fórum abriga dezenas de chats, cada um com seu próprio jogo desafiador.\n\n<#1217987701790212189> ➜ Chat para xadrez/damas\n\n<#1162148926237986866>',
      colour=0x33FF33
    )
    
    emb17 = disnake.Embed(
      description=categs[8] + '\n> **Área especialmente dedicada a leitores e amantes de livros**',
      colour=0xffffff
    )
    emb18 = disnake.Embed(
      description='<#1197315654412419183> **+2.5** <:blank:1124439750208655500> ➜ Estoque de livros separados por categorias. Se você postar um livro que alguém tenha pedido, marque a pessoa na sua postagem e ganhe recompensas\n\n<#1197315979710046288> ➜ Se não está encontrando algum livro na biblioteca, peça nesse chat. O bot marcará seu pedido como pendente e, se alguém adicionar seu livro, marcará como atendido (Você será notificado)',
      colour=0x33FF33
    )
    
    emb19 = disnake.Embed(
      description=categs[9] + '\n> **Nossa grande área do conhecimento que abriga os artigos criados por usuários. Acompanhe assuntos do mais básico ao mais complexo e entenda como tudo se conecta**',
      colour=0xffffff
    )
    emb20 = disnake.Embed(
      description='<#1174127784189239377> :lock: **+1.0 ~ 10.0** <:blank:1124439750208655500> ➜ Atinja o nível <@&1132163320179339344> Para desbloquear esse chat. Nele, você pode criar rascunhos de artigos e escrever algum conteúdo para adicionar à blankpédia!\n\n<#1137504108497080420> ➜ Qualquer post da blankpédia que você reagir com o emoji :bookmark: fica salvo em seu marca-páginas. Entre nesse chat para voltar aos assuntos que estava lendo, sem se perder\n\n<#1145420622575456277>\n<#1137496076954370088>\n<#1137497049022074920>\n<#1137497287648628827>\n<#1137497303016542289>\n<#1137497593929277582>\n<#1137497316694171768>\n<#1137497605564276786>',
      colour=0x33FF33
    )

    emb21 = disnake.Embed(
      description=categs[10] + '\n> **Apenas usuários do modo caverna sabem o que acontece lá...**',
      colour=0xffffff
    )



    
    all_embeds = [[emb1, emb2], [emb3, emb4], [emb5, emb6], [emb7, emb8], [emb9, emb10], [emb11, emb12], [emb13, emb14], [emb15, emb16], [emb17, emb18], [emb19, emb20], [emb21]]

    all_chats = [getSv('cChats')]
				
    c = 0

    async def multichat(chat, chat_embeds, aindex):
      await chat.purge(limit=None)
		
      for i, embeds in enumerate(chat_embeds): 
        await chat.send(embeds=embeds)
        if i + 1 < len(chat_embeds): await chat.send('‎\n\n‎')

      clist = []
      i2 = 0
      rmessages = await chat.history(limit=None).flatten()
      rmessages = rmessages[::-1]
		
      for message in rmessages:
        try:
          if message.embeds:
            char = next(c for c in categs[i2] if c.isalpha())
            categs[i2] = categs[i2].replace(char, char.upper(), 1)


            clist.append(f'- **{categs[i2].replace("# ","")}**➜ https://discord.com/channels/1091742896098660372/{chat.id}/{message.id}\n')
            
            i2 += 1
			  
        except: print(error())
		
      with open('divider_down.png', 'rb') as file: div_down = disnake.File(file)
      await chat.send(file=div_down)	
      await chat.send("‎\n‎")

      with open('chats.jpg', 'rb') as file: chats = disnake.File(file)
    
      await chat.send(file=chats)

      await chat.send(''.join(clist))

    try: [asyncio.create_task(multichat(chat, all_embeds[u], u)) for u, chat in enumerate(all_chats)]
    except: print(error())
   


