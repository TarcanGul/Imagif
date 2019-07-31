// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyBewX9k6W7DZECtGjChZtiog9n1vhqLO9w",
    authDomain: "imagif-199a8.firebaseapp.com",
    databaseURL: "https://imagif-199a8.firebaseio.com",
    projectId: "imagif-199a8",
    storageBucket: "",
    messagingSenderId: "79256708094",
    appId: "1:79256708094:web:49cafe3feeca2510"
};
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);

    document.querySelector("#sign-up-form").addEventListener('submit', function(){
    let email = document.forms["sign-up"]["email"].value;
    let password = document.forms["sign-up"]["password"].value;
    firebase.auth().createUserWithEmailAndPassword(email, password).then(function(){
        document.querySelector(".on-sign-up-success").innerHTML = "Sign-up successful!";
        //Request for database.
    }
    ).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;
    console.log(errorMessage);
    });
});

document.querySelector('#login-form').addEventListener('submit', function(){
    console.log("button pressed");
    let email = document.forms["login"]["email"].value;
    let password = document.forms["login"]["password"].value;
    let authData = {
        "email" : email,
        "password" : password
    };
    firebase.auth().signInWithEmailAndPassword(email, password).then(function(){
        console.log("email successful");
        $.ajax({
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(authData),
            url: '/handleLogin',
            type: 'POST',
            success: function(data){
                console.log("Successfully connected the server.");
                console.log(data["redirect"]);
                window.location.href = data["redirect"];
            }
        });         
    }).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;
    console.log(errorMessage);
    });
});