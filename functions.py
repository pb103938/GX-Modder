import os
import zipfile

def getFolder(category):

    if category == "KeyboardSounds":
        return "/keyboard"
    
    elif category == "BackgroundMusic":
        return "/music"
    
    elif category == "BrowserSounds":
        return "/sound"
    
    elif category == "Wallpapers":
        return "/wallpaper"
    
    else:
        return ""
    

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

                elif filename.endswith('.png') or filename.endswith('.webm'):

                    if "icon" in filename:
                        print("icon file:", filename)
                        file_folder = ''

                    else:
                        print("wallpaper file:", filename)
                        file_folder = 'wallpaper'

                elif filename.endswith('.txt') or filename.endswith('.json'):
                    print("license file:", filename)
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


def createManifest(form: dict):

    #data
    name = form.get('mod name')
    auth = form.get('mod author')
    desc = form.get('mod author')
    version = float(form.get('mod version'))

    #color schemes

    #light primary
    lph = form.get('lph')
    lps = form.get('lps')
    lpl = form.get('lpl')

    #light accent
    lah = form.get('lah')
    las = form.get('las')
    lal = form.get('lal')

    #dark primary
    dph = form.get('dph')
    dps = form.get('dps')
    dpl = form.get('dpl')

    #dark accent
    dah = form.get('dah')
    das = form.get('das')
    dal = form.get('dal')

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
    mani["mod"]["payload"]["theme"]["dark"]["gx_accent"]["h"] = int(dph)
    mani["mod"]["payload"]["theme"]["dark"]["gx_accent"]["s"] = int(dps)
    mani["mod"]["payload"]["theme"]["dark"]["gx_accent"]["l"] = int(dpl)

    #dark accent
    mani["mod"]["payload"]["theme"]["dark"]["gx_secondary_base"]["h"] = int(dah)
    mani["mod"]["payload"]["theme"]["dark"]["gx_secondary_base"]["s"] = int(das)
    mani["mod"]["payload"]["theme"]["dark"]["gx_secondary_base"]["l"] = int(dal)

    #light primary
    mani["mod"]["payload"]["theme"]["light"]["gx_accent"]["h"] = int(lph)
    mani["mod"]["payload"]["theme"]["light"]["gx_accent"]["l"] = int(lpl)
    mani["mod"]["payload"]["theme"]["light"]["gx_accent"]["s"] = int(lps)

    #light accent
    mani["mod"]["payload"]["theme"]["light"]["gx_secondary_base"]["h"] = int(lah)
    mani["mod"]["payload"]["theme"]["light"]["gx_secondary_base"]["s"] = int(las)
    mani["mod"]["payload"]["theme"]["light"]["gx_secondary_base"]["l"] = int(lal)

    mani["mod"]["schema_version"] = 1

    mani["version"] = str(version)

    return mani