/**
 * Gets current time in human readable format.
 */

function getCurrentTime()
{
    var now = new Date();
    return String(now.getDate()).padStart(2 , '0') + '/' + String(now.getMonth() + 1).padStart(2, '0') + '/' 
    + now.getFullYear() + " " 
    + String(now.getHours()).padStart(2, '0') + ":" + String(now.getMinutes()).padStart(2, '0');
}

/**
 * Publishes the message in the notification section.
 * @param {*} message message to send. 
 */
function sendNotification(message)
{
    document.querySelector(".notification").innerHTML = `
    <div class="notif-text"><h5>` + message + `</h5></div><div class="notif-button"><button id="notif-button">Okay</button></div>`;
    scroll(0, 0);
}

document.addEventListener('click', function(e){
    if(e.target && e.target.id === 'notif-button')
    {
        document.querySelector('.notification').innerHTML = "";
    }
});