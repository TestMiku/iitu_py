let entered_objects = JSON.parse(localStorage.getItem('entered_objects')) || [];
let filledNomenclatureData = {};

$(document).ready(function() {
    function addNomenclature(nomenclatureId, nomenclatureKey, nomenclatureName) {
        if (nomenclatureId && nomenclatureKey && nomenclatureName) {
            let nomenclatureData = {
                key_search: nomenclatureKey
            };

            entered_objects.push(nomenclatureData);
            console.log(entered_objects);
            updateSelectedNomenclatureDetails();
            localStorage.setItem('entered_objects', JSON.stringify(entered_objects));
        } else {
            alert('Выберите номенклатурную позицию.');
        }
    }

    $(document).on('click', '.add-product', function() {
        const nomenclatureId = $(this).data('nomenclature-id');
        const nomenclatureKey = $(this).data('nomenclature-key-product');
        const nomenclatureName = $(this).data('nomenclature-name');
        const quantity = $(this).data('quantity');
        const tax = $(this).data('tax');
        const invoiceLine = $(this).data('invoice-line');
        const quantityEntered = $(this).data('quantity-entered');
        const order = $(this).data('order');
        const orderSpecification = $(this).data('order-specification');
        const totalSum = $(this).data('total-sum');
        addNomenclature(nomenclatureId, nomenclatureKey, nomenclatureName, quantity, tax, invoiceLine, quantityEntered, order, orderSpecification, totalSum);
    });

    function updateEnteredObject(index, key, value) {
        if (entered_objects[index]) {
            entered_objects[index][key] = value;
            filledNomenclatureData[entered_objects[index].key_search] = entered_objects[index];
            localStorage.setItem('entered_objects', JSON.stringify(entered_objects));
        }
    }

    $(document).on('input', '#selectedNomenclatureDetailsBody input', function() {
        let index = $(this).closest('tr').index();
        let field = $(this).data('field');
        let value = $(this).val();
        updateEnteredObject(index, field, value);
    });

    function updateSelectedNomenclatureDetails() {
        let tbody = $('#selectedNomenclatureDetailsBody');
        let selectedNomenclatureDetails = $('#selectedNomenclatureDetails');

        if (entered_objects.length > 0) {
            selectedNomenclatureDetails.show();
        } else {
            selectedNomenclatureDetails.hide();
        }

        tbody.empty();

        for (let i = 0; i < entered_objects.length; i++) {
            let tr = $('<tr></tr>');
            tr.html(`
                <td>${entered_objects[i].key_search}</td>
                <td><input type="text" class="form-control" value="${entered_objects[i].quantity || ''}" oninput="updateEnteredObject(${i}, 'quantity', this.value)"></td>
                <td><input type="text" class="form-control" value="${entered_objects[i].tax || ''}" oninput="updateEnteredObject(${i}, 'tax', this.value)"></td>
                <td><input type="text" class="form-control" value="${entered_objects[i].invoice_line || ''}" oninput="updateEnteredObject(${i}, 'invoice_line', this.value)"></td>
                <td><input type="text" class="form-control" value="${entered_objects[i].quantity_entered || ''}" oninput="updateEnteredObject(${i}, 'quantity_entered', this.value)"></td>
                <td><input type="text" class="form-control" value="${entered_objects[i].order || ''}" oninput="updateEnteredObject(${i}, 'order', this.value)"></td>
                <td><input type="text" class="form-control" value="${entered_objects[i].order_specification || ''}" oninput="updateEnteredObject(${i}, 'order_specification', this.value)"></td>
                <td><input type="text" class="form-control" value="${entered_objects[i].total_sum || ''}" oninput="updateEnteredObject(${i}, 'total_sum', this.value)"></td>
                <td><button class="btn btn-danger delete-product" data-index="${i}">Удалить</button></td>
            `);
            tbody.append(tr);
        }
    }

    $(document).on('click', '.delete-product', function() {
        let index = $(this).data('index');
        entered_objects.splice(index, 1);
        updateSelectedNomenclatureDetails();
        localStorage.setItem('entered_objects', JSON.stringify(entered_objects));
    });

    function performSearch(searchQuery) {
        $.ajax({
            url: $('#searchForm').attr('action'),
            data: { search: searchQuery },
            success: function(data) {
                $('#searchResults').html(data.html);

                // Re-attach click event for "Добавить" button after search results are loaded
                $('.add-product').off('click').on('click', function() {
                    const nomenclatureId = $(this).attr('value');
                    const nomenclatureName = $(this).data('nomenclature-name');
                    addNomenclature(nomenclatureId, nomenclatureName);
                });
            }
        });
    }

    let initialSearchQuery = $('#searchInput').val();
    if (initialSearchQuery) {
        performSearch(initialSearchQuery);
    }

    $('#searchInput').on('input', function() {
        var searchQuery = $(this).val();
        performSearch(searchQuery);
    });

    $('#searchInput').on('keyup', function(event) {
        if (event.keyCode === 32) {
            $(this).val('');
            performSearch('');
        }
    });

    $('#searchInput').on('input', function() {
        var searchQuery = $(this).val().trim();
        performSearch(searchQuery);

        if (searchQuery) {
            $('.pagination').hide();
        } else {
            $('.pagination').show();
        }
    });

    updateSelectedNomenclatureDetails();

    function createNomenclatureOrders() {
        let validatedObjects = [];

        // Проходим по всем ключам в filledNomenclatureData и добавляем валидные данные в список validatedObjects
        for (let key in filledNomenclatureData) {
            let obj = filledNomenclatureData[key];
            if (obj.quantity !== "" && obj.tax !== "" && obj.invoice_line !== "" && obj.quantity_entered !== "" && obj.order !== "" && obj.order_specification !== "" && obj.total_sum !== "") {
                validatedObjects.push(obj);
            } else {
                console.log('Неполные данные:', obj);
            }
        }

        if (validatedObjects.length > 0) {
            fetch('/nomenclature_add_to_order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': `{{ csrf_token }}`,
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ nomenclatures: validatedObjects }),
            })
            .then(response => {
                if (!response.ok) {
                    console.log(response.json());
                    throw new Error('Network response was not ok');
                }
                console.log('Ответ:', response);
                return response.json();
            })
            .then(data => {
                console.log('Созданы заказы номенклатуры:', data);
            })
            .catch(error => {
                console.error('Ошибка создания заказов номенклатуры:', error);
            });
        } else {
            console.log('Нет данных для отправки.');
        }
    }

    $('#createButton').on('click', function() {
        createNomenclatureOrders();
    });

});