const baseUrl = window.location.origin;
let currentMonthIndex = new Date().getMonth();
currentYear = new Date().getFullYear()


$(document).ready(function () {
  $('.dropdown-menu').on('click', function (e) {
    e.stopPropagation();
  });
});

$(document).ready(function () {
  var ascending = false; // Флаг для отслеживания направления сортировки

  $('#sortButton').click(function () {
    var rows = $('#dataTable tbody tr').get();

    rows.sort(function (rowA, rowB) {
      var priceA = parseFloat($(rowA).find('td:first').text().replace(' р', '').trim());
      var priceB = parseFloat($(rowB).find('td:first').text().replace(' р', '').trim());
      if (ascending) {
        return priceA - priceB;
      } else {
        return priceB - priceA;
      }
    });

    $('#dataTable tbody').empty().append(rows);
    ascending = !ascending; // Инвертируем направление сортировки
  });
});



filterProjectsByColor()
function filterProjectsByColor(filter = -1) {
  if (filter == -1) {
    document.getElementById('sort-btn').onclick = function () {
      filterProjectsByColor(1);
    };
  } else if (filter == 1) {
    document.getElementById('sort-btn').onclick = function () {
      filterProjectsByColor(-1);
    };
  }
  var tableMenu = document.getElementsByClassName('table-item');
  var tableDeadline = document.getElementsByClassName('item-deadline');

  // Применение стилей к каждой строке
  for (var i = 0; i < tableMenu.length; i++) {
    var projectName = tableMenu[i].getAttribute('name-item');
    var tempArr = Array.from(tableDeadline).filter(item => item.getAttribute('name-item-deadline') === projectName)
      .map(item => parseInt(item.getAttribute('deadline-day').replace(' р', '')));
    red = '#f47171'
    green = '#1cc88a'
    var minDay = Math.min(...tempArr);
    tableMenu[i].style.backgroundColor = minDay < 0 ? red : green;
    tableMenu[i].style.color = 'black';
    // console.log(minDay);

  }
  tableRows = document.querySelectorAll('tr.filtered-item');

  var sortedRows = Array.from(tableRows).sort((a, b) => {
    var bgColorA = a.getElementsByClassName('table-item')[0].style.backgroundColor;
    var bgColorB = b.getElementsByClassName('table-item')[0].style.backgroundColor;

    function isRed(color) {
      // Проверка, является ли цвет красным
      return color === 'rgb(244, 113, 113)'; // Красный в формате RGB: (244, 113, 113)
    }

    if (isRed(bgColorA) && !isRed(bgColorB)) {
      return filter;
    } else if (!isRed(bgColorA) && isRed(bgColorB)) {
      return -filter;
    } else {
      // Примените сравнение цветов как строки
      return bgColorA.localeCompare(bgColorB);
    }
  });

  // Применение отсортированных строк к DOM
  if (tableRows[0]) {
    var parent = tableRows[0].parentNode;
    sortedRows.forEach(row => {
      parent.appendChild(row);
    });
  }
}

function get_and_post_projects(switcher, invoices = '') {
  // console.log(invoices)
  if (!invoices && invoices != '') {
    invoices = null
  }
  var url, elementID;
  if (switcher === 'project') {
    url = `${baseUrl}/deadline/get-all-projects?invoice=${encodeURIComponent(invoices)}`
    elementID = "dropdownProject"
  } else {
    url = `${baseUrl}/deadline/get-all-project-managers?invoice=${encodeURIComponent(invoices)}`
    elementID = "dropdownProjectManager"
  }


  fetch(url).then(response => response.json()).then(json => {
    // console.log(json)
    // console.log(switcher)
    prjectDropMenu = document.getElementById(elementID)
    prjectDropMenu.innerHTML = ''
    for (var i = 0; i < json.length; i++) {
      if (!json[i][switcher]) {
        json[i][switcher] = 'Пустые'
        // continue
      }
      var divElement = document.createElement("div");
      divElement.className = "form-check";

      // Создаем элемент input
      var inputElement = document.createElement("input");
      inputElement.className = `form-check-input input-${elementID}`;
      inputElement.type = "checkbox";
      inputElement.value = json[i][switcher] === 'Пустые' ? 'None' : json[i][switcher];
      inputElement.id = "flexCheck" + json[i][switcher];
      inputElement.checked = true;
      // inputElement.setAttribute('checked', '')

      // Создаем элемент label
      var labelElement = document.createElement("label");
      labelElement.className = "form-check-label";
      labelElement.htmlFor = "flexCheck" + json[i][switcher];
      labelElement.textContent = json[i][switcher];

      // Добавляем элементы внутрь div
      divElement.appendChild(inputElement);
      divElement.appendChild(labelElement);

      prjectDropMenu.appendChild(divElement);
    }
  })
}
get_and_post_projects('project')
get_and_post_projects('project_manager')
















// ПЕРЕЗАГРУЗКА СТРАНИЦЫ
function relad() {
  location.reload();
};
//-----------------------------------------------------
//---------------------ЛОГИКА ПОИСКА-------------------
//-----------------------------------------------------
$(document).ready(function () {
  // Обработка события ввода в поле поиска
  $('#searchInput').on('input', function () {
    // Получение введенного значения
    const searchTerm = $(this).val().toLowerCase();

    // Фильтрация элементов таблицыЦ
    $('#mainTable tr').each(function () {
      const name = $(this).find('.table-item').attr('name-item').toLowerCase();
      const isVisible = name.includes(searchTerm);
      $(this).toggle(isVisible);
    });
  });
});

//---------------------------------------------------------------------------
//----------------------------ВЫБОР НОМЕРА ЗКАЗА-----------------------------
//---------------------------------------------------------------------------
// mainHandlerDM()
function mainHandlerDM() {
  var project_names = document.getElementsByClassName('table-item')
  if (project_names.length > 0) {
    var tempArr = []
    for (var i = 0; i < project_names.length; i++) {
      tempArr.push((project_names[i].textContent).replace('\n              \n\n              \n            ', '').replace('\n              ', ''))
    }
    // console.log(tempArr, '-------------')
    fetch(`${baseUrl}/deadline/get-current-data`).then(response => response.json()).then(json => { //?customer=${encodeURIComponent(tempArr)}
      alldata = json
      console.log(json)
      showAllInfo(alldata)
    })
  }
  // tableBody = document.getElementById('tableBody')
  // tableBody.innerHTML = ''
}


function handleRowsByFilter(value, display, index = 6) {
  // console.log(value, display)
  // Получаем ссылку на таблицу
  var table = document.getElementById("dataTable");

  // Получаем все строки таблицы, начиная с первой (индекс 1, так как нулевая строка содержит заголовки)
  var rows = table.getElementsByTagName("tr");

  var ofOrOnCheckbox = ''


  var regex = /-----/;
  for (var i = 1; i < rows.length; i++) {
    // Получаем все ячейки (столбцы) текущей строки
    var cells = rows[i].getElementsByTagName("td");

    if (value == 'БН') {
      regex = /б.*\s*н/;
    } else if (value == 'onlynum') {
      regex = /^\d+$/
    }
    if (cells[index].textContent.includes(value) || cells[index].textContent.match(regex) || cells[index].textContent == value) {
      rows[i].style.display = display;
      if (index == 8) {
        ofOrOnCheckbox = cells[12].textContent
      } else if (index == 12) {
        ofOrOnCheckbox = cells[8].textContent
      }
    }
  }
  if (ofOrOnCheckbox) {
    return ofOrOnCheckbox
  }
}

function showAllInfo(data) {
  tableBody = document.getElementById('tableBody')
  tableBody.innerHTML = ''
  data.forEach(item => {
    const tr = document.createElement('tr');
    tr.className = 'tr-body text-center';

    const createAndAppendCell = (innerText, className = '') => {
      const td = document.createElement('td');
      td.innerText = innerText || 'None';
      td.className = className;
      return td;
    };
    if (item.deadline < 0) {
      console.log(item.deadline)
    }
    tr.appendChild(createAndAppendCell(item.deadline, item.deadline.includes('-') ? 'text-center marked min' : 'text-center marked plu'));
    tr.appendChild(createAndAppendCell(item.name));
    tr.appendChild(createAndAppendCell(item.document_number));
    tr.appendChild(createAndAppendCell(item.start_date));
    tr.appendChild(createAndAppendCell(item.end_date));
    tr.appendChild(createAndAppendCell(item.max_deadline));
    tr.appendChild(createAndAppendCell(item.no_invoice_1C));
    tr.appendChild(createAndAppendCell(item.project_group));
    tr.appendChild(createAndAppendCell(item.project_manager));
    tr.appendChild(createAndAppendCell(item.order_date));
    tr.appendChild(createAndAppendCell(item.provider));
    tr.appendChild(createAndAppendCell(item.invoice_date));
    tr.appendChild(createAndAppendCell(item.project));
    tr.appendChild(createAndAppendCell(item.responsible_sale));
    tr.appendChild(createAndAppendCell(item.contract_number));
    tr.appendChild(createAndAppendCell(item.date_document_signed));
    tr.appendChild(createAndAppendCell(item.order_sum));
    tr.appendChild(createAndAppendCell(item.account_amount));
    tr.appendChild(createAndAppendCell(item.customer_debt));

    tableBody.appendChild(tr);
  });
  // Получаем все элементы checkbox с классом "order-form-check"
  var checkboxes = document.querySelectorAll('.order-form-check');

  // Создаем массив для хранения информации о чекбоксах (отмечены или нет)
  var checkboxStatus = [];

  // Проходимся по каждому чекбоксу
  checkboxes.forEach(function (checkbox) {
    // console.log(checkbox)
    // Создаем объект, который будет хранить информацию о состоянии чекбокса
    var checkboxInfo = {
      value: checkbox.value,
      checked: checkbox.checked
    };

    // Добавляем информацию о чекбоксе в массив checkboxStatus
    checkboxStatus.push(checkboxInfo);
  });

  // Выводим информацию о состоянии чекбоксов в консоль
  // console.log(checkboxStatus, '4');

  // // Получаем ссылку на таблицу
  // var table = document.getElementById("dataTable");

  // // Получаем все строки таблицы, начиная с первой (индекс 1, так как нулевая строка содержит заголовки)
  // var rows = table.getElementsByTagName("tr");



  for (var value of checkboxStatus) {
    // console.log(value['checked'])
    if (value['checked']) {
      handleRowsByFilter(value['value'], "table-row");
    } else {
      handleRowsByFilter(value['value'], "none");
    }
  }

}


function handleDocumentNumber(index) {
  fetch(`${baseUrl}/deadline/get-all-data-by-id?id=${index + 1}`).then(response => response.json())
    .then(json => {
      showAllInfo(json)
    });
}

// function handleDocument(excelData) {
//   currentMonthIndex = new Date().getMonth();
//   currentYear = new Date().getFullYear()
//   // window.endDate = excelData.end_date
//   endDate = excelData.end_date
//   var whatDate = ''
//   if (endDate) {
//     if (endDate.includes('або')) { //Рабочие дни
//       whatDate = 'workDays'
//       var currentDate = new Date();
//       var numberOnly = endDate.replace(/\D/g, '');
//       var deadline = 0;
//       var startDateForCalc = new Date(excelData.start_date)
//       var daysCount = 0
//       var allDays = 0
//       while (daysCount != numberOnly) {
//         startDateForCalc.setDate(startDateForCalc.getDate() + 1);
//         allDays++
//         // Проверяем, является ли текущий день рабочим
//         if (startDateForCalc.getDay() !== 0 && startDateForCalc.getDay() !== 6) {
//           daysCount++;
//         }
//       }
//       if (currentDate < startDateForCalc) {
//         while (currentDate.toDateString() !== startDateForCalc.toDateString()) {
//           currentDate.setDate(currentDate.getDate() + 1);
//           if (currentDate.getDay() != 0 && currentDate.getDay() != 6) {
//             deadline++;
//           }
//         }
//       }
//       else {
//         while (currentDate.toDateString() !== startDateForCalc.toDateString()) {
//           currentDate.setDate(currentDate.getDate() - 1);
//           deadline += (currentDate.getDay() !== 0 && currentDate.getDay() !== 6) ? 1 : 0;
//         }
//         deadline *= -1
//       }
//       var startDate = new Date(excelData.start_date)
//       endDate = startDate.setDate(startDate.getDate() + allDays)
//       window.endDate = [new Date(endDate), ''];
//       endDateToTable = endDate[0]
//       updateCalendar();
//     } else { //Кален дни
//       whatDate = 'allDays'
//       var numberOnly = endDate.replace(/\D/g, '');
//       var startDate = new Date(excelData.start_date)
//       endDate = startDate.setDate(startDate.getDate() + parseInt(numberOnly))
//       window.endDate = new Date(endDate)
//       endDateToTable = endDate
//       var deadline = Math.floor((endDate - new Date()) / 86400000)
//       updateCalendar()
//     }

//     if (deadline < 0 && whatDate == 'allDays') {
//       document.getElementById('deadlineDay').innerText = deadline
//     } else if (whatDate == 'allDays') {
//       document.getElementById('deadlineDay').innerText = (deadline)
//     }
//     if (deadline < 0 && whatDate == 'workDays') {
//       document.getElementById('deadlineDay').innerText = deadline + " р"
//     } else if (whatDate == 'workDays') {
//       document.getElementById('deadlineDay').innerText = (deadline) + " р"
//     }
//     document.getElementById('customerTable').innerText = (excelData.name !== null) ? excelData.name : '-';
//     document.getElementById('docNumTable').innerText = excelData.document_number
//     document.getElementById('startDateTable').innerText = (excelData.start_date !== null) ? new Intl.DateTimeFormat('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(new Date(excelData.start_date)) : '-';
//     document.getElementById('endDateTable').innerText = (excelData.max_deadline !== null) ? new Intl.DateTimeFormat('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(new Date(excelData.max_deadline)) : '-';
//     document.getElementById('deadlineTable').innerText = (endDateToTable !== null) ? new Intl.DateTimeFormat('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(endDateToTable) : '-';
//     document.getElementById('NumFaktura').innerText = (excelData.no_invoice_1C !== null) ? excelData.no_invoice_1C : '-';

//     document.getElementById('dateOrderEntered').innerText = (excelData.order_date !== null) ? new Intl.DateTimeFormat('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(new Date(excelData.order_date)) : '-';
//     document.getElementById('provider').innerText = (excelData.provider !== null) ? excelData.provider : '-';
//     document.getElementById('projectManager').innerText = (excelData.project_manager !== null) ? excelData.project_manager : '-';
//     document.getElementById('projectGroup').innerText = (excelData.project_group !== null) ? excelData.project_group : '-';
//     document.getElementById('invoiceDate').innerText = (excelData.invoice_date !== null) ? new Intl.DateTimeFormat('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(new Date(excelData.invoice_date)) : '-';
//     document.getElementById('projectData').innerText = (excelData.project !== null) ? excelData.project : '-';
//   } else {
//     document.getElementById('deadlineDay').innerText = 'Не указан!'

//   }
// }
//-------------------------------------------------------------------
//---------------------------ФИЛЬТР----------------------------------
//-------------------------------------------------------------------


function onOrOffAllCheckboxes(inputClassName) {
  var checkBoxes = document.getElementsByClassName(inputClassName);
  var switcher = true;
  if (checkBoxes[0].checked) {
    switcher = false;
  } else {
    switcher = true;
  }
  for (var i = 0; i < checkBoxes.length; i++) {
    checkBoxes[i].checked = switcher;
    $(checkBoxes[i]).change();
    // Вызываем событие 'change' для каждого чекбокса
  }
}


//б.*\s*н
// addEventListener()
var invoiceArr = ['ГП', 'П/О', 'АПП', 'onlynum', 'БН', 'None'];
$(document).ready(function () {
  $('.order-form-check').change(function () {
    var checkboxId = $(this).attr('id');

    if ($(this).is(':checked')) {
      // console.log('Чекбокс с id ' + checkboxId + ' отмечен', $(this).attr('value'));

      invoiceArr.push($(this).attr('value'));
    } else {
      removeIndex = invoiceArr.indexOf($(this).attr('value'));
      invoiceArr.splice(removeIndex, 1);
      // console.log('Чекбокс с id ' + checkboxId + ' не отмечен', $(this).attr('value'));
    }
    // console.log(invoiceArr)
    filterCustomersByInvoice(invoiceArr.join('|'));
    // console.log(invoiceArr.join('|'))
    get_and_post_projects('project', invoiceArr.join('|'))
    get_and_post_projects('project_manager', invoiceArr.join('|'))
  });
  var onOrOff = ''

  function uncheckCheckboxByValue(value, className, bool) {
    $(`.${className}`).each(function () {
      if ($(this).val() == value) {
        $(this)[0].checked = bool;
      }
    });
  }


  $('#dropdownProject').on('change', '.input-dropdownProject', function () {
    var checkboxId = $(this).attr('id');
    if ($(this).is(':checked')) {
      valueToSwitch = handleRowsByFilter($(this).attr('value'), 'table-row', 12)
      uncheckCheckboxByValue(valueToSwitch, 'input-dropdownProjectManager', true)
    } else {
      valueToSwitch = handleRowsByFilter($(this).attr('value'), 'none', 12)
      uncheckCheckboxByValue(valueToSwitch, 'input-dropdownProjectManager', false)
    }
  });

  $('#dropdownProjectManager').on('change', '.input-dropdownProjectManager', function () {
    var checkboxId = $(this).attr('id');
    if ($(this).is(':checked')) {
      valueToSwitch = handleRowsByFilter($(this).attr('value'), 'table-row', 8)
      uncheckCheckboxByValue(valueToSwitch, 'input-dropdownProject', true)
    } else {
      valueToSwitch = handleRowsByFilter($(this).attr('value'), 'none', 8)
      uncheckCheckboxByValue(valueToSwitch, 'input-dropdownProject', false)
    }
  });

});





function filterCustomersByInvoice(invoice) {
  fetch(`${baseUrl}/deadline/get-data-by-invoice?invoice=${invoice}`).then(response => response.json()).then(json => {
    excelData = json;
    showCustomersByInvoice(excelData)
  });
}

function showCustomersByInvoice(excelData) {
  // console.log(excelData)
  var tableMenu = document.getElementById('mainTable');
  tableMenu.innerHTML = ''
  // console.log(tableMenu)
  if (excelData) {
    for (var i = 0; i < excelData.length; i++) {
      //var value = excelData[i].fields.document_number;
      var th = document.createElement('tr');
      th.className = 'dropright filtered-item';
      var cell = document.createElement('th');
      cell.scope = 'row';
      cell.id = 'table-item';
      cell.className = 'dropdown table-item';
      cell.setAttribute('name-item', excelData[i].name);
      cell.setAttribute('onclick', `handleChoiceItems('${excelData[i].name}')`);
      cell.setAttribute('data-toggle', 'dropdown');
      cell.textContent = excelData[i].name;

      var dropdownMenu = document.createElement('div');
      dropdownMenu.className = 'dropdown-menu';

      cell.appendChild(dropdownMenu);
      th.appendChild(cell);
      tableMenu.appendChild(th);
    }
  }
  mainHandlerDM()
  filterProjectsByColor()
  // var table = document.getElementById("dataTable");
  // var rows = table.getElementsByTagName("tr");
  // rows[row_i].style.display = display
  // console.log(row_i, display)
}



//------------------------------------------------------------------
//----------------------ВЫБОР ПОКУПАТЕЛЯ----------------------------
//------------------------------------------------------------------

function handleDropdownList(dropList, searchedItems) {
  var links = dropList.getElementsByTagName("a");

  // Преобразовать HTMLCollection в массив
  var linksArray = Array.from(links);

  // Перебрать все элементы и удалить их
  linksArray.forEach(function (link) {
    link.remove();
  });
  var uniqueValues = new Set();
  for (var i = 0; i < searchedItems.length; i++) {
    var value = searchedItems[i].document_number;
    var id = searchedItems[i].id - 1
    if (!uniqueValues.has(value)) {
      uniqueValues.add(value);
      var aElementTable = document.createElement('a');
      aElementTable.textContent = value;
      aElementTable.id = id;
      aElementTable.setAttribute('onclick', `handleDocumentNumber(${id})`);
      aElementTable.setAttribute('class', 'dropdown-item');
      dropList.appendChild(aElementTable);
    }
  }
}
function handleChoiceItems(selectedName) {
  var selected = document.querySelector(`[name-item='${selectedName}']`);
  var dropList = selected.querySelector('.dropdown-menu');
  dropList.innerHTML = ''
  //   var searchElement = document.getElementById('searchInput');
  var inputElementTable = document.createElement('input');
  inputElementTable.classList.add('mr-sm-2', 'dropdown-item');
  inputElementTable.type = 'search';
  inputElementTable.setAttribute('aria-label', 'Search');
  inputElementTable.setAttribute('placeholder', 'Поиск');
  inputElementTable.id = 'searchInput';
  //   var searchElement = document.getElementById('searchInput');
  var searchValue = ''
  var searchedItems = {};
  //const baseUrl = window.location.origin;
  fetch(`${baseUrl}/deadline/search?customer=${selectedName}&query=${searchValue}`).then(response => response.json())
    .then(json => {
      searchedItems = json;
      handleDropdownList(dropList, searchedItems)
    });
  inputElementTable.addEventListener('input', function () {
    searchValue = inputElementTable.value;
    fetch(`${baseUrl}/deadline/search?customer=${selectedName}&query=${searchValue}`).then(response => response.json())
      .then(json => {
        searchedItems = json;
        handleDropdownList(dropList, searchedItems)
      });
  });
  dropList.appendChild(inputElementTable)
  inputElementTable.addEventListener('click', function (event) {
    event.stopPropagation();
  });
}


//-----------------------------------ЛОГИКА КАЛЕНДАРЯ-----------------------------------------------------
//--------------------------------------------------------------------------------------------------------
// December is index 11 (0-based)
// const months = [
//   "Январь", "Февраль", "Март", "Апрель",
//   "Май", "Июнь", "Июль", "Август",
//   "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
// ];


// function changeMonth(delta) {
//   currentMonthIndex += delta;
//   if (currentMonthIndex < 0) {
//     currentMonthIndex = 11; // Wrap around to December
//     currentYear--;
//   } else if (currentMonthIndex > 11) {
//     currentMonthIndex = 0; // Wrap around to January
//     currentYear++;
//   }
//   updateCalendar();
// }
// endDate = undefined
// updateCalendar(); // Initial setup

// function updateCalendar() {
//   const currentMonthElement = document.getElementById("currentMonth");
//   const currentYearElement = document.getElementById("currentYear")
//   const daysContainer = document.querySelector('.days');

//   // Clear existing days
//   daysContainer.innerText = '';


//   var weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

//   // Проход по массиву дней недели
//   for (var i = 0; i < 7; i++) {
//     // Создать новый <div> элемент для каждого дня
//     var dayElement = document.createElement('div');
//     dayElement.classList.add('day');
//     dayElement.textContent = weekDays[i % 7]; // Использование остатка от деления для циклического повторения дней
//     dayElement.style = 'font-size: 12px;';
//     // Добавить созданный элемент в родительский элемент
//     daysContainer.appendChild(dayElement);
//   }

//   // Get the current date
//   const currentDate = new Date();

//   // Set the calendar header to the current month
//   currentMonthElement.textContent = months[currentMonthIndex] + " ";
//   currentYearElement.textContent = currentYear
//   // Get the first day of the current month
//   const firstDayOfMonth = new Date(currentYear, currentMonthIndex, 1);

//   // Get the last day of the current month
//   const lastDayOfMonth = new Date(currentYear, currentMonthIndex + 1, 0);

//   // Calculate the number of days in the month
//   const daysInMonth = lastDayOfMonth.getDate();

//   // Calculate the day of the week for the first day of the month
//   var startDayOfWeek = firstDayOfMonth.getDay() - 1;
//   if (startDayOfWeek === -1) {
//     startDayOfWeek = 6;
//   }

//   // Add the empty cells for the days before the first day of the month
//   for (let i = 0; i < startDayOfWeek; i++) {
//     const emptyDay = document.createElement('div');
//     emptyDay.className = 'day';
//     daysContainer.appendChild(emptyDay);
//   }
//   // Add the days of the month
//   for (let day = 1; day <= daysInMonth; day++) {
//     const dayElement = document.createElement('div');
//     dayElement.className = 'day';
//     dayElement.textContent = day;
//     dayElement.id = 'week';

//     const currentDay = new Date(currentYear, currentMonthIndex, day);
//     const isWeekend = currentDay.getDay() === 6 || currentDay.getDay() === 0;

//     if (isWeekend) {
//       dayElement.id = 'weekend';
//     }

//     // Add the 'current-day' class to mark the current day
//     if (
//       currentDate.getFullYear() === firstDayOfMonth.getFullYear() &&
//       currentDate.getMonth() === firstDayOfMonth.getMonth() &&
//       day === currentDate.getDate()
//     ) {
//       dayElement.classList.add('current-day');
//     }

//     if (endDate != undefined) {
//       endDate = endDate
//       if (Array.isArray(endDate) && !dayElement.id.includes('weekend')) {

//         endDate_ = endDate[0];
//       }
//       else if (Array.isArray(endDate) && dayElement.id.includes('weekend')) {
//         daysContainer.appendChild(dayElement);
//         continue
//       }
//       else if (!Array.isArray(endDate)) {
//         endDate_ = endDate
//       }
//       if (endDate_ >= currentDate) {
//         if (currentDate.getFullYear() === firstDayOfMonth.getFullYear() && currentDate.getMonth() === firstDayOfMonth.getMonth() && day > currentDate.getDate()) {
//           if (currentDate.getMonth() === endDate_.getMonth() && day <= endDate_.getDate()) {
//             dayElement.classList.add('marked-day');
//           } else if (currentDate.getMonth() < endDate_.getMonth() || currentDate.getFullYear() < endDate_.getFullYear()) {
//             dayElement.classList.add('marked-day');
//           }

//         } else if (firstDayOfMonth.getFullYear() === endDate_.getFullYear() && firstDayOfMonth.getMonth() === endDate_.getMonth() && day <= endDate_.getDate() && (firstDayOfMonth.getMonth() > currentDate.getMonth() || firstDayOfMonth.getFullYear() > currentDate.getFullYear())) {
//           dayElement.classList.add('marked-day');
//         } else if ((firstDayOfMonth.getFullYear() < endDate_.getFullYear() || firstDayOfMonth < endDate_) && firstDayOfMonth.getMonth() != endDate_.getMonth() && (firstDayOfMonth.getMonth() > currentDate.getMonth() || firstDayOfMonth.getFullYear() > currentDate.getFullYear()) && endDate_.getMonth() != currentDate.getMonth()) {
//           dayElement.classList.add('marked-day');
//         }
//       }
//       else {
//         if (currentDate.getFullYear() === firstDayOfMonth.getFullYear() && currentDate.getMonth() === firstDayOfMonth.getMonth() && day < currentDate.getDate()) {
//           if (currentDate.getMonth() === endDate_.getMonth() && day >= endDate_.getDate()) {
//             dayElement.classList.add('marked-passed-day');
//           } else if (currentDate.getMonth() > endDate_.getMonth() || currentDate.getFullYear() > endDate_.getFullYear()) {
//             dayElement.classList.add('marked-passed-day');
//           }
//         } else if ((firstDayOfMonth.getFullYear() > endDate_.getFullYear() || firstDayOfMonth.getMonth() > endDate_.getMonth()) && (firstDayOfMonth.getMonth() < currentDate.getMonth() && firstDayOfMonth.getFullYear() <= currentDate.getFullYear())) {
//           dayElement.classList.add('marked-passed-day');
//         } else if (firstDayOfMonth.getFullYear() === endDate_.getFullYear() && firstDayOfMonth.getMonth() === endDate_.getMonth() && day >= endDate_.getDate() && (firstDayOfMonth.getMonth() < currentDate.getMonth() || firstDayOfMonth.getFullYear() < currentDate.getFullYear())) {
//           dayElement.classList.add('marked-passed-day');
//         }
//       }
//     }
//     daysContainer.appendChild(dayElement);
//   }
// }

// // Function to update the calendar every second
// function updateRealTime() {
//   updateCalendar();
// };

// Call the initial setup functions
// updateRealTime();
