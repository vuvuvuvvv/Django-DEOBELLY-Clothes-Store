$('#btnModalError').trigger("click");
setTimeout(function () {
    $('#btnModalClose').trigger("click");
}, 1800);
let specificAddressOrder, province, district, village, productId,
    colorId, sizeId, quantity, logistic_method, notes, cartId;
cartId = $('.row-product').map(function () {
    return this.getAttribute('data-cart-id');
}).get();
productId = $('.row-product').map(function () {
    return this.getAttribute('data-id');
}).get();
quantity = $('.product-quantity').map(function () {
    return this.getAttribute('data-quantity');
}).get();;
$('#product_id').children('input').val(productId.toString());


$(document).ready(() => {
    queryAdress()
    $("#id_tel").keypress(function (e) {
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });
    let total_payment = 0;
    $('.price').each((index, el) => {
        total_payment += parseInt($(el).attr('data-total-price'));
    })
    $('#total_payment').html(new Intl.NumberFormat(['ban', 'id']).format(total_payment) + ' VND')
})

$('#provinceDataList').change(() => { 
    $('#districtDataList').prop('disabled',false);
    queryAdress(1,$('#provinceDataList').val())
});

$('#districtDataList').change(() => { 
    $('#wardsDataList').prop('disabled',false);
    queryAdress(2,$('#districtDataList').val())
});

function queryAdress(el = 0,parent_id = 0) {
    if(el == 0) {
        el = $('#provinceDataList')
        el.html('<option value="">Tỉnh/Thành phố</option>')
    } else if(el == 1) {
        el = $('#districtDataList')
        el.html('<option value="">Quận/Huyện</option>')
    } else {
        el = $('#wardsDataList')
        el.html('<option value="">Xã/Phường/Thị trấn</option>')
    }
    $.ajax({
        type: "post",
        url: "/api_geolocation_get_address/",
        data: {
            parent_id : parent_id
        },
        success: (response) => {
            let geolocation = response.location
            $.each(geolocation, (index, val)=>{
                let option = `<option value="${val['id']}">${val['name']}</option>`
                el.append(option);
            })
            
        },
        error: (jqXHR, textStatus) => {
            alert("Request failed: " + textStatus);
        }
    });
}

