# Minder Bot — Blank Mind

<p align="center">
  <a href="README-pt.md">🇧🇷 Read this in Portuguese</a>
</p>
<p align="center">
  <em>Kept online as a historical record of where I started and how a chaotic production environment teaches more than any course.</em>
</p>


> **Notice:** This repository is a historical archive and is no longer maintained.

Between **2023 and 2024**, I founded and managed **Blank Mind**, which grew to approximately **2,000 members** (1,800+ active) and became one of the most prominent Brazilian study communities on Discord at the time.

**I built 3 bots:** Minder, Cronos, and Corp. Each bot had its own commands and thematic features:
* **Minder**: Core bot
* **Cronos**: Time tracker
* **Corp**: Guild and sub-group manager

Of this trio, **Minder** was the flagship application: a highly versatile bot handling everything from utility commands, economy systems, gamification, and heavy moderation to custom community features like book requests and the "Blankpedia" (a complex article creation and registry system).

## 100% Spaghetti Code

**This project was my first real-world programming experience.** In practice, the codebase is a tightly coupled monolith, chaotic, and filled with hacky workarounds that bypass almost every software engineering best practice.

With the community growing rapidly, traffic was high and constant. Having hundreds of users interacting simultaneously meant a flood of forced testing in production, where any new bug was discovered in minutes. During much of this period, I essentially operated as a **code plumber**: spending days coding non-stop, putting out production fires, isolating errors in the terminal, and holding everything together to keep the server from crashing.

The biggest technical nightmares I faced were:

* **JSON File-Based Caching:** To reduce database (MongoDB) calls, I used local JSON files as a caching layer. With multiple users triggering asynchronous events simultaneously, concurrent disk reads and writes collided, generating severe *race conditions* and data loss. Users who studied for several hours straight could lose all their logs at once due to a concurrency failure.
* **Uncontrolled Feature Creep:** Every week brought a new idea for the community. Instead of modularizing or separating responsibilities, I kept stacking features into the same bot until it became far too complex for a single project scope.
* **Zero Testability:** Because the business logic was tightly coupled directly to the Discord API events, testing any change required spinning up the entire bot and manually simulating commands. Fixing a bug in a utility command frequently broke something in the moderation module.

Despite the structural mess, this high-pressure real-world environment taught me how to read stack traces, handle concurrency the hard way, and solve actual engineering problems outside of isolated tutorials.

## What I Would Do Differently Today

Looking back with the architectural knowledge I have today, I would change almost everything, primarily:

1. **End the JSON Cache:** I would replace the messy local I/O operations with **Redis** for in-memory caching with atomic operations and session/rate-limit control. I would pair this with a relational database (**PostgreSQL**) featuring ACID transactions backed by a strictly typed ORM, preventing data corruption during simultaneous events.
2. **Decouple the Discord API:** I would separate the interaction layer (Discord cogs and events) from the domain logic. The bot's commands would merely consume isolated services, allowing the business logic to be unit-tested without relying on a Discord connection.
3. **Automated Testing and CI/CD:** I would implement unit and integration tests running on an automated pipeline (GitHub Actions) before any deployment, eliminating the need to manually test everything in production.
4. **Containers and Observability:** I would replace manual deployments with **Docker** containers featuring structured logging, making exception tracking straightforward without having to hunt for lost print statements in a console.

*(I would undoubtedly change much more, but these would be the architectural priorities).*

## The Final Command

When I decided to sunset the Blank Mind cycle in 2024, I didn't want to leave a ghost server behind. On the community's last day, I programmed the bot to automatically kick all members from the server. The same bot that built and sustained the operation for over a year was also tasked with tearing it down. What remains is a shadow of what the project once was:
https://discord.com/invite/2CNsRp8qmu

## Technologies Used at the Time
* **Python**
* **Disnake** (Discord API wrapper)
* **MongoDB / PyMongo** (Primary data persistence)
* **JSON** (Recklessly used as a local disk cache)
* **Plotly & NumPy** (Generation of usage graphs and member statistics)
* **Square Cloud** (Hosting)
