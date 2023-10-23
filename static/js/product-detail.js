let id, size, color, amount, price;
var galleryThumbs = new Swiper('.gallery-thumbs', {
    spaceBetween: 5,
    freeMode: true,
    watchSlidesVisibility: true,
    watchSlidesProgress: true,
    breakpoints: {
        0: {
            slidesPerView: 3,
        },
        992: {
            slidesPerView: 4,
        },
    }
});
var galleryTop = new Swiper('.gallery-top', {
    spaceBetween: 10,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    thumbs: {
        swiper: galleryThumbs
    },
});
// change carousel item height
// gallery-top
let productCarouselTopWidth = $('.gallery-top').outerWidth();
$('.gallery-top').css('height', productCarouselTopWidth);

// gallery-thumbs
let productCarouselThumbsItemWith = $('.gallery-thumbs .swiper-slide').outerWidth();
$('.gallery-thumbs').css('height', productCarouselThumbsItemWith);

// activation zoom plugin
var $easyzoom = $('.easyzoom').easyZoom();
//accept press number into input
$("#amountInput").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
});
$('#btnAddToCart').click(function () {
    if ($('#sth').attr('data-id') == 1) {
        window.location.href = "/login?ref=" + window.location.pathname + '?detail=' + $('.product-information').attr('data-id');
    } else {
        requestData();
    }
});
$('#btnBuyNow').click(function (e) {
    if ($('#sth').attr('data-id') == 1) {
        window.location.href = "/login?ref=" + window.location.pathname + '?detail=' + $('.product-information').attr('data-id');
    } 
    else {
        requestData(1);
    }
});

function requestData(buynow = 0) {
    id = $('.product-information').attr('data-id');
    amount = $('#amountInput').val();
    let request = $.ajax({
        url: "/cart/add-to-cart/",
        method: "POST",
        data: {
            product_id: id,
            amount: amount,
            buynow: buynow
        },
    });
    request.done(function (response) {
        $('#amount_cart').html(response.amount_cart)
        if (buynow == 0) {
            let toast = new bootstrap.Toast(document.getElementById('liveToast'));
            swal("Thành công!", "Đã thêm sản phẩm vào giỏ hàng.", "success");
        }
        
    });
    request.fail(function (response) {
        let toast = new bootstrap.Toast(document.getElementById('liveToast'));
        $('#toastNotify').html('<i class="far fa-times-circle"></i> ' + response.status);
        swal("Lỗi!", response.status, "error");
    });
}

function responsive() {
    $('#bestsellers .product-card').removeClass('d-none');
    $('#onSale .product-card').removeClass('d-none');
    if (window.matchMedia('(min-width: 1200px) and (max-width: 1400px)').matches || window.matchMedia('(min-width: 576px) and (max-width: 992px)').matches) {
        if ($('#bestsellers .product-card').length > 4) {
            $("#bestsellers .product-card:last").addClass('d-none');
        }
        if ($('#onSale .product-card').length > 4) {
            $("#onSale .product-card:last").addClass('d-none');
        }
    } else if (window.matchMedia('(min-width: 992px) and (max-width: 1200px)').matches || window.matchMedia('(max-width: 576px)').matches) {
        if ($('#bestsellers .product-card').length > 3) {
            $("#bestsellers .product-card:first, #bestsellers .product-card:last").addClass('d-none');
        }
        if ($('#onSale .product-card').length > 3) {
            $("#onSale .product-card:first, #onSale .product-card:last").addClass('d-none');
        }
    }
}

$(document).ready(function () {
    responsive();
});
$(window).resize(function () {
    responsive();
});
//accept press number into input
$("#amountInput").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
});
//validate amount
$('#amountInput').change(function () {
    if ($(this).val() == 0) {
        $(this).val(1);
        $('#notify').html('');
    } else if ($(this).val() > parseInt($('#quantity').attr('data-quantity'))) {
        $(this).val(parseInt($('#quantity').attr('data-quantity')));
        $('#notify').html($('#notify').attr('data-out-of-stock'));
        setTimeout(function () {
            $('#notify').html('');
        }, 3000);
    } else {
        $(this).val(parseInt($(this).val()));
        $('#notify').html('');
    }
});

//reduce the number of
function reduceProductQuantity() {
    if ($('#amountInput').val() > 1) {
        let amount = parseInt($('#amountInput').val());
        $('#amountInput').val(amount - 1);
    }
};

//increase the number
function increaseProductQuantity() {
    if ($('#amountInput').val() < parseInt($('#quantity').attr('data-quantity'))) {
        let amount = parseInt($('#amountInput').val());
        $('#amountInput').val(amount + 1);
    }
};

// activation zoom plugin
var $easyzoom = $('.easyzoom').easyZoom();

if (parseInt($('#quantity').attr('data-quantity')) == 0) {
    $('#btnAdd,#btnBuyNow').css('pointer-events', 'none').click((e)=>{e.preventDefault()});
    $('#notify').html('Sản phẩm không đủ để đáp ứng yêu cầu!');
    $('#amountInput').attr('disabled', true);
    $('#outOfStock').addClass('d-inline-block');
} else {
    $('#outOfStock').addClass('d-none');
}