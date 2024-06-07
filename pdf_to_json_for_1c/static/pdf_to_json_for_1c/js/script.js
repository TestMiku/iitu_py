function handleDragOver(event) {
    event.preventDefault();
    // Отмена стандартного действия по умолчанию, чтобы разрешить перетаскивание файла
    event.dataTransfer.dropEffect = 'copy';

    // Добавление класса для эффекта ховера
    document.getElementById('drop-area').classList.add('input-hover');
}

function handleDragLeave(event) {
    // Удаление класса для завершения эффекта ховера
    document.getElementById('drop-area').classList.remove('input-hover');
}

function handleDrop(event) {
    // Обработка события перетаскивания
    const file = event.dataTransfer.files[0];
    const fileInput = document.getElementById("fileInput");
    fileInput.files = event.dataTransfer.files;
    event.preventDefault();

    handleFile(file);
    // Удаление класса для завершения эффекта ховера

    document.getElementById('drop-area').classList.remove('input-hover');
}

function handleFileSelect(event) {
    // Обработка события выбора файла через input[type=file]
    const file = event.target.files[0];
    handleFile(file);
}

function handleFile(file) {

    console.log(fileInput.value)
    const baseUrl = window.location.origin;
    document.getElementById('drop-text').textContent = "Выбран файл: " + file.name;
    document.querySelector('.btn-sbmt').removeAttribute('hidden');


}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Теперь у вас есть CSRF-токен в переменной csrfToken, который вы можете использовать в ваших AJAX-запросах или других местах, где требуется CSRF-токен.


function selectFile() {
    // Имитация клика на input[type=file]
    document.getElementById('fileInput').click();
}
function importFile() {
    // Имитация клика на input[type=file]
    document.getElementById('fileImport').click();
}

function highlightText() {
    var textContainer = document.getElementById("textContainer");
    var selection = window.getSelection();
    console.log(selection)
    if (selection.rangeCount > 0) {
        var range = selection.getRangeAt(0);
        var selectedText = range.toString();

        if (selectedText !== '') {
            var newNode = document.createElement('span');
            newNode.className = 'highlighted';
            range.surroundContents(newNode);
            selection.removeAllRanges();
        }
    }
}


var images = document.querySelectorAll('.zoomable-image');

// Добавляем обработчик событий для каждого изображения
images.forEach(function (image) {
    // Инициализируем переменную для отслеживания текущего масштаба изображения
    var isZoomed = false;

    image.addEventListener('click', function (event) {
        // Если изображение не увеличено, то увеличиваем его
        if (!isZoomed) {
            // Получаем координаты клика пользователя относительно изображения
            var boundingRect = image.getBoundingClientRect();
            var offsetX = event.clientX - boundingRect.left;
            var offsetY = event.clientY - boundingRect.top;

            // Определяем размер области, которую нужно увеличить
            var zoomFactor = 2; // Коэффициент увеличения
            var zoomWidth = image.width / zoomFactor;
            var zoomHeight = image.height / zoomFactor;

            // Определяем координаты увеличенной области
            var zoomX = offsetX - zoomWidth / 2;
            var zoomY = offsetY - zoomHeight / 2;

            // Ограничиваем координаты, чтобы не выйти за границы изображения
            zoomX = Math.max(0, Math.min(zoomX, image.width - zoomWidth));
            zoomY = Math.max(0, Math.min(zoomY, image.height - zoomHeight));

            // Увеличиваем выбранную область изображения
            image.style.transformOrigin = zoomX + 'px ' + zoomY + 'px';
            image.style.transform = 'scale(' + zoomFactor + ')';

            // Помечаем изображение как увеличенное
            isZoomed = true;
        } else {
            // Если изображение уже увеличено, отменяем увеличение
            image.style.transform = 'none';
            isZoomed = false;
        }
    });
});


function addNewRow() {
    tBody = $('#table-body')

    var newRow = '<tr>'
        + `<td>${tBody.children().length + 1}</td>`
        + '<td><input type="text" class="form-control" style="width: 100px;"></td>'
        + '<td><input type="text" class="form-control"></td>'
        + '<td><input type="text" class="form-control" style="width: 100px;"></td>'
        + '<td><input type="text" class="form-control" style="width: 100px;"></td>'
        + '<td><input type="text" class="form-control"></td>'
        + '<td><input type="text" class="form-control"></td>'
        + '</tr>';
    tBody.append(newRow);
};


function downloadJson() {
    var json = [];
    var tempDict = {};
    var bin = $("#bin").val();
    var sender = $("#sender").val();
    var doc_number = $("#doc-number").val();
    var doc_date = $("#doc-date").val();
    var tBodysTr = $("#table-body").children('tr');
    var binByer = $("#bin-buyer").val();
    var schet = $("#schet").val();

    var order_number = $("#order_number").text()
    var fio = $("#fio").text()
    var who_certificate = $("#who_certificate").text()
    var date_certificate = $("#date_certificate").text()
    var iin = $("#iin").text()
    var element_id = $("#element_id").text()
    var gender = $("#gender").text()
    var certificate_number = $("#certificate_number").text()
    var user_prof = $("#user_prof").text()


    var dict = {
        "IDБитрикса": element_id,
        "Пол": gender,
        "НомерУдостоверения": certificate_number,
        "Долженость": user_prof,
        "БанковскийСчет": schet,
        "ОрганизацияБИН": binByer,
        "КонтрагентБИН": bin,
        "Контрагент": sender,
        "НомерЗаказа": order_number,
        "ФизЛицо": fio,
        "КемВыданоУдостоверение": who_certificate,
        "ДатаВыдачиУдостоверения": date_certificate,
        "ИИН": iin,
        "Товары": []
    }
    temparr = []
    tBodysTr.each(function (index, element) {
        cells = element.cells
        temparr.push({
            "НаименованиеТовара": cells[2].children[0].value,
            "ЕдиницаПоКлассификатору": cells[4].children[0].value,
            "Количество": cells[3].children[0].value,
        });
    })
    dict["Товары"] = temparr
    var csrftoken1 = document.querySelector('[name=csrf-token]').content;
    // Добавьте csrftoken в заголовок вашего AJAX-запроса
    console.log([dict])
    const csrftoken = getCookie('csrftoken');

    fetch('https://portal.avh.kz/pdf-t-jsn-f1c/send-to-1c', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken1
        },
        body: JSON.stringify(dict)
    }).then(function (response) {
        response.text().then(text => {
            //if (response.ok) {
            var animationContainer = document.getElementById("success-text-container");
            animationContainer.style.display = "block";
            animationContainer.textContent = text;
            // setTimeout(function () {
            //     animationContainer.style.display = "none";
            // }, 500);
            console.log(text);
            // } else {
            //     var animationContainer = document.getElementById("dungeon-text-container");
            //     animationContainer.style.display = "block";
            //     animationContainer.textContent = text;
            //     alert(text)
            //     console.log(text);
            // }
        });
    })

    R
    // var element = document.createElement('a');
    // element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(json)));
    // element.setAttribute('download', `${sender}-${doc_number}.json`);
    // element.style.display = 'none';
    // document.body.appendChild(element);
    // element.click();
    // document.body.removeChild(element);

}