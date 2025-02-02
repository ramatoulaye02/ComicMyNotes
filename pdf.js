document.getElementById("pdf-upload").addEventListener("change", function() {
    const file = this.files[0];
    const fileNameElement = document.getElementById("file-name");

    if (file) {
        fileNameElement.textContent = "Selected File: " + file.name;
    } else {
        fileNameElement.textContent = "";
    }
    console.log(fileNameElement)
});




document.getElementById("pdf-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent page refresh

    const fileInput = document.getElementById("pdf-upload");
    if (fileInput.files.length === 0) {
        alert("Please select a file.");
        return;
    }

    const formData = new FormData();
    formData.append("pdf", fileInput.files[0]);

    // Send file to the backend (replace with your actual API endpoint)
    fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("File uploaded:", data);
    })
    .catch(error => {
        console.error("Error uploading file:", error);
    });
});
