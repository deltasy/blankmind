import disnake
from random import choices as rchoice, randint
from traceback import format_exc as error

from mongo import udb, readSet
from functions.page1 import tempMsg, specChannel, namedisplay


rarities = [
    ("common", 50),
    ("uncommon", 30),
    ("rare", 15),
    ("epic", 4),
    ("legendary", 1)
]

common = {
  53: ['https://i.imgur.com/oGZKltC.png', 'Rosalind Franklin (1920 ~ 1958)', """
➔ Descobriu o formato do DNA
➔ Trabalhou com a [cristalografia de raios X](https://pt.wikipedia.org/wiki/Cristalografia_de_raios_X)
"""],
  46: ['https://i.imgur.com/mBmGCWJ.png', 'Giotto di Bondone (1267 ~ 1337)', """
➔ Humanização das figuras religiosas em pinturas
➔ Influência no [renascimento](https://pt.wikipedia.org/wiki/Renascimento)
  """],
  45: ['https://i.imgur.com/ul1VQoG.png', 'Claude Monet (1840 ~ 1926)', """
➔ Pioneiro do [impressionismo](https://brasilescola.uol.com.br/artes/impressionismo.htm)
➔ [Principais pinturas](https://www.pariscityvision.com/pt/giverny/obras-claude-monet)
"""],
  44: ['https://i.imgur.com/9yOOXB8.png', 'Pablo Picasso (1881 ~ 1973)', """
➔ Pioneiro [cubista](https://www.todamateria.com.br/cubismo/)
➔ [Principais pinturas](https://www.wikiart.org/pt/pablo-picasso/)
  """],
  42: ['https://i.imgur.com/UDkxbHq.png', 'Machado de Assis (1839 ~ 1908)', """
➔ Fundou a [Academia Brasileira de Letras](https://www.academia.org.br)
➔ [Principais obras](https://www.culturagenial.com/obras-de-machado-de-assis/)
  """],
  41: ['https://i.imgur.com/5aaQdK5.png', 'Jane Austen (1775 ~ 1817)', """
➔ Publicou várias obras anonimamente
➔ [Principais obras](https://pt.wikipedia.org/wiki/Obras_de_Jane_Austen)
  """],
  40: ['https://i.imgur.com/LHPkAgT.png', 'Rosa Parks (1913 ~ 2005)', """
➔ Iniciou um [movimento](https://www.uol.com.br/ecoa/ultimas-noticias/2022/10/24/rosa-parks-a-mulher-que-fez-de-ato-de-desobediencia-uma-luta-por-direitos.htm) em Montgomery
➔ Levou os EUA a declarar a segregação racial em ônibus inconstitucional
  """],
  10: ['https://i.imgur.com/6cOH7PB.png', 'Constantino, o Grande (272 ~ 337)', """
➔ Deu fim às perseguições religiosas no império romano
➔ Convocou o [Primeiro Concílio de Nicéia](https://pt.wikipedia.org/wiki/Primeiro_Concílio_de_Niceia)
  """],
  33: ['https://i.imgur.com/pXMPROu.png', 'William Thomas Green Morton (1819 ~ 1868)', """
➔ Pioneiro do campo da anestesia
➔ Impacto significativo na medicina
  """],
  34: ['https://i.imgur.com/6qpuKxk.png', 'Benjamin Franklin (1706 ~ 1790)', """
➔ Experimentos com raios
➔ [Invenções notáveis](https://www.megacurioso.com.br/ciencia/125507-de-lentes-bifocais-a-fogao-9-invencoes-de-benjamin-franklin.htm)
  """],
}

uncommon = {
  63: ['https://i.imgur.com/hPW7ZU7.png', 'Thomas Hobbes (1588 ~ 1679)', '😡 Aura furiosa\n> Cega os inimigos com uma fúria insana. Ao passar do tempo, Hobbes também vai se enfurecendo', """
➔ Filósofo [contratualista](https://www.todamateria.com.br/contratualismo/)
➔ Defendeu que o homem é naturalmente ruim
➔ Escreveu "Leviatã"
"""],
  62: ['https://i.imgur.com/qre6d5v.png', 'Jean-Jacques Rousseau (1712 ~ 1778)', '😑 Pacifismo\n> Não ataca nem é atacado', """
➔ Filósofo [contratualista](https://www.todamateria.com.br/contratualismo/)
➔ Defendeu que o homem é naturalmente bom, mas a sociedade o corrompe
➔ Foi [exilado e perseguido](https://www.ebiografia.com/jean_jacques_rousseau/)
"""],
  59: ['https://i.imgur.com/4HuJyqY.png', 'Irmãos Wright (1867 ~ 1912)', '🪂 Levitação / 🤝 Elo\n> Podem evitar quedas e voar lentamente. Os irmãos pensam de forma compartilhada', """
➔ Criaram o primeiro [planador guiado](https://pt.wikipedia.org/wiki/Wright_Flyer)
➔ Fundaram a [Wright Company](https://pt.wikipedia.org/wiki/Wright_Company)
➔ Ainda há uma discussão sobre [quem realmente inventou o avião](https://canaltech.com.br/avioes/quem-inventou-o-aviao-213639/)
"""],
  35: ['https://i.imgur.com/dEHTKEb.png', 'Charles Babbage (1791 ~ 1871)', '⚙️ Tecnocinese', """
➔ Pioneiro da ciência da computação
➔ Desenvolveu a [máquina analítica](https://pt.wikipedia.org/wiki/Máquina_analítica)
➔ Iniciou o projeto da [máquina diferencial](https://pt.wikipedia.org/wiki/Máquina_diferencial)
  """],
  8: ['https://i.imgur.com/W91dOdp.png', 'Cristóvão Colombo (1451 ~ 1506)', '🗺️ Localização de rotas', """
➔ Primeiro contato europeu com as américas
➔ Impactou as mudanças geopolíticas
➔ Explorou rotas marítimas
  """],
  7: ['https://i.imgur.com/tgrVx3O.png', 'Nicolau Copérnico (1473 ~ 1543)', '☀️ Fotocinese simples\n> Pode cegar seus inimigos temporariamente', """
➔ Elaborou a teoria [heliocêntrica](https://pt.wikipedia.org/wiki/Heliocentrismo)
➔ Escreveu "De Revolutionibus Orbium Coelestium"
➔ Utilizou modelagens matemáticas para explicar o movimento dos planetas
  """],
  14: ['https://i.imgur.com/gTXKsT6.png', 'Louis Daguerre (1787 ~ 1851)', '📟 Análise\n➔ Pode "escanear" pontos fracos e vantagens inimigas', """
➔ Inventou a [daguerreotipia](https://pt.wikipedia.org/wiki/Daguerreótipo)
➔ Contribuiu para o surgimento da fotografia
➔ Pioneiro da captura de imagens
  """],
  20: ['https://i.imgur.com/9E6Nu2j.png', 'René Descartes (1596 ~ 1650)', '💭 Leitura pensamentos', """
➔ Pai da filosofia moderna
➔ Elaborou a [dúvida metódica](https://pt.wikipedia.org/wiki/Método_da_dúvida)
➔ Elaborou o [plano cartesiano](https://mundoeducacao.uol.com.br/matematica/plano-cartesiano.htm)
  """],
  22: ['https://i.imgur.com/zOExyyP.png', 'Vasco da Gama (1469 ~ 1524)', '🗺️ Localização de rotas', """
➔ Contribuiu para a colonização
➔ Impactou as mudanças geopolíticas
➔ Explorou rotas marítimas
  """],
  27: ['https://i.imgur.com/ZQhgqur.png', 'Mikhail Gorbachev (1931 ~ 2022)', '😑 Pacifismo\n> Não ataca nem é atacado', """
➔ Criou o conceito [Perestroika](https://pt.wikipedia.org/wiki/Perestroika)
➔ Criou o conceito [Glasnost](https://pt.wikipedia.org/wiki/Glasnost) 
➔ Impacto decisivo no fim da [guerra fria](https://pt.wikipedia.org/wiki/Guerra_Fria)
  """],
  36: ['https://i.imgur.com/xMEVp1D.png', 'Mahatma Gandhi (1869 ~ 1948)', '😑 Pacifismo\n> Não ataca nem é atacado', """
➔ Líder espiritual
➔ Liderou campanhas de [desobediência civil](https://educacao.uol.com.br/disciplinas/historia/independencia-da-india-nao-violencia-e-desobediencia-civil-de-ghandi.htm)
➔ Liderou a [marcha do sal](https://pt.wikipedia.org/wiki/Marcha_do_Sal)
"""]
}

rare = {
  70: ['https://i.imgur.com/S43cWzH.png', 'Ludwig van Beethoven (1770 ~ 1827)', '🔊 Pulsos sonoros\n> Pode usar para se ecolocalizar ou incapacitar inimigos temporariamente', """
➔ Criou [composições atemporais](https://pt.wikipedia.org/wiki/Lista_das_composições_de_Ludwig_van_Beethoven)
➔ Foi gradativamente ficando [surdo](https://www.nationalgeographicbrasil.com/historia/2023/08/como-beethoven-ficou-surdo-a-verdade-por-tras-da-surdez-do-compositor)
➔ Expandiu as sinfonias
"""],
  64: ['https://i.imgur.com/GEC6B8g.png', 'Steve Jobs (1955 ~ 2011)', '📱 Armazenagem\n> Pode guardar qualquer objeto dentro de seu celular e pegá-lo depois', """
➔ Co-fundou a [Apple](https://pt.wikipedia.org/wiki/Apple)
➔ Criou o [Iphone](https://pt.wikipedia.org/wiki/IPhone)
➔ Revolucionou a ideia de "celular"
"""],
  58: ['https://i.imgur.com/DG97HHD.png', 'Santos Dumont (1873 ~ 1932)', '✈️ Voo\n> Pode voar para fugir ou ganha impulso em seus ataques', """
➔ Inventou o primeiro avião (independente)
➔ Criou o avião [14-bis](https://pt.wikipedia.org/wiki/14-bis)
➔ Inventou o primeiro [dirigível](https://pt.wikipedia.org/wiki/Santos-Dumont_Nº_6)
"""],
  57: ['https://i.imgur.com/j6p7IE4.png', 'Aristóteles (384 a.C. ~ 322 a.C.)', '👻 Espectrovisão\n> Aristóteles pode ver a essência dos inimigos, causando dano a eles caso ataque essa forma metafísica"', """
➔ Discípulo de Platão
➔ Escreveu "Ética a Nicômaco"
➔ Debateu sobre a lógica, ética, metafísica, etc.
"""],
  55: ['https://i.imgur.com/Of6ENGm.png', 'Mao Tsé-Tung (1893 ~ 1976)', '👥 Unidade\n> Todos os seus seguidores agem em perfeita sincronia em qualquer situação', """
➔ Adepto ao comunismo
➔ Liderou a [Revolução Chinesa](https://www.historiadomundo.com.br/idade-contemporanea/revolucao-chinesa.htm)
➔ Criou o [Maoismo](https://pt.wikipedia.org/wiki/Maoismo)
"""],
  39: ['https://i.imgur.com/Ta5hHGJ.png', 'São Tomás de Aquino (1225 ~ 1274)', '🧠 ✨ Previsão\n> Deus lhe mostra fragmentos do futuro', """
➔ Fez uma síntese da filosofia aristotélica e da teologia cristã
➔ Articulou o conceito de [razão na fé](https://bibliotecacatolica.com.br/blog/formacao/fe-e-razao-em-santo-tomas/)
➔ Escreveu mais de [60 livros](https://ecclesiae.com.br/o-bem-tomas-de-aquino?author_id=78)
  """],
  37: ['https://i.imgur.com/upP60Zr.png', 'Marie Curie (1867 ~ 1934)', '☢️ Aura radioativa\n> Emana radiação ionizante, mas sem ser afetada', """
➔ Descobriu os elementos [rádio](https://brasilescola.uol.com.br/quimica/elemento-radio.htm) e [polônio](https://crqsp.org.br/elemento-quimico-polonio/)
➔ Ajudou soldados com a [radiografia](https://pt.wikipedia.org/wiki/Marie_Curie#Primeira_Guerra_Mundial) na 1º Guerra Mundial
➔ Ganhou 2 [prêmios Nobel](https://impa.br/noticias/pioneira-na-ciencia-marie-curie-ganhou-dois-premios-nobel/)
  """],
  6: ['https://i.imgur.com/pbQMyfX.png', 'Louis Pasteur (1822 ~ 1895)', '🦠 Biocinese microscópica\n> Pode controlar pequenos microrganismos quando está concentrado', """
➔ Desenvolveu a [pasteurização](https://pt.wikipedia.org/wiki/Pasteurização)
➔ Adepto à [teoria dos germes](https://pt.wikipedia.org/wiki/Teoria_microbiana_das_doenças)
➔ Refutou a teoria da [abiogênese](https://www.todamateria.com.br/abiogenese-e-biogenese/)
  """],
  5: ['https://i.imgur.com/W0XEyAb.png', 'Galileu Galilei (1564 ~ 1642)', '☄️ Invocação de pequenos meteoritos', """
➔ Inventou o [termoscópio](https://pt.wikipedia.org/wiki/Termoscópio)
➔ Defendeu a teoria [heliocêntrica](https://mundoeducacao.uol.com.br/fisica/heliocentrismo.htm) e foi perseguido
➔ Aperfeiçoou o [telescópio](https://brasilescola.uol.com.br/historiag/a-invencao-telescopio-por-galileu-galilei.htm)
  """],
  9: ['https://i.imgur.com/ZIrqjBW.png', 'Antoine Lavoisier (1743 ~ 1794)', '➿ Transmutação\n> Pode transformar um elemento em outro, mas fica cansado aos poucos', """
➔ Formulou a [lei da conservação das massas](https://querobolsa.com.br/enem/quimica/lei-de-lavoisier-e-lei-de-proust)
➔ Estabeleceu uma nova percepção sobre o processo de combustão
➔ Sistematizou a [nomenclatura química](https://www.scielo.br/j/ss/a/6jhdG4gvPgBLXN3LBJwZhSh/)
  """],
  13: ['https://i.imgur.com/780YtaO.png', 'Alexander Graham Bell (1847 ~ 1922)', '💫 Telepatia', """
➔ Inventou o [telefone](https://www.todamateria.com.br/historia-do-telefone/)
➔ Inventou o [audiômetro](https://bndigital.bn.gov.br/artigos/historia-da-ciencia-graham-bell-cientista-inventor-e-fonoaudiologo-britanico/)
➔ Fundou a [National Geographic](https://www.nationalgeographic.com/travel/article/tweeting-place)
  """],
  16: ['https://i.imgur.com/zfDsF4p.png', 'Adam Smith (1723 ~ 1790)', '😶‍🌫️ Invisibilidade\n> Sua "mão invisível" agora é literal', """
➔ Pai da [economia moderna](https://livrariadorobertomotta.com.br/a-riqueza-das-nacoes)
➔ Elaborou a [teoria do Livre Mercado](https://investidorsardinha.r7.com/aprender/livre-mercado/)
➔ Elaborou o conceito de [Mão Invisível](https://pt.wikipedia.org/wiki/Mão_invisível)
"""],
  18: ['https://i.imgur.com/pn1kje0.png', 'Friedrich Nietzsche (1844 ~ 1900)', '🚫 Anulação de poderes\n> Nada importa enquanto ele está por perto, nem os poderes inimigos', """
➔ Propõe a ausência de sentido atrelada ao [niilismo](https://www.todamateria.com.br/niilismo/)
➔ Criticou a religião, moralidade, ciência, filosofia, etc.
➔ Escreveu "Além do bem e mal"
"""],
  21: ['https://i.imgur.com/ckMUDKt.png', 'John Kennedy (1917 ~ 1963)', '📜 Planejamento rápido', """
➔ 35º presidente dos Estados Unidos
➔ Discurso ["Ich bin ein Berliner"](https://pt.wikipedia.org/wiki/Ich_bin_ein_Berliner)
➔ Estabeleceu a meta de [enviar um homem à Lua](https://pt.wikipedia.org/wiki/John_F._Kennedy#Programa_espacial)
  """],
  23: ['https://i.imgur.com/83qAgAV.png', 'Gregor Mendel (1822 ~ 1884)', '🧬 Manipulação genética\n> Pode manipular os genes de organismos e induzir doenças após manter contato direto com o organismo por 10s', """
➔ Pai da genética
➔ Formulou as [leis de Mendel](https://www.todamateria.com.br/leis-de-mendel/)
➔ Mudou o rumo da biologia
  """],
  24: ['https://i.imgur.com/EYwnraO.png', 'Nicolau Maquiavel (1469 ~ 1527)', '👥 Controle de massas\n> Pode manipular aglomerações de pessoas', """
➔ Escreveu "O príncipe"
➔ Tentou unir o empirismo e o método indutivo
➔ Separou a política da ética e as desenvolveu
  """],
  25: ['https://i.imgur.com/1DB1fAe.png', 'Leonhard Euler (1707 ~ 1783)', '🟦 Projeção\n> Pode criar e manipular até 5 pequenas estruturas geométricas', """
➔ Desenvolveu a [fórmula de Euler](https://pt.wikipedia.org/wiki/Fórmula_de_Euler)
➔ Criou os [grafos eulerianos](https://pt.wikipedia.org/wiki/Caminho_euleriano)
➔ Foi o primeiro a tratar [seno](https://pt.wikipedia.org/wiki/Seno) e [cosseno](https://pt.wikipedia.org/wiki/Cosseno) como funções
  """],
  29: ['https://i.imgur.com/pREuTul.png', 'Agostinho de Hipona (354 ~ 430)', '👁️ Previsão direcionada\n> Pode prever ataques', """
➔ Escreveu "Confissões"
➔ Escreveu "A cidade de Deus"
➔ Aperfeiçoou doutrinas teológicas
  """],
  51: ['https://i.imgur.com/YCbdt8Z.png', 'Sigmund Freud (1856 ~ 1939)', '💫 Manipulação mental temporária', """
➔ Fundou a [psicanálise](https://pt.wikipedia.org/wiki/Psicanálise)
➔ Formulou os conceitos de [Id, Ego e Super ego](https://www.significados.com.br/diferenca-entre-ego-superego-e-id/)
➔ Impactou a cultura popular
  """],
  66: ['https://i.imgur.com/BrJULZ6.png', 'Stephen Hawking (1942 ~ 2018)', '🌀 Vórtice\n> Pode criar pequenos buracos negros, mas tem pouco controle sobre eles', """
➔ Elaborou o conceito de [Radiação Hawking](https://pt.wikipedia.org/wiki/Radiação_Hawking)
➔ Mudou a concepção mundial sobre [buracos negros](https://pt.wikipedia.org/wiki/Buraco_negro)
➔ Escreveu "A teoria de tudo: A origem e o destino do universo"
"""]
}

epic = {
  67: ['https://i.imgur.com/efLaNoo.png', 'Enéas Carneiro (1938 ~ 2007)', '💥 Golpes nucleares\n> A cada certo tempo, pode carregar seu ataque para desferir golpes com a potência de uma pequena bomba nuclear. Ele não é ferido, mas é jogado para trás', """
➔ Polímata e político brasileiro
➔ Defendia a posse de [armas nucleares](https://www.pensador.com/frase/MTUxNTk5OQ/)
➔ Mestre da oratória
"""],
  60: ['https://i.imgur.com/kHp8ME9.png', 'Irmãos Lumière (1862 ~ 1954) e (1864 ~ 1948)', '🎥 Abstração / 🤝 Elo\n> Podem "puxar" inimigos para dentro de filmes, com a condição de que eles também são puxados. Os irmãos pensam de forma compartilhada', """
➔ Patentearam o [cinematógrafo](https://pt.wikipedia.org/wiki/Cinematógrafo)
➔ Aperfeiçoaram as tecnologias de Thomas Edison
➔ Pais do cinema
"""],
  56: ['https://i.imgur.com/EqQMZYm.png', 'Napoleão Bonaparte (1769 ~ 1821)', '⚜️ Rumo vitorioso\n> Napoleão pode prever o caminho que dá a maior probabilidade de vitória em uma batalha', """
➔ Realizou o [Golpe do 18 de Brumário](https://www.todamateria.com.br/golpe-do-18-de-brumario/)
➔ [Guerras napoleônicas](https://www.todamateria.com.br/guerras-napoleonicas/)
➔ Influenciou o crescimento do Brasil indiretamente
"""],
  54: ['https://i.imgur.com/tSsOji9.png', 'Ada Lovelace (1815 ~ 1852)', '🧠🖥️ Processamento\n> Seu cérebro funciona como um grande algoritmo. É capaz de analisar milhares de possibilidades antes de agir', """
➔ Primeira programadora da história
➔ Pioneira das linguagens de programação
➔ Criou um programa para trabalhar com os [números de Bernoulli](https://pt.wikipedia.org/wiki/Números_de_Bernoulli)
"""],
  52: ['https://i.imgur.com/vp0bXeh.png', 'Thomas Edison (1847 ~ 1931)', ' ⚡ Eletrocinese\n> Emite raios de suas mãos\n\n💡 Iluminar\n➔ Emite luz por um curto momento, cegando inimigos', """
➔ Inventou a lâmpada elétrica incandescente
➔ Inventou o [fonógrafo](https://pt.wikipedia.org/wiki/Fonógrafo)
➔ Registrou milhares de patentes em seu nome
  """],
  48: ['https://i.imgur.com/I0BOPx7.png', 'Arquimedes (287 a.C. ~ 212 a.C.)', '🔥 Pirocinese\n> Pode emitir chamas de suas mãos a um alcance limitado\n\n🔨 Construção rápida\n➔ Arquimedes é capaz de construir perfeitamente equipamentos bélicos de pequeno ou médio porte', """
➔ Criou seu próprio [princípio](https://brasilescola.uol.com.br/fisica/principio-arquimedes.htm)
➔ Criou a [teoria das alavancas](https://mundoeducacao.uol.com.br/matematica/uso-das-proporcoes-na-teoria-alavancas.htm)
➔ Criou um [raio mortal](https://revistapesquisa.fapesp.br/o-raio-mortal-de-arquimedes/) que incendiava navios
  """],
  43: ['https://i.imgur.com/JlCGZ5a.png', 'Fernando Pessoa (1888 ~ 1935)', '🔄 Tri-poder: 🌲 Manipulação de árvores / 🛡️ Resistência / ⚙️ Tecnocinese\n> Pode alternar entre esses 3 poderes. Cada poder é relacionado a um heterônimo', """
➔ Criou várias personalidades distintas para suas obras
➔ **Na forma de Alberto Caeiro:** Mestre ignorante amante da natureza
➔ **Na forma de Ricardo Reis:** Estoico adepto ao classicismo
➔ **Na forma de Álvaro de Campos:** Visão modernista de acepção tecnológica
  """],
  3: ['https://i.imgur.com/WqRECxw.png', 'Nikola Tesla (1856 ~ 1943)', '⚡ 🔄 Eletrocinese espiral\n> Tesla pode manipular energia na forma de 2 orbes elétricos que rotacionam entre si', """
➔ Desenvolveu o motor de indução
➔ Desenvolveu o transformador de corrente alternada
➔ Criou a bobina de Tesla
  """],
  4: ['https://i.imgur.com/uGnlXLb.jpeg', 'Charles Darwin (1809 ~ 1882)', '🐗 Biocinese\n> Darwin pode manipular até 3 organismos de forma complexa', """
➔ Criou a teoria da evolução
➔ Criou o conceito de seleção natural
➔ Viajou a bordo do navio HMS Beagle
  """],
  12: ['https://i.imgur.com/6f1LGEh.png', 'George Washington (1732 ~ 1799)', '👥 Influência\n> Pode convencer inimigos mais fracos que ele\n\n⏫ Fortalecer aliados', """
➔ Líder da guerra revolucionária
➔ Símbolo nacional
➔ Primeiro presidente dos EUA
  """],
  17: ['https://i.imgur.com/aA21ou4.png', 'Platão (427 a.C. ~ 428 a.C.)', '🗣️ Lábia petulante\n> Quanto mais tempo conversar com o inimigo, maior será a chance de convencê-lo a tomar alguma ação', """
➔ Criou a teoria das ideias
➔ Criou o método socrático
➔ Fundou a Academia de Atenas
  """],
  19: ['https://i.imgur.com/OiQjX1u.png', 'Júlio César (100 a.C. ~ 44 a.C.)', '😱 Indução de medo\n> Inimigos machucados sentirão um medo inexplicável e errarão seus ataques', """
➔ Ditador vitalício
➔ Grandes conquistas militares
➔ Reformou o calendário romano
  """],
  26: ['https://i.imgur.com/Gc7oU4p.png', 'Voltaire (1694 ~ 1778)', '🛡️ Imunidade parcial à poderes\n> Voltaire tem a liberdade de negar alguns poderes!', """
➔ Líder do iluminismo
➔ Escritor satírico
➔ Defensor da liberdade de expressão
  """],
  28: ['https://i.imgur.com/bmJmGDl.png', 'Homero (928 a.C. ~ 898 a.C.)', '📓 Invocação de personagens estóricos\n> Pode, de forma limitada, invocar personagens fictícios para ajudá-lo', """
➔ Escreveu o poema "A Ilíada"
➔ Escreveu o poema "A Odisseia"
➔ Criou a tradição épica
  """],
  30: ['https://i.imgur.com/d3bDw8j.png', 'Karl Marx (1818 ~ 1883)', '🛂 Absorção parcial de poderes\n> Marx pode cobrar uma fração dos poderes dos inimigos como um tributo', """
➔ Autor do manifesto comunista
➔ Escreveu o livro "O capital"
➔ Criou a teoria do materialismo histórico
  """],
  47: ['https://i.imgur.com/gfdrwXd.png', 'Wim Hof (1959 ~ Vivo)', '❄️ Criocinese / 🛡️ resistência superior', """
➔ Possui uma resistência térmica sobrenatural
➔ Criador do método de respiração Wim Hof
➔ Realizou desafios insanos, como escalar o Everest de short e correr maratonas no deserto sem água
  """]
}

legendary = {
  69: ['https://i.imgur.com/NuU0Hwx.png', 'Erwin Schrödinger (1887 ~ 1961)', '🌗 Paradoxo\n> Seu poder não pode ser calculado. Ele representa a existência e não existência do conceito que ele escolher. Também se aplica a inimigos', """
➔ Criou a [equação de Schrodinger](https://pt.wikipedia.org/wiki/Equação_de_Schrödinger)
➔ Atuou no [princípio da incerteza](https://mundoeducacao.uol.com.br/quimica/principio-incerteza-heisenberg.htm)
➔ Consolidou a [superposição de ondas](https://www.espacotempo.com.br/a-superposicao-quantica-e-o-gato-de-schrodinger/)
"""],
  68: ['https://i.imgur.com/InGGw9V.png', 'Bruce lee (1940 ~ 1973)', '👊 Golpes sônicos\n> Todos os seus ataques possuem a velocidade do som', """
➔ Criador do [Jeet Kune do](https://pt.wikipedia.org/wiki/Jeet_kune_do)
➔ Usuário do [soco de uma polegada](https://pt.wikipedia.org/wiki/Soco_de_uma_polegada)
➔ Astro de Hollywood
"""],
  1: ["https://i.imgur.com/UoT0r8O.png", "Albert Einstein (1879 ~ 1955)", "🌌 Distorção espacial\n> Pode usar portais para dizimar inimigos ou teleportar-se", """
➔ Formulou as teorias da relatividade [restrita e geral](https://brasilescola.uol.com.br/fisica/teorias-da-relatividade.htm#Teoria+da+relatividade+restrita+e+teoria+da+relatividade+geral)
➔ Formulou a equação de equivalência entre massa e energia (E=mc²) 
➔ Explicou o [efeito fotoelétrico](https://www.wikiwand.com/pt/Efeito_fotoelétrico)
  """],
  2: ["https://i.imgur.com/YDM3eM3.png", "Leonardo Da Vinci (1452 ~ 1519)", "♾️ Adaptação perfeita", """
➔ Gênio polímata
➔ Pintou as obras "Mona Lisa" e "A Última Ceia"
➔ Criou [cadernos](https://blog.taccbook.com.br/cadernos-de-leonardo-da-vinci/) com anotações profundas sobre diversas áreas
  """],
  11: ['https://i.imgur.com/a1fSyda.png', 'Gengis Khan (1162 ~ 1227)', '🗺️ 🧭 Estratégia perfeita\n> Seus planos não possuem defeitos', """
➔ Fundou o [Império Mongol](https://pt.wikipedia.org/wiki/Império_Mongol)
➔ Mestre das táticas militares
➔ Detentor do maior império (em extensão territorial) da história
  """],
  15: ['https://i.imgur.com/eLYvWUe.png', 'Adolf Hitler (1889 ~ 1945)', '🧠 💫 Lavagem cerebral', """
➔ Criou o nazismo
➔ Perseguiu povos
➔ Causou a [2º Guerra Mundial](https://pt.wikipedia.org/wiki/Segunda_Guerra_Mundial)
  """],
  31: ['https://i.imgur.com/0yf8gVk.png', 'Alexandre, o Grande (356 a.C. ~ 323 a.C.)', '🛡️ ⚔️ Imunidade a dano físico', """
➔ Nunca perdeu uma única batalha
➔ Unificou culturas
➔ Fundou a cidade de [Alexandria](https://pt.wikipedia.org/wiki/Alexandria)
  """],
  32: ['https://i.imgur.com/jcEPx0A.png', 'William Shakespeare (1564 ~ 1616)', '😡 😭 😱 😀 Indução emotiva\n> Controla as emoções dos inimigos, deixando-os confusos e com pouca assertividade', """
➔ Escreveu [39 peças de teatro](https://pt.wikipedia.org/wiki/Peças_de_Shakespeare)
➔ Escreveu uma coleção de [154 sonetos](https://shakespearebrasileiro.org/sonetos/)
➔ Aprimorou o [vocabulário inglês](https://ritmoidiomas.com.br/2017/05/31/palavras-ingles-shakespeare.html)
  """],
  38: ['https://i.imgur.com/34Dyiel.png', 'Quéops (**?**)', '⚰️ Imortalidade\n> É uma múmia ambulante incapaz de morrer', """
➔ Construiu a [Grande Pirâmide de Gisé](https://www.historiadomundo.com.br/egipcia/a-grande-piramide-de-gize.htm)
➔ Articulou monumentos complexos
➔ Deixou um grande legado cultural
  """],
  49: ['https://i.imgur.com/mgjmTqi.png', 'Diógenes (404/412 a.C. ~ 323 a.C.)', '💥 🚫 Destruição de poderes\n> Ele não liga se o inimigo é poderoso ou não. Seus poderes logo sumirão', """
➔ Recusou a [oferta](https://www.acropole.org.br/simbolismo/anedota-filosofica-diogenes-e-alexandre-o-grande/) de Alexandre, o Grande
➔ Rejeitou as normas sociais
➔ Representante da filosofia [cínica](https://www.todamateria.com.br/cinismo/)
  """],
  50: ['https://i.imgur.com/PpWyIJe.png', 'Isaac Newton (1642 ~ 1727)', '🔘  Gravitocinese\n> Pode modificar a gravidade de uma certa região para qualquer vetor', """
➔ Formulou as [leis do movimento](https://brasilescola.uol.com.br/fisica/leis-newton.htm)
➔ Formulou a lei da [gravitação universal](https://brasilescola.uol.com.br/fisica/gravitacao-universal.htm)
➔ Inventou o cálculo [integral](https://pt.wikipedia.org/wiki/Cálculo_infinitesimal)
  """],
  61: ['https://i.imgur.com/payFGFj.png', 'John Locke (1632 ~ 1704)', '💨 Esquecimento\n> Locke reverte a mente do inimigo ao seu estado original: sem memórias', """
➔ Filósofo [contratualista](https://www.todamateria.com.br/contratualismo/)
➔ Elaborou o [empirismo crítico](https://brasilescola.uol.com.br/filosofia/o-empirismo-critico-john-locke.htm)
➔ Reinterpretou a [Tábula Rasa](https://pt.wikipedia.org/wiki/Tábula_rasa)
"""],
  65: ['https://i.imgur.com/4Aehrqi.png', 'George Orwell (1903 ~ 1950)', '👀 Onipresença parcial\n> Assim como o [grande irmão](https://pt.wikipedia.org/wiki/Grande_Irmão), Orwell pode estar em qualquer lugar em algumas situações', """
➔ Escreveu "1984"
➔ Escreveu "A revolução dos bichos"
➔ Pró-socialista antifacista
"""]
}

# Pegar apenas os card ids para deixar o codigo mais rapido
common_cids = [cid for cid in common.keys()]
uncommon_cids = [cid for cid in uncommon.keys()]
rare_cids = [cid for cid in rare.keys()]
epic_cids = [cid for cid in epic.keys()]
legendary_cids = [cid for cid in legendary.keys()]

def command(client):  
  @client.slash_command(name="cronocard")
  async def sthinkers(
    inter: disnake.ApplicationCommandInteraction,
    lista = 'normal'
  ): 
    if await specChannel(inter): return

  @sthinkers.sub_command(name="roll")
  async def stlist(
    inter: disnake.ApplicationCommandInteraction,
  ):
    """
    📦 (Custa 1.5 𝔅)┃Procure cards de pessoas influentes para colecionar!
    """
    #return inter.response.send_message("Comando ainda em ajustes! jaja da pra usar de novo")
    await newThinker(inter)


  @sthinkers.sub_command(name="list")
  async def stlist(
    inter: disnake.ApplicationCommandInteraction,
  ):
    """
    📦┃Veja sua coleção de cards
    """
    await thinkerList(inter)

async def thinkerList(inter, lack=None):
  uid = inter.author.id
  uname = inter.author.name
    
  readSet(uid, 'thinkers', {'cardpower': 0, 'cards': []})
  clist = udb.find_one({'uid': uid})['thinkers']['cards']
  
  l1 = ['- **' + legendary[card_id][1].split(' (')[0] + '**  |  ' + legendary[card_id][2].split("\n")[0] for card_id in legendary if card_id in clist]
  l2 = ['- **' + epic[card_id][1].split(' (')[0] + '**  |  ' + epic[card_id][2].split("\n")[0] for card_id in epic if card_id in clist]
  l3 = ['- **' + rare[card_id][1].split(' (')[0] + '**  |  ' + rare[card_id][2].split("\n")[0] for card_id in rare if card_id in clist]
  l4 = ['- **' + uncommon[card_id][1].split(' (')[0] + '**  |  ' + uncommon[card_id][2].split("\n")[0] for card_id in uncommon if card_id in clist]
  l5 = ['- **' + common[card_id][1].split(' (')[0] + '**' for card_id in common if card_id in clist]
    
  if lack != None:
    display = 'Cards totais'
    l1n = '\n'.join(['> ' + legendary[card_id][1].split(' (')[0] + '  |  :grey_question:' for card_id in legendary if card_id not in clist]) + '\n\n'
    l2n = '\n'.join(['> ' + epic[card_id][1].split(' (')[0] + '  |  :grey_question:' for card_id in epic if card_id not in clist]) + '\n\n'
    l3n = '\n'.join(['> ' + rare[card_id][1].split(' (')[0] + '  |  :grey_question:' for card_id in rare if card_id not in clist]) + '\n\n'
    l4n = '\n'.join(['> ' + uncommon[card_id][1].split(' (')[0] + '  |  :grey_question:' for card_id in uncommon if card_id not in clist]) + '\n\n'
    l5n = '\n'.join(['> ' + common[card_id][1].split(' (')[0] + '' for card_id in common if card_id not in clist]) + '\n\n'
  else:
    l1n, l2n, l3n, l4n, l5n = '\n', '\n', '\n', '\n', '\n'
    display = 'Cards possuídos'

  ld1 = len(l1)
  ld2 = len(l2)
  ld3 = len(l3)
  ld4 = len(l4)
  ld5 = len(l5)

  l1 = '\n'.join(l1)
  l2 = '\n'.join(l2)
  l3 = '\n'.join(l3)
  l4 = '\n'.join(l4)
  l5 = '\n'.join(l5)

  desc = f"<a:cronocard:1142933723097084014> **{display} ({len(clist)}/{len(legendary) + len(epic) + len(rare) + len(uncommon) + len(common)})**\n> As raridades são baseadas na força dos superpoderes de cada personagem\n\n<:L1:1142498467818782831> <:L2:1142498471434260610> <:L3:1142498473359442072> <:L4:1142498476974932009> <:L5:1142498480632365226> <:L6:1142498482716942357> <:L7:1142498485850083379> <:L8:1142498489780154419> **({ld1}/{len(legendary)})**\n{l1}\n{l1n}<:E1:1142498412391043076> <:E2:1142498416866377728> <:E3:1142498418573459538> <:E4:1142498422054731796> <:E5:1142498425288532109> **({ld2}/{len(epic)})**\n{l2}\n{l2n}<:R1:1142496422948786201> <:R2:1142496427025637376> <:R1:1142496422948786201> <:R3:1142496429005340773> **({ld3}/{len(rare)})**\n{l3}\n{l3n}<:I1:1142495469717684236> <:I2:1142495473031204964> <:I3:1142495475497435287> <:I4:1142495478886445086> <:I5:1142495482896191528> <:I6:1142495487044362270> <:I5:1142495482896191528> **({ld4}/{len(uncommon)})**\n{l4}\n{l4n}<:C1:1142494346696982650> <:C2:1142494350987755581> <:C3:1142494352971661363> <:C4:1142494357467955230> <:C3:1142494352971661363> **({ld5}/{len(common)})**\n{l5}\n{l5n}\n"
    
  try: imgprof = inter.author.avatar.url
  except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'

  embed = disnake.Embed(
    description=desc,
    colour=0xffffff
  )
  embed.set_author(
    name=f'{uname} - Cronocards',
    icon_url=imgprof
  )

  if lack == None: 
    button = disnake.ui.Button(label='👀', style=disnake.ButtonStyle.primary, custom_id=f"lack_cards")
    msend = await inter.response.send_message(embed=embed, components=[button])
  else:
    await inter.response.send_message(embed=embed, ephemeral=True)
    

displays = {'common': ["<:C1:1142494346696982650> <:C2:1142494350987755581> <:C3:1142494352971661363> <:C4:1142494357467955230> <:C3:1142494352971661363>", 0x90a4a8], 'uncommon': ["<:I1:1142495469717684236> <:I2:1142495473031204964> <:I3:1142495475497435287> <:I4:1142495478886445086> <:I5:1142495482896191528> <:I6:1142495487044362270> <:I5:1142495482896191528>", 0x37d177], 'rare': ["<:R1:1142496422948786201> <:R2:1142496427025637376> <:R1:1142496422948786201> <:R3:1142496429005340773>", 0x2245dc
], 'epic': ["<:E1:1142498412391043076> <:E2:1142498416866377728> <:E3:1142498418573459538> <:E4:1142498422054731796> <:E5:1142498425288532109>", 0xa020e7], 'legendary': ["<:L1:1142498467818782831> <:L2:1142498471434260610> <:L3:1142498473359442072> <:L4:1142498476974932009> <:L5:1142498480632365226> <:L6:1142498482716942357> <:L7:1142498485850083379> <:L8:1142498489780154419>", 0xf1de52]}

price = ['common', 'uncommon', 'rare', 'epic', 'legendary']
cpowers = [5, 10, 25, 50, 100]

async def newThinker(inter, mode='normal'):
  global displays, price

  if mode == 'edit':
    uid = int(inter.content.split(">")[0][2:])
    msg2 = inter

  else:
    uid = inter.author.id

  udata = udb.find_one({'uid': uid, 'blanks': {'$gte': 1.5}})

  if not udata: 
    embed = disnake.Embed(
        description="Blanks insuficientes. Sai daqui, pobre.",
        colour=0xed3325
      )
    try:
      await msg2.edit('', embed=embed)
      await msg2.clear_reactions()
      return await tempMsg(msg2, embed, [f'<@{uid}>'])
    except:
      return await inter.response.send_message("Blanks insuficientes. Sai daqui, pobre", ephemeral=True)

  readSet(uid, 'thinkers', {'cardpower': 0, 'cards': []})
  cardlist = udb.find_one({'uid': uid})['thinkers']['cards']

  rarity_choice = rchoice([rarity for rarity, _ in rarities], [percentage for _, percentage in rarities])
  rarity_list = globals()[rarity_choice[0]]
  rarname = [name for name, value in globals().items() if value is rarity_list][0]
  idkey = rchoice(globals()[f'{rarname}_cids'])[0]
  if idkey in cardlist: # Se o usuário já tiver esse card   
    embed = disnake.Embed(
      description=f'Que peninha! você não achou nenhum card\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n`♻️ Para tentar de novo` | **1.5 <:blank:1124439750208655500>**',
    )

    embed.set_thumbnail(url="attachment://thinker.png")

  else:    
    try:
      image, name, power, about = rarity_list[idkey]
      power = f'\n》**Superpoder:** {power}'
    except: # Se for uma carta comum (sem poder)
      image, name, about = rarity_list[idkey]
      power = ''
    """
    # Abrir a imagem interna diretamente da URL
    response = requests.get(image)
    imagem_bytes = BytesIO(response.content)
    try:
      thinker = Image.open(imagem_bytes)
    except: 
      print(f'erro -> {image}')

    # Abrir a imagem da borda
    border = Image.open(f"images/frames/{rarity_choice[0]}_frame.png")

    # Convert the overlay image to RGBA mode
    try:
      thinker = thinker.convert('RGBA')
      thinker = thinker.resize(border.size)
    except: 
        print(image)
        return inter.response.send_message("O comando deu erro, foi mal :(")

    # Overlay the image over base image
    thinker.paste(border, (0, 0), border)

    border.close()

    thinker_bytes = BytesIO()
    thinker.save(thinker_bytes, format="PNG")
    thinker_bytes.seek(0)
    """
    # Enviar a imagem combinada em um embed
    displays2 = displays[rarity_choice[0]]

    embed = disnake.Embed(
      description=f'{displays2[0]}\n**~ Card {idkey} ~**\n▬▬▬▬▬▬▬▬▬▬▬\n## {name}{power}\n{about}\n▬▬▬▬▬▬▬▬▬▬▬\n`♻️ Para um novo card` | **1.5 <:blank:1124439750208655500>**\n`💼 Para adicionar à coleção` | **{3 * (price.index(rarity_choice[0]) + 1)} <:blank:1124439750208655500>**',
      colour=displays2[1]
    )

    embed.set_thumbnail(url=image)

  udb.update_one({'uid': uid}, {'$inc': {'blanks': -1.5}})

  blanks = round(udata['blanks'] - 1.5, 1)

  try: await namedisplay(uid)
  except: print(error())
	
  if mode == 'edit': # inter é uma mensagem (Comando reagido)
    blanks = float(inter.content.split(' | <:no:1132703732543529000> **Gastou ')[1].split(' ')[0]) + 1.5
    try:
      await inter.edit(f'<@{uid}> | <:no:1132703732543529000> **Gastou {blanks} <:blank:1124439750208655500>**', embed=embed)
    except: 
      await inter.edit(f'<@{uid}> | <:no:1132703732543529000> **Gastou {blanks} <:blank:1124439750208655500>**', embed=embed)

  else: # inter é uma interação (Primeiro uso do comando)
    try:
      msg = await inter.response.send_message(f'{inter.author.mention} | <:no:1132703732543529000> **Gastou 1.5 <:blank:1124439750208655500>**', embed=embed)
    except: 
      await inter.response.send_message(f'{inter.author.mention} | <:no:1132703732543529000> **Gastou 1.5 <:blank:1124439750208655500>**', embed=embed)

    msg = await inter.original_response()
    await msg.add_reaction("♻️")
    await msg.add_reaction("💼")