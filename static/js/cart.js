$('#btnModalSuccess').trigger("click");
setTimeout(function () {
    $('#btnModalClose').trigger("click");
    
}, 1800);
let amount, id;
let total_price = 0;

$(document).ready(() => {
    totalPayment();
});

$(".amountInput").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
}).each((index,item) => {
    $(item).change(() => {
        let id = item.getAttribute("data-id");
        let inputAmount = document.getElementById('amount_' + id);
        let productPrice = document.getElementById('price_' + id);
        let existingProduct = parseInt(document.getElementById('existing_product_' + id).getAttribute('data-existing-product'));;
        let totalPriceProduct = document.getElementById('total_product_price_' + id);
        let notify = document.getElementById('notify_' + id)
        if (inputAmount.value == 0 || inputAmount.value == '') {
            inputAmount.value = 1;
            notify.classList.add('d-none');
        } else if (inputAmount.value > existingProduct) {
            inputAmount.value = existingProduct;
            notify.classList.remove('d-none');
            setTimeout(function () {
                notify.classList.add('d-none');
            }, 2000)
        } else {
            notify.classList.add('d-none');
            inputAmount.val(inputAmount.value);
        }
        updateAmount(id, inputAmount.value);
        let total_price = parseInt(productPrice.getAttribute('data-price')) * inputAmount.value;
        let total_price_format = new Intl.NumberFormat(['ban', 'id']).format(total_price);
        totalPriceProduct.textContent = total_price_format + ' VND';
        totalPriceProduct.setAttribute('data-total-price', total_price);
        totalPayment();
    });
});

function totalPayment() {
    total_price = 0;
    $('.total-price').each((index, val) => {
        total_price += parseInt($(val).attr('data-total-price'));
    })
    let total_price_format = new Intl.NumberFormat(['ban', 'id']).format(total_price);
    $("#total_payment").html(total_price_format + ' VND');
}

$('.btnDESC').each((index, val) => {
    $(val).click(() => {
        let id = $(val).attr('data-id');
        let inputAmount = document.getElementById('amount_' + id);
        let productPrice = document.getElementById('price_' + id);
        let totalPriceProduct = document.getElementById('total_product_price_' + id);
        if (inputAmount.value > 1) {
            inputAmount.value = parseInt(inputAmount.value) - 1;
            updateAmount(id, inputAmount.value);
            let total_price = parseInt(productPrice.getAttribute('data-price')) * inputAmount.value;
            let total_price_format = new Intl.NumberFormat(['ban', 'id']).format(total_price);
            totalPriceProduct.textContent = total_price_format + ' VND';
            totalPriceProduct.setAttribute('data-total-price', total_price);
        }
        totalPayment();
    });
});

$('.btnASC').each((index, val) => {
    $(val).click(() => {
        let id = $(val).attr('data-id');
        let inputAmount = document.getElementById('amount_' + id);
        let productPrice = document.getElementById('price_' + id);
        let totalPriceProduct = document.getElementById('total_product_price_' + id);
        let existingProduct = parseInt(document.getElementById('existing_product_' + id).getAttribute('data-existing-product'));
        let notify = document.getElementById('notify_' + id)
        if (inputAmount.value < existingProduct) {
            notify.classList.add('d-none');
            inputAmount.value = parseInt(inputAmount.value) + 1;
        } else {
            inputAmount.value = existingProduct;
            notify.classList.remove('d-none');
            setTimeout(function () {
                notify.classList.add('d-none');
            }, 2000)
        }
        updateAmount(id, inputAmount.value);
        let total_price = parseInt(productPrice.getAttribute('data-price')) * inputAmount.value;
        let total_price_format = new Intl.NumberFormat(['ban', 'id']).format(total_price);
        totalPriceProduct.textContent = total_price_format + ' VND';
        totalPriceProduct.setAttribute('data-total-price', total_price);
        totalPayment();
    });
});

function updateAmount(product_id, amount) {
    $.ajax({
        url: "/cart/update-cart/",
        method: "POST",
        data: {
            product_id: product_id,
            amount: amount,
        },
        error: (jqXHR, textStatus) => {
            alert("Request failed: " + textStatus); // check errors
        }
});
}

function deleteCart(e) {
    $.ajax({
        url: "/cart/delete-cart/",
        method: "POST",
        data: {
            product_id: $(e).attr('data-id'),
        },
        success: (response)=>{
            $('.cart-item').each((index, val) => {
                if($(val).attr('data-id') == $(e).attr('data-id')) {
                    $(val).remove();
                }
            });
            $('#amount_cart').html(response.amount_cart)
            totalPayment();
        },
        error: (jqXHR, textStatus) => {
            alert("Request failed: " + textStatus); // check errors
        }
    });
}