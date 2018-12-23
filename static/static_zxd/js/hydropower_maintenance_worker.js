function form_add_expense_submit() {
    if($('#form1_expense_duty_id').val()==''||$('#form1_expense_amount').val()==''){
        $('#error').innerHTML  = '输入不完整';
        return false;
    }
     console.log(11);
    $('#form1_expense_submit').submit();
}
function form_add_fix_submit(){
      if($('#form1_equip_id').val()==''||$('#form1_worker_id').val()==''){
        $('#error').html('输入不完整');
        return false;
    }
     console.log(11);
    $('#form1_add_fix_submit').submit();
}
function form_add_equip_submit() {
    if($('#form1_equip_content').val()==''){
        $('#error2').html('输入不完整');
        return false;
    }
    $('#form1_add_equip_submit').submit();
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