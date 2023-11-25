document.addEventListener('DOMContentLoaded', function() {
    const inputFile = document.getElementById("input-file");
    const fileView = document.getElementById("img-view");

    inputFile.addEventListener("change", uploadFile);

    function uploadFile() {
        const file = inputFile.files[0];

        if (file) {
            fileView.lastElementChild.textContent = `Uploaded File: ${file.name}`;
            fileView.style.border = "2px dashed black";
        } else {
            fileView.lastElementChild.textContent = "Please select a file.";
            fileView.style.border = "2px dashed red";
        }
    }

    fileView.parentElement.addEventListener("dragover", function(e) {
        e.preventDefault();
    });

    fileView.parentElement.addEventListener("drop", function(e) {
        e.preventDefault();
        inputFile.files = e.dataTransfer.files;
        uploadFile();
    });

    
});
