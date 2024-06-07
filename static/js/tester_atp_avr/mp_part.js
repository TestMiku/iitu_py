function upload_file_for_parsing() {
    var inputFile = document.getElementById('atp-parse-data');
    let html_tables = document.getElementById("atp-parsed-tables")
    html_tables.innerHTML = `<h1><i class="fas fa-spinner fa-pulse mx-2"></i></h1>`
    // Получаем выбранный файл
    var file = inputFile.files[0];
    
    if (file) {
      if (file.name.toLowerCase().endsWith(".pdf")) {
        console.log("PDF файл загружен");
        document.getElementById('atp-parse-data-file-name').innerHTML = file.name;
      // } else if (file.name.toLowerCase().endsWith(".html")) {
        // console.log("HTML файл загружен");
      } else {
        console.log("Загрузите PDF файл. Текущий файл: " + file.name.split(".")[file.name.split(".").length - 1].toUpperCase());
        alert("Загрузите PDF или HTML файл\nТекущий файл: " + file.name.split(".")[file.name.split(".").length - 1].toUpperCase());
        return; // Прерываем выполнение функции, так как файл не соответствует требованиям
      }
  
      var url = "/p1/tester-atp-avr/get-tables-as-html";
      var formData = new FormData();
      formData.append("file", file);
      formData.append("line-scale", 54);
      var xhr = new XMLHttpRequest();
      xhr.open("POST", url, true);
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            // console.log('Ответ от сервера:', xhr.responseText);
            create_table_response(JSON.parse(xhr.responseText))
            // Ваша обработка успешного ответа
            
          } else {
            console.error('Ошибка:', xhr.status, xhr.statusText);
            html_tables.innerHTML = `<p class="text-danger"><i class="fas fa-warinig fa-pulse mx-2"></i>` + 'Ошибка: ' + xhr.status + ", " + xhr.statusText + `</p>`
            // Ваша обработка ошибок
          }
        }
      };
      
      xhr.send(formData);
    } else {
      alert("Выберите файл для загрузки");
    }
  }
  
  
  function create_table_response(tables){
    enable_selection_index = 3
    enable_selection_index1 = 3

    // console.log(JSON.stringify(tables["additional_values"]))
    set_additional_values(tables["additional_values"])

    let html_tables = document.getElementById("atp-parsed-tables")
    let new_html_tables = `
  
  <label class="btn btn-danger active mb-3">
    <input type="radio" name="table-type-options" id="table-type-option1" checked> Акт монтажа (1)
  </label>
  <label class="btn btn-success active mb-3">
    <input type="radio" name="table-type-options" id="table-type-option3"> Акт монтажа (2)
  </label>
  <label class="btn btn-warning mb-3">
    <input type="radio" name="table-type-options" id="table-type-option2"> Оборудование от Заказчика
  </label>
  <button class="btn btn-primary mb-3" name="table-type-options" id="table-type-option4" onclick="clear_selection()">Сбросить</button>
  <ul class="navbar-nav accordion" id="accordionSidebar">`
  enable_selection_indexes = []
  tables["tables"].forEach( (table, index) => {
    console.log(`${table}`.toLowerCase().includes("код запаса"))
    if (`${table}`.toLowerCase().includes("код запаса")){
      enable_selection_indexes.push(index) // index
    }
    if (`${table}`.toLowerCase().includes("получено по накладной") && enable_selection_index1 == 3 ){
      enable_selection_index1 = index
    }
    new_html_tables += `
        <li class="card">
            <a class="card-header collapsed" href="#" data-toggle="collapse" data-target="#collapse_${index}" aria-expanded="false" aria-controls="collapse_${index}">
                <i class="fas fa-fw fa-table"></i>
                <span>Таблица #${index+1}</span>
            </a>
            <div id="collapse_${index}" class="collapse card-body" style="overflow: scroll; max-height: 600px" aria-labelledby="heading_${index}" data-parent="#accordionSidebar" style="">
            <button class="btn btn-primary mb-3" onclick="add_selection('collapse_${index}')">Выбрать все</button>
            <button class="btn btn-primary mb-3" onclick="remove_selection('collapse_${index}')">Убрать все</button>

                ${table}
            </div>
        </li>
    `  
  })
  new_html_tables += `</ul>` 
  html_tables.innerHTML = new_html_tables


  let tr_elements = html_tables.querySelectorAll("tr")
  let x = 0
  tr_elements.forEach(function(tr) {
    tr.addEventListener("click", function() {
      set_bg(tr)
      x+=1
    });
  });
  console.log(x)

  enable_selection(enable_selection_indexes)
  contractors_positions_table_enable_selection(enable_selection_index1)
}

function enable_selection(indexes){
  let op1 = document.getElementById('table-type-option1');
  let op2 = document.getElementById('table-type-option2');
  let op3 = document.getElementById('table-type-option3');
  
  op1.checked = true 
  op2.checked = false
  op3.checked = false
  
  if (indexes.length > 1){
    try{add_selection('collapse_'+indexes[0])}catch(er){console.log(er.stack)}
    op1.checked = false
    op2.checked = false
    op3.checked = true
    try{add_selection('collapse_'+indexes[1])}catch(er){console.log(er.stack)}
  }


}



function contractors_positions_table_enable_selection(index){
  let op1 = document.getElementById('table-type-option1');
  let op2 = document.getElementById('table-type-option2');
  let op3 = document.getElementById('table-type-option3');

  op1.checked = false 
  op3.checked = false 
  op2.checked = true 

  try{add_selection('collapse_'+index)}catch(er){}
  op3.checked = false
  op2.checked = false
  op1.checked = true
}


function set_bg(tr) {
  let op1 = document.getElementById('table-type-option1').checked;
  let op2 = document.getElementById('table-type-option2').checked;
  let op3 = document.getElementById('table-type-option3').checked;

  let cls1 = "tr_red";
  let cls2 = "tr_yellow";
  let cls3 = "tr_green";


  if (op1) {
    tr.classList.toggle(cls1);
  } else if (op2) {
    tr.classList.toggle(cls2);
  } else if (op3) {
    tr.classList.toggle(cls3);
  }
  
  if_multiple_choiced(tr)
  set_tables_akt1_akt2_smeta()
}


function clear_selection(){
  let html_tables = document.getElementById("atp-parsed-tables");
  let tr_elements = html_tables.querySelectorAll("tr");

  tr_elements.forEach(function(tr) {
    remove_classes(tr)
  });

  set_tables_akt1_akt2_smeta()
}

function remove_classes(tr, main = true, secondary = true){
  if (main){
    try{tr.classList.remove("tr_red");}catch(er){}
    try{tr.classList.remove("tr_yellow");}catch(er){}
    try{tr.classList.remove("tr_green");}catch(er){}
  }

  if (secondary){
    try{tr.classList.remove("tr_red_green");}catch(er){}
    try{tr.classList.remove("tr_red_yellow");}catch(er){}
    try{tr.classList.remove("tr_yellow_green");}catch(er){}
    try{tr.classList.remove("tr_red_yellow_green");}catch(er){}
  }
}


function add_selection(table_id){
  let html_tables = document.getElementById("atp-parsed-tables");
  let table = document.getElementById(table_id);
  let tr_elements = table .querySelectorAll("tr");

  let op1 = document.getElementById('table-type-option1').checked;
  let op2 = document.getElementById('table-type-option2').checked;
  let op3 = document.getElementById('table-type-option3').checked;

  let cls1 = "tr_red";
  let cls2 = "tr_yellow";
  let cls3 = "tr_green";

  if (op1){
    tr_elements.forEach(function(tr, index) {
      if (index != 0){
        try{ tr.classList.remove(cls1)} catch(er){}
        set_bg(tr)
      }
    });
  }
  if (op2){
    tr_elements.forEach(function(tr, index) {
      if (index != 0){
        try{ tr.classList.remove(cls2)} catch(er){}
        set_bg(tr)
      }
    });
  }
  if (op3){
    tr_elements.forEach(function(tr, index) {
      if (index != 0){
        try{ tr.classList.remove(cls3)} catch(er){}
        set_bg(tr)
      }
    });
  }
}

function remove_selection(table_id){
  
  let table = document.getElementById(table_id);
  let tr_elements = table .querySelectorAll("tr");

  let op1 = document.getElementById('table-type-option1').checked;
  let op2 = document.getElementById('table-type-option2').checked;
  let op3 = document.getElementById('table-type-option3').checked;

  let cls1 = "tr_red";
  let cls2 = "tr_yellow";
  let cls3 = "tr_green";
  

  if (op1){
    tr_elements.forEach(function(tr) {
      try{ tr.classList.remove(cls1)} catch(er){}
      if_multiple_choiced(tr)
    });
  }
  if (op2){
    tr_elements.forEach(function(tr) {
      try{ tr.classList.remove(cls2)} catch(er){}
      if_multiple_choiced(tr)
    });
  }
  if (op3){
    tr_elements.forEach(function(tr) {
      try{ tr.classList.remove(cls3)} catch(er){}
      if_multiple_choiced(tr)
    });
  }
  set_tables_akt1_akt2_smeta()
}



function if_multiple_choiced(tr){
  let cls13 = "tr_red_green";
  let cls12 = "tr_red_yellow";
  let cls23 = "tr_yellow_green";
  let cls123 = "tr_red_yellow_green";

  remove_classes(tr, false, true);
  let classListString= Array.from(tr.classList).join(', ');
  
  if (classListString.includes("red") && classListString.includes("yellow") && !classListString.includes("green")) {
    tr.classList.add(cls12);
  } else if (!classListString.includes("red") && classListString.includes("yellow") && classListString.includes("green")) {
    tr.classList.add(cls23);
  } else if (classListString.includes("red") && !classListString.includes("yellow") && classListString.includes("green")) {
    tr.classList.add(cls13);
  } else if (classListString.includes("red") && classListString.includes("yellow") && classListString.includes("green")) {
    tr.classList.add(cls123);
  }
}


function set_tables_akt1_akt2_smeta() {
  let html_tables = document.getElementById("atp-parsed-tables");

  let akt_montaz = document.getElementById("id_akt_montaz");
  let akt_montaz_rows = html_tables.getElementsByClassName("tr_red");
  akt_montaz.innerHTML = getHTMLRows(akt_montaz_rows);

  let akt_montaz1 = document.getElementById("id_akt_montaz1");
  let akt_montaz1_rows = html_tables.getElementsByClassName("tr_yellow");
  akt_montaz1.innerHTML = getHTMLRows(akt_montaz1_rows);

  let akt_montaz2 = document.getElementById("id_akt_montaz2");
  let akt_montaz2_rows = html_tables.getElementsByClassName("tr_green");
  akt_montaz2.innerHTML = getHTMLRows(akt_montaz2_rows);

  // let smeta = document.getElementById("id_smeta");
  // let smeta_rows = html_tables.getElementsByClassName("tr_green");
  // smeta.innerHTML = getHTMLRows(smeta_rows);
  

  document.getElementById("id_akt_montaz_input").value = document.getElementById("id_akt_montaz").innerHTML 
  document.getElementById("id_akt_montaz1_input").value = document.getElementById("id_akt_montaz1").innerHTML 
  document.getElementById("id_akt_montaz2_input").value = document.getElementById("id_akt_montaz2").innerHTML 
  // document.getElementById("id_smeta_input").value = document.getElementById("id_smeta").innerHTML 
}

function getHTMLRows(rows) {
  let htmlCode = "";
  for (let i = 0; i < rows.length; i++) {
    htmlCode += rows[i].outerHTML + "\n";
  }
  return htmlCode;
}


function set_additional_values(additional_values){
  myObject = additional_values
  for (var key in myObject) {
    if (myObject.hasOwnProperty(key)) {
      try{
        document.getElementById("id_" + key).value = myObject[key];
      } catch (er){}
    }
  }

  return
}





document.addEventListener('DOMContentLoaded', function() {
  var downloadLink = document.getElementById('downloadLink');

  downloadLink.addEventListener('click', function(event) {
      // Предотвращаем стандартное действие по клику, чтобы избежать перехода по ссылке
      event.preventDefault();

      // Создаем ссылку для скачивания с новым именем
      var link = document.createElement('a');
      link.href = downloadLink.href;

      // Устанавливаем новое имя файла
      link.download = 'NEW_NAME.docx';

      // Добавляем созданную ссылку в документ
      document.body.appendChild(link);

      // Имитируем клик по созданной ссылке
      link.click();

      // Удаляем ссылку из документа
      document.body.removeChild(link);
  });
});
