from flask import Flask, request, jsonify, render_template_string, send_file, render_template, redirect
import requests
from werkzeug.utils import secure_filename
from randString import gen_rand_str as randStr
import os
import zipfile
import json
from functions import getFolder, createManifest, list_dir, config_list, combineLists, createZip
from time import sleep as wait

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

downLink = str(randStr(10))

TEST_FOLDER = f'mods/{downLink}'

mURL = "127.0.0.1:8080"

@app.route('/<modID>/submit-files', methods=['POST'])
def handle_form_submission(modID):

    # Process files
    uploaded_files = request.files
    for key in uploaded_files:

        file = uploaded_files[key]

        fileCat = file.name.split('_')[0]    
        folder = getFolder(fileCat)

        file.save(f'mods/{modID}{folder}/{file.filename}')
        print(f'file uploaded: mods/{modID}{folder}/{file.filename}')

    return jsonify(success=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        wait(0.2)
        print("form:", request.form)

        global mName
        mName = request.form.get('mod name')

        mani = createManifest(request.form)

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
        return render_template('index.html', modID=downLink)


@app.route("/terms")
def terms():
  return render_template('terms.html')

@app.route(f"/download-mod/{downLink}", methods=['GET', 'POST'])
def downloadFile():
  if request.method == "POST":
    zip_filename = f'mods/{downLink}/{mName.replace(" ", "-")}-mod.zip'
      
    # Return the zip file for download
    response = send_file(zip_filename, as_attachment=True)
    
    return response

  else:
    return render_template(f"exampleDownload.html")

@app.route(f"/test-mod/{downLink}", methods=['GET', 'POST'])
def testMod():
  if request.method == "POST":

    music = list_dir(f"mods/{downLink}/music", "music")
    sound = list_dir(f"mods/{downLink}/sound", "sound")
    keyboard = list_dir(f"mods/{downLink}/keyboard", "keyboard")
    wallpaper = list_dir(f"mods/{downLink}/wallpaper", "wallpaper")

    filenames = combineLists(music, sound, keyboard, wallpaper, ["icon.png", "license.txt", "manifest.json"])

    createZip(filenames, mName, f"mods/{downLink}")

    return redirect(f"/download-mod/{downLink}")

  else:

    return render_template("exampleTest.html", key=downLink)
  
@app.route(f"/test-mod/<mod>", methods=['GET', 'POST'])
def testOtherMod(mod):
  if request.method == "POST":
    pass

  else:

    return render_template(f"exampleTest.html", key=mod)

@app.route('/close_tab', methods=['POST'])
def close_tab():
  if request.method == "POST":
    if request.headers.get("Referer") is None:
      zip_filename = f'{mName.replace(" ", "-")}-mod.zip'
      os.remove(zip_filename)
      os.remove(f"templates/{downLink}.html")
    print("Tab closed successfully!")
    return 'OK'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/privacy', methods=['GET', 'POST'])
def privacy_tab():
  if request.method == 'GET':
    return render_template("privacyPolicy.html")

@app.route('/create', methods=["GET"])
def createPage():
  return redirect('https://home.makeamod.com/create')

@app.route('/mods/<modID>/manifest.json', methods=["GET"])
def getManifest(modID):
   return send_file(f"mods/{modID}/manifest.json")

@app.route('/mods/<modID>/<folder>/<file>', methods=["GET"])
def getFiles(modID, folder, file):
   return send_file(f"mods/{modID}/{folder}/{file}")
  
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(TEST_FOLDER):
        os.makedirs(TEST_FOLDER)
    if not os.path.exists(f"{TEST_FOLDER}/manifest.json"):
        secure_filename(f"{TEST_FOLDER}/manifest.json")
    for folder in ['keyboard', 'music', 'sound', 'wallpaper']:
        folder_path = os.path.join(TEST_FOLDER, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    app.run(host='0.0.0.0', port=8080, debug=True)