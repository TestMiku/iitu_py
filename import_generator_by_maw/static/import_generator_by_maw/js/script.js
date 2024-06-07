const baseUrl = window.location.origin;
var savedJson;

const checkboxContainer = document.querySelector('.checkbox-container');
function handle() {
    var btns = document.getElementsByClassName("btnToExportAndShow");
    var spinners = document.getElementsByClassName("spinnerSwitch")

    for (var i = 0; i < btns.length; i++) {
        spinners[i].style.display = "block";
        btns[i].style.display = "none";

    }
    var userInput = document.getElementById("userInput").value;
    var userInputTrimmed = userInput.replace(/\s/g, "")
    fetch(`${baseUrl}/import-generator-by-maw/search-by-account-number?account_number=${userInputTrimmed}`).then(response => response.json())
        .then(json => {
            searchedItems = json;
            // const checkboxContainer = document.querySelector('.checkbox-container');
            checkboxContainer.innerHTML = '';
            for (var i = 0; i < searchedItems.length; i++) {
                const checkboxDiv = document.createElement('div');
                checkboxDiv.className = 'form-check';

                const checkboxInput = document.createElement('input');
                checkboxInput.className = 'form-check-input';
                checkboxInput.type = 'radio';
                checkboxInput.name = 'flexRadioDefault';
                checkboxInput.id = `flexCheckDefault${i + 1}`;
                checkboxInput.value = searchedItems[i].account_number;

                const checkboxLabel = document.createElement('label');
                checkboxLabel.className = 'form-check-label';
                checkboxLabel.htmlFor = `flexRadioDefault${i + 1}`;
                checkboxLabel.textContent = searchedItems[i].account_number;

                // Добавление элементов в контейнер
                checkboxDiv.appendChild(checkboxInput);
                checkboxDiv.appendChild(checkboxLabel);
                checkboxContainer.appendChild(checkboxDiv);

                checkboxDiv.addEventListener('click', function () {
                    checkboxInput.checked = true;

                    for (var i = 0; i < btns.length; i++) {
                        spinners[i].style.display = "none";
                        btns[i].style.display = "block";

                    }
                    handleCheckboxChange(checkboxInput);
                });
            }
        });
}

// pls = document.getElementsByClassName("pl")[0].innerText("l;dsa")
async function handleCheckboxChange(event) {
    var checkbox = event; // Получаем элемент чекбокса из цели события
    console.log(checkbox.value);
    if (checkbox.checked) {
        try {
            const response = await fetch(`${baseUrl}/import-generator-by-maw/get-all-values?account_number=${checkbox.value}`);
            if (response.ok) {
                const json = await response.json();
                showTableByCheckedItems(json);
                console.log('йцукйцук')
                console.log(json)
            } else {
                console.error('Ошибка HTTP: ' + response.status);
            }
        } catch (error) {
            console.error('Ошибка fetch:', error);
        }
    }
}

// checkboxContainer.addEventListener('change', function (event) {

//     if (event.target.type === 'radio') {//event.target.classList.contains('form-check-input')
//         console.log("Выбранное значение:", event.target.value);

//         handleCheckboxChange(event);
//     }
// });

function createExportFile() {


    var link = document.createElement("a");

    // Получаем ссылку на элемент таблицы
    var table = document.getElementById("all-data-to-import");

    // Создаем Blob из HTML-контента таблицы
    var blob = new Blob([table.outerHTML + `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">`], { type: "text/html" });
    var url = window.URL.createObjectURL(blob);
    link.href = url;
    var nameValue = document.querySelector(`[name="flexRadioDefault"]:checked`).value
    // Устанавливаем атрибуты для скачивания
    link.download = `downloaded_table-${nameValue}.html`;

    // Добавляем элемент в DOM (для того чтобы сработало событие click)
    document.body.appendChild(link);

    // Имитируем клик на элементе
    link.click();

    // Удаляем элемент из DOM
    document.body.removeChild(link);
}


function showTableByCheckedItems(data) {
    savedJson = data;

    var mainTableBody = document.getElementById("maw-data-table");
    var secondaryTableBody = document.getElementById("secondary-data-table");
    mainTableBody.innerHTML = "";
    secondaryTableBody.innerHTML = "";

    var jsonData = { "import_data": [{ "Спецификация счёта": [] }] };
    var rowNum = 10;
    var importDataElements = document.getElementsByTagName('import_data');
    if (importDataElements.length > 0) {
        for (var i = 0; i < importDataElements.length; i++) {
            importDataElements[i].parentNode.removeChild(importDataElements[i]);
        }
    }
    var importDataElement = document.createElement('import_data');

    importDataElement.setAttribute('hidden', '');
    importDataElement.style = "white-space: pre-wrap; overflow: auto;";

    // Use a Map to group by nomenclature_code for JSON data
    let groupedData = new Map();

    data.forEach(function (item) {
        var tr = document.createElement("tr");
        ["nomenclature", "order_number", "account_number", "quantity", "unit_measurement", "price", "nomenclature_code"].forEach(function (property) {
            var td = document.createElement("td");
            if (property == "nomenclature") {
                td.style = "vertical-align: middle;";
            }
            if (property == "account_number") {
                td.style = "white-space: nowrap;";
            }
            td.textContent = item[property];
            tr.appendChild(td);
        });

        var searchKey = item['nomenclature_code'];
        var quanti = parseInt(item["quantity"].replace(/&nbsp;|\s/g, '').trim());
        var interedSum = parseInt(item["price"].replace(/&nbsp;|\s/g, '').trim());
        var orders = item['order_number'];
        var orderTempArr = [];

        var quanti_in_orderTempArr = orders.split(',').length == 1 ? quanti : quanti / orders.split(',').length;
        var interedSum_in_orderTempArr = orders.split(',').length == 1 ? interedSum : interedSum / orders.split(',').length;
        orders.split(',').forEach(function (order) {
            orderTempArr.push({
                "Количество введённое": typeof quanti_in_orderTempArr === 'number' && !Number.isInteger(quanti_in_orderTempArr) ? truncateToTwoDecimals(quanti_in_orderTempArr) : quanti_in_orderTempArr,
                "Заказ": order,
                "Спецификация заказа": 10,
                "Итоговая сумма": typeof interedSum_in_orderTempArr === 'number' && !Number.isInteger(interedSum_in_orderTempArr) ? truncateToTwoDecimals(interedSum_in_orderTempArr) : interedSum_in_orderTempArr,
            });
        });

        if (searchKey) {
            if (!groupedData.has(searchKey)) {
                groupedData.set(searchKey, {
                    "Номер строки": rowNum,
                    "Ключ поиска": searchKey,
                    "Количество (в счете)": 0,
                    "Введённая цена": 0,
                    "Налог": "НДС 12%",
                    "Связь заказ/счёт": []
                });
            }
            let group = groupedData.get(searchKey);

            group["Количество (в счете)"] += quanti;
            group["Введённая цена"] += interedSum;

            orders.split(',').forEach(function (order) {
                group["Связь заказ/счёт"].push({
                    "Количество введённое": quanti_in_orderTempArr,
                    "Заказ": order.trim(),
                    "Спецификация заказа": 10,
                    "Итоговая сумма": interedSum_in_orderTempArr
                });
            });

            mainTableBody.appendChild(tr);
        } else {
            secondaryTableBody.appendChild(tr);
        }

        rowNum += 10;
    });

    // Add grouped data to JSON structure
    groupedData.forEach(function (group) {
        jsonData.import_data[0]["Спецификация счёта"].push(group);
    });

    var textNode = document.createTextNode(JSON.stringify(jsonData, null, 4));
    importDataElement.appendChild(textNode);

    var hiddenImport = document.getElementById("all-data-to-import");
    hiddenImport.insertBefore(importDataElement, hiddenImport.firstChild);
}

function addToAllRows() {
    var inputValue = document.getElementById("input-text").value.trim(); // Получаем значение из поля ввода и удаляем лишние пробелы

    // Проверяем, что в поле ввода есть текст
    if (inputValue) {
        // Добавляем значение инпута ко всем значениям второго столбца таблицы в JSON-объекте
        for (var i = 0; i < savedJson.length; i++) {
            savedJson[i].order_number += ',' + inputValue;
            console.log(savedJson[i].order_number)
        }

        // Перерисовываем таблицу с обновленными данными
        showTableByCheckedItems(savedJson);
    }
    document.getElementById("input-text").value = '';

}


function truncateToTwoDecimals(num) {
    return Math.trunc(num * 100) / 100;
}