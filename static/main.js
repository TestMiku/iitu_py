document.addEventListener("DOMContentLoaded", () => {
    const submitButton = document.getElementById("submitButton");
    const inputData = document.getElementById("inputData");
    const dataSection = document.getElementById("dataSection");
    const table1 = document.getElementById("table1");
    const table2 = document.getElementById("table2");
    const dynamicTable = document.getElementById("dynamicTable");
    const toggleButton = document.getElementById("toggleButton");
    const warningContainer = document.getElementById("warningContainer");



    toggleButton.addEventListener("click", () => {
        if (dataSection.style.display === "none" || dataSection.style.display === "") {
            dataSection.style.display = "block";
        } else {
            dataSection.style.display = "none";
        }
    });

    submitButton.addEventListener("click", () => {
        const inputDataValue = inputData.value;

        // Perform AJAX request to your server with the inputDataValue
        // Process the server response and populate the tables with data

        // For demonstration purposes, I'm simulating data population
        populateTable(table1, 3, 20);
        populateTable(table2, 5, 20);
        populateDynamicTable(dynamicTable, 3, 20);
        dataSection.style.display = "block"; // Show the data section
    });
});


function populateTable(table, columns, rows) {
    // Clear the table first
    table.innerHTML = "";

    // Populate the table with data
    const headerRow = document.createElement("tr");
    for (let i = 0; i < columns; i++) {
        const th = document.createElement("th");
        th.textContent = `Header ${i + 1}`;
        headerRow.appendChild(th);
    }
    table.appendChild(headerRow);

    for (let i = 0; i < rows; i++) {
        const row = document.createElement("tr");
        for (let j = 0; j < columns; j++) {
            const cell = document.createElement("td"); // All cells are editable
            cell.textContent = `Row ${i + 1}, Col ${j + 1}`;
            row.appendChild(cell);
        }
        table.appendChild(row);
    }
}

function populateDynamicTable(table, columns, rows) {
    // Clear the table first
    table.innerHTML = "";

    // Populate the table with data
    const headerRow = document.createElement("tr");
    for (let i = 0; i < columns; i++) {
        const th = document.createElement("th");
        th.textContent = `Header ${i + 1}`;
        headerRow.appendChild(th);
    }
    table.appendChild(headerRow);

    for (let i = 0; i < rows; i++) {
        const row = document.createElement("tr");
        for (let j = 0; j < columns; j++) {
            const cell = document.createElement("td"); // All cells are editable
            if (j === 2) { // Make cells uneditable for the 3rd column
                cell.textContent = `Row ${i + 1}, Col ${j + 1}`;
            } else {
                const input = document.createElement("input");
                input.type = "text";
                input.value = `Row ${i + 1}, Col ${j + 1}`;
                cell.appendChild(input);
            }
            row.appendChild(cell);
        }
        table.appendChild(row);
    }
}
