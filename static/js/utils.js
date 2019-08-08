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