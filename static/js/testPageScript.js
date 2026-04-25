          // Elements

          // Tab Top elements
          const E3 = document.getElementById('Db3'); // Element with close tab button
          const P1 = document.getElementById('P1'); // Element with new tab button

          // Button elements
          const nt = document.getElementById('new_cut'); // Add bookmark element
          const bookContainer = document.querySelector('.book_icon'); // Bookmark element
          
          // Misc elements
          const sld = document.getElementById('sldr'); // Switch element
          const lmt = document.getElementById('lmtswtch'); // Switch - Limiter element
          const ftr = document.getElementById('ftrswtch'); // Switch - Feature element
          const mprt = document.getElementById('importantClick'); // Important Click element
          const lvlup = document.getElementById('levelup'); // Level Upgrade element
          const tabs = document.querySelectorAll('.killTab'); // Kill Tab elements
          const killContainer = document.getElementById('killTabContainer'); // Container for Kill Tab elements

          // Color elements
          const a1 = document.getElementById('dAccent'); // Dark Primary Color element
          const s1 = document.getElementById('dSecondary'); // Dark Secondary Color element
          const a2 = document.getElementById('lAccent'); // Light Primary Color element
          const s2 = document.getElementById('lSecondary'); // Light Secondary Color element

          // Mod Profile Info Elements
          const mpIcon = document.getElementById('modProfileIcon'); // Mod Profile Icon element
          const mpName = document.getElementById('modProfileName'); // Mod Profile Name element
          const mpAuth = document.getElementById('modProfileAuthor'); // Mod Profile Author element
          const mpVers = document.getElementById('modVersion'); // Mod Profile Version element
          const mpDesc = document.getElementById('modProfileDesc'); // Mod Profile Description element
      
      var currentURL = window.location.href;

      // Split the URL by '/'
      var urlParts = currentURL.split('/');

      // Find the part of the URL you want to use as 'key' (in this example, it's the second-to-last part)
      var key = document.querySelector('meta[name="mod_id"]').content;

      function getRandomItem(options) {
        var randomIndex = Math.floor(Math.random() * options.length);
        return options[randomIndex];
      }
      
      fetch(`/mods/${key}/manifest.json`)
        .then(response => response.json())
        .then(data => {

          // Theme Packs
          const dTHEME = data.mod.payload.theme.dark;
          const lTHEME = data.mod.payload.theme.light;
          var tNAME = "dark";

          // Browser Sounds
          const sounds = data.mod.payload.browser_sounds;

          // Changing Theme Colors
          var gxAccent = hexToHsl(dTHEME.gx_accent);
          var gxSecondayBase = hexToHsl(dTHEME.gx_secondary_base);

          var gxAccentrgb = hexToRgb(dTHEME.gx_accent);
          var gxSecondayBasergb = hexToRgb(dTHEME.gx_secondary_base);

          // Constant Theme Colors
          const dGxAccent = hexToHsl(dTHEME.gx_accent);
          const dGxSecondaryBase = hexToHsl(dTHEME.gx_secondary_base);
          const lGxAccent = hexToHsl(lTHEME.gx_accent);
          const lGxSecondaryBase = hexToHsl(lTHEME.gx_secondary_base);

          function themeColors() {

            // Browser element background
            document.getElementById("frame_1").src = `/mods/${key}/${data.mod.payload.wallpaper[tNAME].image}`;

            // nt.style.backgroundColor = `hsl(${gxAccent.h}, ${gxAccent.s}%, ${l2}%)`;

            // Accent Definitions
            document.documentElement.style.setProperty('--gx-accent-h', gxAccent.h);
            document.documentElement.style.setProperty('--gx-accent-s', gxAccent.s);
            document.documentElement.style.setProperty('--gx-accent-r', gxAccentrgb.r);
            document.documentElement.style.setProperty('--gx-accent-g', gxAccentrgb.g);
            document.documentElement.style.setProperty('--gx-accent-b', gxAccentrgb.b);
            
            // Secondary Base Definitions
            document.documentElement.style.setProperty('--gx-secondary-h', gxSecondayBase.h);
            document.documentElement.style.setProperty('--gx-secondary-s', gxSecondayBase.s);
            document.documentElement.style.setProperty('--gx-secondary-r', gxSecondayBasergb.r);
            document.documentElement.style.setProperty('--gx-secondary-g', gxSecondayBasergb.g);
            document.documentElement.style.setProperty('--gx-secondary-b', gxSecondayBasergb.b);
          }

          themeColors();

          // Dark Theme color examples
          a1.style.backgroundColor = `hsl(${dGxAccent.h}, ${dGxAccent.s}%, ${dGxAccent.l}%)`;
          s1.style.backgroundColor = `hsl(${dGxSecondaryBase.h}, ${dGxSecondaryBase.s}%, ${dGxSecondaryBase.l}%)`;

          // Light theme color examples
          a2.style.backgroundColor = `hsl(${lGxAccent.h}, ${lGxAccent.s}%, ${lGxAccent.l}%)`;
          s2.style.backgroundColor = `hsl(${lGxSecondaryBase.h}, ${lGxSecondaryBase.s}%, ${lGxSecondaryBase.l}%)`;

          // Set Mod Profile values
          mpIcon.src = `/mods/${key}/${data.icons["512"]}`;
          mpName.textContent = data.name;
          mpAuth.textContent = data.developer.name;
          mpVers.textContent = `v${data.version}`;
          mpDesc.textContent = data.description;

          // check for Light Mode
          document.addEventListener("click", (e) => {
            if (e.target.id === "light-dark-switch") {
              if (e.target.checked) {

                gxAccent = hexToHsl(lTHEME.gx_accent);
                gxSecondayBase = hexToHsl(lTHEME.gx_secondary_base);
                tNAME = "light";
                themeColors();

              }
              else {

                gxAccent = hexToHsl(dTHEME.gx_accent);
                gxSecondayBase = hexToHsl(dTHEME.gx_secondary_base);
                tNAME = "dark";
                themeColors();

              }
            }
          });

          // Bookmark Click Listener
          bookContainer.addEventListener('click', (event) => {
            try {
              var a = new Audio(`/mods/${key}/${getRandomItem(sounds.CLICK)}`);
              a.play();              
            } catch (error) {}
          });

          // Add Bookmark Click Listener
          nt.addEventListener('click', (event) => {
            try {
              var a = new Audio(`/mods/${key}/${getRandomItem(sounds.CLICK)}`);
              a.play();
            } catch (error) {}
          });

          // Important Click Listener
          mprt.addEventListener('click', (event) => {
            try {
              var a = new Audio(`/mods/${key}/${getRandomItem(sounds.IMPORTANT_CLICK)}`);
              a.play();
            } catch (error) {}

            mprt.style.color = "var(--imprt-button-click-color)";
            setTimeout(() => {
              mprt.style.color = "";
            }, 150);

          });

          // Level Upgrade Listener
          lvlup.addEventListener('click', (event) => {
            try {
              var a = new Audio(`/mods/${key}/${getRandomItem(sounds.LEVEL_UPGRADE)}`);
              a.play();
            } catch (error) {}

            lvlup.style.color = "var(--imprt-button-click-color)";
            setTimeout(() => {
              lvlup.style.color = "";
            }, 150);

          });

          // New Tab Click Listener
          P1.addEventListener('click', (event) => {
            if (event.target.matches(`.new_tab`)) {
              try {
                var a = new Audio(`/mods/${key}/${getRandomItem(sounds.TAB_INSERT)}`);
                a.play();
              } catch (error) {}

            }
          })

          // Close Tab Click Listener
          E3.addEventListener('click', (event) => {
            if (event.target.matches(`.close-button`)) {
              try {
                var a = new Audio(`/mods/${key}/${getRandomItem(sounds.TAB_CLOSE)}`);
                a.play();
              } catch (error) {}

            }
          })
          
          // Bookmark Hover Listener
          bookContainer.addEventListener('mouseenter', (event) => {
            try {
              var a = new Audio(`/mods/${key}/${getRandomItem(sounds.HOVER)}`);
              a.play();
            } catch (error) {}
          });

          // Switch Click Listener
          sld.addEventListener('click', (event) => {
            try {
              var a = new Audio(`/mods/${key}/${getRandomItem(sounds.SWITCH_TOGGLE)}`);
              a.play();
            } catch (error) {}
          });

          // Limiter Click Listener
          lmt.addEventListener('change', (event) => {

            if (lmt.checked) {
              try {
                var a = new Audio(`/mods/${key}/${getRandomItem(sounds.LIMITER_ON)}`);
                a.play();
              } catch (error) {}

              document.getElementById('lmtr').title = "Test 'limiter-off.mp3'";
            }

            else {
              try {
                var b = new Audio(`/mods/${key}/${getRandomItem(sounds.LIMITER_OFF)}`);
                b.play();
              } catch (error) {}

              document.getElementById('lmtr').title = "Test 'limiter-on.mp3'";
            }
            

          });

          // Feature Click Listener
          ftr.addEventListener('change', (event) => {

            if (ftr.checked) {
              try {
                var a = new Audio(`/mods/${key}/${getRandomItem(sounds.FEATURE_SWITCH_ON)}`);
                a.play();
              } catch (error) {}

              document.getElementById('ftre').title = "Test 'feature-switch-off.mp3'";
            }

            else {
              try {
                var b = new Audio(`/mods/${key}/${getRandomItem(sounds.FEATURE_SWITCH_OFF)}`);
                b.play();
              } catch (error) {}

              document.getElementById('ftre').title = "Test 'feature-switch-on.mp3'";
            }
            

          });

          // Hot Tabs Killer Listener
          tabs.forEach(tab => {
            
            btn = tab.querySelector("button");

            btn.addEventListener('click', (event) => {

              try {
                var a = new Audio(`/mods/${key}/${getRandomItem(sounds.TAB_SLASH)}`);
                a.play();
              } catch (error) {}

              killContainer.appendChild(tab);

            });

          });

          })
          .catch(error => {
            console.error('Error:', error);
          });

      function modSubmit(event) {
        event.preventDefault();

        const downMod = document.getElementById('downMod');
        const action = document.getElementById('action');

        res = confirm("Are you sure you're ready to download your mod? Once you download it, all files associated with your mod will be deleted from our servers and you will no longer be able to edit it.");

        if (!res) {}

        else {

          action.value = downMod.value;
          event.target.submit();

        }

      }

      function maxSat(sat) {

        if (sat > 100) {
          return 100;
        }

        if (sat < 0) {
          return 0;
        }

        return sat;
      }

      function satCurve(num, mode) {

        if (mode === "dark") {

          return maxSat((-0.036 * num * num) + (3.98 * num) - 48.5)

        }

      }