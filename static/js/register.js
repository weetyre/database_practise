var email = document.getElementById("id_email");

function emailValidation() {
    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var email_str = email.value;
    if (!reg.test(email_str)) {
        document.getElementById("error_show").innerHTML = "enter a valid email address.";
        return false;
    } else {
        document.getElementById("error_show").innerHTML = "";
        return true;
    }
}

email.onblur = function () {
    emailValidation()
};

var psw1 = document.getElementById("id_password");
var psw2 = document.getElementById("id_password_confirmation");

function passwordValidation() {
    let flag = true;
    if (psw1.value.length < 6 || psw2.value.length < 6) {
        document.getElementById("psw_error").innerHTML = "password too short.";
        flag = false;
    } else {
        document.getElementById("psw_error").innerHTML = "";
    }
    if (psw1.value != psw2.value) {
        document.getElementById("psw_match").innerHTML = "password mismatch!";
        flag = false;
    } else {
        document.getElementById("psw_match").innerHTML = "";
    }

    return flag;
}

psw1.onblur = psw2.onblur = function () {
    passwordValidation()
};


var username = document.getElementById("id_username");

function usernameValidation() {
    var reg2 = /^[a-z]+$/;
    var username_value = username.value;
    if (!reg2.test(username_value)) {
        document.getElementById("name_error").innerHTML = "username has illegal characters.";
        return false;
    } else {
        document.getElementById("name_error").innerHTML = "";
        return true;
    }
}

username.onblur = function () {
    usernameValidation()
};


function validation() {
    return emailValidation() && passwordValidation() && usernameValidation();
}