# Alberta GamePop Discord Bot

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

A bot to manage the suggestion, slaughtering, and voting of game jam themes.

## Development

This project is developed using Nix, and formatted with Ruff. Run `nix develop` and you're off to the races.

## Non-Nix Development

First off, lame. Second off, if this doesn't work for you, it's not my fault.

This bot runs on Python 3.11+ and is managed with Poetry. To get started:
1. [Install poetry][poetry-docs]
2. Create a `.env` file based on `.env.example`.
3. Install the project and run the bot:
   ```console
   $ poetry install
   ...
   $ poetry run python -m app
   ...
   ```
4. After you've made your changes, run the linter and formatter please and thanks:
   ```console
   $ poetry run ruff check
   $ poetry run ruff format
   ```

[discord-docs]: https://discord.com/developers/applications
[poetry-docs]: https://python-poetry.org/docs/#installing-with-pipx
[pipx]: https://pipx.pypa.io/

## Bot Goals

Thanks Matt, you made me install Nix. What's the point of this bot?

### Theme Suggestions

A few months out from the jam, we'd like to accumulate **three themes** from each prospective participant. Everyone in the server will get up to three suggestions of what they'd like the theme to be for the Jam. The bot records these themes, and stores them for the next step in the process.

### Theme Slaughter

About a month out from the event, we will host a **Theme Slaughter**. Blatantly stolen from [Ludum Dare](https://ldjam.com), the theme slaughter is an interactive way for all participants to weed out the good themes from the bad themes. Each participant wanting to help with the slaughter will be DM'd themes one at a time, in random order, reacting a thumbs up or a thumbs down on each theme. This will build out a preference ranking behind the scenes, and give us the fuel we need for the next step.

### Theme Voting

Around a week out from the event, we will put the top 6-8 themes up for Theme Voting. Participants can now vote on their favorite theme from the randomly shuffled list of mostly-liked themes, and get a sneak peek at some of the possible fates for the next 48 hours of their lives.

### Role Assignments

When all is said and done, participants want a way to show off that they went a whole weekend without sleep building a video game. Weird, but alright. By sending their jam submission link to the Bot, they can get a flashy role color, indicating that they submitted to the 202X Game Jam!

### Admin Functionalities

Of course, some additional functionality could be built into the bot as well. A few good ideas could be:

- **Hard-Coded Messages**: Having the Bot send the rules and announcements might look a bit more professional.
- **Moving Messages**: The ability for moderators to move a message from channel A to channel B might help keep channels focused on the topic at hand. No one asking dev questions in the art channel.
- **Coin Flip**: In the case of a tie for the final theme (god forbid), we may need a way for the Bot to flip a hypothetical coin to decide on the winning theme.
