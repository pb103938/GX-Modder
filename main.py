# Imports
from flask import Flask, request, jsonify, render_template_string, send_file, render_template, redirect, after_this_request
#import requests
from werkzeug.utils import secure_filename
from randString import gen_rand_str as randStr
import os
import zipfile
import json
from functions import getFolder, createManifest, list_dir, config_list, combineLists, createZip, cleanFiles, checkFolders
from time import sleep
from datetime import timedelta


# Webapp
app = Flask(__name__)

# App config
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024 # 25 MB

# Allowed file types
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "webp", "mp3", "wav", "txt", "webm", "apng"]

# Allowed categories
ALLOWED_CATEGORIES = ['keyboard', 'music', 'sound', 'wallpaper']

# The ModID and link for all mods
downLink = str(randStr(10))

# Folder containing all mod files
MOD_FOLDER = f'mods/{downLink}'

# Handles submitted files
@app.route('/<modID>/submit-files', methods=['POST'])
def handle_form_submission(modID):

    checkFolders(MOD_FOLDER, ALLOWED_CATEGORIES)

    # get metadata
    metadata = json.loads(request.form.get("metadata", "{}"))

    # Process files
    uploaded_files = request.files
    for key in uploaded_files:

        file = uploaded_files[key] #gets a file

        # gets the file's corresponding category
        fileCat = key.split("_")[0]
        if not fileCat or fileCat not in ["KeyboardSounds", "BackgroundMusic", "BrowserSounds", "Wallpapers", "ModInfo"]:
           continue

        folder = getFolder(fileCat)
        filename = secure_filename(file.filename)

        lenFiles = len(list_dir(f"mods/{downLink}/{folder}", folder))

        if lenFiles >= 10 and folder == "keyboard":
           continue
        
        elif lenFiles >= 5 and folder == "music":
           continue
        
        elif lenFiles >= 15 and folder == "sound":
           continue
        
        elif lenFiles >= 4 and folder == "wallpaper":
           continue
           

        # ensures proper file type
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
           continue
        
        # saves file
        save_path = os.path.join("mods", str(modID), folder, filename)
        print(f"\n\n save path: {str(save_path)} \n\n")
        file.save(save_path)

        print(f'file uploaded: mods/{modID}{folder}/{filename}')

    return jsonify(success=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    checkFolders(MOD_FOLDER, ALLOWED_CATEGORIES)

    if request.method == 'POST':

        print("form:", request.form)

        mName = request.form.get('mod name')

        print("\n\n\n\n     form is:", request.form, "\n\n\n\n")

        mani = createManifest(request.form)

        if mani == None:
           return 400

        # Fetch file lists from directories
        music = list_dir(f"mods/{downLink}/music", "music")
        sound = list_dir(f"mods/{downLink}/sound", "sound")
        keyboard = list_dir(f"mods/{downLink}/keyboard", "keyboard")
        wallpaper = list_dir(f"mods/{downLink}/wallpaper", "wallpaper")

        filenames = combineLists(music, sound, keyboard, wallpaper, ["icon.png", "license.txt", "manifest.json"])
        print(filenames)

        # Update manifest with file data
        if music:
            mani["mod"]["payload"]["background_music"] = music

        if sound:
            mani["mod"]["payload"]["browser_sounds"] = config_list(sound, "sound")

        if keyboard:
            mani["mod"]["payload"]["keyboard_sounds"] = config_list(keyboard, "keyboard")

        if wallpaper:
            mani["mod"]["payload"]["wallpaper"] = config_list(wallpaper, "wallpaper")

        # Write the manifest to a file
        with open(f"mods/{downLink}/manifest.json", "w") as m:
            m.write(str(mani).replace("'", "\""))
            m.flush()  # Ensure data is written to disk
        # The file is automatically closed at the end of the 'with' block

        if request.form.get('action') == "Test Mod":
           return redirect(f"/test-mod/{downLink}")

        # Create the zip file after all operations are completed
        createZip(filenames, mName, f"mods/{downLink}")

        return redirect(f"/download-mod/{downLink}")
    
    else:

        try:
            return render_template('index.html', modID=downLink)
        except:
            return page_not_found("")


@app.route("/terms")
def terms():
  try:
    return render_template('terms.html')
  except:
    return page_not_found(""), 404
 
@app.route(f"/download-mod/<mod>", methods=['GET', 'POST'])
def downloadFileOther(mod):
  if request.method == "POST":

    try:

        with open(f"mods/{mod}/manifest.json", "r") as file:
            data = json.load(file)

        name = str(data["name"])

    except:
       return page_not_found("")

    zip_filename = f'mods/{mod}/{name.replace(" ", "-")}-mod.zip'
      
    @after_this_request
    def cleanup(response):
        cleanFiles(zip_filename, downLink)
        return response
    
    try:
        return send_file(zip_filename, as_attachment=True)
    except:
        return page_not_found("")

  else:
    try:
        return render_template(f"exampleDownload.html")
    except:
      return page_not_found("")

 
@app.route(f"/test-mod/<mod>", methods=['GET', 'POST'])
def testOtherMod(mod):
  
  music = list_dir(f"mods/{mod}/music", "music")
  sound = list_dir(f"mods/{mod}/sound", "sound")
  keyboard = list_dir(f"mods/{mod}/keyboard", "keyboard")
  wallpaper = list_dir(f"mods/{mod}/wallpaper", "wallpaper")

  if request.method == "POST":
    
    filenames = combineLists(music, sound, keyboard, wallpaper, ["icon.png", "license.txt", "manifest.json"])

    try:

        with open(f"mods/{mod}/manifest.json", "r") as file:
            data = json.load(file)

        name = data["name"]

    except:
       return page_not_found("")

    createZip(filenames, name, f"mods/{mod}")

    return redirect(f"/download-mod/{mod}")

  else:

    letters = []

    for i in keyboard:
       if "letter" in i:
          letters.append(i)

    try: 
        return render_template(f"exampleTest.html", key=mod, items=letters, keybs=keyboard, music=music, sounds=sound)
    
    except:
       return page_not_found("")

@app.errorhandler(404)
def page_not_found(error):

    try:
        return render_template('404.html'), 404
    except:
       return "404 - I guess our 404 page broke", 404

@app.errorhandler(400)
def access_denied(error):
   
   try:
    return render_template('400.html'), 400
   except:
      return "400 - I guess our 400 page broke", 400

@app.route('/privacy', methods=['GET', 'POST'])
def privacy_tab():
  if request.method == 'GET':

    try:
        return render_template("privacyPolicy.html")
    
    except:
        return render_template('404.html'), 404

@app.route('/create', methods=["GET"])
def createPage():
  return redirect('https://home.makeamod.com/create')

@app.route('/mods/<modID>/manifest.json', methods=["GET"])
def getManifest(modID):
   
   try:
        return send_file(f"mods/{modID}/manifest.json")
   except:
        return render_template('404.html'), 404

@app.route('/mods/<modID>/icon.<fileType>', methods=["GET"])
def getIcon(modID, fileType):
   
   try:
    return send_file(f"mods/{modID}/icon.{fileType}")
   
   except:
    return render_template('404.html'), 404

@app.route('/mods/<modID>/license.txt', methods=["GET"])
def getLicense(modID):
   
   try:
    return send_file(f"mods/{modID}/license.txt")
   
   except:
    return render_template('404.html'), 404


@app.route('/mods/<modID>/<folder>/<file>', methods=["GET"])
def getFiles(modID, folder, file: str):
   
    ext = file.split('.')

    print(ext)

    if len(ext) < 2:
        return render_template('404.html'), 404
   
    if not str(ext[1]) in ALLOWED_EXTENSIONS:
        return render_template('400.html'), 400
   
    try:
        return send_file(f"mods/{modID}/{folder}/{file}")
   
    except:
        return render_template('404.html'), 404
#     
# @app.route("/how-to")
# def howToMain():
#     try:
#         return render_template("howTo.html")
#     
#     except:
#         return render_template('404.html'), 404
  
if __name__ == '__main__':
    if not os.path.exists("mods"):
       os.makedirs("mods")
    checkFolders(MOD_FOLDER, ALLOWED_CATEGORIES)
    app.run(host='0.0.0.0', port=8080, debug=True)
