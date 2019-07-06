var reader = new FileReader();
document.getElementById("file-input").addEventListener("input", function(){
    console.log("Callback here?");
    if(this.files && this.files[0])
    {
        reader.onload = function(e){
            document.getElementById("imageField").setAttribute('src', e.target.result);
            document.getElementById("imageField").style.visibility = "visible";
            document.getElementById("imageFieldEmpty").style.visibility = "hidden";
        }

        
        reader.readAsDataURL(this.files[0]);
    }
});
document.getElementById('upload-form').addEventListener("submit", function(){
    console.log("Form submitted");
    console.log("Image: " + document.getElementById('file-input').files[0])
}, false);


