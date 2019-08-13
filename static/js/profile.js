

document.querySelector('#email-button').addEventListener('click', function(){
    var url = this.getAttribute('data-redirect');
    var email_form = 
    `
    <form name="email-change" id="email-change-form" method="post" action="${url}">
    <p>New Email<input name="email" type="email" required/></p>     
    <input class="form-element" type="submit" value="Confirm changes"/>

    </form>
    `;
    document.querySelector(".email-change-area").innerHTML = email_form;
});