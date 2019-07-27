var reader = new FileReader();

let uploadingImageView = 
` <img id="imageField" src="#" alt="uploaded image" style="visibility: hidden;"/>
<h4 id="imageFieldEmpty">No image is uploaded yet.</h4> `

document.querySelector(".container-without-gif").innerHTML = uploadingImageView;

document.getElementById("file-input").addEventListener("input", function(){
    console.log("Callback here?");
    if(this.files && this.files[0])
    {
        $(".gif-container").empty();
        if( document.querySelector(".container-without-gif").innerHTML == "")
        {
            document.querySelector(".container-without-gif").innerHTML = uploadingImageView;
            document.querySelector("#welcoming-text").innerHTML = "Welcome to Imagif!";
        }
        reader.onload = function(e){
            document.getElementById("imageField").setAttribute('src', e.target.result);
            document.getElementById("imageField").style.visibility = "visible";
            document.getElementById("imageField").style.paddingTop = "2vh"
            document.getElementById("imageFieldEmpty").style.visibility = "hidden";
        }  
        reader.readAsDataURL(this.files[0]);
    }
});

document.getElementById('upload-form').addEventListener("submit", function(event){

    event.preventDefault();
    var form = document.getElementById("upload-form");
    var files = document.getElementById("file-input").files;
    var algorithmSelect = document.getElementById("algorithm");
    var algorithm = algorithmSelect.options[algorithmSelect.selectedIndex].text;
    console.log(algorithm);
    var formData = new FormData(form);
    console.log(formData);
    $.ajax({
        contentType: false,
        processData: false,
        data: formData,
        url: '/OnImageRecieved',
        type: 'POST',
        success: function(data){
            console.log(data);
        }
    })
    .done(function(data){
        //Do something with image.
        if(data.state == "success")
        {
            console.log("Success!");
            $(".container-without-gif").empty();
            $(".gif-container").empty();
            $(".gif-container").append(`<img id="imageGifField" src="../static/images/outputs/` + data.image + `" alt="uploaded gif image" 
            style="padding-top: 2vh; height:100%; width:100%"/>`);
            $(".gif-container").append('<h3>Enjoy your hot gif!</h3>');
            $(".gif-container").append(`<a class="form-element" href='../static/images/outputs/` + data.image + `'"><button class="form-element">Download</button></a>`);
            document.querySelector("#welcoming-text").innerHTML = "Feel free to convert another!";
        }
        else
        {
            $("#downloadButton").off();
            $(".gif-container").empty();
            $(".gif-container").append('<h2>Error!</h2>');
        }
    });
    $(".gif-container").empty();
    $(".container-without-gif").empty();
    document.querySelector(".container-without-gif").innerHTML = `<div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div>
    <h2>Processing...</h2>`
}, false);




