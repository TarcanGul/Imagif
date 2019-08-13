

document.querySelector('#email-button').addEventListener('click', function(){
    var url = this.getAttribute('data-redirect');
    var email_form = 
    `
    <form name="email-change" id="email-change-form" method="post" action="${url}">
    <p>New Email<input name="email" type="email" required/></p>     
    <input class="form-element setting" type="submit" value="Confirm changes"/>

    </form>
    `;
    document.querySelector(".email-change-area").innerHTML = email_form;
});

document.querySelector('#password-button').addEventListener('click', function(){
    var url = this.getAttribute('data-redirect');
    var password_form = 
    `
    <form name="password-change" id="password-change-form" method="post" action="${url}">
    <p>Current password<input name="old_password" type="password" required/></p>     
    <p>New password<input name="new_password" type="password" required/></p>     
    <input id="password-confirm" class="form-element setting" type="submit" value="Confirm changes"/>
    </form>
    `;
    document.querySelector(".password-change-area").innerHTML = password_form;
});