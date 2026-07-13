    function headers() {
    fetch('/static/header-footer.html') // Replace 'path/to/other/file.html' with the actual path to your other HTML file.
      .then(response => response.text())
      .then(html => {
        // Create a temporary container element to hold the fetched content.
        const tempContainer = document.createElement('div');
        tempContainer.innerHTML = html;
  
        // Find the element you want to clone inside the temporary container.
        const sourceElement = tempContainer.querySelector('#header');
  
        if (sourceElement) {
          // Clone the element and its children.
          const clonedElement = sourceElement.cloneNode(true);
  
          // Insert the cloned element into the destination element.
          const destinationElement = document.getElementById('pageHeader');
          destinationElement.appendChild(clonedElement);
        }
      })
      .catch(error => {
        console.error('Error fetching the file:', error);
      });
    };
    
    function footers() {
    fetch('/static/header-footer.html') // Replace 'path/to/other/file.html' with the actual path to your other HTML file.
      .then(response => response.text())
      .then(html => {
        // Create a temporary container element to hold the fetched content.
        const tempContainer = document.createElement('div');
        tempContainer.innerHTML = html;
  
        // Find the element you want to clone inside the temporary container.
        const sourceElement = tempContainer.querySelector('#footer');
  
        if (sourceElement) {
          // Clone the element and its children.
          const clonedElement = sourceElement.cloneNode(true);
  
          // Insert the cloned element into the destination element.
          const destinationElement = document.getElementById('pageFooter');
          destinationElement.appendChild(clonedElement);
        }
      })
      .catch(error => {
        console.error('Error fetching the file:', error);
      });
    };

    function loadNav() {
    fetch('/static/header-footer.html') // Replace 'path/to/other/file.html' with the actual path to your other HTML file.
      .then(response => response.text())
      .then(html => {
        // Create a temporary container element to hold the fetched content.
        const tempContainer = document.createElement('div');
        tempContainer.innerHTML = html;
  
        // Find the element you want to clone inside the temporary container.
        const sourceElement = tempContainer.querySelector('#fullNav');
  
        if (sourceElement) {
          // Clone the element and its children.
          const clonedElement = sourceElement.cloneNode(true);
  
          // Insert the cloned element into the destination element.
          const destinationElement = document.getElementById('pageNav');
          destinationElement.appendChild(clonedElement);
        }
      })
      .catch(error => {
        console.error('Error fetching the file:', error);
      });
    };

    headers();
    footers();
    loadNav();

    function LightDarkMode() {

      const chgBtn = document.getElementById("light-dark-switch"); // Switch which controls light/dark mode
      const stlsheet = document.getElementById("colorStyle"); // Stylesheet which controls light/dark mode

      const headTitle = document.getElementById("headerTitle"); // Header Title element
      const footTitle = document.getElementById("footerTitle"); // Footer Title element

      if (chgBtn.checked) {
        stlsheet.href = "/static/styleLight.css";
        headTitle.src = "/static/title/titleLight.webp";
        footTitle.src = "/static/title/titleLight.webp";
      }

      else {
        stlsheet.href = "/static/styleDark.css";
        headTitle.src = "/static/title/title.webp";
        footTitle.src = "/static/title/title.webp";
      }      
    }