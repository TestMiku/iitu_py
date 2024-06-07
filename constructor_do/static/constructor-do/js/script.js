$(document).ready(function () {
    // Define variables to store the values of bs_name and on_name
    var bsNameValue = '';
    var onNameValue = '';
    var pnNameValue = '';

    // Handle the dropdown item click for BS
    $('.bs-item').on('click', function () {
        var selectedValue = $(this).text();
        $('#dropdownBSButton').val(selectedValue);
        bsNameValue = selectedValue; // Update bsNameValue
        $(this).parents(3).submit()
        $.ajax({
            type: "POST",
            url: "/constructor-do/",
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'), // Include CSRF token
                showPrevious: document.getElementById('previous_orders').style.display
            },
            success: function (response) {
                console.log('success')
            },
            error: function (xhr, status, error) {
                // Handle error response
                console.log('error')
                console.log(status, error);
            }
        });
    });

    // Handle the dropdown item click for Order Number
    $('.on-item').on('click', function () {
        var selectedValue = $(this).text();
        $('#dropdownONButton').val(selectedValue);
        bsNameValue = document.getElementById('dropdownBSButton').value;
        onNameValue = selectedValue;
        pnNameValue = $(this).attr('name');
    });

    // Handle table row click
    $('#emr-order-table').on('click', 'tr', function () {
        var rawSelectedValue = $(this).find('#order-from-table');
        var selectedValue = rawSelectedValue.text();
        var index = rawSelectedValue.attr('index');
        redirectToView(selectedValue);
    });

    // Handle TCP item click
    $('.tcp-item').on('click', function () {
        var selectedValue = $(this).text();
        $('#dropdownTCP').val(selectedValue);
        var dropdownTCP = document.getElementById('dropdownTCP');
        dropdownTCP.setAttribute('unit', this.getAttribute('unit'));
        dropdownTCP.setAttribute('max-sum', this.getAttribute('max-sum'));
        dropdownTCP.setAttribute('search-key', this.getAttribute('search-key'));
    });

    // Handle form submission
    $('#submitButton').on('click', function (e) {
        e.preventDefault(); // Prevent default form submission

        // Clear the form fields except for on_name
        $('#dropdownBSButton').val('');
        $('#dropdownONButton').val('');
        // document.getElementById('searchFM').submit()
        console.log(document.getElementById('previous_orders').style.display)

        // Send bs_name and on_name to views.py using AJAX with CSRF token
        $.ajax({
            type: "POST",
            url: "/constructor-do/",
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'), // Include CSRF token
                bs_name: bsNameValue,
                on_name: onNameValue,
                product_name: pnNameValue,
                showPrevious: document.getElementById('previous_orders').style.display
            },
            success: function (response) {
                console.log('success')
                // Handle success response
                document.getElementById('searchFM').submit()

                $.ajax({
                    type: "POST",
                    url: "/constructor-do/",
                    data: {
                        csrfmiddlewaretoken: getCookie('csrftoken'), // Include CSRF token
                        showPrevious: document.getElementById('previous_orders').style.display
                    },
                    success: function (response) {
                        console.log('success')
                    },
                    error: function (xhr, status, error) {
                        // Handle error response
                        console.log('error')
                        console.log(status, error);
                    }
                });
                // clearURLParams(); // Clear URL parameters after successful submission
            },
            error: function (xhr, status, error) {
                // Handle error response
                console.log('error')
                console.log(status, error);
            }
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Input filtering for dropdown BS
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

    // Input filtering for dropdown TCP
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
});

document.addEventListener("DOMContentLoaded", function() {
    // When the DOM is fully loaded
    toggleDeleteAllButton(); // Call the function again to ensure correct initial visibility

    // Listen for changes in the order-count table body
    document.getElementById("order-count").addEventListener("DOMSubtreeModified", toggleDeleteAllButton);

    // Listen for changes in the tbodyTCP table body
    document.getElementById("tbodyTCP").addEventListener("DOMSubtreeModified", toggleDeleteAllButton);
});

function toggleDeleteAllButton() {
    // Check if either table body has child elements
    var orderCountTableBody = document.getElementById("order-count");
    var tbodyTCP = document.getElementById("tbodyTCP");

    if (orderCountTableBody.children.length > 0 || tbodyTCP.children.length > 0) {
        // If either table body has child elements, show the button
        document.getElementById("deleteAllButton").style.display = "inline-block";
    } else {
        // If neither table body has child elements, hide the button
        document.getElementById("deleteAllButton").style.display = "none";
    }
}

// Function to clear URL parameters
function clearURLParams() {
    history.replaceState({}, document.title, window.location.pathname);
}

function clearAll() {
    var tableBody = document.getElementById('previous_orders');
    tableBody.innerHTML = '';
    var toggleButton = document.querySelector('.toggle-link');
    toggleButton.textContent = "Показать добавленные";

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


// Redirect to view function
function redirectToView(orderNumber) {
    var index = location.href.indexOf("&order-number=");
    if (index !== -1) {
        location.replace(location.href.replace(/&order-number=.*?(&|$)/, `&order-number=${orderNumber}&index=${index_}`).replace(/&index=.*?(&|$)/, `&index=${index_}`));
    } else {
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
    inputPrice.value = document.getElementById('order-count').childElementCount ? document.getElementById('order-count').childElementCount : 0;
    inputPrice.disabled = true

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

    var tdUrl = document.createElement('td');
    var aUrl = document.createElement('a');
    aUrl.id = 'apply-tcp';
    aUrl.href = '#';
    aUrl.textContent = 'Применить';

    var aUrlDelete = document.createElement('a');
    aUrlDelete.id = 'delete-tcp';
    aUrlDelete.href = '';
    aUrlDelete.textContent = 'Удалить';

    tdUrl.appendChild(aUrl);
    tdUrl.appendChild(aUrlDelete);

    var slashText = document.createTextNode(' / ');
    tdUrl.insertBefore(slashText, aUrlDelete);

    tr.appendChild(tdUrl);

    return tr;
}

function createRowPrev(num, bs, order_number, product_name) {
    // Создание <tr> элемента
    var tr = document.createElement('tr');
    tr.className = 'bc-grey tr-position';

    var tdNum = document.createElement('td');
    var spanNum = document.createElement('span');
    spanNum.className = '';
    spanNum.textContent = num;
    tdNum.appendChild(spanNum);
    tr.appendChild(tdNum);

    var tdBaseStation = document.createElement('td');
    var spanBaseStation = document.createElement('span');
    spanBaseStation.className = '';
    spanBaseStation.textContent = bs;
    tdBaseStation.appendChild(spanBaseStation);
    tr.appendChild(tdBaseStation);


    var tdOrderNumber = document.createElement('td');
    var spanOrderNumber = document.createElement('span');
    spanOrderNumber.className = '';
    spanOrderNumber.textContent = order_number;
    tdOrderNumber.appendChild(spanOrderNumber);
    tr.appendChild(tdOrderNumber);

    var tdProductName = document.createElement('td');
    var spanProductName = document.createElement('span');
    spanProductName.className = '';
    spanProductName.textContent = product_name;
    tdProductName.appendChild(spanProductName);
    tr.appendChild(tdProductName);

    var tdAction = document.createElement('td');
    tr.appendChild(tdAction);

    return tr;
}

function toggleContent() {
    var contentDiv = document.getElementById('previous_orders');
    var toggleButton = document.querySelector('.toggle-link');
    if (contentDiv.style.display === "none" || contentDiv.style.display === "") {
        contentDiv.style.display = "table-row-group";
        toggleButton.textContent = "Скрыть добавленные";
    } else {
        contentDiv.style.display = "none";
        toggleButton.textContent = "Показать добавленные";
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
    var maxSum = (orderData[0].fields.order_sem_without_nds * 0.80).toFixed(2)
    document.getElementById('order-number').innerText = orderData[0].fields.order_number
    document.getElementById('order_customer_name').innerText = orderData[0].fields.customer
    document.getElementById('total-summ-nds').innerText = orderData[0].fields.order_sem_with_nds
    document.getElementById('total-summ-without-nds').innerText = orderData[0].fields.order_sem_without_nds
    document.getElementById('order-region').innerText = orderData[0].fields.region
    document.getElementById('order-type').innerText = orderData[0].fields.field_of_activity
    document.getElementById('max-summ').innerText = maxSum
    document.getElementById('balance').innerText = (orderData[0].fields.order_sem_without_nds * 0.80).toFixed(2)
}


// Функция для форматирования числа с разделением тысяч пробелами
function formatNumberWithSpaces(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}


var btnAddTCP = document.getElementById('add_tcp');

btnAddTCP.addEventListener('click', function () {
    choisedTCP = document.getElementById('dropdownTCP')
    if (choisedTCP.value != '') {
        punkts = document.getElementById('order-count')
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
        document.getElementById('add_tcp').disabled = true;
        document.getElementById('add_nds_container').style.display = 'flex';

        var btnAddTCP = document.getElementById('apply-tcp');

        btnAddTCP.addEventListener('click', function () {
            var tcp_data = tableRow.childNodes

            let orders = document.getElementById('order-count')
            let tax_included = document.getElementById('add_nds').checked
            console.log(document.getElementById('previous_orders').style.display)

            if (orders.childElementCount > 0) {
                // Send bs_name and on_name to views.py using AJAX with CSRF token
                $.ajax({
                    type: "POST",
                    url: "/constructor-do/",
                    data: {
                        csrfmiddlewaretoken: getCookie('csrftoken'), // Include CSRF token
                        searchKey: tcp_data[0].firstChild.textContent,
                        nameTCP: tcp_data[1].firstChild.textContent,
                        unitCount: tcp_data[2].firstChild.value,
                        unitPrice: tcp_data[4].firstChild.value,
                        totalPrice: tcp_data[6].firstChild.textContent,
                        unitName: tcp_data[3].firstChild.textContent,
                        taxIncluded: tax_included,
                        showPrevious: document.getElementById('previous_orders').style.display
                    },
                    success: function (response) {
                        console.log(response)
                        console.log('success');
                        var tableBody = document.getElementById('previous_orders')
                        tableBody.innerHTML = ''

                        for (const [key, value] of Object.entries(response['previous_orders'])) {
                          console.log(key, value);
                            tableRow = createRowPrev(parseInt(key)+1, value[0], value[1], value[2])
                            tableBody.appendChild(tableRow)
                        }



                        clearURLParams(); // Clear URL parameters after successful submission
                        // Select the tbody element
                        const orders = document.getElementById('order-count');
                        // Remove all child elements (tr elements) from tbody
                        while (orders.firstChild) {
                            orders.removeChild(orders.firstChild);
                        }
                        const tcp = document.getElementById('tbodyTCP');
                        // Remove all child elements (tr elements) from tbody
                        while (tcp.firstChild) {
                            tcp.removeChild(tcp.firstChild);
                        }
                        document.getElementById('add_tcp').disabled = false;
                        document.getElementById('add_nds').checked = false;
                        document.getElementById('add_nds_container').style.display = 'none';
                        notifications('alertOrderAdded')
                    },
                    error: function (xhr, status, error) {
                        // Handle error response
                        console.log('error')
                        console.log(status, error);
                    }
                });
            } else {
                notifications('alertOrderEmpty')
            }
        })
    }
})

// Function to get CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function notifications(name) {
    var dangerAlert = document.getElementById(name);
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
    // var maxBalance = document.getElementById('max-summ')
    var tempSum = 0
    for (var i = 0; i < allSums.length; i++) {
        tempSum = parseFloat(allSums[i].textContent.replace(/ /g, "")) + tempSum
    }
    totalSumm.innerText = tempSum
    balance.innerText = `${((orderData[0].fields.order_sem_without_nds * 0.80).toFixed(2) - tempSum).toFixed(2)}`
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