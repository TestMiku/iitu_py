$(document).ready(function () {
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
});



$(document).ready(function () {
    $('.tcp-item').on('click', function () {
        var selectedValue = $(this).text();
        $('#dropdownTCP').val(selectedValue);
        var dropdownTCP = document.getElementById('dropdownTCP')
        dropdownTCP.setAttribute('unit', this.getAttribute('unit'))
        dropdownTCP.setAttribute('max-sum', this.getAttribute('max-sum'))
        dropdownTCP.setAttribute('search-key', this.getAttribute('search-key'))
    });
});



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



if (location.href.indexOf("&order-number=") !== -1) {
    var orderNumberParsed = decodeURIComponent(window.location.href.split("&order-number=")[1]);
    var indexParsed = decodeURIComponent(window.location.href.split("&index=")[1]);

    orderData = JSON.parse(document.getElementById('orderData').getAttribute('data-order'));
    console.log(orderData[0])
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


// Функция для форматирования числа с разделением тысяч пробелами
function formatNumberWithSpaces(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}


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
    var balance = document.getElementById('balance')
    console.log(balance)
    var amount_diff = parseFloat(document.getElementById('amount-diff').innerText.replace(' ', ''))
    // var maxBalance = document.getElementById('max-summ')
    var tempSum = 0
    for (var i = 0; i < allSums.length; i++) {
        tempSum = parseFloat(allSums[i].textContent.replace(/ /g, "")) + tempSum
    }
    totalSumm.innerText = tempSum
    console.log(orderData[0].fields.order_sem_without_nds)
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




function html_download() {
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
    var baseUrl = new URL(currentUrl).origin + "/" + "calculator-emr/" + bitrix_url;

    // Перенаправляем на обрезанный URL
    window.location.href = baseUrl;
}


keepMoneyFormat()