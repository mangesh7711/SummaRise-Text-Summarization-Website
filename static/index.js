function displayFileName() {
      const fileInput = document.getElementById('fileInput');
      const fileNameDisplay = document.getElementById('fileNameDisplay');
      fileNameDisplay.innerText = fileInput.files[0].name;
    }

    function updateFileName() {

      displayFileName();
    }