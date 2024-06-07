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
    // if (file) {
    //     console.log("Выбран файл:", file);
    //     const formData = new FormData(document.getElementById("file-form"));

    //     const xmlHttpRequest = new XMLHttpRequest();
    //     xmlHttpRequest.addEventListener("readystatechange", function () {
    //         if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
    //             console.log(this.response);
    //         }
    //     });
    //     xmlHttpRequest.open("POST", `${baseUrl}/og-by-kcell/excel-file-upload`);
    //     xmlHttpRequest.send(formData);
    // fetch(`${baseUrl}/og-by-kcell/excel-file-upload`, {
    //     method: 'POST',
    //     body: formData,
    // })
    //     .then(response => response.blob())  // Обработка как Blob (файл)
    //     .then(blob => {
    //         // blob - это ваш файл, который вы можете обработать
    //         console.log('File received:', response);

    //         // Пример: создание ссылки для скачивания файла
    //         const downloadLink = document.createElement('a');
    //         downloadLink.href = URL.createObjectURL(blob);
    //         downloadLink.download = 'excek.xlsx';  // Замените на нужное имя файла
    //         document.body.appendChild(downloadLink);
    //         downloadLink.click();
    //         document.body.removeChild(downloadLink);
    //     })
    //     .catch(error => {
    //         console.error('Error during file upload:', error);
    //     });
    // }
    document.getElementById('drop-text').textContent = "Выбран файл: " + file.name;
    document.querySelector('.btn-sbmt').removeAttribute('hidden');


}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }

    return null;
}

function selectFile() {
    // Имитация клика на input[type=file]
    document.getElementById('fileInput').click();
}
function importFile() {
    // Имитация клика на input[type=file]
    document.getElementById('fileImport').click();
}