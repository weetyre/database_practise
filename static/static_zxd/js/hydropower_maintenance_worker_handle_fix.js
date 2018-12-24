function handle_fix(fix_service_id){
    $.ajax({
                url: '/bussiness_fix_handle/',
                type: 'GET',
            data: {
                id: fix_service_id,
                operate_type: 'complete',
            },
            cache: false,
            success: function (data) {
                if(data == '1'){
                    let e = '#handle_fix_info' + fix_service_id;
                    $(e).html(' <p class="btn btn-success">已完成</p>');
                }
                console.log(data);
            },
            error: function (err) {
                console.log(err);
            }
            });
}