document.querySelector('#sign-up-form').addEventListener('submit', function(){
    let email = document.forms["sign-up"]["email"].value;
    let password = document.forms["sign-up"]["password"].value;
    let username = document.forms["sign-up"]["username"].value;

    let signUpData = {
        "username" : username,
        "password" : password,
        "email" : email
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
                    window.location.href = data["redirect"];
                }
                else
                {
                    console.log(data["reason"]);
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