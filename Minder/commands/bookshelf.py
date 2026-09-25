import disnake
from disnake.ext import commands as com
from json import load as jload, dump as jdump
from traceback import format_exc as error
import asyncio

from functions.page1 import specChannel, getSv, namedisplay, newBlank
from mongo import udb


async def shelfmessage(json, user, chat):
    udata = json[str(user.id)]

    categs1 = list(set(book[1] for book in udata["data"]))

    if not categs1: return

    categs2 = {categoria: [] for categoria in categs1}

    [[categs2[categ].append([book[0], book[3]]) for book in udata["data"] if book[1] == categ] for categ in categs2]

    desc, bookdisplays, bid = [], [], 0
    for categ, books in categs2.items():
       desc.append(f'# {categ}')
       for name, pages in books:
          bid += 1
          desc.append(f' - **`L{bid}` {name}** ({pages} págs.)')
          bookdisplays.append(f'L{bid} ➜ {name}')
       desc.append(' ')

    dropdown = disnake.ui.Select(
    placeholder='👀🔎 Explorar estante',
        options=[disnake.SelectOption(label=name, value=name) for name in bookdisplays],
        custom_id=f'shelf_{user.id}',
        min_values=1,
        max_values=1
    )
      
    view = disnake.ui.View()
    view.add_item(dropdown)

    embed = disnake.Embed(
       description='\n'.join(desc),
       colour=0x00F7FF
    )

    try: imgprof = user.avatar.url
    except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'

    embed.set_author(
      name=f'📚 Estante de {user.display_name.split("═")[0]}',
       icon_url=imgprof
	)

    embed_msg = await chat.send(embed=embed, view=view)
    return embed_msg


async def bookdropdown(msg, user):
    embed = msg.embeds[0]

    names = [' '.join(book.split(' ')[2:][:-2]).replace('**', '').replace('`', '').replace(' ', ' ➜  ', 1) for book in embed.description.split('\n') if '# ' not in book and book != '']

    dropdown = disnake.ui.Select(
    placeholder='👀🔎 Explorar estante',
        options=[disnake.SelectOption(label=name, value=name) for name in names],
        custom_id=f'shelf_{user.id}',
        min_values=1,
        max_values=1
    )
      
    view = disnake.ui.View()
    view.add_item(dropdown)

    return view
   

async def bookrew(user, mode='+'):
  uid = user.id

  rew = 1.5

  if mode == '-': rew = -rew

  udb.update_one({'uid': uid}, {'$inc': {'blanks': rew}})
	
  try: await namedisplay(uid)
  except: print(error())

class sendBook(disnake.ui.Modal):
    def __init__(self, modalname='Adicionar um livro a sua estante', name='', categ='', annot='', pages='', link='', valpos='', votes=''):
        self.valpos = valpos

        components = [
            disnake.ui.TextInput(
                label="Nome do livro",
                custom_id="nome",
                value=name,
                placeholder='❗',
                max_length=50
            ),

            'categ',

            'annot',
            disnake.ui.TextInput(
                label="Quantidade de páginas lidas",
                custom_id="paginas",
                placeholder='❗ Insira um número inteiro',
                value=pages,
                max_length=4,
            ),
            disnake.ui.TextInput(
                label="Link (Opcional)",
                custom_id="link",
                value=link,
                max_length=200,
                required=False
            ),
        ]
        if categ:
           components.remove('categ')

        else:
            components[1] = disnake.ui.TextInput(
                label="Categoria",
                custom_id="categ",
                value=categ,
                placeholder='❗ Crie ou use uma categoria já existente da sua estante',
                max_length=20
              )


        if annot:
            components[2] = disnake.ui.TextInput(
                label="Anotações sobre o livro",
                custom_id="annot",
                placeholder="❗ Ensine e relembre tudo que aprendeu",
                value=annot,
                style=disnake.TextInputStyle.paragraph,
                min_length=200,
                max_length=3200,
            )

        else:
            components[2] = disnake.ui.TextInput(
                label="Anotações sobre o livro",
                custom_id="annot",
                placeholder="❗ Ensine e relembre tudo que aprendeu",
                style=disnake.TextInputStyle.paragraph,
                min_length=200,
                max_length=3200,
            )
		
        
        super().__init__(title=modalname, components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        vars = []
        user = inter.author
        suid = str(user.id)
        cShelf = getSv('cShelf')

        for key, value in inter.text_values.items(): vars.append(value.capitalize())

        vars[1] = vars[1].upper()
         
        try: name, categ, annot, pages, link = vars
        except: name, annot, pages, link = vars

        try: pages = int(pages)
        except: return

        if 'https://' not in link: link = ''

        with open('jsons/bookshelf.json', 'r') as file: shelf = jload(file)

        valpos = self.valpos

        if suid in shelf.keys():
          past_msg = await cShelf.fetch_message(shelf[suid]["message"])

          if valpos != '': # Modo de edição
             shelf[suid]["data"][valpos] = [name, shelf[suid]["data"][valpos][1], annot, pages, link, shelf[suid]["data"][valpos][5]]

             respond = f'As informações do livro **{name}** foram alteradas com sucesso.'

          elif f'# {categ}' in past_msg.embeds[0].description: # Categoria já existente
             shelf[suid]["data"].append([name, categ, annot, pages, link, 0])

             respond = f'**Livro adicionado com sucesso**\n{newBlank([0, rew])}'

             asyncio.create_task(bookrew(user))

          await past_msg.delete()

          newmsg = await shelfmessage(shelf, user, cShelf)
          shelf[suid]["message"] = newmsg.id
             

        else: # Primeiro uso do comando
            vars.append(0) # Número de votos
            shelf[suid] = {"message": 0, "data": [vars]}

            newmsg = await shelfmessage(shelf, user, cShelf)

            shelf[suid]["message"] = newmsg.id
            
            respond = f'# :tada: Estante inaugurada!\n{newBlank([0, rew])}'

            newshelf = disnake.Embed(
               description=f'# :izakaya_lantern: :books: :izakaya_lantern: Nova estante\n <@{user.id}> acaba de inaugurar sua estante com o livro **"{name}"!**\n\n> https://discord.com/channels/1091742896098660372/1238934620163276861/{newmsg.id}',
               colour=0x00F7FF
            )

            asyncio.create_task(bookrew(user))

            await getSv('cChat').send(embed=newshelf)
            pinged = await cShelf.send(f'<@{user.id}>')
            await pinged.delete()

        with open('jsons/bookshelf.json', 'w') as file: jdump(shelf, file, indent=2)

        return await inter.response.send_message(respond, ephemeral=True)


def command(client):
  @client.slash_command(name="bookshelf")
  async def sblank(
    inter = disnake.ApplicationCommandInteraction
  ):
    """
    📖 +1.5 𝔅┃Adicione um livro a sua estante
    """

    await inter.response.send_modal(modal=sendBook())