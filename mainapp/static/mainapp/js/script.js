$(document).ready(() => {
    // Top panel on click: add to cart, search header
    let $topPnl = $('.top_panel');
    let $pnlMsk = $('.layer');


    // добавление продукта в корзину
    $('.btn_add_to_cart a').on('click', function (event) {
        $topPnl.addClass('show');
        $pnlMsk.addClass('layer-is-visible');

        // собираем данные для корзины
        const productSlug = $(this).attr('data-slug')
        const productId = $(this).attr('data-id')
        const product_quantity = parseInt($('#quantity_1').val())
        const sizeId = $('#size_select_id').val()
        // console.log(`Selected size id: ${size_id}`)
        // console.log(product_quantity)


        add_to_cart([{
            id: productId,
            quantity: product_quantity,
            size_id: sizeId,
            update: false,
        }], refresh=false)


    });


    const add_to_cart = (products, refresh) => {
        // посылаем запрос на сервер для обновления корзины
        $.ajax({
            type: 'POST',
            url: '/api/add_to_cart/',
            data: JSON.stringify({
                products
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            dataType: 'json',
            success: (data) => {
                // console.log(data)
                $('#quantity_on_top_popup').text(data.product_quantity)
                get_cart()
            },
            fail: (error) => {
                console.log(error)
            },
            complete: () => {
                if (refresh) {
                    location.reload()
                }

            }
        })
    }


    // обновляем данные корзины

    const get_cart = () => {
        $.get('/api/get_cart_items/', (response) => {
            update_cart_view(JSON.parse(response))
        }).fail((error) => {
            console.log(error)
        })
    }

    const update_cart_view = (data) => {
        let cart_total_quantity = 0
        let cart_total_price = 0

        // находим список корзины
        let cart_list = $('#cart ul')

        // очищаем
        cart_list.empty()
        for (const product of data) {
            cart_total_quantity += parseInt(product.quantity)
            cart_total_price += parseFloat(product.total_price)
            cart_list.append(
                `<li>
                    <a href="${product.url}">
                        <figure><img
                            src="${product.image}"
                            data-src="${product.image}" alt="product image"
                            width="50" height="50" class="lazy"></figure>
                        <strong><span>${product.quantity}x ${product.product_name}</span>${product.price}</strong>
                    </a>
                    <a href="#" class="action" "><i data-id="${product.id}" class="ti-trash"></i></a>
                </li>`
            )

            // удаление продукта из корзины
            $("i.ti-trash").on('click', function (event) {
                const productID = $(this).attr('data-id')
                $.ajax({
                    type: 'POST',
                    url: '/api/remove_cart_item/',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    data: JSON.stringify({
                        id: productID,
                    }),
                    dataType: 'json',

                    success: (data) => {
                        $(`#row-item-${productID}`).remove()
                        $('#subtotal-price').html(`<span>Цена</span> ${data.subtotal} ₽`)
                        // $('#total-price').html(`<span>Итого</span> ${data.total} ₽`)
                        get_cart()
                    },
                    fail: (error) => {
                        console.log(error)
                    }


                })
            })

        }
        $('.cart_bt strong').text(`${cart_total_quantity}`)
        $('#cart-header-total').text(`${cart_total_price} ₽`)
        // $('#cart-header-total').text(`${cart_total_price} ₽`)


    }
    // console.log(csrfToken)
    get_cart()

    $('#update_basket').click((e) => {
        let products = []
        $('input.qty2').each((i, el) => {
            const productId = $(el).attr("data-productId")
            const qty = $(el).val()
            const sizeId = $(el).attr("data-sizeId")
            products.push({
                id: productId,
                quantity: qty,
                size_id: sizeId,
                update: true,
            })
        })

        add_to_cart(products, refresh=true)


    })
})