from flask import Flask, request, render_template_string, send_file, render_template, redirect
import requests
from werkzeug.utils import secure_filename
from randString import gen_rand_str as randStr
import os
import zipfile

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

downLink = str(randStr(10))

TEST_FOLDER = f'mods/{downLink}'

mURL = "127.0.0.1:8080"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  
    if request.method == 'POST':
          print("form:", request.form)
          print("files:", request.files)
          # Get the uploaded files and save them to the local file system
          filenames = []
          for i in range(1, 29):
              file = request.files.get(f'file{i}')
              nameFiles = ["backspace.wav", "enter.wav", "letter_1.wav", "letter_2.wav", "letter_3.wav", "space.wav", "track_1.mp3", "track_2.mp3", "track_3.mp3", "track_4.mp3", "click.mp3", "close_tab.mp3", "feature_switch_off.mp3", "feature_switch_on.mp3", "hover.mp3", "important_click.mp3", "level_upgrade.mp3", "limiter_off.mp3", "limiter_on.mp3", "new_tab.mp3", "switch.mp3", "tab_slash.mp3", "dark.png", "light.png", "dark_video.webm", "light_video.webm", "icon_512.png", "license.txt"]
              filename = secure_filename(nameFiles[i - 1])
              if file:
                  if i <= 6:
                      file_folder = 'keyboard'
                  elif i <= 10:
                      file_folder = 'music'
                  elif i <= 22:
                      file_folder = 'sound'
                  elif i <= 26:
                      file_folder = 'wallpaper'
                  else:
                      file_folder = ''
                  file_path = os.path.join(TEST_FOLDER, file_folder, filename)
                  file.save(file_path)
                  filenames.append(file_path)
              if not file:
                  if filename.endswith('.wav'):
                    file_folder = 'keyboard'
                  elif filename.endswith('.mp3'):
                    traks=["track_1.mp3", "track_2.mp3", "track_3.mp3", "track_4.mp3"]
                    if any(name in filename for name in traks):
                      file_folder = 'music'
                    else:
                      file_folder = 'sound'
                  elif filename.endswith('.png') or filename.endswith('.webm'):
                    walls=["dark.png", "light.png", "dark_video.webm", "light_video.webm"]
                    if any(name in filename for name in walls):
                      file_folder = 'wallpaper'
                    else:
                      file_folder = ''
                  elif filename.endswith('.txt'):
                    file_folder = ''
                  with open(f"{TEST_FOLDER}/{file_folder}/{nameFiles[i - 1]}", "w") as nFile:
                      print(nFile)
                      filename = secure_filename(nFile.name)
                      filenames.append(nFile.name)
                      nFile.close()
      
          with open(f"mods/{downLink}/manifest.json", "w") as m:
            m.write(str({"name": str(request.form.get('mod name')),
      "description": str(request.form.get('mod description')),
      "developer":
      {
          "name": str(request.form.get('mod author'))
      },
      "icons":
      {
          "512": "icon_512.png"
      },
      "manifest_version": 3,
      "mod":
      {
          "license": "license.txt",
          "payload":
          {
              "background_music":
              [
                  "music/track_1.mp3",
                  "music/track_2.mp3",
                  "music/track_3.mp3",
                  "music/track_4.mp3"
              ],
              "browser_sounds":
              {
                  "CLICK":
                  [
                      "sound/click.mp3"
                  ],
                  "FEATURE_SWITCH_OFF":
                  [
                      "sound/feature_switch_off.mp3"
                  ],
                  "FEATURE_SWITCH_ON":
                  [
                      "sound/feature_switch_on.mp3"
                  ],
                  "HOVER":
                  [
                      "sound/hover.mp3"
                  ],
                  "HOVER_UP":
                  [
                      "sound/hover.mp3"
                  ],
                  "IMPORTANT_CLICK":
                  [
                      "sound/important_click.mp3"
                  ],
                  "LEVEL_UPGRADE":
                  [
                      "sound/level_upgrade.mp3"
                  ],
                  "LIMITER_OFF":
                  [
                      "sound/limiter_off.mp3"
                  ],
                  "LIMITER_ON":
                  [
                      "sound/limiter_on.mp3"
                  ],
                  "SWITCH_TOGGLE":
                  [
                      "sound/switch.mp3"
                  ],
                  "TAB_CLOSE":
                  [
                      "sound/close_tab.mp3"
                  ],
                  "TAB_INSERT":
                  [
                      "sound/new_tab.mp3"
                  ],
                  "TAB_SLASH":
                  [
                      "sound/tab_slash.mp3"
                  ]
              },
              "keyboard_sounds":
              {
                  "TYPING_BACKSPACE":
                  [
                      "keyboard/backspace.wav"
                  ],
                  "TYPING_ENTER":
                  [
                      "keyboard/enter.wav"
                  ],
                  "TYPING_LETTER":
                  [
                      "keyboard/letter_1.wav",
                      "keyboard/letter_2.wav",
                      "keyboard/letter_3.wav"
                  ],
                  "TYPING_SPACE":
                  [
                      "keyboard/space.wav"
                  ]
              },
              "theme":
              {
                  "dark":
                  {
                      "gx_accent":
                      {
                          "h": int(request.form.get('dph')),
                          "s": int(request.form.get('dps')),
                          "l": int(request.form.get('dpl'))
                      },
                      "gx_secondary_base":
                      {
                          "h": int(request.form.get('dah')),
                          "s": int(request.form.get('das')),
                          "l": int(request.form.get('dal'))
                      }
                  },
                  "light":
                  {
                      "gx_accent":
                      {
                          "h": int(request.form.get('lph')),
                          "s": int(request.form.get('lps')),
                          "l": int(request.form.get('lpl'))
                      },
                      "gx_secondary_base":
                      {
                          "h": int(request.form.get('lah')),
                          "s": int(request.form.get('las')),
                          "l": int(request.form.get('lal'))
                      }
                  }
              },
              "wallpaper":
              {
                  "dark":
                  {   
                      "image": "wallpaper/dark.png",
                      "first_frame": "wallpaper/dark_video.webm",
                      "text_color": "#FFFFFF",
                      "text_shadow": "#757575"
                  },
                  "light":
                  {
                      "image": "wallpaper/light_video.webm",
                      "first_frame": "wallpaper/light.png",
                      "text_color": "#FFFFFF",
                      "text_shadow": "#0B000E"
                  }
              }
          },
          "schema_version": 1
      },
      "version": str(request.form.get('mod version'))
  }).replace(chr(39), chr(34)))
            filenames.append(m.name)
          m.close()

          if 'testButton' in request.form:
            if not os.path.exists(f"templates/{downLink}-test"):
              exdown = open("templates/exampleTest.html", "r")
              with open(f"templates/{downLink}-test.html", "w") as downpage:
                downpage.write(str(exdown.read()))
                exdown.close()
                downpage.close()
              return redirect(f"{mURL}/test-mod/{downLink}")
            else:
              return redirect(f"{mURL}/test-mod/{downLink}")
  
          # Create a zip file containing the uploaded files
          if filenames:
              global mName
              mName = str(request.form.get('mod name'))
              zip_filename = f'{mName.replace(" ", "-")}-mod.zip'
              with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                  for filename in filenames:
                      if filename.endswith('.wav'):
                          file_folder = 'keyboard'
                      elif filename.endswith('.mp3'):
                        traks=["track_1.mp3", "track_2.mp3", "track_3.mp3", "track_4.mp3"]
                        if any(name in filename for name in traks):
                          file_folder = 'music'
                        else:
                          file_folder = 'sound'
                      elif filename.endswith('.png') or filename.endswith('.webm'):
                        walls=["dark.png", "light.png", "dark_video.webm", "light_video.webm"]
                        if any(name in filename for name in walls):
                          file_folder = 'wallpaper'
                        else:
                          file_folder = ''
                      elif filename.endswith('.txt'):
                        file_folder = ''
                      else:
                          file_folder = os.path.basename(os.path.dirname(filename))
                      zip_file.write(filename, os.path.join(file_folder, os.path.basename(filename)))
                      
                      os.remove(filename)
            
          if not os.path.exists(f"templates/{downLink}"):
            exdown = open("templates/exampleDownload.html", "r")
            with open(f"templates/{downLink}.html", "w") as downpage:
              downpage.write(str(exdown.read()))
              exdown.close()
              downpage.close()
            return redirect(f"{mURL}/download-mod/{downLink}")
          else:
            return redirect(f"{mURL}/download-mod/{downLink}")
  
    else:
      return render_template('index.html')


@app.route('/new', methods=['GET', 'POST'])
def upload_new_file():
  
    if request.method == 'POST':
          print("form:", request.form)
          print("files:", request.files)
          # Get the uploaded files and save them to the local file system
          filenames = []
          for i in range(1, 29):
              file = request.files.get(f'file{i}')
              nameFiles = ["backspace.wav", "enter.wav", "letter_1.wav", "letter_2.wav", "letter_3.wav", "space.wav", "track_1.mp3", "track_2.mp3", "track_3.mp3", "track_4.mp3", "click.mp3", "close_tab.mp3", "feature_switch_off.mp3", "feature_switch_on.mp3", "hover.mp3", "important_click.mp3", "level_upgrade.mp3", "limiter_off.mp3", "limiter_on.mp3", "new_tab.mp3", "switch.mp3", "tab_slash.mp3", "dark.png", "light.png", "dark_video.webm", "light_video.webm", "icon_512.png", "license.txt"]
              filename = secure_filename(nameFiles[i - 1])
              if file:
                  if i <= 6:
                      file_folder = 'keyboard'
                  elif i <= 10:
                      file_folder = 'music'
                  elif i <= 22:
                      file_folder = 'sound'
                  elif i <= 26:
                      file_folder = 'wallpaper'
                  else:
                      file_folder = ''
                  file_path = os.path.join(TEST_FOLDER, file_folder, filename)
                  file.save(file_path)
                  filenames.append(file_path)
              if not file:
                  if filename.endswith('.wav'):
                    file_folder = 'keyboard'
                  elif filename.endswith('.mp3'):
                    traks=["track_1.mp3", "track_2.mp3", "track_3.mp3", "track_4.mp3"]
                    if any(name in filename for name in traks):
                      file_folder = 'music'
                    else:
                      file_folder = 'sound'
                  elif filename.endswith('.png') or filename.endswith('.webm'):
                    walls=["dark.png", "light.png", "dark_video.webm", "light_video.webm"]
                    if any(name in filename for name in walls):
                      file_folder = 'wallpaper'
                    else:
                      file_folder = ''
                  elif filename.endswith('.txt'):
                    file_folder = ''
                  with open(f"{TEST_FOLDER}/{file_folder}/{nameFiles[i - 1]}", "w") as nFile:
                      print(nFile)
                      filename = secure_filename(nFile.name)
                      filenames.append(nFile.name)
                      nFile.close()
      
          with open(f"mods/{downLink}/manifest.json", "w") as m:
            m.write(str({"name": str(request.form.get('mod name')),
      "description": str(request.form.get('mod description')),
      "developer":
      {
          "name": str(request.form.get('mod author'))
      },
      "icons":
      {
          "512": "icon_512.png"
      },
      "manifest_version": 3,
      "mod":
      {
          "license": "license.txt",
          "payload":
          {
              "background_music":
              [
                  "music/track_1.mp3",
                  "music/track_2.mp3",
                  "music/track_3.mp3",
                  "music/track_4.mp3"
              ],
              "browser_sounds":
              {
                  "CLICK":
                  [
                      "sound/click.mp3"
                  ],
                  "FEATURE_SWITCH_OFF":
                  [
                      "sound/feature_switch_off.mp3"
                  ],
                  "FEATURE_SWITCH_ON":
                  [
                      "sound/feature_switch_on.mp3"
                  ],
                  "HOVER":
                  [
                      "sound/hover.mp3"
                  ],
                  "HOVER_UP":
                  [
                      "sound/hover.mp3"
                  ],
                  "IMPORTANT_CLICK":
                  [
                      "sound/important_click.mp3"
                  ],
                  "LEVEL_UPGRADE":
                  [
                      "sound/level_upgrade.mp3"
                  ],
                  "LIMITER_OFF":
                  [
                      "sound/limiter_off.mp3"
                  ],
                  "LIMITER_ON":
                  [
                      "sound/limiter_on.mp3"
                  ],
                  "SWITCH_TOGGLE":
                  [
                      "sound/switch.mp3"
                  ],
                  "TAB_CLOSE":
                  [
                      "sound/close_tab.mp3"
                  ],
                  "TAB_INSERT":
                  [
                      "sound/new_tab.mp3"
                  ],
                  "TAB_SLASH":
                  [
                      "sound/tab_slash.mp3"
                  ]
              },
              "keyboard_sounds":
              {
                  "TYPING_BACKSPACE":
                  [
                      "keyboard/backspace.wav"
                  ],
                  "TYPING_ENTER":
                  [
                      "keyboard/enter.wav"
                  ],
                  "TYPING_LETTER":
                  [
                      "keyboard/letter_1.wav",
                      "keyboard/letter_2.wav",
                      "keyboard/letter_3.wav"
                  ],
                  "TYPING_SPACE":
                  [
                      "keyboard/space.wav"
                  ]
              },
              "theme":
              {
                  "dark":
                  {
                      "gx_accent":
                      {
                          "h": int(request.form.get('dph')),
                          "s": int(request.form.get('dps')),
                          "l": int(request.form.get('dpl'))
                      },
                      "gx_secondary_base":
                      {
                          "h": int(request.form.get('dah')),
                          "s": int(request.form.get('das')),
                          "l": int(request.form.get('dal'))
                      }
                  },
                  "light":
                  {
                      "gx_accent":
                      {
                          "h": int(request.form.get('lph')),
                          "s": int(request.form.get('lps')),
                          "l": int(request.form.get('lpl'))
                      },
                      "gx_secondary_base":
                      {
                          "h": int(request.form.get('lah')),
                          "s": int(request.form.get('las')),
                          "l": int(request.form.get('lal'))
                      }
                  }
              },
              "wallpaper":
              {
                  "dark":
                  {   
                      "image": "wallpaper/dark.png",
                      "first_frame": "wallpaper/dark_video.webm",
                      "text_color": "#FFFFFF",
                      "text_shadow": "#757575"
                  },
                  "light":
                  {
                      "image": "wallpaper/light_video.webm",
                      "first_frame": "wallpaper/light.png",
                      "text_color": "#FFFFFF",
                      "text_shadow": "#0B000E"
                  }
              }
          },
          "schema_version": 1
      },
      "version": str(request.form.get('mod version'))
  }).replace(chr(39), chr(34)))
            filenames.append(m.name)
          m.close()

          if 'testButton' in request.form:
            if not os.path.exists(f"templates/{downLink}-test"):
              exdown = open("templates/exampleTest.html", "r")
              with open(f"templates/{downLink}-test.html", "w") as downpage:
                downpage.write(str(exdown.read()))
                exdown.close()
                downpage.close()
              return redirect(f"{mURL}/test-mod/{downLink}")
            else:
              return redirect(f"{mURL}/test-mod/{downLink}")
  
          # Create a zip file containing the uploaded files
          if filenames:
              global mName
              mName = str(request.form.get('mod name'))
              zip_filename = f'{mName.replace(" ", "-")}-mod.zip'
              with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                  for filename in filenames:
                      if filename.endswith('.wav'):
                          file_folder = 'keyboard'
                      elif filename.endswith('.mp3'):
                        traks=["track_1.mp3", "track_2.mp3", "track_3.mp3", "track_4.mp3"]
                        if any(name in filename for name in traks):
                          file_folder = 'music'
                        else:
                          file_folder = 'sound'
                      elif filename.endswith('.png') or filename.endswith('.webm'):
                        walls=["dark.png", "light.png", "dark_video.webm", "light_video.webm"]
                        if any(name in filename for name in walls):
                          file_folder = 'wallpaper'
                        else:
                          file_folder = ''
                      elif filename.endswith('.txt'):
                        file_folder = ''
                      else:
                          file_folder = os.path.basename(os.path.dirname(filename))
                      zip_file.write(filename, os.path.join(file_folder, os.path.basename(filename)))
                      
                      os.remove(filename)
            
          if not os.path.exists(f"templates/{downLink}"):
            exdown = open("templates/exampleDownload.html", "r")
            with open(f"templates/{downLink}.html", "w") as downpage:
              downpage.write(str(exdown.read()))
              exdown.close()
              downpage.close()
            return redirect(f"{mURL}/download-mod/{downLink}")
          else:
            return redirect(f"{mURL}/download-mod/{downLink}")
  
    else:
      return render_template('UpdatedIndex.html')


@app.route("/terms")
def terms():
  return render_template('terms.html')

@app.route(f"/download-mod/{downLink}", methods=['GET', 'POST'])
def downloadFile():
  if request.method == "POST":
    zip_filename = f'{mName.replace(" ", "-")}-mod.zip'
      
    # Return the zip file for download
    response = send_file(zip_filename, as_attachment=True)
    
    return response

  else:
    return render_template(f"{downLink}.html")

@app.route(f"/test-mod/{downLink}", methods=['GET', 'POST'])
def testMod():
  if request.method == "POST":
    pass

  else:

    return render_template(f"{downLink}-test.html", key=downLink)
  
@app.route(f"/test-mod/<mod>", methods=['GET', 'POST'])
def testOtherMod(mod):
  if request.method == "POST":
    pass

  else:

    return render_template(f"{mod}-test.html", key=mod)

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