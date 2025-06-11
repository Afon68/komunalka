// Когда html документ готов (прорисован)
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        console.log(`goodsInCartCount=${goodsInCartCount}`)

        var cartCount = parseInt(goodsInCartCount.text() || 0);
        console.log(`cartCount=${cartCount}`)

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");
        console.log(`product_id=${product_id}`)

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");
        console.log(`add_to_cart_url=${add_to_cart_url}`)
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
                // console.log(`data=${data.text()}`)
                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);



            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });




    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });




    // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Изменяем количество товаров в корзине
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }
    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    // При клике по значку корзины открываем всплывающее(модальное) окно
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });
    ///////////////////////////////////////////////////////////////////
    // Обработчик события радиокнопки выбора способа доставки
    function toggleRadioButton(radioname, sectionId) {
        $(radioname).change(function () {
            var selectedValue = $(this).val();
            if (selectedValue === "0") {
                $(sectionId).attr("placeholder", "Заполните поле");
            } else {
                $(sectionId).attr("placeholder", "");
            }
        });
    }
    toggleRadioButton("input[name=gas_type]", "#id_number_registered")
    toggleRadioButton("input[name=water_type]", "#id_number_registered")
    toggleRadioButton("input[name=hot_water_type]", "#id_number_registered")


    
    ///////////////////////////////////////////////////////////////////////
    
    $("input[name='gas_type']").change(function () {
        var selectedValue = $(this).val();
        // Скрываем или отображаем input ввода адреса доставки
        if (selectedValue === "0") {
            $("#lift-opt").show();
        } else {
            $("#lift-opt").hide();
        }
    });
    // Форматирования ввода номера телефона в форме (xxx) xxx-хххx
    document.getElementById('id_phone_number').addEventListener('input', function (e) {
        var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });
    // Проверяем на стороне клинта коррекность номера телефона в форме xxx-xxx-хх-хx
    $('#create_order_form').on('submit', function (event) {
        var phoneNumber = $('#id_phone_number').val();
        var regex = /^\(\d{3}\) \d{3}-\d{4}$/;

        if (!regex.test(phoneNumber)) {
            $('#phone_number_error').show();
            event.preventDefault();
        } else {
            $('#phone_number_error').hide();

            // Очистка номера телефона от скобок и тире перед отправкой формы
            var cleanedPhoneNumber = phoneNumber.replace(/[()\-\s]/g, '');
            $('#id_phone_number').val(cleanedPhoneNumber);
        }
    });
});

// function toggleSection(checkboxId, sectionId) {
//     const checkbox = document.getElementById(checkboxId);
//     const section = document.getElementById(sectionId);
//     checkbox.addEventListener('change', () => {
//         section.classList.toggle('hidden', !checkbox.checked);
//     });
//     // Показывать при начальной загрузке, если галочка уже стоит
//     section.classList.toggle('hidden', !checkbox.checked);
// }

// toggleSection('has_gas', 'gas-options');
// toggleSection('has_water', 'water-options');
// toggleSection('has_electricity', 'electrika-options');
// document.addEventListener("DOMContentLoaded", function () {
// function toggleSection(checkboxId, sectionId) {
//     const checkbox = document.getElementById(checkboxId);
//     const section = document.getElementById(sectionId);
    
        
    
//     checkbox.addEventListener('change', () => {
//         section.classList.toggle('hidden', !checkbox.checked);
//     });
//     // Показывать при начальной загрузке, если галочка уже стоит
//     section.classList.toggle('hidden', !checkbox.checked);
// }

// toggleSection('id_has_gas_checkbox', 'gas-options');
// toggleSection('id_has_water_checkbox', 'water-options');
// toggleSection('id_has_hot_water_checkbox', 'hot_water-options');
// toggleSection('id_has_electricity_checkbox', 'electrika-options');
    
// })
// toggleSection('id_has_heating', 'heating-options');
// toggleSection('id_uses_lift', 'lift-options');
// toggleSection('id_has_garbage', 'lift-options');
// toggleSection('id_has_apart_payment', 'lift-options');
// toggleSection('id_no_counter', 'lift-options');
////////////////////////////////////////////////////////////////
// document.addEventListener("DOMContentLoaded", function () {
function togglePlaceholder(checkboxId, sectionId) {
    console.log("Скрипт загружен!");
    const checkbox = document.getElementById(checkboxId);
    const input = document.getElementById(sectionId);

    checkbox.addEventListener("change", function () {
        if (checkbox.checked) {
            input.placeholder = "Заполните поле";
        } else {
            input.placeholder = "";
        }
    });
}

// if (checkbox.checked) {
//     input.placeholder = "Обязательное заполнение";
//     document.getElementById("heating-options").classList.remove("hidden");
// }

togglePlaceholder('id_has_heating', 'id_area_apartment');
togglePlaceholder('id_uses_lift', 'id_number_registered');
togglePlaceholder('id_has_garbage', 'id_number_registered');
togglePlaceholder('id_has_apart_payment', 'id_number_registered');
// })
// togglePlaceholder('id_radio', 'id_number_registered');
////////////////////////////////////////////////////////////////////////////////////////////
// document.addEventListener("DOMContentLoaded", function () {
//     const checkbox = document.getElementById("id_has_heating");
//     const input = document.getElementById("id_area_apartment");

//     checkbox.addEventListener("change", function () {
//         if (checkbox.checked) {
//             input.placeholder = "Обязательное заполнение";
//         } else {
//             input.placeholder = "";
//         }
//     });
// });
// document.addEventListener("DOMContentLoaded", function () {
//     console.log("✅ DOM загружен!");
// })
// // var successMessage = $("#jq-notification");
// let notification = document.getElementById("notification"); //$('#notification');
// // И через 7 сек. убираем
// if (notification.length > 0) {
//     setTimeout(function () {
//         notification.alert('close');
//     }, 7000);
// }


//     document.addEventListener("DOMContentLoaded", function () {
//         function toggleSection2(checkboxId, sectionId) {
//             const checkbox = document.getElementById(checkboxId);
//             const section = document.getElementById(sectionId);

//             if (checkbox && section) {
//                 function updateVisibility() {
//                     section.classList.toggle("d-none", !checkbox.checked);
//                 }
//             } else {
//                 section.classList.add("d-none");
//             }

//                 checkbox.addEventListener("change", updateVisibility);
//                 updateVisibility(); // установить начальное состояние
//             }


// toggleSection2("id_has_gas_checkbox", "id_gas_section");
// toggleSection2("id_has_water_checkbox", "id_water_section");
//     toggleSection2("id_uses_lift", "id_lift_section");
//});

// document.addEventListener("DOMContentLoaded", function () {
//     function toggleSection2(checkboxId, sectionId) {
//         console.log("Скрипт загружен!");
//         const checkbox = document.getElementById(checkboxId);
//         const section = document.getElementById(sectionId);

//         if (checkbox && section) {
//             function updateVisibility() {
//                 console.log(`Checkbox ${checkboxId} checked:`, checkbox.checked);
//                 if (checkbox.checked) {
//                     section.classList.remove("hidden");
//                 } else {
//                     section.classList.add("hidden");
//                 }
//             }

//             checkbox.addEventListener("change", updateVisibility);
//             updateVisibility(); // установить начальное состояние
//         } else {
//             console.warn("Не найден элемент:", checkboxId, sectionId);
//         }
//     }
// // });
//     toggleSection2("id_has_gas_checkbox", "id_gas_section");
//     toggleSection2("id_has_water_checkbox", "id_water_section");
//     toggleSection2("id_uses_lift", "id_lift");



