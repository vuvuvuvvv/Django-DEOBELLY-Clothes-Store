let category, type, typeName, cursor, sort, keyWord;

let toastLive = document.getElementById('liveToast');


//get param in url
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const parseUrlQuery = (value) => {
    let urlParams = new URL(value).searchParams
    return Array.from(urlParams.keys()).reduce((acc, key) => {
        acc[key] = urlParams.getAll(key)
        return acc
    }, {})
}

//Check type in param
let myUrl = location;
if (parseUrlQuery(myUrl)['type'] !== undefined) {
    type = parseUrlQuery(myUrl)['type'][0];
}

// Get search query 
let keySearch = $('#content-search').attr('data-query');

//send request to get link & title
jQuery(document).ready(function () {
    $('#current_page').val(0);
    requestParam()
    // requestData()
});

function requestParam() {
    if (keySearch != null && keySearch != undefined && keySearch != '') {
        keyWord = keySearch;
        $('#notify-search').removeClass('d-none');
        $('#content-search').html(keyWord);
    } else {
        if (keyWord != null && keyWord != undefined && keyWord != '') {
            $('#notify-search').removeClass('d-none');
            $('#content-search').html(keyWord);
        } else {
            $('#notify-search').addClass('d-none');
            $('#content-search').html('');
        }
    }
    requestData();
}

let checkboxes = $('input[type=checkbox]');
$('.accordion-button').click(function () {
    truncateData()
    checkboxes.prop("checked", false);
    $('#current_page').val(0);
    if (!$(this).hasClass('collapsed')) {
        type = $(this).attr('data-type');
        typeName = $(this).attr('data-type-name');
    } else {
        type = typeName = null;
    }
    requestParam();
});

let categoryCb = $('.category-checkbox input[type=checkbox]');
categoryCb.change(function () {
    truncateData()
    category = getCheckedBoxes(categoryCb);
    $('#current_page').val(0);
    requestData();
});

// sort
$(".lowToHigh").click(function () {
    sort = 1;
    $('#current_page').val(0);
    cursor = null;
    requestData();
});
$(".highToLow").click(function () {
    sort = 2;
    $('#current_page').val(0);
    cursor = null;
    requestData();
});
$(".sortByDate").click(function () {
    sort = 3;
    $('#current_page').val(0);
    cursor = null;
    requestData();
});

//get value from checkboxes
function getCheckedBoxes(checkbox) {
    return checkbox.filter(":checked")
        .map(function () {
            return $(this).attr('data-value');
        })
        .get();
}

function requestData() {
    $.ajax({
        url: "/api_product_filter/", // send request to
        type: "POST", // sending method
        data: JSON.stringify({
            'cate': category,
            'cursor': cursor,
            'type': type,
            'sort': sort,
            'search': keyWord,
        }), // sending data
        success: response => {
            // let arrRes = $.parseJSON(response);
            let arrRes = response;
            if (typeName !== null) {
                $('#category-name').html(typeName);
                $('#offcanvas-category-name').html(typeName);
            } else {
                $('#category-name').html($('#category-name').attr('data-value'));
                $('#offcanvas-category-name').html($('#offcanvas-category-name').attr('data-value'));
            }
            if (arrRes.status === 1) {
                $('#pagination').show();
                let result = "";
                for (let i = 0; i < arrRes.products.length; i++) {
                    let selling_price = new Intl.NumberFormat(['ban', 'id']).format(arrRes.products[i].selling_price);
                    let regular_price = new Intl.NumberFormat(['ban', 'id']).format(arrRes.products[i].regular_price);
                    let discount = parseInt(arrRes.products[i].discount);
                    result += `<div class="col-12 col-sm-6 col-lg-4 col-xl-3 mx-0 mb-3 mb-md-4 py-3 overflow-hidden">
                                <a href="/shop/detail?slug=${ arrRes.products[i].slug }" class="text-dark text-decoration-none">
                                    <div class='product-card w-100'>
                                        <div class='product-image'>
                                            <img src="/images/${ arrRes.products[i].image}" loading='lazy'>
                                        </div>
                                        <div class='product-info'>
                                            <div class='product-price'>
                                                <span class="px-0 fw-bold mt-2 p-price">
                                                    ${
                                                        !isNaN(discount) && discount !== 0 ?
                                                        `<span class="text-decoration-line-through text-dark fw-light fs-regular-price">${ regular_price }VND</span> <span class="text-danger">${new Intl.NumberFormat(['ban', 'id']).format(arrRes.products[i].sale_price)}VND</span>`:
                                                        `${ selling_price }VND`
                                                    }
                                                </span>
                                            </div>
                                            <div class='product-name position-relative'>${ arrRes.products[i].name }</div>
                                        </div>
                                        <!--               
                                        <div class='product-button'>
                                            <a class='btn btn-buy-now fs-2' href='#'>+</a>
                                            <span class='fw-light'>|</span>
                                            <button class='btn btn-add fs-2' onclick="javascript:void(0)">&#9829;</button>
                                        </div> 
                                        -->
                                        ${ !isNaN(discount) && discount !== 0 ? `<div class="product-discount"><span>-${ discount }%</span></div>`:''}
                                    </div>
                                </a>
                            </div>`;
                }
                $("#result").html(result);
                //show pagination
                let number_of_items = arrRes.amount;
                let product_per_page = 8
                let number_of_pages = Math.ceil(number_of_items / product_per_page);
                console.log(number_of_pages, number_of_items);
                jQuery(document).ready(function () {
                    let navigation_html = '<a class="first_link" href="javascript:first();">&#10094;&#10094;</a><a class="previous_link" href="javascript:previous();">&#10094;</a>';
                    let current_link = 0;
                    while (number_of_pages > current_link) {
                        navigation_html += ' <a class="page_link" href="javascript:go_to_page(' + current_link + ')" id="page' + (current_link + 1) + '">' + (current_link + 1) + '</a>';
                        current_link++;
                    }
                    navigation_html += ' <a class="next_link" href="javascript:next();">&#10095;</a> <a class="last_link" href="javascript:last(' + number_of_pages + ');">&#10095;&#10095;</a>';
                    $('#page_navigation').html(navigation_html);
                    let active = parseInt($('#current_page').val()) + 1;
                    $('#page' + active + '').addClass('p-active bg-dark text-light');
                    //hide button when first or last page is active
                    if (active == 1) {
                        $('.first_link, .previous_link').css({
                            'display': 'none',
                        });
                    } else if (active == current_link) {
                        $('.next_link, .last_link').css({
                            'display': 'none',
                        });
                    }
                    if (number_of_pages == 1) {
                        $('#page_navigation').hide();
                    } else {
                        $('#page_navigation').show();
                    }
                    if (number_of_pages > 3) {
                        if (active < 2) {
                            $('.page_link').addClass('d-none');
                            let i = 1;
                            while (i < 4) {
                                $('#page' + i + '').removeClass('d-none');
                                i++;
                            }
                        } else if (active > current_link - 1) {
                            $('.page_link').addClass('d-none');
                            let i = current_link;
                            while (i > current_link - 3) {
                                $('#page' + i + '').removeClass('d-none');
                                i--;
                            }
                        } else {
                            $('.page_link').addClass('d-none');
                            $('#page' + (active - 1) + ',#page' + active + ',#page' + (active + 1) + '').removeClass('d-none');
                        }
                    }
                });
                $('html').scrollTop(0);
            } else {
                let result = '<div class="text-center col-12 p-0"><h1 class="mainColor"><i class="fab fa-sistrix"></i></h1><h5 class="mainColor"><i>Không có sản phẩm để hiển thị</i></h5><h5 class="mainColor"><i>Bạn hãy thử tìm kiếm lại!</i></h5></div>';
                $('#pagination').hide();
                $("#result").html(result);
                $('html').scrollTop(0);
            }
        },
        error: (jqXHR, textStatus) => {
            alert("Request failed: " + textStatus); // check errors
        }
    })

    if(category != null) {
        $('#sm-offcanvas-close').trigger('click');
    }
}
function first() {
    if ($('#current_page').val() != 0) {
        go_to_page(0);
    }
}

function previous() {
    let new_page = parseInt($('#current_page').val()) - 1;
    if ($('#current_page').val() != 0) {
        go_to_page(new_page);
    }
}

function next() {
    let new_page = parseInt($('#current_page').val()) + 1;
    if ($('#current_page').val() != ($("#page_navigation").children(".page_link").length - 1)) {
        go_to_page(new_page);
    }
}

function last() {
    let number_of_pages = $("#page_navigation").children(".page_link").length;
    if ($('#current_page').val() != number_of_pages - 1) {
        go_to_page(number_of_pages - 1);
    }
}

function go_to_page(page_num) {
    cursor = page_num;
    $('#current_page').val(page_num);
    requestData();
}
//search data with enter key press
$("#key-word").keypress(function (event) {
    if (event.which == 13) {
        search();
    }
});

$('#remove-keyword').click(function () {
    keyWord = keySearch = null;
    $('#notify-search').addClass('d-none');
    requestData();
});

function search() {
    truncateData();
    if ($.trim($("#key-word").val()) != '') {
        keyWord  = $("#key-word").val()
        requestParam()
    }
}

function truncateData() {
    category = null;
    type = null;
    typeName = null;
    cursor = null;
    sort = null;
    keyWord = null;
    keySearch = null;
    $("#content-search").html('').attr('data-query','');
}