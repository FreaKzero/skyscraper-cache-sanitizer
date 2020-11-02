# Skyscraper Cache Sanitizer

Script runs very well on Openretro scraped data (with default config), didnt try other scrapedata from skyscraper

- Sanitizes multiple Tagclouds like:
`action, horizontal, jumper, platform, scifi, shooter, sideways`
to 1 Category based on a user defined priority list to
`jumper` (or even other categories with replacement feature)

- Can fix typing errors and senseless categories

- Fixes Player Strings

- writes db.xml and creates a backup for every platform named db.xml.orig automatically

- "Dry Run" to check the sanitized data is possible and logs out errors/problems as also sanitizion statistics for players
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

Example using:

```
python3 clean.py ./test 
======================================================================
Skyscraper Cache Sanitizer - 2020 FreaKzero (http://www.freakzero.com)
======================================================================

Start Cleaning Process ? (y/n)y
Reading/Cleaning ./test/cache/gba/db.xml
Writing ./test/cache/gba/db.xml
Reading/Cleaning ./test/cache/megadrive/db.xml
Writing ./test/cache/megadrive/db.xml
Reading/Cleaning ./test/cache/nes/db.xml
Writing ./test/cache/nes/db.xml
Reading/Cleaning ./test/cache/snes/db.xml
Writing ./test/cache/snes/db.xml
* Used Fallback Categories for 5 Games
[T]: Arcade Classics
[P]: Mega Drive
[O]: centipede, compilation, missilecommand, multigame, multiviev, ultrapong
[W]: multiviev 

[T]: Caesars Palace
[P]: Mega Drive
[O]: casiono, dice, gamble, rouletter, slotmachine
[W]: gamble 

[T]: Fun 'n Games
[P]: Mega Drive
[O]: multitype
[W]: multitype 

[T]: Soul Blade
[P]: Mega Drive
[O]: unlicensed
[W]: unlicensed 

[T]: Action 52
[P]: Nintendo
[O]: collection, games, multiangle, multitype, unlicensed
[W]: collection 

* Player sanitization statistics
1       x       1121
1-2     x       840
1-4     x       96
1-9     x       1
1-6     x       8
1-3     x       15
1-8     x       28
1-10    x       2
1-5     x       6
1-12    x       2
1-16    x       2
🐙  ~/openretro-skyscraper-sanitizer (master) 
```
