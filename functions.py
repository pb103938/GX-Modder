import os
import zipfile
import re

HEX_COLOR = re.compile(r"^#?[0-9a-fA-F]{6}$")
NUMBER_REGEX = re.compile(r"^\d{1,5}(\.\d{1,5}){1,4}$")

WALLPAPER_FILE_TYPES = [".png", ".jpg", ".jpeg", ".webp", ".webm", ".apng"]

def getFolder(category):

    if category == "KeyboardSounds":
        return "keyboard"
    
    elif category == "BackgroundMusic":
        return "music"
    
    elif category == "BrowserSounds":
        return "sound"
    
    elif category == "Wallpapers":
        return "wallpaper"
    
    else:
        return ""
    
def cleanFiles(zipFile, modID):

    music = list_dir(f"mods/{modID}/music", "music")
    sound = list_dir(f"mods/{modID}/sound", "sound")
    keyboard = list_dir(f"mods/{modID}/keyboard", "keyboard")
    wallpaper = list_dir(f"mods/{modID}/wallpaper", "wallpaper")

    files = combineLists(music, sound, keyboard, wallpaper, ["icon.png", "license.txt", "manifest.json"])

    for file in files:
        if os.path.exists(f"mods/{modID}/{file}"):
            os.remove(f"mods/{modID}/{file}")

    try: os.rmdir(f"mods/{modID}/music") 
    except: pass

    try: os.rmdir(f"mods/{modID}/sound") 
    except: pass

    try: os.rmdir(f"mods/{modID}/keyboard") 
    except: pass

    try: os.rmdir(f"mods/{modID}/wallpaper") 
    except: pass

    if os.path.exists(zipFile):
        os.remove(zipFile)

    try: os.rmdir(f"mods/{modID}") 
    except: pass



def config_list(lst: list, category: str) -> dict:

    mani = {}

    if category == "sound":

        for i in lst:

            cat = ""

            if "click" in i:
                cat = "CLICK"

            elif "feature-switch-off" in i:
                cat = "FEATURE_SWITCH_OFF"

            elif "feature-switch-on" in i:
                cat = "FEATURE_SWITCH_ON"

            elif "hover" in i:
                cat = "HOVER"

            elif "important-click" in i:
                cat = "IMPORTANT_CLICK"

            elif "level-upgrade" in i:
                cat = "LEVEL_UPGRADE"

            elif "limiter-off" in i:
                cat = "LIMITER_OFF"

            elif "limiter-on" in i:
                cat = "LIMITER_ON"

            elif "switch" in i:
                cat = "SWITCH_TOGGLE"

            elif "close-tab" in i:
                cat = "TAB_CLOSE"

            elif "new-tab" in i:
                cat = "TAB_INSERT"

            elif "tab-slash" in i:
                cat = "TAB_SLASH"

            try:
                mani[cat]

            except:
                mani[cat] = []

            mani[cat].append(i)

        try:
            mani["HOVER_UP"] = mani["HOVER"]
        except:
            pass

    elif category == "keyboard":

        for i in lst:

            cat = ""

            if "backspace" in i:
                cat = "TYPING_BACKSPACE"

            elif "enter" in i:
                cat = "TYPING_ENTER"

            elif "letter" in i:
                cat = "TYPING_LETTER"

            elif "space" in i:
                cat = "TYPING_SPACE"

            try:
                mani[cat]

            except:
                mani[cat] = []

            mani[cat].append(i)

    elif category == "wallpaper":

        mani["light"] = {}
        mani["dark"] = {}
        for i in lst:

            cat = ""
            subcat = ""

            if "light-image" in i:
                cat = "light"
                subcat = "image"

            elif "dark-image" in i:
                cat = "dark"
                subcat = "image"

            elif "light-video" in i:
                cat = "light"
                subcat = "first_frame"

            elif "dark-video" in i:
                cat = "dark"
                subcat = "first_frame"

            try:
                mani[cat]

            except:
                mani[cat] = {}

            mani[cat][subcat] = i

        mani["dark"]["text_color"] = "#FFFFFF"
        mani["dark"]["text_shadow"] = "#757575"
        mani["light"]["text_color"] = "#FFFFFF"
        mani["light"]["text_shadow"] = "#0B000E"
        

    return mani


def createZip(filenames: list, mName: str, path):   
    if len(filenames) > 0:

        zip_filename = f'{mName.replace(" ", "-")}-mod.zip'
        print(zip_filename)

        with zipfile.ZipFile(f"{path}/{zip_filename}", 'w') as zip_file:

            for filename in filenames:

                if filename.endswith('.wav'):
                    file_folder = 'keyboard'
                    print("keyboard file:", filename)

                elif filename.endswith('.mp3'):

                    if "song" in filename:
                        file_folder = 'music'
                        print("music file:", filename)
                    else:
                        file_folder = 'sound'
                        print("sound file:", filename)

                elif any(filename.lower().endswith(fType) for fType in WALLPAPER_FILE_TYPES):

                    if "icon" in filename:
                        print("icon file:", filename)
                        file_folder = ''

                    else:
                        print("wallpaper file:", filename)
                        file_folder = 'wallpaper'

                elif filename.endswith('.txt') or filename.endswith('.json'):
                    print("license or manifest file:", filename)
                    file_folder = ''

                else:
                    print("deleting file:", filename, "at", os.path.join(path, filename))
                    os.remove(os.path.join(path, filename))

                print("adding to zip file at:", os.path.join(path, file_folder, os.path.basename(filename)))

                zip_file.write(os.path.join(path, file_folder, os.path.basename(filename)), filename)


def combineLists(*args):
    """
    Combine any number of lists into one list by merging their contents.

    :param args: Variable number of list arguments
    :return: A single list containing all elements from the input lists
    """
    combined_list = []
    for lst in args:
        # Ensure the argument is a list before extending
        if isinstance(lst, list):
            combined_list.extend(lst)
        else:
            print(f"Warning: Non-list argument encountered: {lst}")
    return combined_list


def list_dir(directory, category) -> list:
    """
    Get the names of all files in the specified directory.

    :param directory: Directory to list files from
    :return: List of file names in the directory
    """
    try:
        # List all entries in the directory
        entries = os.listdir(directory)

        files = []
        
        # Filter out the directories, keeping only files
        for entry in entries:

            obj = os.path.join(directory, entry)

            if os.path.isfile(obj):
                files.append(f"{category}/{entry}")
        
        print(files)
        return files
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []
    except PermissionError:
        print(f"Permission denied: {directory}")
        return []

def checkColor(color: str):
    if color and HEX_COLOR.match(color):
        return color if color.startswith("#") else f"#{color}"
    else:
        return False
    
def checkVersion(ver):

    if not ver or not NUMBER_REGEX.match(ver):
        return False

    parts = ver.split('.')
    if any(int(p) > 60000 for p in parts):
        return False
    
    return ver


def createManifest(form: dict):

    #data
    name = form.get('mod name')
    auth = form.get('mod author')
    desc = form.get('mod description')
    version = checkVersion(form.get('mod version'))

    if not name or not auth or not version or name.lower() == "none":
        return None

    #color schemes

    #light primary
    lp = checkColor(form.get('lp'))

    #light accent
    la = checkColor(form.get('la'))

    #dark primary
    dp = checkColor(form.get('dp'))

    #dark accent
    da = checkColor(form.get('da'))

    if not lp and la and dp and da:
        return None

    mani = {
        "name": str(name),
        "description": str(desc),
        "developer":
        {
          "name": str(auth)
        },
        "mod": 
        {
            "payload":
            {
                "browser_sounds":{},
                "keyboard_sounds":{},
                "theme":
                {
                    "dark":
                    {
                        "gx_accent":{},
                        "gx_secondary_base":{}
                    },
                    "light":
                    {
                        "gx_accent":{},
                        "gx_secondary_base":{}
                    }
                },
                "wallpaper":
                {
                    "dark":{},
                    "light":{}
                },
            }
        },
        "icons":
        {
          "512": "icon.png"
        },
        "manifest_version": 3
    }

    #mod info

    #license
    mani["mod"]["license"] = "license.txt"

    #color scheme

    #dark primary
    mani["mod"]["payload"]["theme"]["dark"]["gx_accent"] = str(dp)

    #dark accent
    mani["mod"]["payload"]["theme"]["dark"]["gx_secondary_base"] = str(da)

    #light primary
    mani["mod"]["payload"]["theme"]["light"]["gx_accent"] = str(lp)

    #light accent
    mani["mod"]["payload"]["theme"]["light"]["gx_secondary_base"] = str(la)

    mani["mod"]["schema_version"] = 1

    mani["version"] = str(version)

    return mani