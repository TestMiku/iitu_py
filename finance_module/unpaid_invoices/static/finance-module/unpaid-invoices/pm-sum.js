$(function () {
    const numberFormat = new Intl.NumberFormat("ru-RU", {
        maximumFractionDigits: 2,
        minimumFractionDigits: 2
    });
    const accountsTable = new AccountsTable({ url: "/p1/finance-module/api/project-region-accounts-table", canSelectAccount: false });
    accountsTable.reload();
    $("#unpaid-invoices-table").smartTableWithVirtualScroll({
        name: "pm-sum-unpaid-invoices",
        csrfToken,
        numberFormat,
        unload: [
            {
                html: `<i class="fa-solid fa-file-excel"></i> XLSX`,
                async onUnload(fieldValuesList, order) {
                    console.log(123);
                }
            }
        ],
        lastRowTarget: "#unpaid-invoices-last-row",
        rowsTarget: "#unpaid-invoices",
        getValuesUrl: "/p1/finance-module/pm-sum-unpaid-invoices-get-values",
        getRowsUrl: "/p1/finance-module/pm-sum-unpaid-invoices-get-rows",
        getSubtotalsUrl: "/p1/finance-module/pm-sum-unpaid-invoices-get-subtotals",
        loadingHtml: `
            <tr>
                <td class="text-center" colspan="52">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,
        getTr(row) {
            const $tr = $(`
                <tr class="unpaid-invoice-row" id="unpaid-invoice-row-${row.id}">
                    <td><div class="td-content">${row.number}</div></td>
                    <td><div class="td-content">${row.date}</div></td>
                    <td><div class="td-content">${row.invoice_number}</div></td>
                    <td><div class="td-content">${row.invoice_date}</div></td>
                    <td><div class="td-content" style="width: 90px;">${row.project}</div></td>
                    <td><div class="td-content">${row.responsible_user_id}</div></td>
                    <td><div class="td-content" style="width: 200px;">${row.approver}</div></td>
                    <td><div class="td-content" style="width: 120px;">${row.llc}</div></td>
                    <td><div class="td-content" style="width: 200px;">${row.contractor}</div></td>
                    <td><div class="td-content" style="width: 300px;">${row.comment}</div></td>
                    <td><div class="td-content">${row.currency}</div></td>
                    <td><div class="td-content"></div></td>
                    <td><div class="td-content">${row.invoice_category}</div></td>
                    <td><div class="td-content" style="width: 120px;">${row.revenue_expense_articles || ""}</div></td>
                    <td><div class="td-content" style="width: 90px;">${row.sales_order}</div></td>
                    <td><div class="td-content" style="width: 100px;">${row.bin_or_iin}</div></td>
                    <td><div class="td-content"></div></td>
                    <td><div class="td-content"></div></td>
                    <td><div class="td-content">${row.iic || ""}</div></td>
                    <td><div class="td-content">${row.payment_destination_code || ""}</div></td>
                    <td><div class="td-content">${row.contract_number}</div></td>
                    <td><div class="td-content">${numberFormat.format(row.invoice_amount)}</div></td>
                    <td><div class="td-content">${row.paid_amount_1c ? numberFormat.format(row.paid_amount_1c) : ""}</div></td>
                    <td><div class="td-content">${numberFormat.format(row.today_paid)}</div></td>
                    <td><div class="td-content">${numberFormat.format(row.planned_payment || 0)}</div></td>
                    <td><div class="td-content">${numberFormat.format(row.remainder)}</div></td>
                    <td><div class="td-content">${numberFormat.format(row.allowed_payment_amount)}</div></td>
                    <td class="p-1">
                        <select class="form-control form-control-sm unpaid-invoice-account-select" disabled>
                            <option value="">
                                Выберете расчётный счёт
                            </option>
                        </select>
                    </td> 
                    <td class="p-1">
                        <input type="number" min="0" max="${row.allowed_payment_amount}" step="0.01" class="form-control form-control-sm unpaid-invoice-sum-input" aria-describedby="sum-input-validation-${row.number}">
                        <div id="sum-input-validation-${row.number}"></div>
                    </td> 
                    <td><div class="td-content">${row.payment_decision}</div></td>
                    <td><div class="td-content">${row.bank}</div></td>
                </tr>
            `);
            const $accountSelect = $(".unpaid-invoice-account-select", $tr);
            if (accountsTable.loaded) {
                $accountSelect.prop("disabled", false);
                for (const account of accountsTable.getAccounts()) {
                    $accountSelect.append(`
                        <option value="${account.id}">
                            ${account.name}
                        </option>
                    `);
                }
            }
            const $sumInput = $(".unpaid-invoice-sum-input", $tr);
            const $validation = $(`#sum-input-validation-${row.number}`, $tr);
            $sumInput.prop("disabled", row.payment_decision != "OK");
            $sumInput.prop("title", row.payment_decision);
            if (row.pm_sum) {
                $sumInput.val(row.pm_sum);
            }
            function clamp() {
                const value = Math.min(row.allowed_payment_amount, Math.max(parseFloat($($sumInput).val()) || 0, 0));
                $($sumInput).val(value);
            }
            $sumInput.on("input", function() {
                clamp();
            });
            function valid(message) {
                $validation.addClass("valid-feedback");
                $validation.text(message);
                $sumInput.addClass("is-valid");
                $sumInput.prop("disabled", true);
                setTimeout(() => {
                    $sumInput.removeClass("is-valid");
                    $sumInput.prop("disabled", false);
                    $validation.removeClass("valid-feedback");
                    $validation.text(null);
                }, 1500);
            }
            function invalid(message) {
                $validation.addClass("invalid-feedback");
                $validation.text(message);
                $sumInput.addClass("is-invalid");
                $sumInput.prop("disabled", true);
                setTimeout(() => {
                    $sumInput.removeClass("is-invalid");
                    $sumInput.prop("disabled", false);
                    $validation.removeClass("invalid-feedback");
                    $validation.text(null);

                }, 1500);
            }
            $sumInput.on("change", async function() {
                clamp();
                const value = $(this).val();
                try {

                    const response = await fetch(updatePmSumUrl, {
                        method: "POST",
                        body: JSON.stringify({
                            sum: value,
                            number: row.number
                        }),
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    });
                    const json = await response.json();
                    if (json.detail == "OK") {
                        valid("OK");
                    } else {
                        invalid(json.detail);
                    }
                } catch (error) {
                    invalid(error);
                }
            });
            return $tr;
        }
    });
});