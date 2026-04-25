      let activeCategory = null;
      let categoryFiles = {
          KeyboardSounds: [],
          BackgroundMusic: [],
          BrowserSounds: [],
          Wallpapers: [],
          ModInfo: []
      };
      let modInfoFiles = {
        license: false,
        icon: false,
      };
      let modInfoData = {};

      let categoryCount = {
        KeyboardSounds: 0,
        BackgroundMusic: 0,
        BrowserSounds: 0,
        Wallpapers: 0,
        ModInfo: 0
      }
      let categoryContainer = {
        KeyboardSounds: 2,
        BackgroundMusic: 1,
        BrowserSounds: 3,
        Wallpapers: 1,
        ModInfo: 1
      }
      let currentCategory = '';
      let modal = document.getElementById("myModal");
      let modalOverlay = document.getElementById("modalOverlay");
      let fileInput = document.getElementById("fileInput");
      let fileDesc = document.getElementById("fileDesc");
      let uploadBtn = document.getElementById("uploadBtn");
  
      // Define category-specific file type options
      const categoryFileTypeOptions = {
          KeyboardSounds: [
              { value: '.wav', name: 'backspace', label: 'Backspace Key', desc: 'This sound will play whenever you press Backspace.'},
              { value: '.wav', name: 'enter', label: 'Enter (Return) Key', desc: 'This sound will play whenever you press Enter (Return).'},
              { value: '.wav', name: 'space', label: 'Space Key', desc: 'This sound will play whenever you press Space.'},
              { value: '.wav', name: 'letter', label: 'Other Key', desc: 'This sound will play whenever you press any key other than Backspace, Space, or Enter (Return).'}
          ],
          BackgroundMusic: [
              { value: '.mp3', name: 'song', label: 'Background Song', desc: 'This song will play in the background as you browse.'}
          ],
          BrowserSounds: [
              { value: '.mp3', name: 'click', label: 'Click', desc: "This sound wll play whenever you click on something."},
              { value: '.mp3', name: 'close-tab', label: 'Close Tab', desc: "This sound will play whenever you close a tab."},
              { value: '.mp3', name: 'feature-switch-off', label: 'Feature Switch Off', desc: "This sound will play whenever you turn off a feature switch. This feature is currently not used by Opera GX and may be added in the future."},
              { value: '.mp3', name: 'feature-switch-on', label: 'Feature Switch On', desc: "This sound will play whenever you turn on a feature switch. This feature is currently not used by Opera GX and may be added in the future."},
              { value: '.mp3', name: 'hover', label: 'Hover', desc: "This sound will play whenever you hover over a shortcut on the Speed Dial."},
              { value: '.mp3', name: 'important-click', label: 'Important Click', desc: "This sound will play whenever you do an important click. This feature is currently not used by Opera GX and may be added in the future."},
              { value: '.mp3', name: 'level-upgrade', label: 'Level Upgrade', desc: "This sound will play whenever a level upgrades. This feature is currently not used by Opera GX and may be added in the future."},
              { value: '.mp3', name: 'limiter-off', label: 'Limiter Off', desc: "This sound will play whenever you turn off a limiter (ex. CPU Usage Limiter)."},
              { value: '.mp3', name: 'limiter-on', label: 'Limiter On', desc: "This sound will play whenever you turn on a limiter (ex. RAM Usage Limiter)."},
              { value: '.mp3', name: 'new-tab', label: 'New Tab', desc: "This sound will play whenever you open a new tab."},
              { value: '.mp3', name: 'switch', label: 'Switch', desc: "This sound will play whenever you enable or disable a switch."},
              { value: '.mp3', name: 'tab-slash', label: 'Tab Slash', desc: "This sound will play whenever you slash a tab."}
          ],
          Wallpapers: [
              { value: '.png, .jpg, .jpeg, .webp', name: 'light-image', label: 'Static Light Wallpaper', desc: "This is the wallpaper image that will show in light mode."},
              { value: '.png, .jpg, .jpeg, .webp', name: 'dark-image', label: 'Static Dark Wallpaper', desc: "This is the wallpaper video that will show in light mode."},
              { value: '.webm, .apng', name: 'light-video', label: 'Dynamic Light Wallpaper', desc: "This is the wallpaper image that will show in dark mode."},
              { value: '.webm, .apng', name: 'dark-video', label: 'Dynamic Dark Wallpaper', desc: "This is the wallpaper video that will show in dark mode."}
          ],
          ModInfo: [
              { value: '.txt', name: 'license', label: 'License', desc: "This is the license which verifies you are allowed to use the content in this mod."},
              { value: '.png', name: 'icon', label: 'Icon (512x512)', desc: "This is the mod's icon."}
          ]
      };
      

      function handleInput(type, event) {
        const input = event.target;
        modInfoData[type] = input.value;
        console.log(`Input received: ${input.value}`);
        console.log(modInfoData)
        console.log(input.id);
      }

      function getValue(type, event) {
        const input = event.target;
        input.value = modInfoData[type];
      }

      function toggleInput() {
        // Use setTimeout to delay the execution of the code to ensure the element is in the DOM
        setTimeout(() => {
          // Get the modBox element
          const modBox = document.getElementById('modBox');

          // Check if modBox exists
          if (!modBox) {
            console.error('modBox element not found');
            return;
          }

          const boxes = [
            {name: "mod name", id: "modName"},
            {name: "mod author", id: "modAuth"},
            {name: "mod description", id: "modDesc"},
            {name: "mod version", id: "modVer"},
            {name: "lp", id: "lp"},
            {name: "la", id: "la"},
            {name: "dp", id: "dp"},
            {name: "da", id: "da"},
          ];

          boxes.forEach(box => {
            // Retrieve the input data
            var input = modInfoData[box.name];
            console.log('Input value:', input);

            // Find the input element with the ID 'modName' within the modBox
            const inputElement = modBox.querySelector(`#${box.id}`);

            if (inputElement) {
              // If the inputElement is found, update its value
              if (input) {
                inputElement.value = input;
              }
            } else {
              // Log if the inputElement is not found
              console.error(`Element with ID ${box.id} not found within modBox`);
            }
          });

        }, 100); // Adjust the delay as needed (100 milliseconds in this example)
      }

      // Add this function to serialize the categoryFiles dictionary
      function serializeCategories() {
          const formData = {};
          
          for (let category in categoryFiles) {
              formData[category] = categoryFiles[category].map(file => ({
                  name: file.name,
                  type: file.type,
                  size: file.size,
                  lastModified: file.lastModified
              }));
          }

          return JSON.stringify(formData);
      }

      function validateModInfo() {
        // Ensure all Mod Info fields are filled out

          const ct = Object.keys(modInfoData).length;

          if (ct < 8) {
              return false;
          }

        // Ensure icon and license files are uploaded
        const requiredFiles = ['icon.png', 'license.txt'];
        for (let file of requiredFiles) {
            if (!categoryFiles.ModInfo.some(f => f.name === file)) {
                return false;
            }
        }
        
        return true;
      }

      // Modify the form submission event to include serialized data
      function handleSubmit(event) {
          event.preventDefault();

          console.log(categoryFiles)

          var verifiles = validateModInfo();

          var wallps = categoryFiles.Wallpapers.some(item => item.name.includes("dark-image")) && categoryFiles.Wallpapers.some(item => item.name.includes("light-image"));

          if (verifiles && wallps && checkVersion()) {

            const clickedButton = event.submitter;
            const action = document.getElementById('action');
            action.value = clickedButton.value;
            console.log(clickedButton.value);

            const form = document.getElementById('submitForm');

            if (clickedButton.value === "Test Mod") {
              form.target = "_blank";
            }

            else {
              form.target = "";
            }

            if (currentCategory != "ModInfo") {

              for (const [key, value] of Object.entries(modInfoData)) {
                // Create a new hidden input element
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                input.value = value;

                // Append the hidden input to the form
                form.appendChild(input);
              }
            }

            // Serialize metadata
            const serializedMetadata = serializeCategories();
            const formData = new FormData();
            formData.append('metadata', serializedMetadata);

            // Append actual files to FormData
            for (let category in categoryFiles) {
                categoryFiles[category].forEach((file, index) => {
                    formData.append(`${category}_${index}`, file);
                });
            }

            // Send the form data to the server using fetch

            const modID = document.querySelector('meta[name="mod_id"]').content;

            fetch(`/${modID}/submit-files`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                event.target.submit();
            })
            .catch(error => {
                console.error('Error:', error);
            });

          }

          else {
            if (wallps) {
              alert('There is missing or incorrect info in the Mod Info section! Please fix this and try again.');
            }

            else {
              alert('You are missing a wallpaper! Please make sure you have BOTH a light and a dark wallpaper!');
            }
          }

      }
  
      function displayBox(category, element) {
          // Prevent changing categories when modal is open
          if (modal.style.display === "block") return;
  
          var content = document.getElementById('modBox');
          var catName = document.getElementById('catName');
          var fullCat = cateName(category);
          currentCategory = category;
  
          if (activeCategory === element) {
              content.innerHTML = '<div class="message" style="font-size: 50px;">Select a category to start modding!</div>';
              catName.innerHTML = 'Categories';
              element.classList.remove('active');
              activeCategory = null;
               content.className = "modBoxDef"
          } else {
              content.className = "modBox"
              catName.innerHTML = `Category: ${fullCat}`;
              var xhr = new XMLHttpRequest();
              xhr.open('GET', '/static/categories.html', true);
              xhr.onreadystatechange = function () {
                  if (xhr.readyState === 4 && xhr.status === 200) {
                      var tempDiv = document.createElement('div');
                      tempDiv.innerHTML = xhr.responseText;
                      var newContent = tempDiv.querySelector('#' + category);
                      content.innerHTML = newContent ? newContent.innerHTML : '<div class="message">No content available</div>';
                      displayUploadedFiles(category);  // Display files for the selected category
                      if (category === 'ModInfo') {
                        const verInput = document.getElementById("modVer");
                        const verWarn = document.getElementById("verWarn");

                        // ensures proper version input
                        verInput.addEventListener('input', () => {
                          if (checkVersion()) {
                            verInput.style.border = "2px solid #8C32CD";
                            verWarn.style.display = "none";
                          }
                          else {
                            verInput.style.border = "2px solid red";
                            verWarn.style.display = "block";
                          }
                        });
                      }
                  }
              };
              xhr.send();
  
              if (activeCategory) {
                  activeCategory.classList.remove('active');
              }
              element.classList.add('active');
              activeCategory = element;
          }
      }
  
      function displayUploadedFiles(category) {

        var num = 0;

        var uploadsDiv;
        uploadsDiv = document.getElementById(`${category}Uploads1`);
        uploadsDiv.innerHTML = '';

        categoryFiles[category].forEach((file, index) => {
            num += 1;
            uploadsDiv = document.getElementById(`${category}Uploads1`);
            const fileDiv = document.createElement('div');
            fileDiv.classList.add('fileContainer');
            
            // Create a file name and remove button
            let fileContent = `<div class="fileInfo">
                                <span>${file.name}</span> 
                                <br> 
                                  <button type="button" onclick="removeFile('${category}', ${index})">
                                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="red" version="1.1" id="Capa_1" width="25px" height="25px" viewBox="0 0 482.428 482.429" xml:space="preserve">
                                      <g>
                                        <g>
                                          <path d="M381.163,57.799h-75.094C302.323,25.316,274.686,0,241.214,0c-33.471,0-61.104,25.315-64.85,57.799h-75.098    c-30.39,0-55.111,24.728-55.111,55.117v2.828c0,23.223,14.46,43.1,34.83,51.199v260.369c0,30.39,24.724,55.117,55.112,55.117    h210.236c30.389,0,55.111-24.729,55.111-55.117V166.944c20.369-8.1,34.83-27.977,34.83-51.199v-2.828    C436.274,82.527,411.551,57.799,381.163,57.799z M241.214,26.139c19.037,0,34.927,13.645,38.443,31.66h-76.879    C206.293,39.783,222.184,26.139,241.214,26.139z M375.305,427.312c0,15.978-13,28.979-28.973,28.979H136.096    c-15.973,0-28.973-13.002-28.973-28.979V170.861h268.182V427.312z M410.135,115.744c0,15.978-13,28.979-28.973,28.979H101.266    c-15.973,0-28.973-13.001-28.973-28.979v-2.828c0-15.978,13-28.979,28.973-28.979h279.897c15.973,0,28.973,13.001,28.973,28.979    V115.744z"/>
                                          <path d="M171.144,422.863c7.218,0,13.069-5.853,13.069-13.068V262.641c0-7.216-5.852-13.07-13.069-13.07    c-7.217,0-13.069,5.854-13.069,13.07v147.154C158.074,417.012,163.926,422.863,171.144,422.863z"/>
                                          <path d="M241.214,422.863c7.218,0,13.07-5.853,13.07-13.068V262.641c0-7.216-5.854-13.07-13.07-13.07    c-7.217,0-13.069,5.854-13.069,13.07v147.154C228.145,417.012,233.996,422.863,241.214,422.863z"/>
                                          <path d="M311.284,422.863c7.217,0,13.068-5.853,13.068-13.068V262.641c0-7.216-5.852-13.07-13.068-13.07    c-7.219,0-13.07,5.854-13.07,13.07v147.154C298.213,417.012,304.067,422.863,311.284,422.863z"/>
                                        </g>
                                      </g>
                                    </svg>
                                  </button>
                                </div>`;

            // Check if the file is an audio file
            const fileExtension = file.name.split('.').pop().toLowerCase();
            if (fileExtension === 'mp3' || fileExtension === 'wav') {
                // Create an audio element
                const audioElement = document.createElement('audio');
                audioElement.classList.add('fileAudio')
                audioElement.controls = true;

                // Create a URL for the file and set it as the source of the audio element
                const fileURL = URL.createObjectURL(file);
                audioElement.src = fileURL;

                // Append the audio element to the file content
                fileContent += '<br>';
                fileDiv.appendChild(audioElement);
            }

            fileDiv.innerHTML += fileContent;
            uploadsDiv.appendChild(fileDiv);
        });
        if (num >= 15 && category === 'BrowserSounds') {}
        else if (num >= 10 && category === 'KeyboardSounds') {}
        else if (num >= 5 && category === 'BackgroundMusic') {}
        else if (num >= 4 && category === 'Wallpapers') {}
        else if (num >= 2 && category === 'ModInfo') {}
        else {
          document.getElementById(`${category}Uploads1`).innerHTML += `<button type="button" class="addButton" onclick="addFileInput('${category}')">+ <br> Add File</button>`;
        }
      }

  
      function addFileInput(category) {
          currentCategory = category;

          if (category === 'ModInfo') {
              if (modInfoFiles.license && modInfoFiles.icon) {
                  alert("Both license and icon files are already uploaded.");
                  return;
              }
          }

          if (category === 'KeyboardSounds' && categoryFiles[category].length >= 10) {
            alert("You have already uploaded 10 files! You have reached your file upload limit.");
            return;
          }
          if (category === 'BackgroundMusic' && categoryFiles[category].length >= 5) {
            alert("You have already uploaded 5 files! You have reached your file upload limit.");
            return;
          }
          if (category === 'BrowserSounds' && categoryFiles[category].length >= 15) {
            alert("You have already uploaded 15 files! You have reached your file upload limit.");
            return;
          }
          if (category === 'Wallpapers' && categoryFiles[category].length >= 4) {
            alert("You have already uploaded 4 files! You have reached your file upload limit.");
            return;
          }

          modal.style.display = "block";
          modalOverlay.style.display = "block";

          const select = document.getElementById('fileTypeSelect');
          select.innerHTML = '<option value="">Select...</option>';
          categoryFileTypeOptions[category].forEach(option => {
              let disabled = '';
              if (category === 'ModInfo' && ((option.value === '.txt' && modInfoFiles.license) || (option.value === '.png' && modInfoFiles.icon))) {
                  disabled = 'disabled';
              }
              if (category === 'Wallpapers' && (categoryFiles.Wallpapers.some(item => item.name.includes("dark-image"))) && option.name === 'dark-image') {
                disabled = 'disabled';
              }
              if (category === 'Wallpapers' && (categoryFiles.Wallpapers.some(item => item.name.includes("dark-video"))) && option.name === 'dark-video') {
                disabled = 'disabled';
              }
              if (category === 'Wallpapers' && (categoryFiles.Wallpapers.some(item => item.name.includes("light-image"))) && option.name === 'light-image') {
                disabled = 'disabled';
              }
              if (category === 'Wallpapers' && (categoryFiles.Wallpapers.some(item => item.name.includes("light-video"))) && option.name === 'light-video') {
                disabled = 'disabled';
              }
              select.innerHTML += `<option ${disabled} name="${option.name}" desc="${option.desc}" value="${option.value}">${option.label}</option>`;
          });

          fileInput.value = '';
          fileInput.disabled = true;
          uploadBtn.disabled = true;
      }

  
      function handleFileTypeChange() {
        const select = document.getElementById('fileTypeSelect');
        const fileType = select.value;
        const fDesc = select.options[select.selectedIndex].getAttribute('desc');

        if (fileType === '') {
            fileInput.value = ''; // Clear previous file input
            fileInput.disabled = true;
            uploadBtn.disabled = true;
            fileDesc.innerHTML = '';
        } else {
            fileInput.disabled = false;
            uploadBtn.disabled = false;
            fileDesc.innerHTML = fDesc;
            fileInput.accept = fileType;
        }
      }

  
      function uploadFile() {
          const file = fileInput.files[0];
          const select = document.getElementById('fileTypeSelect');
          if (file) {
              const newFileName = getFileInfo(select, file.name);
              const newFile = new File([file], newFileName, { type: file.type });

              if (currentCategory === 'ModInfo') {
                  const fileType = select.value;
                  if (fileType === '.txt') {
                      modInfoFiles.license = true;
                  } else if (fileType === '.png') {
                      modInfoFiles.icon = true;
                  }
              }

              categoryFiles[currentCategory].push(newFile);
              displayUploadedFiles(currentCategory);
              closeModal();
              categoryCount[currentCategory] += 1;
              const ct = document.getElementById(`${currentCategory}Count`);
              ct.innerHTML = `${categoryCount[currentCategory]}/${ct.getAttribute('maxCt')}`;
          }
      }



      function getFileInfo(select, originalName) {
        const choice = select.options[select.selectedIndex].getAttribute('name');
        let baseName = choice || originalName.split('.')[0];
        const fileExtension = originalName.split('.').pop();

        let newFileName = `${baseName}.${fileExtension}`;
        let counter = 1;

        // Check if the new file name already exists in the current category
        while (categoryFiles[currentCategory].some(file => file.name === newFileName)) {
            newFileName = `${baseName} (${counter}).${fileExtension}`;
            counter++;
        }

        return newFileName;
      }
  
      function removeFile(category, index) {
        const file = categoryFiles[category][index];

        // Special handling for ModInfo files
        if (category === 'ModInfo') {
            if (file.type === 'text/plain') {
                modInfoFiles.license = false;
            } else if (file.type === 'image/png') {
                modInfoFiles.icon = false;
            }
        }

        categoryFiles[category].splice(index, 1);
        categoryCount[category] -= 1;
        displayUploadedFiles(category);
        const ct = document.getElementById(`${category}Count`);
        ct.innerHTML = `${categoryCount[category]}/${ct.getAttribute('maxCt')}`;
      }

  
      function closeModal() {
          modal.style.display = "none";
          modalOverlay.style.display = "none";
          document.getElementById('fileTypeSelect').value = '';
          fileInput.value = '';
          fileDesc.innerHTML = '';
          fileInput.disabled = true;
          uploadBtn.disabled = true;
      }

      function cateName(category) {
        if (category === 'KeyboardSounds') {
          return 'Keyboard Sounds';
        }
        else if (category === 'BackgroundMusic') {
          return 'Background Music';
        }
        if (category === 'BrowserSounds') {
          return 'Browser Sounds';
        }
        if (category === 'ModInfo') {
          return 'Mod Info';
        }

        else {return category;}
      }

      function checkVersion() {
        // Regex check for version input
        const verReg = /^\d{1,5}(\.\d{1,5}){1,4}$/;
        const verIn = document.getElementById("modVer");
        const verVal = (verIn && verIn.value) || modInfoData['mod version'];

        return verReg.test(verVal);
                        
      }

      // Close the modal when the user clicks on <span> (x)
      document.querySelector('.close').onclick = closeModal;
      document.getElementById('closeButton').onclick = closeModal;
  
      // Close the modal when the user clicks anywhere outside of the modal content
      window.onclick = function(event) {
          if (event.target === modalOverlay) {
              closeModal();
          }
      }

