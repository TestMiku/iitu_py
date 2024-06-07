$(function() {
    $("#copy-table-btn").on("click", function() {
        this.disabled = true;
        const html = $(this).html();
        $(this).html(html + `<span class="ml-2">Скопировано</span>`);
        const $includeHeaderCheckbox = $("#include-header-checkbox");
        const $paidInvoicesTable = $("#paid-invoices-table");
        const $thead = $paidInvoicesTable.find("thead");
        if (!$includeHeaderCheckbox.prop("checked")) {
            $thead.addClass("d-none");
        }
        const selection = document.getSelection();
        selection.removeAllRanges();
        const range = document.createRange();
        range.selectNode($paidInvoicesTable[0]);
        selection.addRange(range);
        document.execCommand("copy");
        selection.removeAllRanges();
        if (!$includeHeaderCheckbox.prop("checked")) {
            $thead.removeClass("d-none");
        }
        setTimeout(() => {
            this.disabled = false;
            $(this).html(html);
        }, 2000);
    });
});