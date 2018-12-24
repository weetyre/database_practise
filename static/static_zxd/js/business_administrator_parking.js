function park_handle(gar_num,par_location,operate){
    switch (operate) {
        case 'add':
            var x = document.getElementById('content')
            x.style.display = 'none';
            var y = document.getElementById('add_park');
            y.style.display = 'block';
            return;

        case 'concel_add':
            var x = document.getElementById('content')
            x.style.display = 'block';
            var y = document.getElementById('add_park');
            y.style.display = 'none';
            return;

        case 'delete':
            $.ajax({
                url: '/bussiness_park_handle/',
                type: 'GET',
                data: {
                    operate: operate,
                    gar_num: gar_num,
                    par_location: par_location,
                },
                cache: false,
                success: function (data) {
                    let tbody = document.getElementById('table_tbody');
                    tbody.innerHTML = data;
                },
                error: function (err) {
                    console.log('err');
                }
            });
            break;

        case 'add_post':
            if($('#gar_num').val()==""||$('#price').val()=="" ||
                $('#par_id').val()==""||$('#rent').val()=="")
            {
                $('#error').html("<h5 style='color:red'>不能为空</h5>");
                 console.log(2);
                return false;
            }$('#error').html("");
            $.ajax({
                url: '/bussiness_park_handle/',
                type: 'GET',
                data: {
                    operate: operate,
                    gar_num: $('#gar_num').val(),
                    par_location: $('#par_id').val(),
                    price: $('#price').val(),
                    rent: $('#rent').val(),
                },
                cache: false,
                success: function (data) {
                    if(data == '404'){
                        $('#error').html("<h5 style='color:red'>添加失败</h5>");
                    }else{
                        var x = document.getElementById('content');
                        x.style.display = 'block';
                        var y = document.getElementById('add_park');
                        y.style.display = 'none';
                        var tbody = document.getElementById('table_tbody');
                        tbody.innerHTML = data;
                        return false;
                    }
                },
                error: function (err) {
                    console.log('err');
                }
            });
            break;
        case 'update':
            $('#form1_update_park').submit()
            break;
        case 'detail':
            $.ajax({
                url: '/bussiness_park_handle/',
                type: 'GET',
                data: {
                    operate: operate,
                    gar_num: gar_num,
                    par_location: par_location,
                },
                cache: false,
                success: function (data) {
                    console.log(data)
                    $('#detail_park_modify_2').html(data);
                },
                error: function (err) {
                    console.log('err');
                }
            });
        break;
        case 'close':
            $('#detail_park_modify_2').html('');
            break;  

        default:
            break;
    }
    console.log(1);

}