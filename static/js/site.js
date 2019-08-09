var reader = new FileReader();

let uploadingImageView = 
` <img id="imageField" src="#" alt="uploaded image" style="visibility: hidden;"/>`;

document.getElementById("file-input").addEventListener("input", function(){
    if(this.files && this.files[0])
    {
        document.querySelector(".notification").innerHTML = "";
        document.querySelector(".gif-container").innerHTML = "";
        if(document.querySelector(".container-without-gif").innerHTML == "")
        {
            document.querySelector(".container-without-gif").innerHTML = uploadingImageView;
        }
        reader.onload = function(e){
            document.querySelector('#imageField').setAttribute('src', e.target.result);
            document.querySelector('#imageField').style.visibility = "visible";
            var initialText = document.querySelector("#imageFieldEmpty");
            document.querySelector(".container-without-gif").removeChild(initialText);
        }  
        reader.readAsDataURL(this.files[0]);
    }
});

document.getElementById('upload-form').addEventListener("submit", function(event){

    event.preventDefault();
    var timestampNode = document.createElement("input");
    timestampNode.setAttribute("type", "hidden");
    timestampNode.setAttribute("name", "timestamp");
    timestampNode.setAttribute("value", getCurrentTime());
    this.appendChild(timestampNode);
    var files = document.getElementById("file-input").files;
    var algorithmSelect = document.getElementById("algorithm");
    var algorithm = algorithmSelect.options[algorithmSelect.selectedIndex].text;
    console.log(algorithm);
    var formData = new FormData(this);
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
        if(data.state === "success")
        {
            $(".container-without-gif").empty();
            $(".gif-container").empty();
            $(".gif-container").append(`<img id="imageGifField" src="../static/images/outputs/` + data.image + `" alt="uploaded gif image" 
            />`);
            $(".gif-container").append('<h3>Enjoy your hot gif!</h3>');
            $(".gif-container").append(`<a class="btn form-element" href='../static/images/outputs/` + data.image + `'" download target="_blank">Download</a>`);
            document.querySelector("#welcoming-text").innerHTML = "Feel free to convert another!";
            if(data.authorized)
            {
                document.querySelector(".notification").innerHTML = `<div class="notif-text"><h5>Gif saved under 'Your gifs'.</h5></div><div class="notif-button"><button id="notif-button">Okay</button></div>`;
            }
            else
            {
                document.querySelector(".notification").innerHTML = 
                `<div class="notif-text"><h5>If you don't download it now, the image will not be saved. Signed up users enjoy the benefit of autosaving gifs! Consider being a part of us.</h5></div>
                <div class="notif-button"><button id="notif-button">Okay</button></div>`
                
            }
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
    <h4>Processing...</h4>`;
}, false);

document.addEventListener('click', function(e){
    if(e.target && e.target.id === 'notif-button')
    {
        document.querySelector('.notification').innerHTML = "";
    }
});