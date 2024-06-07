
document.addEventListener("DOMContentLoaded", function() {
    let qwer = get_hide_indexes_from_localstorage()
    let trs = document.querySelectorAll("tr")
    set_hide_indexes_to_localstorage(qwer)


    
    qwer.forEach(function(index) {
        for (let i = 0; i < trs.length; i++) {
            let tds = trs[i].children
            
            tds[index].style.width = "0"; // Устанавливаем ширину на 0
            tds[index].style.overflow = "hidden"; // Скрываем контент
            tds[index].style.display = "none"; // Скрываем ячейку
        }
    })


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


