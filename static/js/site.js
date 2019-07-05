document.getElementById('upload-form').addEventListener("submit", function(){
    console.log("Form submitted");
    console.log("Image: " + document.getElementById('file-input').files[0])
}, false);

