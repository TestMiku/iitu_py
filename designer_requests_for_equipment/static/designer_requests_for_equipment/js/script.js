countMainBlocks = 0;
BaseURL = window.location.origin;

function createTransitionBlock() {

    var oldShowBtn = $('#showBtn')
    oldShowBtn.attr('id', 'showBtn-disabled');

    var oldAddBtn = $('#addBtn')[0]
    oldAddBtn.id = 'addBtn-disabled';
    oldAddBtn.disabled = true
    $('#table-body').attr('id', 'table-body-disabled');

    const oldMainBlock = $(`.main-block-${countMainBlocks}`)[0]
    const elements = oldMainBlock.querySelectorAll('input, button');

    elements.forEach(element => {
        element.disabled = true; // Устанавливаем атрибут disabled для каждого элемента
    });

    var mainBlock = document.createElement('div');
    mainBlock.style = 'margin-top: 100px';
    mainBlock.classList.add('main-block', `main-block-${countMainBlocks + 1}`, 'm-5');
    var formBLock = document.createElement('div')
    formBLock.classList.add('form-block')
    // Создаем левую часть
    var leftCol = document.createElement('div');
    leftCol.classList.add('col-2', 'main-form');
    leftCol.id = `main-form-${countMainBlocks + 1}`;

    // Добавляем блоки внутри левой части
    var labels = ['Имя сайта:', 'JR номер:', 'Адрес:'];
    var inputIds = ['site_name', 'jr_number', 'address'];
    var index = 0;
    labels.forEach(function (labelText) {
        var row = document.createElement('div');
        row.classList.add('row');
        var label = document.createElement('label');
        label.textContent = labelText;
        var input = document.createElement('input');
        input.type = 'text';
        if (index == 1) {
            input.value = $('#jr_number-disabled').val()
            input.disabled = true
        }
        input.id = inputIds[index++];
        input.classList.add('form-control', 'main-form-input');
        row.appendChild(label);
        row.appendChild(input);
        leftCol.appendChild(row);
    });

    // Создаем центральную часть
    var centerCol = document.createElement('div');
    var button = document.createElement('button');
    button.classList.add('btn', 'btn-secondary', 'add-btn', 'btn-block');
    button.setAttribute('hidden', '');
    button.id = 'showBtn';
    button.setAttribute('onclick', 'showList()');
    button.innerHTML = '<i class="fas fa-arrow-down"></i>';
    centerCol.appendChild(button);

    leftCol.appendChild(centerCol);
    // Создаем правую часть
    // var rightCol = document.createElement('div');
    // rightCol.classList.add('list');

    var listBLock = document.createElement('div');
    listBLock.classList.add('list-block');
    //клонируем и сбрасываем
    var rightCol = document.getElementsByClassName('list')[0].cloneNode(true);
    rightCol.hidden = true;
    var buttons = rightCol.getElementsByTagName('button');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].disabled = false;
    }

    formBLock.appendChild(leftCol);
    // mainBlock.appendChild(centerCol);
    mainBlock.appendChild(formBLock);
    listBLock.appendChild(rightCol);
    // Создаем элемент div с классом "transition-tbl"
    var tableDiv = document.createElement('div');
    tableDiv.className = 'transition-tbl';

    // Создаем элемент таблицы с классом "table col-auto ml-auto table-hover"
    const table = document.createElement('table');
    table.className = 'table col-auto ml-auto table-hover';

    // Создаем thead
    const thead = document.createElement('thead');
    const theadRow = document.createElement('tr');

    // Добавляем заголовки
    const headers = ['#', 'Наименование', 'Кол-во'];
    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.scope = 'col';
        th.textContent = headerText;
        theadRow.appendChild(th);
    });
    thead.appendChild(theadRow);

    // Создаем tbody
    const tbody = document.createElement('tbody');
    tbody.id = 'table-body'

    // Добавляем thead и tbody к таблице
    table.appendChild(thead);
    table.appendChild(tbody);


    // Добавляем таблицу к table
    tableDiv.appendChild(table);
    tableDiv.setAttribute('hidden', true)
    listBLock.appendChild(tableDiv);
    mainBlock.appendChild(listBLock);

    var addButton = document.createElement('button');
    addButton.classList.add("btn", "btn-primary", "add-btn", "btn-lg", 'btn-block');
    addButton.style = "transform: translate(366%, 0%);"
    addButton.style.maxWidth = '300px';
    addButton.textContent = 'Добавить';
    addButton.setAttribute('onclick', 'createTransitionBlock()');
    addButton.id = 'addBtn';
    addButton.hidden = true;

    // Добавляем горизонтальную линию
    var horizontalLine = document.createElement('div');
    horizontalLine.classList.add('horizontal-line');

    // Возвращаем созданный div
    parentDiv = document.getElementsByClassName('main-block')[0].parentNode
    parentDiv.appendChild(mainBlock);
    parentDiv.appendChild(addButton);
    parentDiv.appendChild(horizontalLine);
    // return div;
    countMainBlocks++;
}


function createMainBlock() {
    // Создаем основной блок


    // Создаем блок с таблицей
    var tableDiv = document.createElement('div');
    tableDiv.classList.add('tbl');
    var table = document.createElement('table');
    table.classList.add('table', 'col-auto', 'ml-auto');
    var thead = document.createElement('thead');
    var tbody = document.createElement('tbody');
    var headers = ['#', 'Найменование', 'Кол-во'];
    var rowCount = 7; // Количество строк в таблице
    for (var i = 0; i < rowCount; i++) {
        var tr = document.createElement('tr');
        headers.forEach(function (headerText, index) {
            var td = document.createElement(index === 0 ? 'th' : 'td');
            if (index === 0) {
                var checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                td.appendChild(checkbox);
            } else if (index === 1) {
                td.textContent = 'Some text';
            } else {
                var input = document.createElement('input');
                input.type = 'number';
                input.classList.add('form-control', 'quantity-input');
                td.appendChild(input);
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    }
    headers.forEach(function (headerText) {
        var th = document.createElement('th');
        th.textContent = headerText;
        thead.appendChild(th);
    });
    table.appendChild(thead);
    table.appendChild(tbody);
    tableDiv.appendChild(table);

    // Добавляем созданные элементы в основной блок
    mainBlock.appendChild(tableDiv);

    // Добавляем основной блок и горизонтальную линию на страницу
    // document.body.appendChild(mainBlock);
    // document.body.appendChild(horizontalLine);
    parentDiv = document.getElementsByClassName(`main-block`)[0].parentNode
    parentDiv.appendChild(mainBlock);
}

firstCheck = false
secondCheck = false
thirdCheck = false
function showList() {
    var list = document.getElementsByClassName('list')[countMainBlocks]
    list.hidden = false

    // var form = document.getElementsByClassName('main-form')[countMainBlocks]
    $(`#main-form-${countMainBlocks} input`).each(function () {
        $(this)[0].setAttribute('disabled', true)
        $(this)[0].id = $(this)[0].id + '-disabled'
    })

    $(`.main-block .transition-tbl`).each(function () {
        $(this)[0].hidden = false
    })
}



function check() {
    if ($('#jr_number').val()) {
        secondCheck = true
    }

    if (firstCheck && secondCheck && thirdCheck) {
        // $('.add-btn').prop('disabled', false)
        nextBtn = document.getElementById('showBtn')
        nextBtn.hidden = false
        firstCheck = false;
        secondCheck = false;
        thirdCheck = false;
    }
}
$(document).on('input', '#site_name', function () {
    if ($(this).val()) {
        firstCheck = true
    } else {
        firstCheck = false
    }
    check()
})
$(document).on('input', '#jr_number', function () {
    if ($(this).val()) {
        secondCheck = true
    } else {
        secondCheck = false
    }
    check()
})
$(document).on('input', '#address', function () {
    if ($(this).val()) {

        thirdCheck = true
    } else {
        thirdCheck = false
    }
    check()
})


// })


function addToTable(baseEquipmentName, id) {
    var urlForFetch = `${BaseURL}/designer-rfe/get-data-by-equip?equip=${baseEquipmentName}&id=${id}`
    if (id == null) urlForFetch = `${BaseURL}/designer-rfe/get-data-by-equip?category=${baseEquipmentName}`

    fetch(urlForFetch).then(response => response.json()).then(json => {
        var table = document.createElement('table')
        table.classList.add('table', 'table-hover', 'col-auto', 'ml-auto')
        var tableHead = document.createElement('thead')
        var tableBody = document.createElement('tbody')
        tableBody.id = 'choices-rwos-table-body'
        var tr = document.createElement('tr')
        var headers = ['#', 'Наименование', 'Кол-во']
        headers.forEach(function (headerText) {
            var th = document.createElement('th')
            th.textContent = headerText
            tr.appendChild(th)
        })
        tableHead.appendChild(tr)
        json.forEach(function (data) {
            var tr = document.createElement('tr')
            var th = document.createElement('th')
            th.innerHTML = '<input type="checkbox" class="checkbox-input" aria-label="Checkbox for following text input">'
            th.setAttribute('scope', 'row')
            var td = document.createElement('td')
            td.innerText = data.transition_name
            td.setAttribute('onclick', `showSubEquipmentList(${data.id})`)//
            td.setAttribute('data-toggle', 'modal')
            td.setAttribute('data-target', `#transition-backdrop`)
            tr.id = `transition-id-${data.id}`
            var tdInput = document.createElement('td')
            tdInput.innerHTML = '<td><input type="number" class="form-control quantity-input" value="1"></td>'

            tr.appendChild(th)
            tr.appendChild(td)
            tr.appendChild(tdInput)
            tableBody.appendChild(tr)
            // if (id == null) {
            //     $('#table-body').append(tr)
            // }
        });
        table.appendChild(tableHead)
        table.appendChild(tableBody)
        modalBody = $('#transition-modal-body')
        modalBody.empty()
        modalBody.append(table)
        $('#addRowsBtn').prop('hidden', false)

    })
    $('#addBtn').prop('hidden', false)
    $('#downloadBtn').prop('hidden', false)
}

function showSubEquipmentList(id) {
    fetch(`${BaseURL}/designer-rfe/get-sub-data-by-id?id=${id}`).then(response => response.json()).then(json => {
        modalBody = $('#transition-modal-body')
        modalBody.empty()
        // Создаем таблицу
        const table = document.createElement('table');
        table.className = 'table table-bordered col-auto ml-auto';

        // Создаем thead
        const thead = document.createElement('thead');
        const theadRow = document.createElement('tr');

        // Создаем заголовки для столбцов
        const headers = ['Set Code', 'SAP', 'Description', 'Product code', 'Unit', 'Q-ty in set'];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.scope = 'col';
            th.textContent = headerText;
            theadRow.appendChild(th);
        });
        thead.appendChild(theadRow);

        // Создаем tbody
        const tbody = document.createElement('tbody');

        json.forEach(data => {
            quantValue = 0
            const tr = document.createElement('tr');
            for (var key in data) {
                if (key == 'id') {
                    tr.id = `row-id-${data[key]}`
                    continue
                }
                var value = data[key];
                const td = document.createElement('td');
                td.textContent = value;
                if (key == 'q_ty_in_set') {
                    $(`#transition-id-${id} input`).each(function () {
                        if ($(this)[0].value) {
                            quantValue = value * $(this)[0].value
                        }
                    })
                    continue
                }
                tr.appendChild(td);

            }
            const qtyInputTd = document.createElement('td');
            qtyInputTd.innerText = quantValue
            tr.appendChild(qtyInputTd);
            tbody.appendChild(tr);
        })

        // Добавляем thead и tbody к таблице
        table.appendChild(thead);
        table.appendChild(tbody);
        modalBody.append(table);
    })
}

function choiceMainRow() {
    var modalBody = $("#choices-modal-body")
    modalBody.empty()
    $('#addRowsBtn').prop('hidden', true)
    allMainForms = $('.main-form')

    const table = document.createElement('table');
    table.className = 'table col-auto ml-auto table-hover';

    // Создаем thead
    const thead = document.createElement('thead');
    const theadRow = document.createElement('tr');

    const headers = ["Имя сайта", "Адрес"];
    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.scope = 'col';
        th.textContent = headerText;
        theadRow.appendChild(th);
    });
    thead.appendChild(theadRow);
    const tbody = document.createElement('tbody');
    allMainForms.each(function () {
        var siteName = $(this).find('#site_name-disabled').val().replace(/"/g, '\'');
        var address = $(this).find('#address-disabled').val().replace(/"/g, '\'');
        const tr = document.createElement('tr');
        // tr.setAttribute('onclick', `exportToExcel("${siteName}", "${address})`)
        const tdSite = document.createElement('td');
        const tdadress = document.createElement('td');
        tdSite.textContent = siteName;
        tdSite.setAttribute('onclick', `exportToExcel("${siteName}", "${address}")`)
        tdadress.textContent = address;
        tdadress.setAttribute('onclick', `exportToExcel("${siteName}", "${address}")`)
        tr.appendChild(tdSite);
        tr.appendChild(tdadress);
        tbody.appendChild(tr);
    })
    table.appendChild(thead);
    table.appendChild(tbody);

    modalBody.append(table);
}


function exportToExcel(site_name, address) {
    allMainBlocks = document.getElementsByClassName('main-block');
    jrNumber = allMainBlocks[0].querySelector('#jr_number-disabled').value;
    allData = [];
    var fetchPromises = [];
    for (var i = 0; i < allMainBlocks.length; i++) {
        var mainBlock = allMainBlocks[i];
        var siteNameValue = mainBlock.querySelector('#site_name-disabled').value; // Захватываем значение site_name
        var addressValue = mainBlock.querySelector('#address-disabled').value; // Захватываем значение address

        // Здесь используем замыкание для сохранения значений site_name и address для каждой итерации
        (function (siteNameValue, addressValue) {
            var dataDict = {};
            dataDict['site_name'] = siteNameValue;
            dataDict['jr_number'] = jrNumber;
            dataDict['address'] = addressValue;
            var tableRows = mainBlock.querySelectorAll('tbody > tr');
            var subItemDataPromises = []; // Массив для хранения промисов fetch внутри итерации

            for (var j = 0; j < tableRows.length; j++) {
                if ((tableRows[j].id).includes('transition-id') && tableRows[j].querySelector('input[type="checkbox"]').checked) {
                    var id = tableRows[j].id.substring((tableRows[j].id).lastIndexOf('-') + 1);
                    var quantity = tableRows[j].querySelector('input[type="number"]').value;
                    // Создаем замыкание для захвата значения quantity
                    (function (id, quantity) {
                        subItemDataPromises.push(
                            fetch(`${BaseURL}/designer-rfe/get-sub-data-by-id?id=${id}`)
                                .then(response => response.json())
                                .then(json => {
                                    json.forEach(function (data) {
                                        data['q_ty_in_set'] *= parseInt(quantity);
                                    });
                                    return json;
                                })
                        );
                    })(id, quantity);
                }
            }

            // Создаем промис, который ожидает завершения всех запросов fetch для данной итерации
            var subItemDataPromise = Promise.all(subItemDataPromises).then(subItemData => {
                var newDataDict = {}; // Создаем новый объект для избежания проблемы с замыканием
                newDataDict['site_name'] = siteNameValue; // Используем захваченное значение
                newDataDict['jr_number'] = jrNumber;
                newDataDict['address'] = addressValue; // Используем захваченное значение
                newDataDict['table_data'] = subItemData;
                return newDataDict;
            });

            // Добавляем промис в массив fetchPromises
            fetchPromises.push(subItemDataPromise);
        })(siteNameValue, addressValue); // Вызываем замыкание с текущими значениями site_name и address
    }
    Promise.all(fetchPromises).then(completedData => {
        allData = completedData
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

        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: `${BaseURL}/designer-rfe/export-to-excel`,
            data: JSON.stringify({
                "all_data": allData,
                "main_site_name": site_name,
                "main_address": address
            }),
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            xhrFields: {
                responseType: 'blob'
            },
            success: function (blob) {
                var link = document.createElement('a');
                var url = window.URL.createObjectURL(blob);
                link.href = url;
                link.download = `${site_name} ${jrNumber}.xlsx`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
            },
            error: function (xhr, textStatus, errorThrown) {
                console.error('Ошибка при выполнении запроса:', errorThrown);
            }
        });
    })
}

function addRows() {
    checkedRows = $('#choices-rwos-table-body').find('tr').has('input[type="checkbox"]:checked');
    console.log(checkedRows)
    if (checkedRows.length > 0) {
        for (var i = 0; i < checkedRows.length; i++) {
            var row = checkedRows[i];
            $('#table-body').append(row)

        }
    }
}