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

document.getElementById('upload-form').addEventListener("submit", function(event){

    event.preventDefault();
    var form = document.getElementById("upload-form");
    var files = document.getElementById("file-input").files;
    var algorithmSelect = document.getElementById("algorithm");
    var algorithm = algorithmSelect.options[algorithmSelect.selectedIndex].text;
    console.log(algorithm);
    var formData = new FormData(form);
    console.log(formData);
    jQuery.ajax({
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
        if(data.State == "Success")
        {
            console.log("Success!");
            imagePath = "../images/output.gif";
            jQuery(".container-without-gif").empty();
            jQuery(".gif-container").empty();
            jQuery(".gif-container").append('<img id="imageGifField" src="../static/images/output.gif" alt="uploaded gif image" />');
            jQuery(".gif-container").append('<button>Download</button>');
        }
        else
        {
            $(".gif-container").append('<h2>Error!</h2>')
        }
    })


}, false);



