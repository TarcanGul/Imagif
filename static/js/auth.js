document.querySelector('#sign-up-form').addEventListener('submit', function(){
    let email = document.forms["sign-up"]["email"].value;
    let password = document.forms["sign-up"]["password"].value;
    let username = document.forms["sign-up"]["username"].value;

    let signUpData = {
        "username" : username,
        "password" : password,
        "email" : email,
        "joined_user_timestamp" : getCurrentTime()
    };

    $.ajax({
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(signUpData),
        url:'/handleSignup',
        type: 'POST',
        success: function(data){
            if(data['status'] === 'success')
            {
                document.querySelector(".sign-up-response").innerHTML = "<h6>"  + data['message'] + "</h6>";
                document.querySelector(".sign-up-response").innerHTML += `<input type='submit' class='resend-button' value='Resend confirmation' />`;
                document.querySelector(".sign-up-button-container").innerHTML = "";
                /*document.querySelector('.resend-button').addEventListener('click', function(){
                    $.ajax({
                        processData: false,
                        contentType: false,
                        url: `/retry-email-config?email=${email}`
                    })
                });*/
            }
            else
            {
                if(data['reason'] === "second account with username")
                {
                    sendNotification('Username already taken.');
                }
                else if(data['reason'] === 'Already signed up')
                {
                    sendNotification('There is already a user with this confirmed email. Please use the login form.')
                }
                else if(data['reason'] === 'Email not confirmed')
                {
                    document.querySelector(".sign-up-response").innerHTML = "<h6>It seems like you did not confirm your email. Email confirmation sent. Please check " + data["email"] + ".</h6>";
                    document.querySelector(".sign-up-response").innerHTML += `<input type='submit' class='resend-button' value='Resend confirmation' />`;
                    document.querySelector(".sign-up-button-container").innerHTML = "";
                }
                else
                {
                    document.querySelector(".sign-up-response").innerHTML = "Unexpected error occured.";
                }
            }
        }
    })
});

function onMainPageLoad(data,_callback)
{
    window.location.href = data["redirect"];
    _callback();
}

document.querySelector('#login-form').addEventListener('submit', function(){
    let email = document.forms["login"]["email"].value;
    let password = document.forms["login"]["password"].value;
    let authData = {
        "email" : email,
        "password" : password
    };
        $.ajax({
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(authData),
            url: '/handleLogin',
            type: 'POST',
            success: function(data){
                console.log(data["status"]);
                if(data["status"] === "success")
                {
                    onMainPageLoad(data, function(){                       
                         document.querySelector(".notification").innerHTML = 
                        `<div class="notif-text"><h5>Logged into user ` + data["username"] + `</h5></div>
                        <div class="notif-button"><button id="notif-button">Okay</button></div>`;
                    });
                }
                else
                {
                    if(data["reason"] === "password")
                    {
                        sendNotification('Wrong password. Please try again.');
                    }
                    else if(data["reason"] = "no account")
                    {
                        sendNotification('No account with this email has been created yet. Please sign up.');
                    }
                }   
            }
        });         
});