console.log('Page loaded.');
var allButtons = document.querySelectorAll('.remove-button');
for(var i = 0; i < allButtons.length; i++)
{
    allButtons[i].addEventListener('click', function(){
        var imageContainer = this.parentNode.parentNode.parentNode;
        var data = {
            "id" : this.getAttribute('data-image-id')
        }
        $.ajax({
            dataType: 'json', 
            contentType: 'application/json', 
            data: JSON.stringify(data),
            url: '/removegif',
            type: 'POST',
            success: function(response)
            {
                if(response['status'] === 'success')
                {
                    sendNotification('Deletion successful!');
                    imageContainer.parentNode.removeChild(imageContainer);
                }
            }
        })
    });
}