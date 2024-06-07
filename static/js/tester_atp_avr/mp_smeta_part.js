
function upload_file_for_parsing_smeta(){
    var inputFile = document.getElementById('id_smeta_input');
    // let html_tables = document.getElementById("smeta-parsed-tables")
    // html_tables.innerHTML = `<h1><i class="fas fa-spinner fa-pulse mx-2"></i></h1>`
    // Получаем выбранный файл
    var file = inputFile.files[0];
    
    if (file) {
      if (file.name.toLowerCase().endsWith(".docx")) {
        console.log("WORD (.docx) файл загружен");
        document.getElementById('smeta-parse-data-file-name').innerHTML = file.name;
        return file
      // } else if (file.name.toLowerCase().endsWith(".html")) {
        // console.log("HTML файл загружен");
      } else {
        console.log("Загрузите WORD (.docx) файл. Текущий файл: " + file.name.split(".")[file.name.split(".").length - 1].toUpperCase());
        alert("Загрузите WORD файл\nТекущий файл: " + file.name.split(".")[file.name.split(".").length - 1].toUpperCase());
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
            smeta_create_table_response(JSON.parse(xhr.responseText))
            // alert(xhr.responseText)
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
  
  
function smeta_create_table_response(tables){
    let html_tables = document.getElementById("smeta-parsed-tables")
    let new_html_tables = ``
    enable_selection_index = 3
    
    new_html_tables+= `
        <button class="btn btn-primary mb-3" name="table-type-options" id="table-type-option3"onclick="clear_selection_smeta()">Сбросить</button>
        <ul class="navbar-nav accordion" id="accordionSidebar">
    `


    tables["tables"].forEach( (table, index) => {
        if (`${table}`.toLowerCase().includes("код запаса") && enable_selection_index == 3 ){
            enable_selection_index = index
        }
        new_html_tables += `
            <li class="card">
                <a class="card-header collapsed" href="#" data-toggle="collapse" data-target="#smeta_collapse_${index}" aria-expanded="false" aria-controls="smeta_collapse_${index}">
                    <i class="fas fa-fw fa-table"></i>
                    <span>Таблица #${index+1}</span>
                </a>
                <div id="smeta_collapse_${index}" class="collapse card-body" style="overflow: scroll; max-height: 600px" aria-labelledby="heading_${index}" data-parent="#accordionSidebar" style="">
                <button class="btn btn-primary mb-3" onclick="add_selection_smeta('smeta_collapse_${index}')">Выбрать все</button>
                <button class="btn btn-primary mb-3" onclick="remove_selection_smeta('smeta_collapse_${index}')">Убрать все</button>

                    ${table}
                </div>
            </li>
        `
    })
    new_html_tables += `</ul>` 
    html_tables.innerHTML = new_html_tables

    smeta_enable_selection(enable_selection_index)
}


function smeta_enable_selection(index){
    let html_tables = document.getElementById("smeta-parsed-tables");
    let tr_elements = html_tables.querySelectorAll("tr");

    tr_elements.forEach(function(tr) {
        tr.addEventListener("click", function() {
            smeta_set_bg(tr)
        });
    });

    // try{smeta_add_selection('collapse_'+index)}catch(er){}
}


function smeta_set_bg(tr) {
    tr.classList.toggle("tr_green");
    set_tables_smeta()
}

function set_tables_smeta() {
    let html_tables = document.getElementById("smeta-parsed-tables");    
    let smeta = document.getElementById("id_smeta");
    let smeta_rows = html_tables.getElementsByClassName("tr_green");
    smeta.innerHTML = getHTMLRows(smeta_rows);
    
    document.getElementById("id_smeta_input").value = document.getElementById("id_smeta").innerHTML
    }
    
function getHTMLRows(rows) {
    let htmlCode = "";
    for (let i = 0; i < rows.length; i++) {
        htmlCode += rows[i].outerHTML + "\n";
    }
    return htmlCode;
}


function add_selection_smeta(smeta_collapse_index){
    let table = document.getElementById(smeta_collapse_index)
    let rows = table.getElementsByTagName("tr")
    for (let i = 0 ; i < rows.length; i++){
        let tr = rows[i]
        try{tr.classList.remove("tr_green");}catch(er){console.log(er.stack)}
        tr.classList.add("tr_green");
    }
    set_tables_smeta()
}


function remove_selection_smeta(smeta_collapse_index){
    let table = document.getElementById(smeta_collapse_index)
    let rows = table.getElementsByTagName("tr")
    for (let i = 0 ; i < rows.length; i++){
        let tr = rows[i]
        try{tr.classList.remove("tr_green");}catch(er){console.log(er.stack)}
    }
    set_tables_smeta()
}

function clear_selection_smeta(){
    let html_tables = document.getElementById("smeta-parsed-tables");    
    let rows = html_tables.getElementsByTagName("tr")
    
    for(let i = 0 ; i < rows.length; i++){
        let tr = rows[i];
        try{tr.classList.remove("tr_green");}catch(e){}
    }

    set_tables_smeta()
}




  
//   function upload_file_for_parsing() {
//       var inputFile = document.getElementById('atp-parse-data');
//       let html_tables = document.getElementById("atp-parsed-tables")
//       html_tables.innerHTML = `<h1><i class="fas fa-spinner fa-pulse mx-2"></i></h1>`
//       // Получаем выбранный файл
//       var file = inputFile.files[0];
      
//       if (file) {
//         if (file.name.toLowerCase().endsWith(".pdf")) {
//           console.log("PDF файл загружен");
//           document.getElementById('atp-parse-data-file-name').innerHTML = file.name;
//         // } else if (file.name.toLowerCase().endsWith(".html")) {
//           // console.log("HTML файл загружен");
//         } else {
//           console.log("Загрузите PDF файл. Текущий файл: " + file.name.split(".")[file.name.split(".").length - 1].toUpperCase());
//           alert("Загрузите PDF файл\nТекущий файл: " + file.name.split(".")[file.name.split(".").length - 1].toUpperCase());
//           return; // Прерываем выполнение функции, так как файл не соответствует требованиям
//         }
    
//         var url = "/p1/tester-atp-avr/get-tables-as-html";
//         var formData = new FormData();
//         formData.append("file", file);
//         formData.append("line-scale", 54);
//         var xhr = new XMLHttpRequest();
//         xhr.open("POST", url, true);
//         xhr.onreadystatechange = function () {
//           if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {
//               // console.log('Ответ от сервера:', xhr.responseText);
//               create_table_response(JSON.parse(xhr.responseText))
//               // Ваша обработка успешного ответа
              
//             } else {
//               console.error('Ошибка:', xhr.status, xhr.statusText);
//               html_tables.innerHTML = `<p class="text-danger"><i class="fas fa-warinig fa-pulse mx-2"></i>` + 'Ошибка: ' + xhr.status + ", " + xhr.statusText + `</p>`
//               // Ваша обработка ошибок
//             }
//           }
//         };
        
//         xhr.send(formData);
//       } else {
//         alert("Выберите файл для загрузки");
//       }
//     }
    
    

  
//   function enable_selection(index){
//     let html_tables = document.getElementById("atp-parsed-tables");
//     let tr_elements = html_tables.querySelectorAll("tr");
  
//     tr_elements.forEach(function(tr) {
//       tr.addEventListener("click", function() {
//         set_bg(tr)
//       });
//     });
  
//     try{add_selection('collapse_'+index)}catch(er){}
//   }
  
  
//   function smeta_enable_selection(index){
//     let html_tables = document.getElementById("smeta-parsed-tables");
//     let tr_elements = html_tables.querySelectorAll("tr");
  
//     tr_elements.forEach(function(tr) {
//       tr.addEventListener("click", function() {
//         set_bg(tr)
//       });
//     });
  
//     try{add_selection('smeta_collapse_'+index)}catch(er){}
//   }
  
  
//   function set_bg(tr, is_smeta = false) {
//     try{
  
//       let op1 = document.getElementById('table-type-option1').checked;
//       let op2 = document.getElementById('table-type-option2').checked;
//       let op3 = document.getElementById('table-type-option3').checked;
//     }catch(error){
//       console.log(error.stack)
//     }
//     let cls1 = "tr_red";
//     let cls2 = "tr_yellow";
//     let cls3 = "tr_green";
  
//     if (is_smeta){
//       tr.classList.toggle(cls3);
//     }
  
//     try{if (op1) {
//       tr.classList.toggle(cls1);
//     } else if (op2) {
//       tr.classList.toggle(cls2);
//     } else if (op3) {
//       tr.classList.toggle(cls3);
//     }}catch(e){}
    
//     if_multiple_choiced(tr)
//     set_tables_akt1_akt2_smeta()
  
//   }
  
  
//   function clear_selection(){
//     let html_tables = document.getElementById("atp-parsed-tables");
//     let tr_elements = html_tables.querySelectorAll("tr");
  
//     tr_elements.forEach(function(tr) {
//       remove_classes(tr)
//     });
  
//     set_tables_akt1_akt2_smeta()
//   }
  
//   function remove_classes(tr, main = true, secondary = true){
//     if (main){
//       try{tr.classList.remove("tr_red");}catch(er){}
//       try{tr.classList.remove("tr_yellow");}catch(er){}
//       try{tr.classList.remove("tr_green");}catch(er){}
//     }
  
//     if (secondary){
//       try{tr.classList.remove("tr_red_green");}catch(er){}
//       try{tr.classList.remove("tr_red_yellow");}catch(er){}
//       try{tr.classList.remove("tr_yellow_green");}catch(er){}
//       try{tr.classList.remove("tr_red_yellow_green");}catch(er){}
//     }
//   }
  
  
//   function add_selection(table_id, is_not_smeta=true){
//     let html_tables = document.getElementById("atp-parsed-tables");
//     let table = document.getElementById(table_id);
//     let tr_elements = table .querySelectorAll("tr");
    
//     try{
//     let op1 = document.getElementById('table-type-option1').checked;
//     let op2 = document.getElementById('table-type-option2').checked;
//     let op3 = document.getElementById('table-type-option3').checked;}catch(e){}
  
//     let cls1 = "tr_red";
//     let cls2 = "tr_yellow";
//     let cls3 = "tr_green";
  
//     if(is_not_smeta){
//       if (op1){
//         tr_elements.forEach(function(tr) {
//           try{ tr.classList.remove(cls1)} catch(er){}
//           set_bg(tr)
//         });
//       }
//       if (op2){
//         tr_elements.forEach(function(tr) {
//           try{ tr.classList.remove(cls2)} catch(er){}
//           set_bg(tr)
//         });
//       }
//       if (op3){
//         tr_elements.forEach(function(tr) {
//           try{ tr.classList.remove(cls3)} catch(er){}
//           set_bg(tr)
//         });
//       }
//       else{
//         try{ tr.classList.remove(cls3)} catch(er){}
//         set_bg(tr)
//       }
//     } else {
//       try{ tr.classList.remove(cls3)} catch(er){}
//       set_bg(tr, true)
//     }
//   }
  
//   function remove_selection(table_id, is_not_smeta=true){
    
//     let table = document.getElementById(table_id);
//     let tr_elements = table .querySelectorAll("tr");
    
//     try{ let op1 = document.getElementById('table-type-option1').checked;
//     let op2 = document.getElementById('table-type-option2').checked;
//     let op3 = document.getElementById('table-type-option3').checked;}catch(e){}
  
//     let cls1 = "tr_red";
//     let cls2 = "tr_yellow";
//     let cls3 = "tr_green";
  
//     if (is_not_smeta){
//       if (op1){
//         tr_elements.forEach(function(tr) {
//           try{ tr.classList.remove(cls1)} catch(er){}
//           if_multiple_choiced(tr)
//         });
//       }
//       if (op2){
//         tr_elements.forEach(function(tr) {
//           try{ tr.classList.remove(cls2)} catch(er){}
//           if_multiple_choiced(tr)
//         });
//       }
//       if (op3){
//         tr_elements.forEach(function(tr) {
//           try{ tr.classList.remove(cls3)} catch(er){}
//           if_multiple_choiced(tr)
//         });
//       }
//     }
//     else{
//       try{ tr.classList.remove(cls3)} catch(er){}
//       if_multiple_choiced(tr)
  
//     }
//     set_tables_akt1_akt2_smeta()
//   }
  
  
  
//   function if_multiple_choiced(tr){
//     let cls13 = "tr_red_green";
//     let cls12 = "tr_red_yellow";
//     let cls23 = "tr_yellow_green";
//     let cls123 = "tr_red_yellow_green";
  
//     remove_classes(tr, false, true);
//     let classListString= Array.from(tr.classList).join(', ');
    
//     if (classListString.includes("red") && classListString.includes("yellow") && !classListString.includes("green")) {
//       tr.classList.add(cls12);
//     } else if (!classListString.includes("red") && classListString.includes("yellow") && classListString.includes("green")) {
//       tr.classList.add(cls23);
//     } else if (classListString.includes("red") && !classListString.includes("yellow") && classListString.includes("green")) {
//       tr.classList.add(cls13);
//     } else if (classListString.includes("red") && classListString.includes("yellow") && classListString.includes("green")) {
//       tr.classList.add(cls123);
//     }
//   }
  
  
//   function set_tables_akt1_akt2_smeta() {
//     let html_tables = document.getElementById("atp-parsed-tables");
  
//     let akt_montaz = document.getElementById("id_akt_montaz");
//     let akt_montaz_rows = html_tables.getElementsByClassName("tr_red");
//     akt_montaz.innerHTML = getHTMLRows(akt_montaz_rows);
  
//     let akt_montaz1 = document.getElementById("id_akt_montaz1");
//     let akt_montaz1_rows = html_tables.getElementsByClassName("tr_yellow");
//     akt_montaz1.innerHTML = getHTMLRows(akt_montaz1_rows);
  
//     let smeta = document.getElementById("id_smeta");
//     let smeta_rows = html_tables.getElementsByClassName("tr_green");
//     smeta.innerHTML = getHTMLRows(smeta_rows);
    
  
//     document.getElementById("id_akt_montaz_input").value = document.getElementById("id_akt_montaz").innerHTML 
//     document.getElementById("id_akt_montaz1_input").value = document.getElementById("id_akt_montaz1").innerHTML 
//     document.getElementById("id_smeta_input").value = document.getElementById("id_smeta").innerHTML 
//   }
  
//   function getHTMLRows(rows) {
//     let htmlCode = "";
//     for (let i = 0; i < rows.length; i++) {
//       htmlCode += rows[i].outerHTML + "\n";
//     }
//     return htmlCode;
//   }
  
  
//   function set_additional_values(additional_values){
//     myObject = additional_values
//     for (var key in myObject) {
//       if (myObject.hasOwnProperty(key)) {
//         try{
//           document.getElementById("id_" + key).value = myObject[key];
//         } catch (er){}
//       }
//     }
  
//     return
//   }











