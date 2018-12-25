function handle_fix(fix_service_id, operate) {
    "use strict";

    switch (operate) {
        case 'complete':
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
                    console.log('complete');
                    let com = 'complete_' + fix_service_id;
                    let ele = document.getElementById(com);
                    ele.style.display = 'none';
                }
                console.log(data);
            },
            error: function (err) {
                console.log(err);
            }
            });
            return;

        case 'share':
            let ip = '#input_' + fix_service_id;
            let mg = '#message_' + fix_service_id;
            if($(ip).val() == ''){
                $(mg).html('null');
                return;
            }
            $.ajax({
                url: '/bussiness_fix_handle/',
                type: 'GET',
                data: {
                    id: fix_service_id,
                    fix_worker: $(ip).val(),
                    operate_type: 'share',
                },
                cache: false,
                success: function (data) {
                    let com = '#share_fix_' + fix_service_id;
                    let mg = '#message_' + fix_service_id;
                    if(data == '2'){
                        let mes = '<input readonly="readonly" class="form-control"  style="width: 200px;margin: 0px 10px  0px 0px" value="'+ $(ip).val() +'"> <li class=""><span class="btn btn-info ">受理</span></li>';
                        $(com).html(mes);
                    }else if (data == '500'){
                        $(mg).html('员工忙碌');
                    }else{
                        $(mg).html('失败');
                    }
                    console.log(data);
                 },
                error: function (err) {
                    console.log(err);
                 }
                });
                break;

        default:
            break;
    }


}