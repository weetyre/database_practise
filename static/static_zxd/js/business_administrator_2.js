function form_add_host(){
    console.log(1)
    let x = document.getElementById("content");
    x.style.display = "none";
    let y = document.getElementById('form_add_host');
    y.style.display = 'block';

}

function form_close_host_submit(){
    console.log(2)
    let x = document.getElementById("content");
    x.style.display = "block";
    let y = document.getElementById('form_add_host')
    y.style.display = 'none';
}
function form_host_delete(id,form_type) {
    console.log(id)
    $.ajax({
        url: '/bussiness_checkin_delete/',
        // 为了避免加入csrf_token令牌，所以使用GET请求
        type: 'GET',
        // 返回的数据用于创建一个操作记录
        data: {
            content_type: form_type,
            id: id,
            operate_type: 'delete',
        },
        cache: false,
        success: function (data) {
             $("#allBody").html(data);
            console.log(data)
            },
        error: function (err) {
            console.log('err')
        }
        });
        return false;

}

function form_add_host_submit() {
    $('#form1_submit').submit();
    console.log('submit')
}
function form_update_host_submit(type){
    $('#form1_update').submit();
}
