import xml.etree.ElementTree as ET
import re, os,sys,argparse, json

LOGGER = {
  "nocat": [],
  "players": []
}

def getconfig(path): 
  CONFIG = {
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

  if (path is not None) :
    try:
      print("Loading Config from {}".format(path))
      with open(path, "r") as f:
        TOMERGE = ["definedorder", "replacements"]
        conf = json.load(f)
        for prop in TOMERGE:
          if prop in conf:
            CONFIG[prop] = conf[prop]
    except:
      q("Problem while reading Configfile from {}".format(path))
    
  CONFIG["definedorder"] = CONFIG["definedorder"].split(",")
  return CONFIG

def outputlog(what):
  if (what == 'nocat' and len(LOGGER["nocat"]) > 0):
    print("* Used Fallback Categories for {} Games".format(len(LOGGER["nocat"])))
    print("\n".join(LOGGER["nocat"]))
  elif (len(LOGGER["players"]) > 0): 
    print("* Player sanitization statistics")
    for item in LOGGER['players']:
      print("{}\tx\t{}".format(item["players"], item["count"]))

def q(msg):
  print("{} \nExit".format(msg))
  sys.exit(1)

def quest(msg):
  answer = input("{} (y/n)".format(msg))
  ANSWERS = ["y","n"]
  if (answer.lower() in ANSWERS):
    if answer == "y": 
      return True
    else:
      return False
  else:
    q("Invalid Answer")

if sys.version_info[0] < 3:
  q("Must be using Python 3")
  
if len(sys.argv) < 2:
  q("Please provide a path")

print("======================================================================")
print("Skyscraper Cache Sanitizer - 2020 FreaKzero (http://www.freakzero.com)")
print("======================================================================")
print("")

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path")
parser.add_argument("--mode", help="DRY (dryrun - no writing) RESTORE (restore backup files)")
parser.add_argument("--player", help="DEFAULT (1-4) or MAXPLAYER (4)")
parser.add_argument("--nocat", help="String for category which cant be resolved otherwise first tag will be used")
parser.add_argument("--config", help="JSON File configuration for replacements and category decider")
args = parser.parse_args()

BACKUP_EXT = ".orig"
DRY_RUN = False

# MAXPLAYER for only max player numbers
# Everything else => n-n (example: 1-12)
PLAYERFORMAT = "DEFAULT"

# None => use the first grabbed tag as category
# String => use the given String as category
NO_CAT_STRING = None

if args.config is not None:
  CONFIG = getconfig(args.config)
else:
  CONFIG = getconfig(None)

if args.mode is not None:
  MODES = ["DRY","RESTORE"]
  ARG = args.mode.upper()
  
  if ARG not in MODES:
    q("{} is not a valid mode (DRY or RESTORE)".format(args.mode))
  
  if ARG == "DRY":
    print("Dryrun Active, will not write delete or rename any files")
    DRY_RUN = True

if args.player is not None:
  MODES = ["MAXPLAYER", "DEFAULT"]
  ARG = args.mode.upper()
  if ARG not in MODES:
    q("{} is not a valid player parameter (MAXPLAYER or DEFAULT)".format(args.mode))
  else:
    PLAYERFORMAT = ARG

if args.nocat is not None:
    NO_CAT_STRING = args.nocat

def writeFile(file, root):
  if (DRY_RUN):
    print("[DRY] Write: {}".format(file))
  else:
    try:
      os.rename(file,file+BACKUP_EXT)
      f = open(file, "w")
      f.write(ET.tostring(root, encoding='unicode'))
      print("Writing {}".format(file))
      f.close() 
    except:
      print("Cant write File {}".format(file)) 

def findFile(dir_path, search):
  found = []
  for root, dirs, files in os.walk(dir_path): 
      for file in files:  
          if file == search:
            found.append(root+'/'+str(file))

  return found   

def findDict(lst, key, value):
  for i, dic in enumerate(lst):
      if dic[key] == value:
          return i
  return -1

def catsort(str):
  if (str in CONFIG["definedorder"]):
    return CONFIG["definedorder"][::-1].index(str)
  else:
    return -1

def replacetag(str):
  if str in CONFIG["replacements"]:    
    return CONFIG["replacements"][str]
  else:
    return str

def tagclean(child, root):
  c = child.text.split(', ')
  x = list(set(list(map(replacetag, c))))
  x.sort(reverse=True, key=catsort)
  tpl = "[T]: {}\n[P]: {}\n[O]: {}\n[W]: {} \n"

  for cat in x:
    if (cat in CONFIG["definedorder"]):
      return cat
    else:
      game = root.find("./resource[@id='{}'][@type='title']".format(child.attrib["id"])).text
      platform = root.find("./resource[@id='{}'][@type='platform']".format(child.attrib["id"])).text
      write = x[0]

      if (isinstance(NO_CAT_STRING, str)):
        write = NO_CAT_STRING

      LOGGER["nocat"].append(tpl.format(game, platform, child.text, write))
      return write

def playerclean(child):
  cleaned = re.sub(" ", "", re.sub("\s*\(.*.?\s*", "", child.text))
  plstr = cleaned

  if(PLAYERFORMAT == "MAXPLAYER"):
    match = re.match("\d-(\d{1,3})", plstr)
    if match is not None:
      plstr = match[1]
      
  if(cleaned.find('-') < 0 and len(cleaned) > 2):
    plstr = "1"
  
  found = findDict(LOGGER["players"], "players", plstr)

  if (found > -1):
    LOGGER["players"][found]["count"] += 1
  else:
    LOGGER["players"].append(dict({"players": plstr, "count": 1}))
  
  return plstr

def removebackups(backups):
  if (len(backups) > 0):
    if quest("Found Backups, delete them and reclean ?") == False:
      q("User decided to quit")

    for backdb in backups:
      print("Removing Backup: {}".format(backdb))
      if(DRY_RUN):
        print("[DRY] Remove {}".format(backdb))
      else:
        os.remove(backdb)

def main(databases, backups):
  if (len(backups) > 0):
    removebackups(backups)

  for db in databases:
    print("Reading/Cleaning {}".format(db))
    root = ET.parse(db).getroot()

    for child in root:  
      if (child.attrib["type"] == "tags"):
        child.text = tagclean(child, root)
      if (child.attrib["type"] == "players"):
        child.text = playerclean(child)
    
    writeFile(db, root)

def restore(databases, backups):
  
  for db in databases:
    print("Restoring Database: {}".format(db))
    os.remove(db)
    os.rename(db+BACKUP_EXT, db)

    if(DRY_RUN):
      print("[DRY] Restoring Database {}".format(db))
        
databases = findFile(args.path, "db.xml")
backups = findFile(args.path, "db.xml"+BACKUP_EXT)

if (len(databases) < 1):
  q("No Databases found on given Path")

if args.mode != None and args.mode.lower() == "restore":
  if len(backups) < 1:
    q("No Backups found on given Path")
  
  if quest("Really delete current databases and restore backups ?") == False:
    q("User decided to quit")

  restore(databases, backups)
else:
  if quest("Start Cleaning Process ?") == False:
    q("User Decided to quit")
  
  main(databases, backups)

outputlog('nocat')
outputlog('players')

