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

    let old_psw = document.getElementById("id_old_password");
    let p1 = document.getElementById("id_new_password1");
    let p2 = document.getElementById("id_new_password2");

function pswValidation2() {

    let flag = true;
    if (old_psw.value.length < 6 || p1.value.length < 6 || p2.value.length < 6) {
        document.getElementById("psw_error").innerHTML = "password too short.";
        flag = false;
    } else {
        document.getElementById("psw_error").innerHTML = "";
    }
    if (p1.value != p2.value) {
        document.getElementById("psw_match").innerHTML = "password mismatch!";
        flag = false;
    } else {
        document.getElementById("psw_match").innerHTML = "";
    }

    return flag;
}

old_psw.onblur = p1.onblur = p2.onblur = function () {
    pswValidation2()
};