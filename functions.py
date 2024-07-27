import os

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
            if "click" in i:
                try:
                    mani["CLICK"]

                except:
                    mani["CLICK"] = []

                mani["CLICK"].append(i)

            elif "feature-switch-off" in i:
                try:
                    mani["FEATURE_SWITCH_OFF"]

                except:
                    mani["FEATURE_SWITCH_OFF"] = []

                mani["FEATURE_SWITCH_OFF"].append(i)

            elif "feature-switch-on" in i:
                try:
                    mani["FEATURE_SWITCH_ON"]

                except:
                    mani["FEATURE_SWITCH_ON"] = []

                mani["FEATURE_SWITCH_ON"].append(i)

            elif "hover" in i:
                try:
                    mani["HOVER"]

                except:
                    mani["HOVER"] = []

                mani["HOVER"].append(i)

            elif "important-click" in i:
                try:
                    mani["IMPORTANT_CLICK"]

                except:
                    mani["IMPORTANT_CLICK"] = []

                mani["IMPORTANT_CLICK"].append(i)


        mani["HOVER_UP"] = mani["HOVER"]


def list_dir(directory, category) -> list:
    """
    Get the names of all files in the specified directory.

    :param directory: Directory to list files from
    :return: List of file names in the directory
    """
    try:
        # List all entries in the directory
        entries = os.listdir(directory)
        
        # Filter out the directories, keeping only files
        files = [os.path.join(category, entry) for entry in entries if os.path.isfile(os.path.join(directory, entry))]
        
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