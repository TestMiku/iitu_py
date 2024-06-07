


function getTotalSum() {
    return Array.from($(".sum-input")).reduce((previousValue, currentValue) => previousValue + (parseFloat($(currentValue).val()) || 0), 0);
}

function getSum() {
    return parseFloat($("#sum-input").val()) || 0;
}


function onSumInput() {
    const totalSum = getTotalSum();
    const sum = getSum();
    $("#total-sum").text(` - Общая сумма: ${formatPrice(totalSum)} = Остаток: ${formatPrice(sum - totalSum)}`)
}

function replaceEnteredSum() {
    $(this).parent().next().text(formatPrice(parseFloat($(this).val()) || 0));
}

$(function () {
    onSumInput();
    $("#import-file-form").on("submit", function () {
        $("#import-file-loading-icon").removeClass("d-none");
    });
    const sumInput = $(".sum-input");
    sumInput.on("input", onSumInput);
    sumInput.on("input", replaceEnteredSum);
    $("#sum-input").on("input", onSumInput);
    
    let distribute = false;
    $("#distribute-between-project-regions-form").on("submit", function (event) {
        const totalSum = getTotalSum();
        const sum = getSum();
        if (sum && sum - totalSum !== 0 && !distribute) {
            $("#difference-is-not-0-warning-modal").modal("show");
            event.preventDefault();
        }

    });
    $("#modal-distribute-button").on("click", function () {
        distribute = true;
        $("#distribute-between-project-regions-form").submit();
    });
});