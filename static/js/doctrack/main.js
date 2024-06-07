
document.addEventListener("DOMContentLoaded", function() {

    let qwer = get_hide_indexes_from_localstorage()
    let trs = document.querySelectorAll("tr")
    set_hide_indexes_to_localstorage(qwer)
    if(!`${window.location.pathname}`.includes("info")){
    
    qwer.forEach(function(index) {
        for (let i = 0; i < trs.length; i++) {
            let tds = trs[i].children
            tds[index].style.width = "0"; // Устанавливаем ширину на 0
            tds[index].style.overflow = "hidden"; // Скрываем контент
            tds[index].style.display = "none"; // Скрываем ячейку
        }
    })
    }
    document.querySelectorAll('.hide-column-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            let search_th = btn.parentNode
            let th = document.querySelectorAll("th")
            let hide_indexes = get_hide_indexes_from_localstorage() // Предполагается, что у вас есть функция get_hide_indexes_from_localstorage(), которая возвращает список скрытых индексов
            
            for (let i = 0; i < th.length; i++) {
                console.log(th[i].textContent == search_th.textContent)
                if (th[i].textContent == search_th.textContent) {
                    hide_indexes.push(i)
                    break; // Оптимизация: можно выйти из цикла, когда индекс найден
                }
            }

            tds = document.querySelectorAll("td")
            for (let i = 0; i < tds.length; i++) {
                tds[i].style.width = "auto"; // Возвращаем исходную ширину
                tds[i].style.overflow = "visible"; // Возвращаем исходное значение
            }
            
            hide_indexes.forEach(function(index) {
                for (let i = 0; i < trs.length; i++) {
                    let tds = trs[i].children
                    
                    tds[index].style.width = "0"; // Устанавливаем ширину на 0
                    tds[index].style.overflow = "hidden"; // Скрываем контент
                    tds[index].style.display = "none"; // Скрываем ячейку
                }
            })
            set_hide_indexes_to_localstorage(hide_indexes)

        });

    });

});


function get_hide_indexes_from_localstorage() {
    let hideIndexes = [];
    // Проверяем, есть ли данные в локальном хранилище
    if (localStorage.getItem('hideIndexes')) {
        // Если данные есть, парсим их из строки JSON
        hideIndexes = JSON.parse(localStorage.getItem('hideIndexes'));
    }
    return hideIndexes;
}

function set_hide_indexes_to_localstorage(hideIndexes) {
    const uniqueHideIndexes = new Set(hideIndexes);
    hideIndexes = Array.from(uniqueHideIndexes);

    set_show_buttons_to_container(hideIndexes)
    // Преобразуем массив скрытых индексов в строку JSON и сохраняем в локальное хранилище
    localStorage.setItem('hideIndexes', JSON.stringify(hideIndexes));
}



function set_show_buttons_to_container(hideIndexes) {
    try{
        let container = document.getElementById("hidden-columns");
        container.innerHTML = "";
        
        hideIndexes.forEach(index => {
            let th = document.querySelectorAll("th")[index];
            let thId = index;
            let textContent = th.textContent.trim();
            
            let button = document.createElement("a");
            button.setAttribute("class", "btn btn-secondary m-2");
            button.setAttribute("onclick", `show_table_column('${thId}')`);
            
            let icon = document.createElement("i");
            icon.setAttribute("class", "fas fa-eye mr-2");
            button.appendChild(icon);
            
            let buttonText = document.createTextNode(textContent);
            button.appendChild(buttonText);
            
            container.appendChild(button);
        });
    }catch(er){
        console.log(er.stack)
    }
}

function show_table_column(thId) {

    let hideIndexes = get_hide_indexes_from_localstorage()
    let new_hideIndexes = []
    hideIndexes.forEach(index => {
        if (index == thId) {
        } else{
            new_hideIndexes.push(index)
        }
    })
    set_hide_indexes_to_localstorage(new_hideIndexes)
    
    
    let th = document.querySelectorAll("th")
    for (let i = 0; i < th.length; i++) {
    th[i].style.width = "auto"; // Возвращаем исходную ширину
    th[i].style.overflow = "visible"; // Возвращаем исходное значение
    th[i].style.display = "table-cell"; // Возвращаем исходное значение
}

let tds = document.querySelectorAll("td")
for (let i = 0; i < tds.length; i++) {
    tds[i].style.width = "auto"; // Возвращаем исходную ширину
    tds[i].style.overflow = "visible"; // Возвращаем исходное значение
    tds[i].style.display = "table-cell"; // Возвращаем исходное значение
    }
    
    

    let hide_indexes = get_hide_indexes_from_localstorage() 
    let trs = document.querySelectorAll("tr")
    
    hide_indexes.forEach(function(index) {
        for (let i = 0; i < trs.length; i++) {
            let tds = trs[i].children
            
            tds[index].style.width = "0"; // Устанавливаем ширину на 0
            tds[index].style.overflow = "hidden"; // Скрываем контент
            tds[index].style.display = "none"; // Скрываем ячейку
        }
    })
}


let rotate_buttons = document.querySelectorAll('.rotate-button')
rotate_buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        this.classList.toggle('rotate');
    });
})



document.addEventListener('DOMContentLoaded', function() {
    var modalLinks = document.querySelectorAll('.open-modal');
    
    modalLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault();
        
        var url = this.getAttribute('href');
        var modalBody = document.querySelector('.modal-body-iframe');
        
        // Очищаем содержимое тела модального окна перед добавлением iframe
        modalBody.innerHTML = '';
        
        // Создаем iframe и добавляем его в тело модального окна
        var iframe = document.createElement('iframe');
        iframe.setAttribute('src', url);
        iframe.setAttribute('frameborder', '0');
        iframe.style.width = '100%'; // Устанавливаем ширину в 90% ширины окна браузера
        iframe.style.height = '80vh'; // Устанавливаем высоту в 80% высоты окна браузера
        modalBody.appendChild(iframe);
        
        // Показываем модальное окно
        var myModal = new bootstrap.Modal(document.getElementById('myModal'));
        myModal.show();
      });
    });
  });
  
  
  


  function changeDocumentStatus(doc_id){
    let doc_status = document.getElementById("id_document_status_"+doc_id)
    let doc_comment = document.getElementById("id_doc_comment_"+doc_id)
    let doc_comment_div = document.getElementById("id_doc_comment_div_"+doc_id)


    if (doc_status.value === "rejected") {
        doc_comment_div.style.display = "block";
        doc_comment.focus()
    } else {
        doc_comment_div.style.display = "none";
        doc_comment.value = ""
    }

  }
  function onchangeDocumentComment(doc_id) {
    let doc_comment = document.getElementById("id_doc_comment_" + doc_id);
    if (doc_comment.value.trim()) {
        doc_comment.classList.remove("red_light_box");
    } else {
        doc_comment.classList.add("red_light_box");
    }
}


async function get_rejected_status(status_id, request_id) {
    return fetch(`/mp/doctrack/is_rejected_status/${request_id}/${status_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
    }).then(response => response.json())
}


async function change_documents_status(status_id, request_id){
    get_rejected_status(status_id, request_id).then(data => {
        console.log('data:', data);
        let is_rejected = data.is_rejected;
        if (is_rejected) {
            document.querySelector('.write_comment_modal_body_content').style.display = 'block';

            document.querySelector('.background').classList.add('add-document-modal-open');

            document.querySelector('#close-write-comment').addEventListener('click', () => {
                document.querySelector('.background').classList.remove('add-document-modal-open');
                document.querySelector('.write_comment_modal_body_content').style.display = 'none';
            })

            document.querySelector('#send_comment_for_reject_order').addEventListener('click', () => {
                let comment = document.querySelector('#comment_rejected_order').value;
                fetch(`/mp/doctrack/comment_for_rejected_order/${request_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        comment: comment,
                    })
                }).then(response => response.json())
                    .then(data => {
                        console.log(data);
                        change_status(status_id, request_id);
                        window.location.reload();
                    }).catch(error => {
                        console.log(error)
                });
            });
        }
        else {
            change_status(status_id, request_id);
        }
    })

}


function change_status(status_id, request_id) {
    if (status_id == 0 && !document.getElementById("main_comment_text").value){
        alert("Заполните поле \"Комментарий\"")
        return
    }

    let doc_id__class = "document_id_class_for_upload"
    let doc_id_inputs = document.querySelectorAll("." + doc_id__class)

    let documents_for_send = []
    for (let i = 0; i < doc_id_inputs.length; i++){
        let doc_id = doc_id_inputs[i].value
        let doc_comment = document.getElementById("id_doc_comment_"+doc_id).value
        let doc_status = document.getElementById("id_document_status_"+doc_id).value
        let document_name = document.getElementById("document_name_"+doc_id).textContent.trim()


        let doc_comment_is_empty = true
        if (status_id == 0){
            doc_comment_is_empty = false
            doc_comment = document.getElementById("main_comment_text").value + " (Для всех отклоненных документов)"
            doc_status = "rejected"
        }

        if (doc_comment == "" && doc_status == "rejected"){
            let prompt_text = `Напишите комментарии для документа:\n - ${document_name}`
            while (doc_comment_is_empty){
                let new_comment = prompt(prompt_text, "");
                if (new_comment == null){
                    return 0
                }

                if (new_comment == ""){
                    prompt_text = "Вы не написали комментарии!!!\n" + prompt_text
                }
                else {
                    doc_comment = new_comment
                    doc_comment_is_empty = false
                }
            }
        }
        documents_for_send.push({
            "id" : doc_id,
            "comment" : doc_comment,
            "status" : doc_status
        })
    }
    url = `/mp/doctrack/change_document_status/${request_id}`
    let method = "POST"
    let body = {
        "documents" : documents_for_send,
        "request_status" : status_id,
        "request_id" : request_id
    }

    send_request(url, method, body)
}

function send_request(url, method, body) {
    document.body.innerHTML = `
    <style>
    .overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(255, 255, 255, 0.8); /* Прозрачный белый фон */
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999; /* Поверх всего остального контента */
    }
  </style>
</head>
<body>

<div class="overlay">
  <div class="text-center">
    <h2>Загрузка...</h2>
    <div class="spinner-border" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </div>
</div>
`
    let xhr = new XMLHttpRequest();
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            console.log("url: ", url)
            console.log("method: ", method)
            console.log("body: ", body)
            console.log("Запрос выполнен успешно");
            console.log(xhr.responseText);
        } else {
            console.error("Произошла ошибка при выполнении запроса: " + xhr.status);
        }
        location.reload();
    };
    xhr.onerror = function () {
        console.error("Произошла ошибка сети");
    };
    xhr.open(method, url, true);
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken()); 
    xhr.setRequestHeader("Content-Type", "application/json");
    let jsonBody = JSON.stringify(body);
    xhr.send(jsonBody);
}

function getCSRFToken() {
    var csrfToken = null;
    var cookieValue = document.cookie.match(/(?:^|;) ?csrftoken=([^;]*)(?:;|$)/);
    if (cookieValue) {
        csrfToken = cookieValue[1];
    }
    return csrfToken;
}

document.addEventListener("keydown", function(event) {
    if (event.keyCode == 116 || (event.ctrlKey && event.keyCode == 82)) {
        event.preventDefault(); // Предотвращаем стандартное поведение обновления страницы
        location.reload()
    }
});