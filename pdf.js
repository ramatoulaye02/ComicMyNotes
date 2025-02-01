document.getElementById("pdf-upload").addEventListener("change", function(event) {
    let file = event.target.files[0]; // Get the selected file

    if (file) {
        console.log("Selected PDF:", file.name); // Log file name (for debugging)
        document.getElementById("file-name").textContent = "Selected File: " + file.name;

        // Example: Send the file reference to backend
        let formData = new FormData();
        formData.append("pdf", file);

        fetch("https://your-backend-url.com/upload", {  // Change this to your API endpoint
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => console.log("File uploaded successfully:", data))
        .catch(error => console.error("Upload failed:", error));
    }
});
