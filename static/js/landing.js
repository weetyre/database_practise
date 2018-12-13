window.onload=function () {
    //倒计时跳转页面
    var i = 2;
    var num = 0;
    time = setInterval(function(){
        num = --i;
        if(num<0){
            clearInterval(time);
            location = "/profile";
        }
    },1000)
}