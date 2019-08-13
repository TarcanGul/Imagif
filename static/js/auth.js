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
            document.querySelector('.sign-up-response').innerHTML = "";
            if(data['status'] === 'success')
            {
                sendNotification(data['message']);
                document.querySelector(".sign-up-button-container").innerHTML = `<button id="sign-up-resend" class='resend-button form-element'>Resend confirmation</button>`;
            }
            else
            {
                if(data['reason'] === "second account with username")
                {
                    sendNotification('Username already taken.');
                }
                else if(data['reason'] === 'Already signed up')
                {
                    sendNotification('There is already a user with this confirmed email.')
                }
                else
                {
                    sendNotification("Unexpected error occured.");
                }
            }
        }
    });
    document.querySelector('.sign-up-response').innerHTML = `<h4 class="loading-element">Processing...</h4>`;
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
                    document.querySelector('.login-response').innerHTML = "";  
                    if(data["reason"] === "password")
                    {
                        sendNotification('Wrong password. Please try again.');
                    }
                    else if(data["reason"] === "no account")
                    {
                        sendNotification('No account with this email has been created yet. Please sign up.');
                    }
                    else if(data["reason"] === "email not verified")
                    {
                        sendNotification("It seems like you did not confirm your email. Email confirmation sent. Please check " + data["email"] + ". If you want to resend confirmation, click resend confirmation in the place of old login button.");
                        document.querySelector(".login-button-container").innerHTML = `<button id="login-resend" class='resend-button form-element'>Resend confirmation</button>`;
                    }
                }   
            }
        });
        document.querySelector('.login-response').innerHTML = `<h4 class="loading-element">Processing...</h4>`;         
});

document.addEventListener('click', function(e){
    if(e.target && e.target.classList.contains('resend-button'))
    {
        let email = e.target.id == 'login-resend' ? document.forms["login"]["email"].value : document.forms["sign-up"]["email"].value;
        let data = { "email" :  email };
        $.ajax({
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(data),
            url: "/retry-email-config",
            type: 'POST'
        })
        .done(function(data){
            if(data['status'] === 'success')
            {
                sendNotification(data['message']);
            }
        })
    }
});