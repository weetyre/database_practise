


// 隐藏div,打开form1
function form_add_host(){
    console.log(1)
    let x = document.getElementById("content");
    x.style.display = "none";
    let y = document.getElementById('form_add_host');
    y.style.display = 'block';

}
// 关闭表单1
function form_close_host_submit(){
    console.log(2)
    let x = document.getElementById("content");
    x.style.display = "block";
    let y = document.getElementById('form_add_host')
    y.style.display = 'none';
}
// 提交表单1,POST数据至服务器，增加小区住户
function form_add_host_submit() {
    var sex = document.getElementsByName("sex");
    if((sex[0].checked==false)&&(sex[1].checked==false)) {
        return false
    }

     if($("#form1_hos_name").val()==""||$("#form1_contact").val()==""
         ||$("#form1_bonus").val()==""||$("#form1_login_nam").val()==""
         ||$("#form1_pass").val()=="" )
     {
        return false;
     }

    $('#form1_submit').submit();
    console.log('submit')
}
function form_update_host_submit(type){
    $('#form1_update').submit();
}

function form_host_detail(id, form_type){
    if(form_type=='form1'){
        console.log(id);
        let element = document.getElementById('form1_detail');
        element.style.display = 'inline';
    }else {
        let element = document.getElementById('form2_detail');
        element.style.display = 'inline';
    }


     $.ajax({
        url: '/bussiness_checkin_detail/',
        // 为了避免加入csrf_token令牌，所以使用GET请求
        type: 'GET',
        // 返回的数据用于创建一个操作记录
        data: {
            content_type: form_type,
            id: id,
            operate_type: 'detail',
        },
        cache: false,
        success: function (data) {
            if(form_type=='form2'){
                 $("#form2_detail_text").html(data);
            }
            else{
               $("#form1_detail_text").html(data);
            }

            console.log(data)
            },
        error: function (err) {
            console.log('err')
        }
        });
        return false;



}
function form1_detail_close(form_type) {
    if(form_type=='form1'){
        let element = document.getElementById('form1_detail');
        element.style.display = 'none';
    }else{
        let element = document.getElementById('form2_detail');
        element.style.display = 'none';
    }


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


function finish_advice(advice_id){
     $.ajax({
        url: '/management_manager_advice_finish/',
        // 为了避免加入csrf_token令牌，所以使用GET请求
        type: 'GET',
        // 返回的数据用于创建一个操作记录
        data: {
            id: advice_id,
            operate_type: 'finish',
        },
        cache: false,
        success: function (data) {
            let e = document.getElementById(advice_id)
            e.style.display = 'none';
            console.log(data)
            },
        error: function (err) {
            console.log('err')
        }
        });
        return false;

}



function share_advice(advice_id){
     ip_id = '#input_' + advice_id
     sha_id = $(ip_id).val()
     $.ajax({
        url: '/management_manager_advice_share/',
        // 为了避免加入csrf_token令牌，所以使用GET请求
        type: 'GET',
        // 返回的数据用于创建一个操作记录
        data: {
            id: advice_id,
            operate_type: 'finish',
            share_id: sha_id
        },
        cache: false,
        success: function (data) {
            if (data=='404'){
                me_id = '#message_' + advice_id
                $(me_id).html( '<p style="color:red;margin: 0px 0px  0px 20px" >fail to send</p>') ;
                console.log('fail to send')
            }else{
                me_id = '#message_' + advice_id
                  $(me_id).html( '\'<p style="color:lightseagreen;margin: 0px 0px  0px 20px" >success to send</p>\'') ;
                console.log('success send')
            }
            },
        error: function (err) {
            console.log('err')
        }
        });
        return false;

}