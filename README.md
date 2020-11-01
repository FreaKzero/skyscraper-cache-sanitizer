# Skyscraper Cache Sanitizer

Script runs very well on Openretro scraped data, didnt try other scrapedata from skyscraper

- Sanitizes multiple Tagclouds like:
`action, horizontal, jumper, platform, scifi, shooter, sideways`
to 1 Category based on a user defined priority list to
`jumper` (or even other categories with replacement feature)

- Can fix typing errors and senseless categories

- Fixes Player Strings

- writes db.xml and creates a backup for every platform named db.xml.orig automatically
```
======================================================================
Skyscraper Cache Sanitizer - 2020 FreaKzero (http://www.freakzero.com)
======================================================================

usage: clean.py [-h] [--mode MODE] [--player PLAYER] [--nocat NOCAT]
                [--config CONFIG]
                path

positional arguments:
  path             Path

optional arguments:
  -h, --help       show this help message and exit
  --mode MODE      DRY (dryrun - no writing) RESTORE (restore backup files)
  --player PLAYER  DEFAULT (1-4) or MAXPLAYER (4)
  --nocat NOCAT    String for category which cant be resolved otherwise first
                   tag will be used
  --config CONFIG  JSON File configuration for replacements and category
                   decider
```

Example config.json (default values here if no json is given)

```
{
    "replacements": {
    "fighting": "beatemup",
    "fighter": "beatemup",
    "fight": "beatemup",
    "beatempup": "beatemup",
    "car": "racing",
    "actionadventure": "adventure",
    "actionadvenure": "adventure",
    "jumper": "platform",
    "jumponthings": "platform",
    "wanderer": "rpg",
    "puzzlesolve": "puzzle",
    "blackjack": "cards",
  },
    "definedorder": "disney,educational,sports,shooter,rpg,puzzle,shootemup,racing,beatemup,cards,quiz,topdown,strategy,platform,adventure,reaction,arcade,simulation,action,maze,pinball,boardgame,movie,creativity"
  }
```
