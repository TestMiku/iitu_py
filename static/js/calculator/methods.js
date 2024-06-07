function flashBorderColor(elementId) {
    location.href = "#" + elementId

    let element = document.getElementById(elementId);

    if (element) {
        let originalBorderStyle = element.style.border;

        element.style.border = "3px solid red";

        setTimeout(function () {
            element.style.border = originalBorderStyle;
        }, 3000);
    }
}


function set_text_report() {
    let trs = document.getElementsByClassName("tr-position");
    let text = "";
    let is_previshenie = false

    for (let i = 0; i < trs.length; i++) { // Замените tr_danger на trs
        let spans = trs[i].getElementsByTagName("span");

        if (spans.length > 0 && spans[0].innerHTML !== "") {
            let customInfo = trs[i].getElementsByClassName("custom-info");

            if (customInfo.length > 0) {
                text += "<p>" + spans[0].innerHTML + " - <a class='text-danger' onclick=\"flashBorderColor('" + trs[i].id + "')\">" + customInfo[0].innerHTML + "</a></p>";
            }
        }
    }

    if (text !== "") {
        document.getElementById("notes-info").style.display = "initial";
        document.getElementById("margin-delete").style.display = "none";
        document.getElementById("notes-info-text").innerHTML = text;
        is_previshenie = true
    }
    return is_previshenie
}


function change_dangers_count() {
    let notes = document.getElementsByClassName("position_notes");
    let sum = 0;
    if (notes) {
        for (let i = 0; i < notes.length; i++) {
            if (notes[i].innerHTML != "") {
                sum += 1
            }
        }
        DRC = document.getElementById("danger-rows-couts");
        if (DRC) {
            DRC.innerHTML = sum
        }
    }
}


function notification_count() {
    var dangerAlert = document.getElementById("dangerAlertCount");
    // console.log(dangerAlert.innerHTML)
    dangerAlert.style.display = "initial"

    setTimeout(function () {
        dangerAlert.style.display = "none";
    }, 3000);
}

function notification_price() {
    var dangerAlert = document.getElementById("dangerAlertPrice");
    dangerAlert.style.display = "initial"

    setTimeout(function () {
        dangerAlert.style.display = "none";
    }, 3000);
}


function tr_danger(id, max_count, max_price, count_value, price_value) {
    var table_row = document.getElementById(("tr-" + id));
    let is_danger = parseFloat(max_count) < parseFloat(count_value) || parseFloat(max_price) < parseFloat(price_value)

    if (is_danger) {
        table_row.style.backgroundColor = "#ffd3d3"
    } else {
        table_row.style.backgroundColor = ""
    }
}

function float_parser(input) {
    let number = 0;
    number = parseFloat(input);
    let str = input.toString()
    let new_str = ""
    let ar = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ","]
    for (let i = 0; i < str.length; i++) {
        for (let j = 0; j < ar.length; j++) {
            if (str[i] == ar[j]) {
                new_str += str[i]
            }
        }
    }


    return parseFloat(new_str)
}


function formatAsCurrency(input) {
    let parts = input.toString().split(/[.,]/);

    // Целая часть числа
    let integerPart = parts[0];

    // Дробная часть числа (если есть)
    let decimalPart = parts.length > 1 ? ',' + parts[1].slice(0, 2) : '';

    // Добавление пробелов для разделения тысячных разрядов в целой части числа
    integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    // Возвращение числа в формате денежной строки
    return integerPart + (decimalPart || ',00');
}


function formatToMoney(input) {
    if (typeof input !== 'string') {
        input = input.toString(); // Преобразуем в строку, если это не строка
    }


    // Преобразуем во float, убирая все нечисловые символы
    const number = float_parser(input.replace(/[^0-9.]/g, ''));

    if (!isNaN(number)) {
        // Форматируем число с разделителями тысяч и двумя знаками после запятой
        const formattedNumber = number.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$& ').toString();
        if (input < 0) {
            return "-" + formattedNumber;
        }
        return formattedNumber;
    } else {
        // Если не удалось распарсить число, возвращаем сообщение об ошибке
        return 'Неверное значение';
    }
}


function change_sum(id, max_count, max_price, price_or_count, thisvalue) {

    var total_value = document.getElementById("total-sum-" + id)

    try {
        var count_value = document.getElementById("position-count-" + id).value;
        var price_value = document.getElementById("position-sum-" + id).value;
        var notes = document.getElementById("note-" + id)
        if ($("#limit").text().includes("True")) {
            if (float_parser(price_value) > max_price) {
                price_value = max_price;
                document.getElementById("position-sum-" + id).value = max_price;
            }
            if (float_parser(count_value) > max_count) {
                count_value = max_count;
                document.getElementById("position-count-" + id).value = max_count;
            }
        }

        total_value.innerHTML = formatToMoney(float_parser(count_value) * float_parser(price_value))

        let is_count_danger = false;
        let is_price_danger = false;

        if (float_parser(count_value) > max_count) is_count_danger = true;
        else if (float_parser(price_value) > max_price) is_price_danger = true;
        if (price_or_count == "count" && float_parser(count_value) > max_count) notification_count();
        else if ((price_or_count == "price" || price_or_count == "price-zout-notif") && float_parser(price_value) > max_price) notification_price();

        if (is_count_danger && is_price_danger) notes.innerHTML = "Превышены и цена и количество"
        else if (is_count_danger) notes.innerHTML = "Превышено количество"
        else if (is_price_danger) notes.innerHTML = "Превышена цена"
        else notes.innerHTML = ""

        tr_danger(id, max_count, max_price, count_value, price_value)
        set_total_sum()

        if (price_or_count == "count" || price_or_count == "count-zout-notif") thisvalue = count_value
        else if (price_or_count == "price" || price_or_count == "price-zout-notif") thisvalue = price_value

        document.getElementById(`span-${price_or_count}-${id}`).innerHTML = thisvalue

        var balance = $('#balance');
        if (balance) {
            var totlSumm = float_parser($("#total-summ").text())
            var morhz = $("#morzh")
            if (morhz) {
                let moneyWasted = $("#money_wasted")
                calcedMorzh = (parseFloat(moneyWasted.text()) / totlSumm).toFixed(2)
                if (calcedMorzh) {
                    morhz.text(calcedMorzh)
                } else {
                    morhz.text("0,00")
                }
            }
            var ms = parseFloat($('#ms').text())
            currentBalance = ms - totlSumm
            balance.text(formatToMoney(ms - totlSumm))
            var dwnl = $("#html-download")
            if (currentBalance < 0) {
                dwnl.removeClass("btn-success")
                dwnl.addClass("btn-danger")
                dwnl.attr("disabled", true)

            } else {
                dwnl.addClass("btn-success")
                dwnl.removeClass("btn-danger")
                dwnl.attr("disabled", false)
            }

        }


    } catch (er) {
        // alert(er.stack)
        total_value.innerHTML = 0
    }


}

function ShowSMR(e) {
    console.log('works')

    document.getElementById("html-download-button").style.display = "none"
    document.getElementById('main-table-container').innerHTML = `
        <div class="d-flex justify-content-center pt-5 pb-5">
            <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>`;
    e.preventDefault(); // Отменяем стандартное отправление формы

    // Получение данных из формы
    var formData = new FormData(document.getElementById('show-srm-form'));
    console.log(formData)

    // Построение query string из данных формы
    var queryString = new URLSearchParams(formData).toString();
    console.log(queryString)

    // Формирование URL для GET-запроса
    var url = '/mp/calculator/find/?' + queryString;
    if (window.location.href.includes('header_page')) {
        url += '&header_page=true'
    }

    // Создание XMLHttpRequest объекта
    var xhr = new XMLHttpRequest();

    // Настройка GET-запроса
    xhr.open('GET', url, true);

    // Отправка GET-запроса
    xhr.send();

    // Обработка ответа (это можно дополнить по вашим потребностям)
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Обработка успешного ответа
            console.log('GET запрос выполнен успешно.');
            document.getElementById('main-table-container').innerHTML = xhr.responseText

            var positionContractor = $('.positionContractor')
            if (positionContractor.length == 1 && positionContractor.text() == "общий пункт" && ($(".custom-info").text().includes("Строительные работы") || $(".custom-info").text().includes("Электромонтажные работы") || $(".custom-info").text().includes("Монтажные работы") || $(".custom-info").text() == ("Монтаж"))) {
                find_key = $('.custom-info').text()
                orderNumber = $("#order-number").text().trim().replace(/\n/g, '').replace(/\s+/g, ' ')
                if ($("#projectgroup").text().includes("252")) {
                    location.href = `/mp/calculator/zero-order?order_number=${orderNumber}&key_word=${find_key}&projectgroup=252`
                } else {
                    location.href = `/mp/calculator/zero-order?order_number=${orderNumber}&key_word=${find_key}`
                }
            }
            // Дополнительный код обработки ответа
            set_total_sum()
            change_dangers_count()
            document.getElementById("html-download-button").style.display = "initial"
        } else if (xhr.status == 404) {
            let nf_404 = `
            <div class="text-center pt-4 pb-4">
            <div class="error mx-auto" style="width:205px;" data-text="404">404</div>
            <p class="lead text-gray-800 mb-4 pt-4">Не найдено</p>
            <p class="text-gray-500 mb-0 pb-4">Такого номера заказа нет...</p>
            </div>`
            document.getElementById('main-table-container').innerHTML = nf_404

        } else {

        }
    };

}

document.getElementById('find_order_form').addEventListener('submit', function (e) {
    document.getElementById("html-download-button").style.display = "none"
    document.getElementById('main-table-container').innerHTML = `
        <div class="d-flex justify-content-center pt-5 pb-5">
            <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>`;
    e.preventDefault(); // Отменяем стандартное отправление формы

    // Получение данных из формы
    var formData = new FormData(this);

    // Построение query string из данных формы
    var queryString = new URLSearchParams(formData).toString();

    // Формирование URL для GET-запроса
    var url = '/mp/calculator/find/?' + queryString;
    if (window.location.href.includes('header_page')) {
        url += '&header_page=true'
    }

    // Создание XMLHttpRequest объекта
    var xhr = new XMLHttpRequest();

    // Настройка GET-запроса
    xhr.open('GET', url, true);

    // Отправка GET-запроса
    xhr.send();

    // Обработка ответа (это можно дополнить по вашим потребностям)
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Обработка успешного ответа
            console.log('GET запрос выполнен успешно.');
            document.getElementById('main-table-container').innerHTML = xhr.responseText

            var positionContractor = $('.positionContractor')
            if (positionContractor.length == 1 && positionContractor.text() == "общий пункт" && ($(".custom-info").text().includes("Строительные работы") || $(".custom-info").text().includes("Электромонтажные работы") || $(".custom-info").text().includes("Монтажные работы") || $(".custom-info").text() == ("Монтаж"))) {
                find_key = $('.custom-info').text()
                orderNumber = $("#order-number").text().trim().replace(/\n/g, '').replace(/\s+/g, ' ')
                if ($("#projectgroup").text().includes("252")) {
                    location.href = `/mp/calculator/zero-order?order_number=${orderNumber}&key_word=${find_key}&projectgroup=252`
                } else {
                    location.href = `/mp/calculator/zero-order?order_number=${orderNumber}&key_word=${find_key}`
                }
            }
            // Дополнительный код обработки ответа
            set_total_sum()
            change_dangers_count()
            document.getElementById("html-download-button").style.display = "initial"
        } else if (xhr.status == 404) {
            let nf_404 = `
            <div class="text-center pt-4 pb-4">
            <div class="error mx-auto" style="width:205px;" data-text="404">404</div>
            <p class="lead text-gray-800 mb-4 pt-4">Не найдено</p>
            <p class="text-gray-500 mb-0 pb-4">Такого номера заказа нет...</p>
            </div>`
            document.getElementById('main-table-container').innerHTML = nf_404

        } else {

        }
    };
});

// document.getElementById('find_order_form_bx').addEventListener('submit', function (e) {
//     document.getElementById("html-download-button").style.display = "none"
//     document.getElementById('main-table-container').innerHTML = `
//         <div class="d-flex justify-content-center pt-5 pb-5">
//             <div class="spinner-border" role="status">
//                 <span class="sr-only">Loading...</span>
//             </div>
//         </div>`;

//     e.preventDefault(); // Отменяем стандартное отправление формы

//     // Получение данных из формы
//     var formData = new FormData(this);

//     // Построение query string из данных формы
//     var queryString = new URLSearchParams(formData).toString();

//     // Формирование URL для GET-запроса
//     var url = '/mp/calculator/find/bx/?' + queryString;

//     // Создание XMLHttpRequest объекта
//     var xhr = new XMLHttpRequest();

//     // Настройка GET-запроса
//     xhr.open('GET', url, true);

//     // Отправка GET-запроса
//     xhr.send();

//     // Обработка ответа (это можно дополнить по вашим потребностям)
//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === 4 && xhr.status === 200) {
//             // Обработка успешного ответа
//             console.log('GET запрос выполнен успешно.');
//             document.getElementById('main-table-container').innerHTML = xhr.responseText
//             // Дополнительный код обработки ответа
//             set_total_sum()
//             change_dangers_count()
//             document.getElementById("html-download-button").style.display = "initial"
//         }
//     };
// });

$(document).ready(function () {
    if ($("#balance")) {
        $("#balance").text(formatAsCurrency($("#balance").text()))
    }

    $('.bs-item').on('click', function () {
        var selectedValue = $(this).text();
        $('#dropdownBSButton').val(selectedValue);
        console.log(selectedValue)
    });

    $('#emr-order-table').on('click', 'tr', function () {
        var rawSelectedValue = $(this).find('#order-from-table');
        var selectedValue = rawSelectedValue.text();
        var index = rawSelectedValue.attr('index')
        console.log(index)

        redirectToView(selectedValue, index)
    })

        $('.tcp-item').on('click', function () {
        var selectedValue = $(this).text();
        $('#dropdownTCP').val(selectedValue);
        var dropdownTCP = document.getElementById('dropdownTCP')
        dropdownTCP.setAttribute('unit', this.getAttribute('unit'))
        dropdownTCP.setAttribute('max-sum', this.getAttribute('max-sum'))
        dropdownTCP.setAttribute('search-key', this.getAttribute('search-key'))
    });
})

function redirectToView(orderNumber, index_) {
    var index = location.href.indexOf("&order-number=");
    console.log(index_)
    if (index !== -1) {
        location.replace(location.href.replace(/&order-number=.*?(&|$)/, `&order-number=${orderNumber}&index=${index_}`).replace(/&index=.*?(&|$)/, `&index=${index_}`));
    }
    else {
        location.replace(location.href.replace(/#$/, "") + `&order-number=${orderNumber}`);
    }
}

if (location.href.indexOf("&order-number=") !== -1) {
    var orderNumberParsed = decodeURIComponent(window.location.href.split("&order-number=")[1]);
    var indexParsed = decodeURIComponent(window.location.href.split("&index=")[1]);

    orderData = JSON.parse(document.getElementById('orderData').getAttribute('data-order'));
    // for (var i = 0; i < orderData.length; i++){
    //     if orderData[i]
    // }
    // indexParsed - нужен для повторяющихся номеров заказа
    var maxSum = (orderData[0].fields.order_sem_with_nds * 0.60).toFixed(2)
    var amount_diff = parseFloat(document.getElementById('amount-diff').innerText.replace(',', '.'))
    document.getElementById('order-number').innerText = orderData[0].fields.order_number
    document.getElementById('order_customer_name').innerText = orderData[0].fields.customer
    document.getElementById('total-summ-nds').innerText = orderData[0].fields.order_sem_with_nds
    document.getElementById('total-summ-without-nds').innerText = orderData[0].fields.order_sem_without_nds
    document.getElementById('order-region').innerText = orderData[0].fields.region
    document.getElementById('order-type').innerText = orderData[0].fields.field_of_activity
    document.getElementById('max-summ').innerText = maxSum
    // document.getElementById('balance').innerText = amount_diff
}

document.getElementById('dropdownBSButton').addEventListener('input', function () {
    var inputText = this.value.toLowerCase();
    var bsItems = document.querySelectorAll('.bs-item');

    bsItems.forEach(function (item) {
        var projectText = item.textContent.toLowerCase();
        if (projectText.indexOf(inputText) > -1) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});
document.getElementById('dropdownTCP').addEventListener('input', function () {
    var inputText = this.value.toLowerCase();
    var bsItems = document.querySelectorAll('.tcp-item');

    bsItems.forEach(function (item) {
        var projectText = item.textContent.toLowerCase();
        if (projectText.indexOf(inputText) > -1) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});

var btnAddTCP = document.getElementById('add_tcp');

btnAddTCP.addEventListener('click', function () {
    choisedTCP = document.getElementById('dropdownTCP')
    if (choisedTCP.value != '') {
        punkts = document.getElementById('order-punkts')
        punkts.innerText = parseInt(punkts.textContent) + 1
        nameTCP = choisedTCP.value
        unit = choisedTCP.getAttribute('unit')
        maxSum = choisedTCP.getAttribute('max-sum')
        searchKey = choisedTCP.getAttribute('search-key')
        tableRow = createTableRow(searchKey, nameTCP, unit, maxSum)
        var tableBody = document.getElementById('tbodyTCP')
        tableBody.appendChild(tableRow)
        keepMoneyFormat()
        choisedTCP.value = ''
        document.querySelectorAll('.tcp-item[search-key="' + searchKey + '"]').forEach(function (item) {
            item.remove()
        });

    }
})

function notification_price() {
    var dangerAlert = document.getElementById("dangerAlertPrice");
    dangerAlert.style.display = "initial"

    setTimeout(function () {
        dangerAlert.style.display = "none";
    }, 3000);
}


function calculateSumm(maxSum, articule) {
    var unit = document.getElementById('unit-' + articule)
    var count = document.getElementById('count-' + articule)
    if (parseFloat(count.value) > parseFloat(maxSum)) {
        count.value = parseFloat(maxSum)
        count.classList.add('shake'); // добавляем класс с анимацией
        setTimeout(function () {
            count.classList.remove('shake'); // удаляем класс через 0.5 секунды
        }, 500);
    }

    document.getElementById('total-' + articule).innerText = count.value * unit.value

    var allSums = document.getElementsByClassName("total-sum-td")
    var totalSumm = document.getElementById('total-summ')
    var balance = document.getElementById('balance_emr')
    var amount_diff = parseFloat(document.getElementById('amount-diff').innerText.replace(' ', ''))
    // var maxBalance = document.getElementById('max-summ')
    var tempSum = 0
    for (var i = 0; i < allSums.length; i++) {
        tempSum = parseFloat(allSums[i].textContent.replace(/ /g, "")) + tempSum
    }
    totalSumm.innerText = tempSum
    balance.innerText = `${((orderData[0].fields.order_sem_with_nds * 0.60).toFixed(2) - amount_diff - tempSum).toFixed(2)}`
    document.querySelectorAll('.even').forEach(function (item) {
        if (parseFloat(balance.textContent) < 0) {
            item.style.backgroundColor = "#ffd3d3"
            notification_price()
        } else {
            item.style.backgroundColor = "#f6f6ff"
        }
    })
    keepMoneyFormat()
}

function keepMoneyFormat() {
    // Находим все элементы с классом money-format
    var moneyElements = document.getElementsByClassName('money-format');

    // Проходим по каждому элементу и форматируем его содержимое
    for (var i = 0; i < moneyElements.length; i++) {
        var originalNumber = parseFloat(moneyElements[i].textContent.replace(/\s/g, '')); // Удаляем пробелы и преобразуем в число
        var formattedNumber = formatNumberWithSpaces(originalNumber);
        moneyElements[i].textContent = formattedNumber; // Устанавливаем отформатированное значение
    }
}

function formatNumberWithSpaces(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

function createTableRow(articule, nomenclature, unit, maxSum) {
    // Создание <tr> элемента
    var tr = document.createElement('tr');
    tr.className = 'even tr-position';

    // Создание <td> элемента для nomenclature Артикул
    var tdNomenclature = document.createElement('td');
    var spanNomenclature = document.createElement('span');
    spanNomenclature.className = 'json_nomenclatures';
    spanNomenclature.textContent = articule;
    tdNomenclature.appendChild(spanNomenclature);
    tr.appendChild(tdNomenclature);

    // Создание <td> элемента для info Номенклатура
    var tdInfo = document.createElement('td');
    tdInfo.className = 'custom-info';
    tdInfo.textContent = nomenclature;
    tr.appendChild(tdInfo);

    // Создание <td> элемента для quant Кол-во
    var tdPrice = document.createElement('td');
    tdPrice.className = 'td-in';

    var inputPrice = document.createElement('input');
    inputPrice.id = `unit-${articule}`
    inputPrice.setAttribute('oninput', `calculateSumm('${maxSum}', '${articule}')`)
    inputPrice.style.background = '#e1e8ff';
    inputPrice.style.width = '100px';
    inputPrice.className = 'form-control';
    inputPrice.type = 'number';
    inputPrice.value = 0;

    tdPrice.appendChild(inputPrice);
    tr.appendChild(tdPrice);

    // Создание <td> элемента для шт
    var tdUnit = document.createElement('td');
    tdUnit.style.paddingTop = '20px';
    tdUnit.textContent = unit;
    tr.appendChild(tdUnit);

    // Создание <td> элемента для count 	Цена за ед.
    var tdCount = document.createElement('td');
    tdCount.style.paddingTop = '20px';
    tdCount.className = 'td-in';
    var inputCount = document.createElement('input');
    inputCount.id = `count-${articule}`
    inputCount.setAttribute('oninput', `calculateSumm('${maxSum}', '${articule}')`)
    inputCount.style.background = '#e1e8ff';
    inputCount.style.width = '150px';
    inputCount.max = maxSum
    inputCount.className = 'form-control';
    inputCount.type = 'number';
    inputCount.value = 0;

    tdCount.appendChild(inputCount);
    tr.appendChild(tdCount);

    // Создание <td> элемента для price Цена за ед. (Макc.)
    var tdPriceDisplay = document.createElement('td');
    tdPriceDisplay.style.paddingTop = '20px';
    tdPriceDisplay.className = 'money-format';
    tdPriceDisplay.textContent = maxSum;
    tr.appendChild(tdPriceDisplay);

    // Создание <td> элемента для totalSum Сумма
    var tdTotalSum = document.createElement('td');
    tdTotalSum.style.paddingTop = '20px';
    tdTotalSum.id = `total-${articule}`
    tdTotalSum.className = 'total-sum-td money-format';
    tdTotalSum.textContent = 0;
    tr.appendChild(tdTotalSum);
    return tr;
}

function set_total_sum() {
    let tds = document.getElementsByClassName("total-sum-td")
    // console.log(tds.length > 0)
    if (tds.length > 0) {
        let sum = 0;
        for (let i = 0; i < tds.length; i++) {
            sum += float_parser(tds[i].innerHTML)
        }
        let total_sum = document.getElementById("total-summ")
        console.log(formatAsCurrency(sum))
        total_sum.innerHTML = formatAsCurrency(sum)
        let morhz = $("#morzh")
        if (morhz) {
            let moneyWasted = $("#money_wasted")
            console.log(parseFloat(moneyWasted.text()), parseFloat(total_sum.innerHTML))
            calcedMorzh = parseFloat(moneyWasted.text()) / parseFloat(total_sum.innerHTML)
            console.log(calcedMorzh)
            if (calcedMorzh && calcedMorzh != Infinity) {
                morhz.text(calcedMorzh)
            } else {
                morhz.text("0,00")
            }
        }
    }
    change_dangers_count()
    let money_formats = document.getElementsByClassName("money_format")
    for (let i = 0; i < money_formats.length; i++) {
        // console.log(money_formats[i].textContent)
        money_formats[i].innerHTML = formatAsCurrency(money_formats[i].innerHTML)
    }
}


function html_download(zeroOrNot = true) {
    // let is_previshenie = false
    // if (zeroOrNot) is_previshenie = set_text_report()
    is_previshenie = set_text_report()
    let input_versions = document.getElementsByClassName("input-out")
    let text_versions = document.getElementsByClassName("text_version")
    let tds = document.getElementsByClassName("td-in")


    set_total_sum()
    for (let i = 0; i < tds.length; i++) {
        tds[i].style.paddingTop = "20px"
    }
    for (let i = 0; i < input_versions.length; i++) {
        input_versions[i].style.display = "none"
    }
    for (let i = 0; i < text_versions.length; i++) {
        text_versions[i].style.display = "initial"
        text_versions[i].innerHTML = text_versions[i].innerHTML.replace('.', ',')
    }
    repalce_text = "JSON_format_for_import_in_adem_replace_here_to_this_text"


    let nomenclatures = document.getElementsByClassName("json_nomenclatures") // "Номенклатура"
    let initial_coutn = document.getElementsByClassName("json_initial_coutn") // "Количество (в счете)"
    let new_price = document.getElementsByClassName("json_new_price") // "Введённая цена"
    let new_count = document.getElementsByClassName("json_new_count") // "Количество введённое"
    let order_number = document.getElementById("order-number").innerHTML.trim() // "Заказ"
    let total_sum = document.getElementsByClassName("json_total_sum") // "Итоговая сумма"


    let import_data = {
        "import_data": [{
            "Спецификация счёта": []
        }]
    };

    for (let i = 0; i < nomenclatures.length; i++) {
        var total_summs = parseFloat(total_sum[i].innerHTML.replace(/\s/g, '').replace(',', '.'))
        let item = {};
        if (total_summs > 0) {
            item = {
                "Номер строки": (i + 1) * 10,
                "Ключ поиска": nomenclatures[i].innerHTML,
                "Количество (в счете)": parseFloat(initial_coutn[i].value),
                "Введённая цена": parseFloat(new_price[i].innerHTML.replace(/\s/g, '').replace(',', '.')),
                "Налог": "Без налога",
                "Связь заказ/счёт": [{
                    "Количество введённое": parseFloat(new_count[i].innerHTML.replace(/\s/g, '').replace(',', '.')),
                    "Заказ": order_number,
                    "Спецификация заказа": 10,
                    "Итоговая сумма": total_summs
                }]
            };
        } else {
            item = {
                "Номер строки": (i + 1) * 10,
                "Ключ поиска": nomenclatures[i].innerHTML,
                "Количество (в счете)": parseFloat(initial_coutn[i].value),
                "Введённая цена": parseFloat(new_price[i].innerHTML.replace(/\s/g, '').replace(',', '.')),
                "Налог": "Без налога"
            };
        }
        import_data.import_data[0]["Спецификация счёта"].push(item);
    }

    let json_format = JSON.stringify(import_data, null, 4);
    document.getElementById("import_data").innerHTML = `<import_data hidden>${json_format}</import_data>`


    downloadHtmlFile(is_previshenie)

}


function formatDate(date) {
    return [
        padTo2Digits(date.getDate()),
        padTo2Digits(date.getMonth() + 1),
        date.getFullYear(),
    ].join('.');
}

function padTo2Digits(num) {
    return num.toString().padStart(2, '0');
}

function downloadHtmlFile(is_previshenie) {


    // Получите элемент div по его ID
    const mainTableContainer = document.getElementById("main-table-container");

    if (mainTableContainer) {
        // Получите HTML-код из элемента
        const htmlContent = html_start + mainTableContainer.innerHTML + html_end;

        // Создайте новый Blob с HTML-кодом
        const blob = new Blob([htmlContent], { type: "text/html" });

        // Создайте временную ссылку для загрузки
        const url = URL.createObjectURL(blob);

        // Создайте элемент <a> для скачивания
        const a = document.createElement("a");
        a.href = url;
        let order_name = document.getElementById("order-number").innerHTML.trim()
        let order_customer_name = document.getElementById("order_customer_name").innerHTML.trim()
        let projectgroup = $("#projectgroup").text()
        let current_date = new Date()
        if (is_previshenie) {
            order_customer_name = "!!! " + order_customer_name
        }

        let regex = /[a-zA-Z]{1,3}_[a-zA-Z]{1,15}(_[a-zA-Z0-9_]{0,9})? - [a-zA-Z]{1,3}_[a-zA-Z]{1,15}(_[a-zA-Z0-9_]{0,9})?/;
        let comments = document.getElementById("bs-comments").textContent
        let bs_name = regex.exec(comments)
        if (!bs_name) {
            regex = /[a-zA-Z]{1,3}_[a-zA-Z]{1,15}(_[a-zA-Z0-9_]{0,9})?/;
            bs_name = regex.exec(comments)
        }
        if (bs_name) {
            bs_name = bs_name[0]
        } else {
            bs_name = ""
        }




        a.download = `${projectgroup} - ${order_customer_name} - (${bs_name}) - ${order_name} ${formatDate(current_date)}.html`;

        // Симулируйте клик по элементу <a> для скачивания
        a.click();

        // Освободите ресурсы
        URL.revokeObjectURL(url);

        let responsible = document.getElementById("resp-name-id").textContent.trim()
        sendReport(responsible, "calculator - Скачивание HTML файла", "Скачивание - " + `${order_customer_name} - (${bs_name}) - ${order_name} ${formatDate(current_date)}.html`)
    }
}

function openHeaderPager(bx = null) {
    if (bx) {
        window.location.href += "?header_page=true&bx=true";
    } else {
        window.location.href += "?header_page=true";
    }
}


function export_excel() {
    var loadingScreen = document.getElementById('loading-screen');
    loadingScreen.style.display = 'block'; // Показываем загрузочный экран

    var xhr = new XMLHttpRequest();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const date = new Date();
    xhr.open("GET", "/mp/calculator/export_excel/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.responseType = 'blob'; // Указываем, что ответ будет в бинарном формате (для файла Excel)
    xhr.onload = function () {
        // Проверяем статус ответа
        if (xhr.status === 200) {
            // Создаем ссылку для скачивания файла
            var url = window.URL.createObjectURL(xhr.response);
            var a = document.createElement('a');
            a.href = url;

            a.download = `экспорт - ${date}.xlsx`; // Указываем имя файла
            document.body.appendChild(a);
            a.click();
            // Освобождаем ресурсы
            window.URL.revokeObjectURL(url);
        }
        loadingScreen.style.display = 'none'; // Скрываем загрузочный экран после получения ответа
    };
    xhr.send();
}

function html_download_emr() {
    tcpInputElement = document.getElementById('tcp-form')
    tcpInputElement.remove()



    var importData = document.getElementsByTagName('import_data')[0];
    var allTable = document.getElementsByClassName('even');
    var importDataElement = document.createElement('import_data');
    importDataElement.setAttribute('hidden', '');

    var orderNumberValue = document.getElementById('order-from-table').innerText;
    var currentUrl = window.location.href;

    var bitrix_url = ''
    if (currentUrl.includes('bitrix')) {
        bitrix_url = 'bitrix-v/'
    }

    var url = new URL(currentUrl);
    var bsName = url.searchParams.get("bs_name");

    var arrToImport = {
        "import_data": [{
            "Спецификация счёта": []
        }]
    }

    for (var i = 0; i < allTable.length; i++) {
        var unitValue = parseInt(allTable[i].cells[2].firstChild.value);
        var priceForUnit = allTable[i].cells[4].firstChild.value;
        var searchKeyValue = allTable[i].cells[0].textContent;
        var totalSumValue = parseFloat(allTable[i].cells[6].textContent.replace(' ', ''));

        var item = {
            "Номер строки": (i + 1) * 10,
            "Ключ поиска": searchKeyValue,
            "Количество (в счете)": unitValue,
            "Введённая цена": priceForUnit,
            "Налог": "Без налога"
        };

        var orderItem = {
            "Количество введённое": unitValue,
            "Заказ": orderNumberValue,
            "Спецификация заказа": 10,
            "Итоговая сумма": totalSumValue
        };

        item["Связь заказ/счёт"] = [orderItem];

        arrToImport["import_data"][0]["Спецификация счёта"].push(item);
    }

    importData.textContent = JSON.stringify(arrToImport, null, 4);


    var mainContainer = document.getElementById('main-container');
    var inputElements = mainContainer.getElementsByTagName('input');
    while (inputElements.length > 0) {
        var inputValue = inputElements[0].value;

        // Создаем новый текстовый узел
        var textNode = document.createTextNode(inputValue);

        // Заменяем тег <input> текстовым узлом
        inputElements[0].parentNode.replaceChild(textNode, inputElements[0]);
    }

    var link = document.createElement('a');

    // Получаем стили
    var cssLinks = document.querySelectorAll('link[rel="stylesheet"]');
    var promises = [];

    cssLinks.forEach(function (link) {
        const response = fetch(link.href);
        promises.push(fetch(link.href).then(response => response.text()));
    });

    Promise.all(promises).then(function (styles) {



        // Добавляем стили к HTML-коду
        var htmlContent = '<html><head> <meta charset="UTF-8">  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />';
        styles.forEach(function (style) {
            htmlContent += '<style>' + style + '</style>';
        });
        htmlContent += '</head><body>';

        // Добавляем содержимое таблицы
        htmlContent += document.getElementById('main-container').outerHTML;

        htmlContent += '</body></html>';

        // Создаем Blob из HTML-кода с включенными стилями
        var blob = new Blob([htmlContent], { type: 'text/html' });
        var url = window.URL.createObjectURL(blob);
        link.href = url;

        // Устанавливаем атрибуты для скачивания
        link.download = `${bsName} - ${orderNumberValue}.html`;

        // Добавляем элемент в DOM (для того чтобы сработало событие click)
        document.body.appendChild(link);

        // Имитируем клик на элементе
        link.click();

        // Удаляем элемент из DOM
        document.body.removeChild(link);
    });

    // Обрезаем его до базовой части
    var baseUrl = new URL(currentUrl).origin + "/" + "mp/calculator/" + bitrix_url;

    // Перенаправляем на обрезанный URL
    window.location.href = baseUrl;
}

keepMoneyFormat()