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
                window.location.href = data['redirect'];
            }
            else
            {
                if(data['reason'] === "second account with email")
                {
                    document.querySelector(".sign-up-response").innerHTML = "There is already an account made with the specified mail. Please try another mail.";
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
                        document.querySelector(".login-response").innerHTML = 'Wrong password. Please try again.';
                    }
                    else if(data["reason"] = "no account")
                    {
                        document.querySelector(".login-response").innerHTML = 'No account with this email has been created yet. Please sign up.</h3>';
                    }
                }   
            }
        });         
});