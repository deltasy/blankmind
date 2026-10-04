# Minder Bot — Blank Mind

> **Aviso:** Este repositório é um arquivo histórico e não recebe mais atualizações.

Entre **2023 e 2024**, criei e gerenciei a **Blank Mind**, que cresceu até cerca de **2.000 membros** (1800+ ativos) e se tornou uma das comunidades de estudos brasileiras mais conhecidas no Discord na época. 

**Criei 3 bots:** Minder, Cronos e Corp. Cada bot tinha seus próprios comandos e funcionalidades temáticas
* **Minder**: Bot principal
* **Cronos**: Tracker de tempo 
* **Corp**: Gerenciador de guildas e sub-grupos

Desse trio, o **Minder** era o bot principal: um faz-tudo encarregado desde comandos utilitários, sistema de economia, gamificação e moderação pesada até sistemas específicos da comunidade, como pedidos de livros e a "blankpédia" (um sistema complexo de criação e registro de artigos).

## Código 100% espaguete

**Esse projeto foi minha primeira experiência real com programação.** Na prática, o código é um monolito fortemente acoplado, caótico e cheio de gambiarras que ignoram quase todas as boas práticas de engenharia de software.

Com a comunidade crescendo rápido, o tráfego era alto e constante. Ter centenas de usuários interagindo simultaneamente significava uma enxurrada de testes forçados em produção, em que qualquer bug novo era descoberto em minutos. Durante boa parte desse período, atuei basicamente como um **encanador de código**: passava dias seguidos programando sem parar, apagando incêndios, isolando erros no terminal e segurando as pontas para o servidor não cair.

Os maiores pesadelos técnicos que enfrentei foram:

* **Cache baseado em arquivos JSON:** Para aliviar chamadas ao banco de dados (MongoDB), usei arquivos JSON locais como camada de cache. Com múltiplos usuários disparando eventos assíncronos ao mesmo tempo, leituras e escritas concorrentes em disco atropelavam umas às outras, gerando *race conditions* severas e perda de dados importantes. Os usuários estudavam várias horas seguidas e podiam perder o registro de tudo de uma vez por causa de uma falha de concorrência.

* **Feature creep descontrolado:** Toda semana surgia uma ideia nova para a comunidade. Em vez de modularizar ou separar responsabilidades, fui empilhando funcionalidades dentro do mesmo bot até ele virar um sistema complexo demais para um projeto só.

* **Testabilidade zero:** Como a regra de negócio estava colada diretamente nos eventos da API do Discord, testar qualquer alteração exigia subir o bot inteiro e simular comandos manualmente. Consertar um bug num comando utilitário frequentemente quebrava algo na moderação.

Apesar da bagunça estrutural, foi esse ambiente de pressão real que me ensinou a ler *stack traces*, lidar com concorrência na marra e resolver problemas de verdade fora de tutoriais.

## O que eu faria diferente hoje

Olhando para trás com a bagagem que tenho hoje, mudaria muitas coisas, principalmente:

1. **Fim do cache em arquivos JSON:** Substituiria toda a gambiarra de I/O em arquivos locais por **Redis** para cache em memória com operações atômicas e controle de sessão/rate-limit, aliado a um banco de dados relacional (**PostgreSQL**) com transações ACID garantidas por um ORM bem tipado, evitando corrupção de dados em eventos simultâneos.

2. **Desacoplamento da API do Discord:** Separaria a camada de interação (os *cogs* e eventos do Discord) da lógica de domínio. Os comandos do bot apenas consumiriam serviços isolados, permitindo testar a regra de negócio sem depender de conexão com o Discord.

3. **Testes automatizados e CI/CD:** Implementaria testes unitários e de integração rodando em uma esteira automatizada (GitHub Actions) antes de qualquer deploy, eliminando a necessidade de testar tudo no braço em produção.

4. **Containers e observabilidade:** Trocaria o deploy manual por containers **Docker** com logs estruturados, facilitando o rastreamento de exceções sem precisar caçar prints perdidos no console.

*(Com certeza eu mudaria muito mais coisa, mas essas seriam as alterações principais).*

## O último comando

Quando decidi encerrar o ciclo da Blank Mind em 2024, não quis deixar um servidor fantasma para trás. No último dia da comunidade, programei o bot para expulsar todos os membros do servidor de forma automatizada. O mesmo bot que construiu e manteve a operação de pé por mais de um ano também foi encarregado de destruir o servidor. Aqui restou a sombra do que um dia o projeto foi:
https://discord.com/invite/2CNsRp8qmu


## Tecnologias utilizadas na época
* **Python**
* **Disnake** (wrapper da API do Discord)
* **MongoDB / PyMongo** (persistência principal de dados)
* **JSON** (usado de forma imprudente como cache local em disco)
* **Plotly & NumPy** (geração de gráficos de uso e estatísticas dos membros)
* **Square Cloud** (hospedagem)

---

*Mantido no ar como registro histórico de onde comecei e de como um ambiente de produção caótico ensina mais do que qualquer curso.*