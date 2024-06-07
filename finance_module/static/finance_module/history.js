$(function () {
    const mandatoryPaymentRows = $(".mandatory-payment-row");
    const dateFilterTypeSelect = $("#date-filter-type-select");
    const rangeInputs = $("#range-inputs");
    const startDateInput = $("#start-date-input");
    const endDateInput = $("#end-date-input");
    const filterForm = $("#filter-form");
    const mandatoryPaymentSeizures = $("#mandatory-payment-seizures");
    let lastSelectedMandatoryPaymentRow = null;
    const $totalSum = $("#total-sum");
    const submitId = null;

    async function submit() {
        const numberFormat = Intl.NumberFormat("ru-RU", {minimumFractionDigits: 2, maximumFractionDigits: 2});
        if (dateFilterTypeSelect.val() === "range" && (!startDateInput.val() || !endDateInput.val())) {
            return;
        }

        const queryString = new URLSearchParams(new FormData(filterForm[0])).toString();
        $(`.mandatory-payment-row .sum`).add($totalSum).html(`<i class="fas fa-spinner fa-pulse"></i>`);
        mandatoryPaymentSeizures.html(`<tr><td colspan="6" class="text-center"><i class="fas fa-spinner fa-pulse"></i></td></tr>`)

        const response = await fetch(`${getMandatoryPaymentSeizuresUrl}?${queryString}`);
        $(`.mandatory-payment-row .sum`).add($totalSum).text(numberFormat.format(0));
        mandatoryPaymentSeizures.html(`<tr><td colspan="6" class="text-center">Ничего не удалось найти</td></tr>`)
        if (response.ok) {
            let totalSum = 0;
            mandatoryPaymentSeizures.html(null);
            const json = await response.json();
            const sums = {};
            console.log(json);
            for (const mandatoryPaymentSeizure of json) {
                const mandatoryPaymentId = mandatoryPaymentSeizure.mandatory_payment.id;
                if (mandatoryPaymentId in sums) {
                    sums[mandatoryPaymentId] += mandatoryPaymentSeizure.sum;
                } else {
                    sums[mandatoryPaymentId] = mandatoryPaymentSeizure.sum;
                }
                totalSum += mandatoryPaymentSeizure.sum;
                const responsible = mandatoryPaymentSeizure.responsible ? `${mandatoryPaymentSeizure.responsible.first_name} ${mandatoryPaymentSeizure.responsible.last_name} ${mandatoryPaymentSeizure.responsible.email}` : '';
                mandatoryPaymentSeizures.append(`
                    <tr class="mandatory-payment-seizure" data-mandatory-payment-id="${mandatoryPaymentId}">
                        <td>${mandatoryPaymentSeizure.mandatory_payment.name}</td>
                        <td>${mandatoryPaymentSeizure.project_region.name}</td>
                        <td>${mandatoryPaymentSeizure.account ? mandatoryPaymentSeizure.account.name : ''}</td>
                        <td>${new Date(mandatoryPaymentSeizure.datetime).toLocaleString()}</td>
                        <td>${responsible}</td>
                        <td class="text-right">${numberFormat.format(mandatoryPaymentSeizure.sum)}</td>
                    </tr>
                `);
            }
            $totalSum.text(numberFormat.format(totalSum));

            for (const [mandatoryPaymentId, sum] of Object.entries(sums)) {
                $(`.mandatory-payment-row[data-mandatory-payment-id=${mandatoryPaymentId}] .sum`).text(numberFormat.format(sum));
            }


        } else {
            console.error(response);
        }
    }

    mandatoryPaymentRows.on("click", function () {
        if (lastSelectedMandatoryPaymentRow != null) {
            $(lastSelectedMandatoryPaymentRow).removeClass("table-active");
            $(`.mandatory-payment-seizure.d-none`).removeClass("d-none");
            if (lastSelectedMandatoryPaymentRow === this) {
                lastSelectedMandatoryPaymentRow = null;
                return;
            }
        }
        const mandatoryPaymentId = $(this).data("mandatoryPaymentId");
        $(`.mandatory-payment-seizure:not([data-mandatory-payment-id=${mandatoryPaymentId}])`).addClass("d-none");
        $(this).addClass("table-active");
        lastSelectedMandatoryPaymentRow = this;
    });
    dateFilterTypeSelect.on("change", function () {
        rangeInputs.toggleClass("d-none", $(this).val() !== "range");
        rangeInputs.toggleClass("d-flex", $(this).val() === "range");
        $("input", rangeInputs).attr("required", $(this).val() === "range");
        $("input", rangeInputs).attr("hidden", $(this).val() !== "range");
        submit();
    });

    startDateInput.on("change", function () {
        endDateInput.prop("min", $(this).val());
        submit();

    });
    endDateInput.on("change", function () {
        startDateInput.prop("max", $(this).val());
        submit();
    });

    submit();
});