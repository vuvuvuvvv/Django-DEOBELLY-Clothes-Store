$('form').submit( e =>{
    let email = $('#id_email').val();
    if (email) {
        e.preventDefault();
        $.ajax({
            type: "post",
            url: "/api_check_user_validated/",
            data: JSON.stringify({
                'email': email
            }),
            success: response => {
                if (!response.is_verified) {
                    swal({
                        title: "Cảnh báo!",
                        text: "Tài khoản chưa hoàn thiện thông tin! Hãy thử đăng nhập lại và hoàn thiện thông tin!",
                        icon: "warning",
                        dangerMode: true,
                        })
                } else if(response.undefind) {
                    swal({
                        title: "Lỗi!",
                        text: "Tài khoản không tồn tại! Hãy thử lại",
                        icon: "warning",
                        dangerMode: true,
                        })
                } else {
                    $("#send_confirm_mail").prop("disabled", true)
                    $("a").click( (e) => { 
                        e.preventDefault();
                    });
                    e.currentTarget.submit();
                }
            },
            error: err => {
                console.log('Error: ', err)
            }
        });
    }
})