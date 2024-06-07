/*
ВНИМАНИЕ!!!
Читать с закрытыми глазами и ничего не трогать.
И еще прошу прощение за такой ужасный код, я это писал думая что перепишу нахуй всё это.
*/


function mandatoryPaymentsAddEventListeners() {
    const $mandatoryPaymentTableContainer = $("#mandatory-payments-table-container");
    const $mandatoryPaymentTableContentContainer = $(`
        <div class="mandatory-payments-table__selected-content-container">
            <div class="mandatory-payments-table__selected-content-container-blackout"></div>
            <div class="mandatory-payments-table__selected-content-column"></div>
            <div class="mandatory-payments-table__selected-content-menu">
                <form id="menu-form">
                    <input type="number" id="mandatory-payments-sum-input" step="0.01" class="form-control" placeholder="Введите сумму">
                    <div id="min-input-sum-container">
                        <small>Минимум: <a id="mandatory-payments-set-min-sum" href="#" title="Поставить минимальную сумму"><span id="min-input-sum"></span></a></small> 
                    </div>
                    <small id="deadline-text">Оплатить надо до: <span id="deadline"></span></small>
                </form>
            </div>
        </div>
    `).appendTo($mandatoryPaymentTableContainer);
    const $mandatoryPaymentTableContentColumn = $mandatoryPaymentTableContentContainer.find(".mandatory-payments-table__selected-content-column");
    const $mandatoryPaymentTableContentMenu = $mandatoryPaymentTableContentContainer.find(".mandatory-payments-table__selected-content-menu");
    const $mandatoryPaymentTable = $(".mandatory-payments-table");
    const $menuForm = $mandatoryPaymentTableContentContainer.find("#menu-form");
    $mandatoryPaymentsSumInput = $mandatoryPaymentTableContentContainer.find("#mandatory-payments-sum-input");
    const $minInputSum = $mandatoryPaymentTableContentContainer.find("#min-input-sum");
    const $deadline = $mandatoryPaymentTableContentContainer.find("#deadline");
    const $deadlineText = $mandatoryPaymentTableContentContainer.find("#deadline-text");
    let column = null;
    function addClasses() {
        $mandatoryPaymentTableContainer.addClass("mandatory-payments-table-container_selected-content-is-active");
        $mandatoryPaymentTableContentContainer.addClass("mandatory-payments-table__selected-content-container_active");
    }
    function removeClasses() {
        $mandatoryPaymentTableContainer.removeClass("mandatory-payments-table-container_selected-content-is-active");
        $mandatoryPaymentTableContentContainer.removeClass("mandatory-payments-table__selected-content-container_active");
    }

    $mandatoryPaymentTableContentContainer.find(".mandatory-payments-table__selected-content-container-blackout").on("click", function () {
        removeClasses();
        column = null;
    });

    function showColumnMenu(target) {
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'center'
        });
        addClasses();
        column = $(target);
        const position = $(target).position();
        const min = parseFloat($(target).data("min")) || 0;
        $mandatoryPaymentsSumInput.val($(target).data("sum") || min);
        $deadlineText.prop("hidden", !$(target).data("deadline"));
        $deadline.text($(target).data("deadline"));
        $mandatoryPaymentsSumInput.prop("min", min);
        $("#min-input-sum-container").toggleClass("d-none", !min)
        $minInputSum.text(numberFormat.format(min));
        $mandatoryPaymentTableContentColumn.css({
            ...position,
            width: `calc(${$(target).outerWidth()}px - var(--border-width))`,
            height: $(target).outerHeight()
        });
        const rightTop = position.left + $mandatoryPaymentTableContentMenu.outerWidth();
        if (rightTop > $mandatoryPaymentTableContainer.outerWidth() + $mandatoryPaymentTableContainer.scrollLeft() || rightTop > $mandatoryPaymentTable.outerWidth()) {
            position.left -= $mandatoryPaymentTableContentMenu.outerWidth() - $mandatoryPaymentTableContentColumn.outerWidth();
            position.left = `calc(${position.left}px + var(--border-width))`;

        } else {
            position.left = `calc(${position.left}px - var(--border-width))`;
        }
        const leftBottom = position.top + $mandatoryPaymentTableContentMenu.outerHeight() + $(target).outerHeight();
        if (leftBottom > $mandatoryPaymentTableContainer.outerHeight() + $mandatoryPaymentTableContainer.scrollTop() || leftBottom > $mandatoryPaymentTable.outerHeight()) {
            $mandatoryPaymentTableContentColumn.css({
                top: `calc(${parseFloat(position.top)}px - var(--border-width))`
            });
            position.top -= $mandatoryPaymentTableContentMenu.outerHeight() + $mandatoryPaymentTableContentColumn.outerHeight();
            position.top = `calc(${position.top}px - var(--border-width))`;
            $mandatoryPaymentTableContentMenu.css({
                borderBottom: "none",
                borderTop: "var(--border)"
            });
        } else {
            $mandatoryPaymentTableContentMenu.css({
                borderBottom: "",
                borderTop: ""

            });
        }
        $mandatoryPaymentTableContentMenu.css({
            top: position.top,
            left: position.left
        })
        const initial = parseFloat($(target).data("initial")) || 0;
        if (initial > 0) {
            $mandatoryPaymentTableContentColumn.html(`
                <a id="mandatory-payments-set-max-sum" href="#" title="Поставить максимальную сумму">${numberFormat.format(initial)}</a>
            `);
        } else {
            $mandatoryPaymentTableContentColumn.text(numberFormat.format(initial));
        }
        $mandatoryPaymentsSumInput.focus();
    }

    $mandatoryPaymentTableContainer.on("click", "#mandatory-payments-set-min-sum", function (event) {
        event.preventDefault();
        const min = parseFloat($(column).data("min")) || 0;
        $mandatoryPaymentsSumInput.val(min);
        $menuForm.submit();
    });
    $mandatoryPaymentTableContainer.on("click", "#mandatory-payments-set-max-sum", function (event) {
        event.preventDefault();
        const initial = parseFloat($(column).data("initial")) || 0;
        $mandatoryPaymentsSumInput.val(initial);
        $menuForm.submit();
    });

    $(".mandatory-payments-table__column").on("click", function () {
        showColumnMenu(this);
    });
    $(document).on("keydown", function (event) {
        if (event.keyCode === 27) {
            removeClasses();
        }
    });
    $mandatoryPaymentsSumInput.on("input", function () {
        setSumInput(column);
    });
    $menuForm.on("submit", function (event) {
        removeClasses();
        setSumInput(column);
        return false;
    });
}

function setSumInput(column) {
    const min = parseFloat(column.data("min")) || 0;
    let value = $mandatoryPaymentsSumInput.val();
    if (value) {
        value = Math.max(parseFloat(value), min);
    }
    const initial = parseFloat(column.data("initial"));
    if (value) {
        column.data("sum", value);
        column.attr("data-sum", value);
    } else {
        column.data("sum", 0);
        column.removeAttr("data-sum");
    }

    column.text(numberFormat.format(initial - value));
    saveMandatoryPaymentSums();
    checkCanSubmit();
}

let directors = null;
let numberFormat = Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 })
let balanceNumberFormat = Intl.NumberFormat("ru-RU", { maximumFractionDigits: 2, minimumFractionDigits: 2, })
let selectedAccounts = {};
let mandatoryPaymentsSums = null;
let tableCellColors = null;
let unpaidInvoices = {};
let projectRegionMandatoryPayments = {};
let allAccounts = {};
let allAccountsData = null;
let allAvailableFor = {};
let allProjectRegions = {};
let unpaidInvoiceNumberSum = {};
let interdivisionalDebtsData = null;
let allInterdivisionalDebtTransfers = []
let $mandatoryPaymentsSumInput = null;

const accountsTable = new AccountsTable({ url: "/p1/finance-module/api/project-region-accounts-table", canSelectAccount: true });


async function getMandatoryPaymentsSums(signal = null) {
    const response = await fetch("/p1/finance-module/api/mandatory-payments-sums");
    if (response.ok) {
        return await response.json();
    }
    return null;
}


async function getTableCellColors() {
    const response = await fetch("/p1/finance-module/api/table-cell-colors");
    if (response.ok) {
        return await response.json();
    }
    return null;
}

async function displayMandatoryPaymentsTable(options = { subdivision: undefined, force: true }) {
    function* groupby(x, key) {
        let keyValueDefault = {};
        let keyValue = keyValueDefault;
        let group = [];
        for (const i of x) {
            if (keyValue === keyValueDefault) {
                keyValue = key(i);
                group.push(i);
            } else if (keyValue === key(i)) {
                group.push(i);
            } else {
                yield [keyValue, group];
                group = [i];
                keyValue = key(i);
            }
        }
        yield [keyValue, group]
    }
    if (!options.force && (mandatoryPaymentsSums == null || tableCellColors == null)) {
        return;
    }
    const $mandatoryPaymentsTableContainer = $("#mandatory-payments-table-container");
    $mandatoryPaymentsTableContainer.empty();
    const $loading = $("#mandatory-payments-loading");
    $loading.removeClass("d-none");
    if (options.force) {
        [mandatoryPaymentsSums, tableCellColors] = await Promise.all([getMandatoryPaymentsSums(),  getTableCellColors()])
    }
    const $table = $(`
        <table class="mandatory-payments-table">
            <thead>
                <tr class="mandatory-payments-subtotals">
                    <td style="background-color: white" class="mandatory-payments-border-thin mandatory-payments-border-start mandatory-payments-border-end mandatory-payments-border-top sticky-relative sticky-relative-top sticky-relative-left" colspan="${mandatoryPaymentsSums.categories_colspan}"></td>
                    <td style="background-color: white" class="mandatory-payments-border-thin mandatory-payments-border-end mandatory-payments-border-top sticky-relative sticky-relative-top sticky-relative-left"></td>
                </tr>
                <tr class="mandatory-payments-directors">
                    <td style="background-color: white" class="mandatory-payments-border-end mandatory-payments-border-start mandatory-payments-border-bottom mandatory-payments-border-top sticky-relative sticky-relative-top sticky-relative-left" colspan="${mandatoryPaymentsSums.categories_colspan}" rowspan="3"></td>
                    <td style="background-color: white" class="mandatory-payments-border-end mandatory-payments-border-bottom mandatory-payments-border-top sticky-relative sticky-relative-top sticky-relative-left" rowspan="3"></td>
                </tr>
                <tr class="mandatory-payments-managers">
                </tr>
                <tr class="mandatory-payments-project-managers">
                </tr>
                <tr class="mandatory-payments-project-regions">
                    <td style="background-color: white" class="mandatory-payments-border-end mandatory-payments-border-start mandatory-payments-border-bottom sticky-relative sticky-relative-top sticky-relative-left" colspan="${mandatoryPaymentsSums.categories_colspan}" rowspan="2"></td>
                    <td style="background-color: white" class="text-center align-middle mandatory-payments-border-end mandatory-payments-border-bottom sticky-relative sticky-relative-top sticky-relative-left" rowspan="2">Статья</td>
                </tr>
                <tr class="mandatory-payments-percents">
                </tr>
            </thead>
            <tbody class="mandatory-payments-rows">

            </tbody>
        </table>
    `);
    const $directors = $table.find(".mandatory-payments-directors");
    const $managers = $table.find(".mandatory-payments-managers");
    const $projectManagers = $table.find(".mandatory-payments-project-managers");
    const $projectRegions = $table.find(".mandatory-payments-project-regions");
    const $percents = $table.find(".mandatory-payments-percents");
    const $subtotals = $table.find(".mandatory-payments-subtotals");
    const percentNumberFormat = Intl.NumberFormat("ru-RU", {
        maximumFractionDigits: 2,
        minimumFractionDigits: 2
    });
    function appendProjectRegion(element, projectRegion, color) {
        $(element).append(`
            <th scope="col" style="min-width: 6.25em; max-width: 6.25em; background-color: ${color}" rowspan="${$(element).is($projectManagers) ? 2 : 1}" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-end mandatory-payments-border-bottom">
                ${projectRegion.name}
            </th>
        `);
        $percents.append(`
            <th scope="col" style="background-color: #d6dce5" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-end mandatory-payments-border-bottom">
                ${percentNumberFormat.format(projectRegion.percent)}%
            </th>
        `);
    }
    const subdivision = options.subdivision;
    const projectRegions = subdivision === undefined ? mandatoryPaymentsSums.project_regions : mandatoryPaymentsSums.project_regions.filter(projectRegion => projectRegion.subdivision ? (!projectRegion.subdivision && !subdivision) || projectRegion.subdivision.name === subdivision : !subdivision);
    for (const [director, directorProjectRegions] of groupby(projectRegions, project_region => project_region.director_display)) {
        const directorColor = tableCellColors[`Ежемесячные выплаты.Директора.${director}`] || "white";
        const directorProjectRegionsColor = tableCellColors[`Ежемесячные выплаты.Директора.Регион проекты.${director}`];
        $directors.append(`
            <th style="background-color: ${directorColor}" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-end mandatory-payments-border-top mandatory-payments-border-bottom ${directorProjectRegions.length - 1 === 0 ? "d-none" : ""}" colspan=${directorProjectRegions.length - 1}>
                ${director || ""}
            </th>
            <td style="background-color: ${directorColor}" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-end mandatory-payments-border-top mandatory-payments-border-bottom">
                ${percentNumberFormat.format(directorProjectRegions.reduce((percent, projectRegion) => percent + parseFloat(projectRegion.percent), 0))}%
            </td>
        `);
        for (const [manager, managerProjectRegions] of groupby(directorProjectRegions, projectRegion => projectRegion.manager_display)) {
            const managerProjectRegionsColor = tableCellColors[`Ежемесячные выплаты.Руководители.Регион проекты.${manager}`];

            $managers.append(`
                <th scope="col" style="background-color: white" class="sticky-relative sticky-relative-top text-center align-middle mandatory-payments-border-end mandatory-payments-border-bottom" colspan=${managerProjectRegions.length}>
                    ${manager || ""}
                </th>
            `);
            for (const projectRegion of managerProjectRegions) {
                const projectRegionColor = tableCellColors[`Ежемесячные выплаты.Регион проекты.${projectRegion.name}`];
                const color = projectRegionColor || managerProjectRegionsColor || directorProjectRegionsColor || "white";
                if (projectRegion.project_manager_display == null) {
                    appendProjectRegion($projectManagers, projectRegion, color);
                } else {
                    $projectManagers.append(`
                        <th scope="col" style="background-color: ${color}" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-end mandatory-payments-border-bottom">
                            ${projectRegion.project_manager_display}
                        </th>
                    `);
                    appendProjectRegion($projectRegions, projectRegion, color);
                }
            }
        }
    }
    $directors.append(`
        <th style="background-color: #d9d9d9" rowspan="3" scope="col" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-end mandatory-payments-border-top mandatory-payments-border-bottom">
            АДМ
        </th>
    `);
    $directors.append(`
        <th style="background-color: #d9d9d9" rowspan="5" scope="col" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-end mandatory-payments-border-top mandatory-payments-border-bottom">
            Срок оплаты
        </th>
    `);
    $projectRegions.append(`
        <th style="background-color: #d9d9d9; max-width: 8em" rowspan="2" scope="col" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-end mandatory-payments-border-bottom">
            Осталось к оплате, всего
        </th>
    `);
    const $rows = $table.find(".mandatory-payments-rows");
    const subtotals = {};
    let totalSum = 0;
    for (const mandatoryPayment of mandatoryPaymentsSums.mandatory_payments) {
        const $tr = $(`<tr></tr>`);
        for (let i = 0; i < mandatoryPayment.levels.length; i++) {
            const level = mandatoryPayment.levels[i];
            if (!level) {
                continue;
            }
            $tr.append(`
                <th scope="row" colspan="${level.colspan}" rowspan="${level.rowspan}" style="background-color: ${level.category.color || "white"}" class="text-center align-middle sticky-relative sticky-relative-left ${i === 0 ? "mandatory-payments-border-start" : ""} mandatory-payments-border-end mandatory-payments-border-bottom">
                    <div style="writing-mode: vertical-rl; rotate: 180deg">${level.category.name || ""}<div>
                </th>
            `);
        }
        $tr.append(`
            <th scope="row" style="background-color: ${mandatoryPayment.color || "white"}; " class="mandatory-payments-border-end sticky-relative sticky-relative-left mandatory-payments-border-bottom">
                <div style="width: 12em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${mandatoryPayment.name}</div> 
            </th>
        `);
        let totalMandatoryPaymentSum = 0;
        for (const projectRegion of projectRegions) {
            const sum = mandatoryPaymentsSums.sums[mandatoryPayment.id][projectRegion.id];
            subtotals[projectRegion.id] = (subtotals[projectRegion.id] || 0) + +sum.sum;
            totalMandatoryPaymentSum += +sum.sum;
            const $td = $(`
                <td 
                    class="mandatory-payments-table__column mandatory-payments-border-end mandatory-payments-border-bottom text-center align-middle"
                    data-min="${sum.min}" 
                    data-initial="${sum.sum}"
                    data-deadline="${sum.deadline ? new Date(sum.deadline).toLocaleDateString("ru-RU") : ""}"
                    data-mandatory-payment-id="${mandatoryPayment.id}"
                    data-project-region-id="${projectRegion.id}"
                    data-type="${sum.type}"
                >
                    ${numberFormat.format(sum.sum)}
                </td>
            `);
            const data = projectRegionMandatoryPayments[projectRegion.id]?.find(data => data.mandatoryPaymentId == mandatoryPayment.id);
            if (data) {
                $td.attr("data-sum", data.sum);
                $td.text(numberFormat.format(sum.sum - data.sum));
            }
            if (sum.sum < 0) {
                $td.addClass("mandatory-payments-table__column_minus-sum");
            }
            if (sum.paid_today) {
                $td.addClass("mandatory-payments-table__column_paid-today");
            }
            $tr.append($td);
        }
        totalSum += totalMandatoryPaymentSum;
        const $td = $(`
            <td style="min-width: 8em;" data-mandatory-payment-id="${mandatoryPayment.id}" class="mandatory-payments-border-end mandatory-payments-border-bottom text-center align-middle">
                ${numberFormat.format(totalMandatoryPaymentSum)}
            </td>
        `);
        if (totalMandatoryPaymentSum < 0) {
            $td.addClass("mandatory-payments-table__column_minus-sum");
        } else {
            $td.css("background-color", "#d9d9d9")
        }
        $tr.append($td);
        $tr.append(`
            <td style="background-color: #fff2cc" class="mandatory-payments-border-end mandatory-payments-border-bottom text-center align-middle">
                <div style="width: 8em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${mandatoryPayment.short_deadline_template || ""}</div> 
            </td>
        `);
        $rows.append($tr);
    }
    for (const projectRegion of projectRegions) {
        $subtotals.append(`
            <td style="background-color: white" class="text-center sticky-relative sticky-relative-top align-middle mandatory-payments-border-thin mandatory-payments-border-end mandatory-payments-border-top">
                ${numberFormat.format(subtotals[projectRegion.id])}
            </td>
        `);
    }

    $subtotals.append(`<td style="background-color: white" class="text-center aling-middle sticky-relative sticky-relative-top mandatory-payments-border-thin mandatory-payments-border-end mandatory-payments-border-top">${numberFormat.format(totalSum)}</td>`);
    $subtotals.append(`<td style="background-color: white" class="mandatory-payments-border-thin sticky-relative sticky-relative-top mandatory-payments-border-end mandatory-payments-border-top"></td>`);
    $loading.addClass("d-none");
    $mandatoryPaymentsTableContainer.append($table);
    stickyRelativeUpdatePositions($table[0]);
    displayTotalMandatoryPayments();
    checkCanSubmit();
    mandatoryPaymentsAddEventListeners();
}

let mandatoryPaymentsFilterWithSubdivision = null;

async function filterMandatoryPaymentsTableWithSubdivision(subdivision = undefined) {
    if (mandatoryPaymentsFilterWithSubdivision) {
        await displayMandatoryPaymentsTable({ subdivision, force: false });
    } else {
        await displayMandatoryPaymentsTable({ force: false });
    }
}

async function showUnpaidInvoiceRestInfoModal(unpaidInvoice) {
    const modal = $(`
        <div class="modal fade">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Остальная информация</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>№ счёта: ${unpaidInvoice.invoice_number || ""}</p>
                    <p>Дата счёта: ${unpaidInvoice.invoice_date || ""}</p>
                    <p>Комментарий: ${unpaidInvoice.comment || ""}</p>
                    <p>Валюта: ${unpaidInvoice.currency || ""}</p>
                    <p>Статьи доходов/расходов: ${unpaidInvoice.revenue_expense_articles || ""}</p>
                    <p>БИН/ИИН: ${unpaidInvoice.bin_or_iin || ""}</p>
                    <p>Расчетный счет (ИИК): ${unpaidInvoice.iic || ""}</p>
                    <p>Заказ на продажу: ${unpaidInvoice.sales_order || ""}</p>
                    <p>Номер документа: ${unpaidInvoice.document_number || ""}</p>
                    <p>Дата документа: ${unpaidInvoice.document_date || ""}</p>
                    <p>Создатель счёта: ${unpaidInvoice.creator_user_id || ""}</p>
                    <p>Банк: ${unpaidInvoice.bank || ""}</p>
                    <p>Оплатить до(дата): ${unpaidInvoice.due_date || ""}</p>
                    <p>ТИП: ${unpaidInvoice.payment_type || ""}</p>
                    <p>Статус ДО: ${unpaidInvoice.status || ""}</p>
                    <p>Фактический номер договора: ${unpaidInvoice.contract_number || ""}</p>
                    <p>Подразделение: ${unpaidInvoice.department || ""}</p>
                </div>
                </div>
            </div>
        </div>
    `);
    modal.on("hidden.bs.modal", function () {
        modal.remove();
    });
    modal.modal("show");
}

let tableWithFilterUnpaidInvoices = null;

async function showUnpaidInvoiceRows(fieldUniqueValues) {
    $("#unpaid-invoices-table tbody tr").each(function () {
        $(this).toggleClass("d-none", !Array.from(Object.entries(fieldUniqueValues)).every(([field, uniqueValues]) => {
            const tdContent = $(`.td-content[data-field="${field}"]`, this);
            const value = $(tdContent).data("value");
            if ("exclude" in uniqueValues) {
                return !uniqueValues["exclude"].includes(value);
            } else {
                return uniqueValues["include"].includes(value);
            }
        }));
    });
}

async function showUnpaidInvoicesUniqueValues(field, fieldUniqueValues) {
    const list = $("#unpaid-invoices-filter-menu-unique-value-list");
    list.html(`
        <li class="list-group-item d-flex align-items-center justify-content-center">
            <div class="spinner-border text-primary spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </li>
    `);
    const uniqueValues = new Set(Array.from($(`.td-content[data-field="${field}"]`)).map(tdContent => $(tdContent).data("value")));
    await wait(700);
    list.empty();
    let index = 0;
    for (const uniqueValue of uniqueValues) {
        list.append(`
            <li class="list-group-item unpaid-invoices-unique-value" data-twf-unique-value="${uniqueValue}">
                <div class="form-check">
                    <input class="form-check-input unique-value-checkbox" type="checkbox" 
                        id="flexCheckDefault${index}">
                    <label class="form-check-label" for="flexCheckDefault${index}">
                        ${uniqueValue}
                    </label>
                </div>
            </li>
        `);
        index++;
    }
}
const unpaidInvoiceNumberFormat = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 2, minimumFractionDigits: 2 });

async function unpaidInvoicesShowSubtotal() {
    $("th[data-subtotal-field][data-subtotal]").text(function () {
        const subtotal = $(this).data("subtotal");
        const subtotalField = $(this).data("subtotalField");
        let values = null;
        if (subtotalField === "sum") {
            values = Array.from($(`input.unpaid-invoices-sum-input`)).map(input => parseFloat($(input).val()) || 0);
        } else {
            values = Array.from($(`tr:not(.d-none) .td-content[data-field=${subtotalField}]`)).map(tdContent => $(tdContent).data("value"));
        }
        const truthyValues = values.filter(value => value && value != "null" && value != "undefined");
        switch (subtotal) {
            case 2:
                return truthyValues.length;
            case 9:
                return unpaidInvoiceNumberFormat.format(truthyValues.reduce((previousValue, currentValue) => previousValue + (parseFloat(currentValue) || 0), 0));
        }
    });
}

const getInterdivisionalDebtsDataUrl = "/p1/finance-module/api/interdivisional-debts-data";
async function getInterdivisionalDebtsData() {
    const response = await fetch(getInterdivisionalDebtsDataUrl);
    if (response.ok) {
        interdivisionalDebtsData = await response.json();
        return interdivisionalDebtsData;
    }
    return null;
}

const getAllAccountsUrl = "/p1/finance-module/api/all-accounts";
async function getAllAccounts() {
    const response = await fetch(getAllAccountsUrl);
    if (response.ok) {
        const json = await response.json();
        allAccountsData = json.accounts;
        return allAccountsData;
    }
    return null;
}

const getAccountAvaiableForUrl = "/p1/finance-module/get-account-available-for";
async function getAccountAvaiableFor(accountId) {
    const response = await fetch(`${getAccountAvaiableForUrl}?id=${accountId}`);
    if (response.ok) {
        const json = await response.json();
        for (const availableFor of json) {
            allAvailableFor[availableFor.id] = availableFor;
        }
        return json;
    }
    return null;
}

let allProjectRegionsData = {};
const getAllProjectRegionsUrl = "/p1/finance-module/api/all-project-regions";
async function getAllProjectRegions() {
    const response = await fetch(getAllProjectRegionsUrl);
    if (response.ok) {
        const json = await response.json();
        allProjectRegionsData = json.project_regions;
        return allProjectRegionsData;
    }
    return null;
}

let projectRegionAccounts = {};
const getProjectRegionAccountsUrl = "/p1/finance-module/api/project-region-accounts";
async function getProjectRegionAccounts(projectRegionId) {
    const response = await fetch(`${getProjectRegionAccountsUrl}?project-region-id=${projectRegionId}`);
    if (response.ok) {
        const json = await response.json();
        projectRegionAccounts[projectRegionId] = json.accounts;
        return projectRegionAccounts[projectRegionId];
    }
    return null;
}

async function displayInterdivisionalDebtsData() {
    const interdivisionalDebtsTableContainer = $("#interdivisional-debts-table-container");
    interdivisionalDebtsTableContainer.empty();
    const $loading = $(".interdivisional-debts-loading");
    $loading.removeClass("d-none");
    const interdivisionalDebtstransfersContainer = $("#interdivisional-debts-transfers-container");
    interdivisionalDebtstransfersContainer.empty();
    await getInterdivisionalDebtsData();
    const table = $(`<table id="interdivisional-debts-table"></table>`);
    const thead = $(`<thead></thead>`);
    let tr = $(`<tr></tr>`);
    tr.append(`<th class="position-sticky bg-white top-0 start-0 z-2">ПМ</th>`);
    for (const projectRegion of interdivisionalDebtsData.project_regions) {
        tr.append(`<th scope="col" class="position-sticky bg-white top-0 project-region-th"><div class="project-region">${projectRegion.name}</div></th>`);
    }
    thead.append(tr);
    table.append(thead);
    const tbody = $(`<tbody></tbody>`);
    const totalSums = {};
    for (const [participant, rows] of interdivisionalDebtsData.rows) {
        tr = $(`<tr></tr>`);
        tr.append(`<th scope="row" class="position-sticky bg-white start-0 participant-th"><div class="participant">${participant}</div></th>`)
        for (const row of rows) {
            if (row.project_region_id in totalSums) {
                totalSums[row.project_region_id] += row.sum;
            } else {
                totalSums[row.project_region_id] = row.sum;
            }
            tr.append(`<td>${numberFormat.format(row.sum)}</td>`)
        }
        tbody.append(tr);
    }
    table.append(tbody);
    const tfoot = $(`<tfoot></tfoot>`);
    tr = $(`<tr></tr>`)
    tr.append(`<th scope="row" class="position-sticky z-2 bottom-0 bg-white start-0">Итого</th>`)
    for (const projectRegion of interdivisionalDebtsData.project_regions) {
        const totalSum = totalSums[projectRegion.id];
        const td = $(`<td class="position-sticky bottom-0 fw-bold">${numberFormat.format(totalSums[projectRegion.id])}</th>`);
        if (totalSum > 0) {
            td.addClass("bg-success-subtle")
        } else {
            td.addClass("bg-danger-subtle")
        }
        tr.append(td);
    }
    tfoot.append(tr);
    table.append(tfoot);

    await getAllProjectRegions();
    setTimeout(() => {
        allInterdivisionalDebtTransfers = [];
        displayTotalInterdivisionalDebts();
        checkCanSubmit();
        interdivisionalDebtsTableContainer.empty();
        interdivisionalDebtsTableContainer.append(table);
        interdivisionalDebtstransfersContainer.empty();

        const div = $(`
            <div class="mb-3">
                <div>
                    <form class="interdivisional-debts-transfer-form" id="interdivisional-debts-transfer-form">
                        <div class="mb-2">
                            <label for="interdivisional-debts-transfer-to-whom-select" class="form-label mb-0">Кому</label>
                            <select id="interdivisional-debts-transfer-to-whom-select" class="to-whom-select form-select form-select-sm me-1" name="to-whom" required>
                                <option value="" selected disabled>Выберите проект регион</option>
                            </select>
                        </div>
                        <div class="mb-1">
                        <label for="interdivisional-debts-transfer-sum-input" class="form-label mb-0">Сумма</label>
                        <input type="number" id="interdivisional-debts-transfer-sum-input" min="0" name="sum" step="0.01" placeholder="Введите сумму" required class="form-control form-control-sm me-1"/>
                        </div>
                        <div class="mb-1">
                            <label for="interdivisional-debts-transfer-to-account-select" class="form-label mb-0">На расчётный счёт</label>
                            <select id="interdivisional-debts-transfer-to-account-select" name="to-account" class="to-account-select form-select form-select-sm me-1" disabled required>
                                <option value="" selected disabled>Выберите расчётный счёт</option>
                            </select>
                        </div>
                        <button type="submit" class="submit-btn btn btn-sm btn-primary" disabled>Перевести</button>
                    </form>
                </div>
            </div>
        `);

        const toAccountSelect = $(".to-account-select", div);
        const toWhomSelect = $('.to-whom-select', div);
        const transferForm = $(".interdivisional-debts-transfer-form", div);
        const submitBtn = $(".submit-btn", transferForm);
        for (const projectRegion of allProjectRegionsData) {
            toWhomSelect.append(`
                <option value="${projectRegion.id}">${projectRegion.name}</option>
            `);
        }

        toWhomSelect.on("change", async function () {
            const accounts = await getProjectRegionAccounts($(this).val());
            toAccountSelect.html(`<option value="" selected disabled>Выберите расчётный счёт</option>`);
            if (accounts.length) {
                toAccountSelect.prop("disabled", false);
                for (const account of accounts) {
                    toAccountSelect.append(`<option value="${account.id}">${account.name}</option>`)
                }
                submitBtn.prop("disabled", false);
            } else {
                toAccountSelect.prop("disabled", true);
                submitBtn.prop("disabled", true);
            }
        });
        transferForm.on("submit", function () {
            const data = {};
            transferForm.serializeArray().map(function (x) { data[x.name] = x.value; });
            const existsTransfer = allInterdivisionalDebtTransfers.find(transfer => {
                for (const key in transfer) {
                    if (key != "sum" && data[key] != transfer[key]) {
                        return false;
                    }
                }
                return true;
            });
            if (existsTransfer) {
                existsTransfer.sum = +existsTransfer.sum + +data.sum;
            } else {
                allInterdivisionalDebtTransfers.push(data);
            }
            displayTotalInterdivisionalDebts();
            transferForm[0].reset();
            checkCanSubmit();
            return false;
        });
        interdivisionalDebtstransfersContainer.append(div);
        $loading.addClass("d-none");
    }, 700);
}

function displayTotalInterdivisionalDebts() {
    const $interdivisionalDebtsSumsContainer = $("#interdivisional-debts-sums-container");
    const $interdivisionalDebtsSums = $("#interdivisional-debts-sums");
    const $interdivisionalDebtsTotalSum = $("#interdivisional-debts-total-sum");
    $interdivisionalDebtsSums.empty();

    if (allInterdivisionalDebtTransfers.length) {
        $interdivisionalDebtsSumsContainer.removeClass("d-none");
        let index = 1;
        let totalSum = 0;
        for (const transfer of allInterdivisionalDebtTransfers) {
            const fromWhom = interdivisionalDebtsData.project_regions.find(projectRegion => projectRegion.id == transfer["from-whom"]);
            const fromAccount = accountsTable.getAccount(transfer["from-account"]);
            const toWhom = allProjectRegionsData.find(projectRegion => projectRegion.id == transfer["to-whom"]);
            const toAccount = projectRegionAccounts[transfer["to-whom"]].find(account => account.id == transfer["to-account"]);
            totalSum += +transfer["sum"];
            $interdivisionalDebtsSums.append(`
                <tr data-selected-account="${transfer["from-account"]}-${transfer["from-whom"]}">
                    <th class="text-center" scope="row">${index}</th>
                    <td>${fromWhom.name}</td>
                    <td>${fromAccount.name}</td>
                    <td>${toWhom.name}</td>
                    <td>${toAccount.name}</td>
                    <td>${numberFormat.format(transfer["sum"])}</td>
                </tr>
            `);

            // $(".remove-interdivisional-debt-btn", li).on("click", function () {
            //     const index = allInterdivisionalDebtTransfers.indexOf(transfer);
            //     if (index !== -1) {
            //         allInterdivisionalDebtTransfers.splice(index, 1);
            //     }
            //     markDisabledSubmitBtnIfNotCanSubmit();
            //     displayInterdivisionalDebtsTransfers();
            // });

            index++;
        }
        $interdivisionalDebtsTotalSum.text(numberFormat.format(totalSum));
    } else {
        $interdivisionalDebtsSumsContainer.addClass("d-none");
    }
}



function loadSelectedAccounts(tab) {
    if (tab in selectedAccounts) {
        for (const account of selectedAccounts[tab]) {
            $(`.account-radio[data-account-id="${account.id}"][data-project-region-id="${account.projectRegionId}"]`).prop("checked", true);
        }
    }
}

function saveMandatoryPaymentSums() {
    projectRegionMandatoryPayments = {};
    $(`.mandatory-payments-table__column[data-sum]:not([data-sum=""])`).each(function () {
        const data = $(this).data();
        if (data.projectRegionId in projectRegionMandatoryPayments) {
            projectRegionMandatoryPayments[data.projectRegionId].push(data);
        } else {
            projectRegionMandatoryPayments[data.projectRegionId] = [data];
        }
    });
    displayTotalMandatoryPayments();
}

function getAccountFromProjectRegionId(projectRegionId, tab) {
    if (tab in selectedAccounts) {
        account = selectedAccounts["mandatory-payments"].find(account => account.projectRegionId == projectRegionId);
        return account && allAccounts[`${account.id}-${projectRegionId}`];
    }
    return null;
}


function displayTotalMandatoryPayments() {
    const $mandatoryPaymentSumsContainer = $("#mandatory-payments-sums-container");
    const $mandatoryPaymentSums = $("#mandatory-payments-sums");
    const $mandatoryPaymentsTotalSum = $("#mandatory-payments-total-sum");
    $mandatoryPaymentSums.empty();
    $mandatoryPaymentsTotalSum.empty();
    if (Object.keys(projectRegionMandatoryPayments).length) {
        $mandatoryPaymentSumsContainer.removeClass("d-none");
        let index = 1;
        let totalSum = 0;
        for (const [projectRegionId, mandatoryPayments] of Object.entries(projectRegionMandatoryPayments)) {
            const projectRegion = mandatoryPaymentsSums.project_regions.find(projectRegion => projectRegion.id == projectRegionId);
            let accountData = getAccountFromProjectRegionId(projectRegionId, "mandatory-payments");
            for (const mandatoryPaymentData of mandatoryPayments) {
                const mandatoryPayment = mandatoryPaymentsSums.mandatory_payments.find(mandatoryPayment => mandatoryPayment.id == mandatoryPaymentData.mandatoryPaymentId);
                totalSum += +mandatoryPaymentData.sum;
                $mandatoryPaymentSums.append(`
                    <tr${accountData ? ` data-selected-account="${`${accountData.id}-${projectRegionId}`}"` : ""}>
                        <th class="text-center" scope="row">${index}</th>
                        <td>${mandatoryPayment.name}</td>
                        <td>${projectRegion.name}</td>
                        <td>${accountData ? accountData.name : "Расчётный счёт не указан"}</td>
                        <td>${numberFormat.format(mandatoryPaymentData.sum)}</td>
                    </tr>
                `);
                index++;
            }
        }
        $mandatoryPaymentsTotalSum.text(numberFormat.format(totalSum));
    } else {
        $mandatoryPaymentSumsContainer.addClass("d-none");
    }
}

function displayTotalUnpaidInvoices() {
    const $unpaidInvoicesSumsContainer = $("#unpaid-invoices-sums-container");
    const $unpaidInvoicesSums = $("#unpaid-invoices-sums");
    const $unpaidInvoicesTotalSum = $("#unpaid-invoices-total-sum")
    $unpaidInvoicesSums.empty();
    $unpaidInvoicesTotalSum.empty();
    if (Object.keys(unpaidInvoiceNumberSum).length) {
        $unpaidInvoicesSumsContainer.removeClass("d-none");
        let account = null;
        if ("unpaid-invoices" in selectedAccounts) {
            account = selectedAccounts["unpaid-invoices"][0];
            if (account) {
                account = allAccounts[`${account.id}-${account.projectRegionId}`];
            }
        }
        let projectRegion = null;
        if (account) {
            projectRegion = allProjectRegions[account.projectRegionId];
        }
        let index = 1;
        for (const [unpaidInvoiceNumber, sum] of Object.entries(unpaidInvoiceNumberSum)) {
            const unpaidInvoice = unpaidInvoices[unpaidInvoiceNumber];
            $unpaidInvoicesSums.append(`
                <tr${account && projectRegion ? ` data-selected-account="${account.id}-${projectRegion.id}"` : ""}>
                    <th class="text-center align-middle" scope="row" >${index++}</th>
                    <td class="align-middle">${unpaidInvoice.number}</td>
                    <td class="align-middle">${unpaidInvoice.project}</td>
                    <td class="align-middle">${unpaidInvoice.contractor}</td>
                    <td class="align-middle">${unpaidInvoice.comment}</td>
                    <td class="align-middle">${projectRegion ? projectRegion.name : "-"}</td>
                    <td class="align-middle">${account ? account.name : "Расчётный счёт не указан"}</td>
                    <td class="align-middle">${numberFormat.format(sum)}</td>
                </tr>
            `);
        }
        const totalSum = Object.values(unpaidInvoiceNumberSum).reduce((previousValue, currentValue) => previousValue + currentValue, 0);
        $unpaidInvoicesTotalSum.text(numberFormat.format(totalSum));
    } else {
        $unpaidInvoicesSumsContainer.addClass("d-none");
    }
}

function formToObject(form) {
    const data = {};
    $(form).serializeArray().map(function (x) { data[x.name] = x.value; });
    return data;
}

const getAccountsUrl = "/p1/finance-module/api/accounts"
async function getAccounts(projectRegionId) {
    const response = await fetch(`${getAccountsUrl}?project-region-id=${projectRegionId}`);
    if (response.ok) {
        const json = await response.json();
        return json.accounts;
    }
    return null;
}


async function getSubdivisions() {
    try {
        const response = await fetch(`/p1/finance-module/api/subdivisions`);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.error(error);
    }
    return [];
}

let allTransfers = [];
let transfersEventListenersAdded = false;
let sutochnyeFormDatas = [];
let subdivisions = null;
async function displayTransfers() {
    const $transferForm = $(`#transfer-form`);
    const $toAccountSelect = $(".to-account-select", $transferForm);
    $toAccountSelect.html(`<option value="" selected disabled>Выберите расчётный счёт</option>`);
    $toAccountSelect.prop("disabled", true);
    const $projectRegionSelect = $(".project-region-select", $transferForm);
    
}

async function displayTotalTransfers() {
    const transferList = $("#transfers-list");
    transferList.empty();
    const $transfersSumsContainer = $("#transfers-sums-container");
    const $transfersSums = $("#transfers-sums");
    const $transfersTotalSum = $("#transfers-total-sum");
    $transfersSums.empty();
    $transfersTotalSum.empty();
    if (allTransfers.length !== 0) {
        $transfersSumsContainer.removeClass("d-none");
        let index = 1;
        let totalSum = 0;
        for (const transfer of allTransfers) {
            const projectRegion = accountsTable.data.project_regions.find(projectRegion => projectRegion.id == transfer["project-region-id"]);
            const fromAccount = accountsTable.data.accounts.find(account => account.id == transfer["from-account"]);
            const toAccount = accountsTable.data.accounts.find(account => account.id == transfer["to-account"]);
            const sum = transfer["sum"];
            totalSum += +sum;
            $transfersSums.append(`
                <tr data-selected-account="${fromAccount.id}-${projectRegion.id}">
                    <th scope="row" class="text-center">${index}</th>
                    <td>${projectRegion.name}</td>
                    <td>${fromAccount.name}</td>
                    <td>${toAccount.name}</td>
                    <td>${numberFormat.format(sum)}</td>
                </tr>
            `);
            // $(".remove-transer-btn", li).on("click", function() {
            //     const index = allTransfers.indexOf(transfer);
            //     if (index !== -1) {
            //         allTransfers.splice(index, 1);
            //     }
            //     markDisabledSubmitBtnIfNotCanSubmit();
            //     displayTransferList();
            // });
        }
        $transfersTotalSum.text(numberFormat.format(totalSum));
    } else {
        $transfersSumsContainer.addClass("d-none");
    }

}

async function displaySutochnye() {
    const $sutochnyeForm = $("#sutochnye-form");
    const $sutochnyeFormSubdivisionSelect = $sutochnyeForm.find(`select[name="subdivision-id"]`);
    $sutochnyeFormSubdivisionSelect.find(`option:not([value=""])`).remove();
    subdivisions = await getSubdivisions();
    for (const subdivision of subdivisions) {
        $sutochnyeFormSubdivisionSelect.append(`
            <option value="${subdivision.id}">
                ${subdivision.name}
            </option>
        `);
    }
}

function displayTotalSutochnye() {
    const $sutochnyeSumsContainer = $("#sutochnye-sums-container");
    const $sutochnyeSums = $("#sutochnye-sums");
    const $sutochnyeTotalSum = $("#sutochnye-total-sum");
    $sutochnyeSums.empty();
    $sutochnyeTotalSum.empty();
    if (sutochnyeFormDatas.length !== 0) {
        $sutochnyeSumsContainer.removeClass("d-none");
        let index = 1;
        let totalSum = 0;
        for (const formData of sutochnyeFormDatas) {
            const projectRegion = accountsTable.data.project_regions.find(projectRegion => projectRegion.id == formData.get("project-region-id"));
            const account = accountsTable.data.accounts.find(account => account.id == formData.get("account-id"));
            const subdivision = subdivisions.find(subdivision => subdivision.id == formData.get("subdivision-id"));
            const sum = formData.get("sum");
            totalSum += +sum;
            $sutochnyeSums.append(`
                <tr data-selected-account="${account.id}-${projectRegion.id}">
                    <th scope="row" class="text-center">${index}</th>
                    <td class="align-middle">${projectRegion.name}</td>
                    <td class="align-middle">${account.name}</td>
                    <td class="align-middle">${formData.get("name")}</td>
                    <td class="align-middle">${formData.get("days")}</td>
                    <td class="align-middle">${subdivision.name}</td>
                    <td class="align-middle">${formData.get("project")}</td>
                    <td class="align-middle">${formData.get("responsible")}</td>
                    <td class="align-middle">${`${new Date(formData.get("business-trip-start-date")).toLocaleDateString()}-${new Date(formData.get("business-trip-end-date")).toLocaleDateString()}`}</td>
                    <td class="align-middle">${formData.get("destination-point")}</td>
                    <td class="align-middle">${numberFormat.format(sum)}</td>
                </tr>
            `);
        }
        $sutochnyeTotalSum.text(numberFormat.format(totalSum));
    } else {
        $sutochnyeSumsContainer.addClass("d-none");
    }
}


let projectRegionMandatoryPaymentsPaid = null;
async function getProjectRegionMandatoryPaymentsPaid() {
    const response = await fetch("/p1/finance-module/api/project-region-mandatory-payments-paid");
    if (response.ok) {
        return await response.json();
    }
    return null;
}

function saveSelectedAccounts(tab) {
    selectedAccounts[tab] = Array.from($(".account-radio:checked")).map(accountRadio => ({ id: $(accountRadio).data("accountId"), projectRegionId: $(accountRadio).data("projectRegionId") }));
    console.log("Selected accounts saved: ", tab);
}

function accountSelection(tab) {
    switch (tab) {
        case "mandatory-payments":
            accountsTable.canSelectAnyProjectRegionAccount();
            break;
        case "unpaid-invoices":
            accountsTable.canSelectAnyAccount();
            break;
        case "interdivisional-debts":
            accountsTable.canSelectAnyAccount({ required: true, form: "interdivisional-debts-transfer-form", name: "from-account", projectRegionName: "from-whom" });
            break;
        case "transfers":
            accountsTable.canSelectAnyAccount({ required: true, form: "transfer-form", name: "from-account" });
            break;
        case "sutochnye":
            accountsTable.canSelectAnyAccount({ required: true, form: "sutochnye-form" });
            break;
        default:
            accountsTable.cantSelectAccount();
            break;
    }
}

async function initalizeTransfers() {

}

let activeTab = null;
let loadedTabs = new Set();
let loadingTabs = new Set();
let initializedTabs = new Set();
const tabInitializers = {
    async sutochnye() {
        const $sutochnyeForm = $("#sutochnye-form");
        $sutochnyeForm.on("submit", function (event) {
            event.preventDefault();
            sutochnyeFormDatas.push(new FormData(this));
            displayTotalSutochnye();
            checkCanSubmit();
            this.reset();
        });
    },
    async transfers() {
        const $transferForm = $(`#transfer-form`);
        const $toAccountSelect = $(".to-account-select", $transferForm);
        $(document).on("change", ".account-radio", async function (event) {
            if (activeTab !== "transfers") {
                return;
            }
            const accountId = $(this).val();
            const projectRegionId = $(this).data("projectRegionId");
            const accounts = await getAccounts(projectRegionId);
            $toAccountSelect.html(`<option value="" selected disabled>Выберите расчётный счёт</option>`);
            if (accounts) {
                for (const account of accounts) {
                    if (account.id == accountId) {
                        continue;
                    }
                    $toAccountSelect.append(`<option value="${account.id}">${account.name}</option>`)
                }
                $toAccountSelect.prop("disabled", false);
            } else {
                $toAccountSelect.prop("disabled", true);
            }
        });
    
        $transferForm.on("submit", function (event) {
            event.preventDefault();
            const data = formToObject(this);
            const existsTransfer = allTransfers.find(transfer => {
                console.log(data, transfer)
                for (const key in transfer) {
                    if (key !== "sum" && data[key] != transfer[key]) {
                        return false;
                    }
                }
                return true;
            });
            if (existsTransfer) {
                existsTransfer.sum = +existsTransfer.sum + +data.sum;
            } else {
                allTransfers.push(data);
            }
            displayTotalTransfers();
            checkCanSubmit();
            this.reset();
        });
    },
};
const tabLoaders = {

}

async function initializeTab(tab) {
    if (tab in tabInitializers) {
        if (!initializedTabs.has(tab)) {
            console.log("Tab initializing: ", tab);
            await tabInitializers[tab]();
            console.log("Tab initalized: ", tab);
        } else {
            console.log("Tab initialized: ", tab);
        }
    }
}

async function loadTab(tab, check = true) {
    if (check && loadedTabs.has(tab)) {
        console.log("Tab is already loaded, canceled: ", tab);
        return false;
    }
    console.log("Tab loading: ", tab);
    loadedTabs.delete(tab);
    loadingTabs.add(tab);
    try {
        switch (tab) {
            case "mandatory-payments":
                await displayMandatoryPaymentsTable();
                break;
            case "unpaid-invoices":
                break;
            case "interdivisional-debts":
                await displayInterdivisionalDebtsData();
                break;
            case "transfers":
                await displayTransfers();
                break;
            case "sutochnye":
                await displaySutochnye();
                break;
        }
    } catch (error) {
        console.error("Error in loading tab: ", tab, error);
        return false;
    }
    console.log("Tab loaded: ", tab);
    loadingTabs.delete(tab);
    loadedTabs.add(tab);
    return true;
}

async function onTabChange(tab) {
    activeTab = tab;
    console.log("Tab changed: ", tab);
    accountsTable.unselectAccounts();
    accountSelection(tab);
    loadSelectedAccounts(tab);
    if (loadingTabs.has(tab)) {
        console.log("Tab is loading, canceled: ", tab);
        return;
    }
    await initializeTab(tab);
    const loaded = await loadTab(tab);
    if (loaded && tab == "mandatory-payments") {
        stickyRelativeUpdatePositions($(".mandatory-payments-table")[0]);
    }
}

async function sync(force = false) {
    const tab = activeTab;
    projectRegionMandatoryPaymentsPaid = await getProjectRegionMandatoryPaymentsPaid();

    if (force && tab == "unpaid-invoices") {
        $("#unpaid-invoices-table").smartTableReload();
    } else {
        await loadTab(tab, false);
    }
}

function displayErrors(errors) {
    const errorsDiv = $("#errors");
    errorsDiv.empty();
    for (const error of errors) {
        errorsDiv.append(`<p class="text-danger">${error}</p>`)
    }
}

function displayTotalAccounts(projectRegionAccountSum) {
    const $accountsSumsContainer = $("#accounts-sums-container");
    const $accountsSums = $("#accounts-sums");
    const $accountsTotalSum = $("#accounts-total-sum");
    $accountsSums.empty();
    $accountsTotalSum.empty();
    if (Object.keys(projectRegionAccountSum).length !== 0) {
        $accountsSumsContainer.removeClass("d-none");
        let totalSum = 0;
        for (const [projectRegionId, accounts] of Object.entries(projectRegionAccountSum)) {
            for (const [accountId, sum] of Object.entries(accounts)) {
                let tr = null;
                totalSum += sum;
                if (accountId != "Не указан") {
                    const account = accountsTable.data.accounts.find(account => account.id == accountId);
                    const projectRegion = accountsTable.data.project_regions.find(projectRegion => projectRegion.id == projectRegionId);
                    tr = $(`
                        <tr>
                            <td>${projectRegion.name}</td>
                            <td>${account.name}</td>
                            <td>${numberFormat.format(sum)}</td>
                        </tr>
                    `);
                } else {
                    tr = $(`
                        <tr>
                            <td colspan="2">Не указан</td>
                            <td>${numberFormat.format(sum)}</td>
                        </tr>
                    `);
                }
                $accountsSums.append(tr);
            }
        }
        $accountsTotalSum.text(numberFormat.format(totalSum));
    } else {
        $accountsSumsContainer.addClass("d-none");
    }
}
const MINIMUM_OUTSTANDING_BALANCE = 0;
const MINIMUM_AMOUNT_FOR_UNPAID_UNVOICES = 0;
function canSubmit() {
    const errors = [];
    const projectRegionIds = Object.keys(projectRegionMandatoryPayments);
    const projectRegionAccountSum = {};
    const accountSum = {};
    function addAccountSum(projectRegionId, accountId, sum) {
        if (accountId == "Не указан") {
            projectRegionId = null;
        }
        if (!(projectRegionId in projectRegionAccountSum)) {
            projectRegionAccountSum[projectRegionId] = {};
        }
        projectRegionAccountSum[projectRegionId][accountId] = (projectRegionAccountSum[projectRegionId][accountId] || 0) + sum;
        accountSum[accountId] = (accountSum[accountId] || 0) + sum;
    }

    if (mandatoryPaymentsSums && projectRegionIds.length !== 0) {
        for (const projectRegionId of projectRegionIds) {
            const selectedAccount = "mandatory-payments" in selectedAccounts ? selectedAccounts["mandatory-payments"].find(account => account.projectRegionId == projectRegionId) : null;
            const projectRegion = mandatoryPaymentsSums.project_regions.find(projectRegion => projectRegion.id == projectRegionId);
            const totalSum = projectRegionMandatoryPayments[projectRegionId].reduce((previousValue, currentValue) => previousValue + currentValue.sum, 0);
            let accountId = null;
            if (selectedAccount) {
                accountId = selectedAccount.id;
            } else {
                errors.push(`Выберите расчётный счёт для ${projectRegion.name}`)
                accountId = "Не указан";
            }
            addAccountSum(projectRegionId, accountId, totalSum);
        }
    }
    const checkProjectRegionMandatoryPaymentsPaidIds = new Set();
    const unpaidInvoiceNumbers = Object.keys(unpaidInvoiceNumberSum);
    if (unpaidInvoiceNumbers.length !== 0) {
        let x = 0; // Total sum
        let y = 0; // Has exception
        let z = 0; // Doesn't has exception
        for (const [number, sum] of Object.entries(unpaidInvoiceNumberSum)) {
            x += sum;
            const unpaidInvoice = unpaidInvoices[number];
            if (unpaidInvoice.has_exception) {
                y += sum;
            } else {
                z += sum;
            }
        }   
        if (!("unpaid-invoices" in selectedAccounts) || selectedAccounts["unpaid-invoices"].length === 0) {
            errors.push("Вы не выбрали расчётный счёт для реестра неоплаченных счетов")
            addAccountSum(null, "Не указан", x)
        } else {
            const accountData = selectedAccounts["unpaid-invoices"][0];
            addAccountSum(accountData.projectRegionId, accountData.id, x)
            checkProjectRegionMandatoryPaymentsPaidIds.add(accountData.projectRegionId);
            if (x < MINIMUM_AMOUNT_FOR_UNPAID_UNVOICES) {
                errors.push(`Минимальная сумма для погашение реестра неоплаченных счетов: ${numberFormat.format(MINIMUM_AMOUNT_FOR_UNPAID_UNVOICES)}`)
            }
        }
    }
    if (allInterdivisionalDebtTransfers.length !== 0) {
        for (const transfer of allInterdivisionalDebtTransfers) {
            addAccountSum(transfer["from-whom"], transfer["from-account"], +transfer["sum"]);
            checkProjectRegionMandatoryPaymentsPaidIds.add(parseInt(transfer["from-whom"]));
        }
    }
    if (allTransfers.length !== 0) {
        for (const transfer of allTransfers) {
            addAccountSum(transfer["project-region-id"], transfer["from-account"], +transfer["sum"])
        }
    }
    if (sutochnyeFormDatas.length !== 0) {
        for (const formData of sutochnyeFormDatas) {
            addAccountSum(formData.get("project-region-id"), formData.get("account-id"), +formData.get("sum"))
        }
    }
    displayTotalAccounts(projectRegionAccountSum);
    for (const [accountId, sum] of Object.entries(accountSum)) {
        const balance = accountsTable.accountBalance[accountId];
        if (sum > balance - MINIMUM_OUTSTANDING_BALANCE) {
            const account = accountsTable.data.accounts.find(account => account.id == accountId);
            errors.push(`Недостаточно средств в расчётном счету ${account.name}`);
        }
    }
    for (const projectRegionId of checkProjectRegionMandatoryPaymentsPaidIds) {
        if (!projectRegionMandatoryPaymentsPaid[projectRegionId]) {
            const projectRegion = accountsTable.data.project_regions.find(projectRegion => projectRegion.id == projectRegionId);
            if (!projectRegion) {
                continue;
            }
            errors.push(`Сперва погасите обязательные платежи ${projectRegion.name}`);
        }
    }
    displayErrors(errors);

    const hasAnyPayment = projectRegionIds.length !== 0 || unpaidInvoiceNumbers.length !== 0 || allInterdivisionalDebtTransfers.length !== 0 || allTransfers.length !== 0 || sutochnyeFormDatas.length !== 0;
    const $noPaymentsMessage = $("#no-payments-message");
    $noPaymentsMessage.toggleClass("d-none", hasAnyPayment);
    return errors.length === 0 && hasAnyPayment;
}

function removeFromLoadedTabs(tabs) {
    for (const tab of tabs) {
        if (tab === activeTab) {
            continue;
        }
        loadedTabs.delete(tab);
    }
}


function checkCanSubmit() {
    $("#submit-button").prop("disabled", !canSubmit());
}


async function submit() {
    const formLoading = $("#form-loading");
    const formLog = $("#form-log");
    formLog.empty();
    formLoading.removeClass("d-none");
    try {
        const sutochnyeIds = [];
        for (const formData of sutochnyeFormDatas) {
            const response = await fetch("/p1/finance-module/create-sutochnye", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken
                }
            });
            const json = await response.json();
            if (response.ok) {
                sutochnyeIds.push(json.id);
            } else {
                throw new Error(json.detail);
            }
        }

        const response = await fetch("/p1/finance-module/api/process-transactions", {
            method: "POST",
            body: JSON.stringify({
                selectedAccounts,
                allInterdivisionalDebtTransfers,
                unpaidInvoices: unpaidInvoiceNumberSum,
                projectRegionMandatoryPayments,
                allTransfers,
                sutochnyeIds
            }),
            headers: {
                "X-CSRFToken": csrfToken
            }
        });
        const json = await response.json();
        formLog.toggleClass("text-danger", !response.ok);
        formLog.toggleClass("text-success", response.ok);
        if (response.ok) {
            unpaidInvoiceNumberSum = {};
            selectedAccounts = {};
            allInterdivisionalDebtTransfers = [];
            projectRegionMandatoryPayments = {};
            allTransfers = [];
            sutochnyeFormDatas = [];
            displayTotalTransfers();
            displayTotalMandatoryPayments();
            displayTotalUnpaidInvoices();
            displayTotalInterdivisionalDebts();
            displayTotalSutochnye();
            displayErrors([]);
            loadedTabs = new Set([activeTab]);
            sync(true);
            formLog.text(`${json.detail}`);
            accountsTable.reload();
            $("#mandatory-payment-seizures-history-table").smartTableReload("intersected");
            $("#paid-invoices-history-table").smartTableReload("intersected");
            $("#interdivisional-debts-history-table").smartTableReload("intersected");
            $("#debts-history-table").smartTableReload("intersected");
            $("#unpaid-invoices-table").smartTableReload("intersected");
            $("#sutochnye-history-table").smartTableReload("intersected");
            checkCanSubmit();
        } else {
            formLog.text(`Ошибка при обработке транцакций: ${json.detail}`);
        }
    } catch (error) {
        formLog.text(`Ошибка: ${error}`);
        console.error(error);
    }
    formLoading.addClass("d-none");
}


function unpaidInvoiceParseApprover(approver) {
    const match = approver.match(/(\d+)\s+-\s+(.+)/);
    return match && {
        avhUserId: parseInt(match[1]),
    }
}

function unpaidInvoiceCheckCanPay($row) {
    $row = $($row);
    const $sumInput = $(".unpaid-invoice-sum-input", $row);
    $sumInput.prop("disabled", false);
    if (accountsTable.data) {
        const number = $row.data('number');
        const unpaidInvoice = unpaidInvoices[number];
        const approverAvhUserId = unpaidInvoiceParseApprover(unpaidInvoice.approver).avhUserId;
        const projectMatch = unpaidInvoice.project.match(/(\d+)\s*-\s*(\d+)\s*-\s*(.+)/);
        const projectNumber = projectMatch[2];
        const projectRegion = accountsTable.data.project_regions.find(projectRegion => projectRegionMandatoryPaymentsPaid[projectRegion.id] && projectRegion.approvers.find(approver => approver.user.avh_user_id == approverAvhUserId && approver.projects.find(project => project.number == projectNumber)));
        if (!projectRegion) {
            $sumInput.prop("title", "АДМ для этого ПМ не оплачено")
            $sumInput.prop("disabled", true);
        } 
        $row.removeClass("unpaid-invoice-row-check-can-pay");
    } else {
        $row.addClass("unpaid-invoice-row-check-can-pay");
        $sumInput.prop("title", "");
        $sumInput.prop("disabled", true);
    }
}


function smartTables() {
    $("#mandatory-payment-seizures-history-table").smartTableWithVirtualScroll({
        name: "all-mandatory-payment-seizures",
        csrfToken,
        unloadTypes: [
            {
                html: `<i class="fa-solid fa-file-excel"></i> Изьятие (новый)`,
                type: "mandatory-payment-seizures-xlsx-1"
            }
        ],
        unloadUrl: "/p1/finance-module/unload",
        defaultOrder: [{ "field": "datetime", "sort": "desc" }],
        firstShowRows: "intersected",
        numberFormat: new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
        lastRowTarget: "#mandatory-payment-seizures-history-last-row",
        rowsTarget: "#mandatory-payment-seizures-history-table-rows",
        getValuesUrl: "/p1/finance-module/mandatory-payment-seizure-get-values",
        getRowsUrl: "/p1/finance-module/mandatory-payment-seizure-get-rows",
        getSubtotalsUrl: "/p1/finance-module/mandatory-payment-seizure-get-subtotals",
        loadingHtml: `
            <tr>
                <td class="text-center" colspan="6">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,
        getTr(row) {
            return `
                <tr>
                    <td class="smart-table__cell active" data-st-field="project_region__name">${row.project_region.name}</td>
                    <td class="smart-table__cell active" data-st-field="mandatory_payment__name">${row.mandatory_payment.name}</td>
                    <td class="smart-table__cell active" data-st-field="account__name">${row.account ? row.account.name : ""}</td>
                    <td class="smart-table__cell active" data-st-field="sum">${numberFormat.format(row.sum)}</td>
                    <td class="smart-table__cell active" data-st-field="datetime">${new Date(row.datetime).toLocaleDateString("ru-RU")}</td>
                    <td>${row.status.name}</td>
                </tr>
            `;
        }
    });
    $("#paid-invoices-history-table").smartTableWithVirtualScroll({
        name: "all-paid-invoices",
        csrfToken,
        firstShowRows: "intersected",
        unloadTypes: [
            {
                html: `<i class="fa-solid fa-file-excel"></i> ДДС`,
                type: "paid-invoices-xlsx-1"
            }
        ],
        unloadUrl: "/p1/finance-module/unload",
        defaultOrder: [{ "field": "at", "sort": "desc" }],
        numberFormat: new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
        lastRowTarget: "#paid-invoices-history-last-row",
        rowsTarget: "#paid-invoices-history-table-rows",
        getValuesUrl: "/p1/finance-module/paid-invoices-get-values",
        getRowsUrl: "/p1/finance-module/paid-invoices-get-rows",
        getSubtotalsUrl: "/p1/finance-module/paid-invoices-get-subtotals",
        loadingHtml: `
            <tr>
                <td class="text-center" colspan="10">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,
        getTr(row) {
            return `
                <tr>
                    <td class="smart-table__cell active" data-st-field="number">${row.number}</td>
                    <td class="smart-table__cell active" data-st-field="project">${row.project || ""}</td>
                    <td class="smart-table__cell active" data-st-field="contractor">${row.contractor || ""}</td>
                    <td class="smart-table__cell active" data-st-field="comment">${row.comment || ""}</td>
                    <td class="smart-table__cell active" data-st-field="project_region__name">${row.project_region ? row.project_region.name : ""}</td>
                    <td class="smart-table__cell active" data-st-field="account__name">${row.account ? row.account.name : ""}</td>
                    <td class="smart-table__cell active" data-st-field="sum">${numberFormat.format(row.sum)}</td>
                    <td class="smart-table__cell active" data-st-field="sum">${row.commission ? numberFormat.format(row.commission) : "-"}</td>
                    <td class="smart-table__cell active" data-st-field="at">${new Date(row.at).toLocaleDateString("ru-RU")}</td>
                    <td>${row.status.name}</td>
                </tr>
            `;
        }
    });
    $("#interdivisional-debts-history-table").smartTableWithVirtualScroll({
        name: "all-interdivisional-debts",
        csrfToken,
        firstShowRows: "intersected",

        defaultOrder: [{ "field": "datetime", "sort": "desc" }],
        numberFormat: new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
        lastRowTarget: "#interdivisional-debts-history-last-row",
        rowsTarget: "#interdivisional-debts-history-table-rows",
        getValuesUrl: "/p1/finance-module/interdivisional-debts-get-values",
        getRowsUrl: "/p1/finance-module/interdivisional-debts-get-rows",
        getSubtotalsUrl: "/p1/finance-module/interdivisional-debts-get-subtotals",
        loadingHtml: `
            <tr>
                <td class="text-center" colspan="8">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,
        getTr(row) {
            const id = `interdivisional-debts-${row.id}`;
            let type = null;
            switch (row.type) {
                case "minus_plus":
                    type = "Погашение долга";
                    break;
                case "plus_minus":
                    type = "Прямой долг";
                    break;
                case "plus_minus_plus":
                    type = "Взаимозачёт когда плюс дают плюсу через минус";
                    break;
                case "minus_plus_minus":
                    type = "Взаимозачёт когда минус дают минусу через плюс";
                    break;
                case "minus_plus_and_plus_minus_plus":
                    type = "Полное погашение долгов и взаимозачёт когда плюс дают плюсу через минус"
                default:
                    break;
            }
            const trs = $(`
                <tr>
                    <td class="align-middle border-bottom-0 smart-table__always-shown">
                        <button class="btn btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#${id}" aria-expanded="false" aria-controls="${id}">
                            <i class="fa-solid fa-square-minus"></i>
                        </button>
                    </td>
                    <td class="border-bottom-0 align-middle" data-st-field="from_whom">
                        ${row.from_whom}
                    </td>
                    <td class="align-middle border-bottom-0" data-st-field="from_account__name">${row.from_account.name}</td>
                    <td class="align-middle border-bottom-0" data-st-field="to_whom">${row.to_whom}</td>
                    <td class="align-middle border-bottom-0" data-st-field="to_account__name">${row.to_account.name}</td>
                    <td class="align-middle border-bottom-0" data-st-field="sum">${numberFormat.format(row.sum)}</td>
                    <td class="align-middle border-bottom-0" data-st-field="datetime">${new Date(row.datetime).toLocaleDateString()}</td>
                    <td class="align-middle border-bottom-0">${row.status.name}</td>
                </tr>
                <tr>
                    <td class="smart-table__always-shown  p-0" colspan="8">
                        <div class="collapse" id="${id}">
                            <div class="p-2">
                                <h6>${type}</h6>
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>От кого</th>
                                            <th>Кому</th>
                                            <th>Сумма</th>
                                        </tr>
                                    </thead>
                                    <tbody class="debts">

                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </td>
                </tr>
            `);
            const $debts = $(".debts", trs);
            for (const debt of row.debts) {
                $debts.append(`
                    <tr>
                        <td>${debt.from_whom}</td>
                        <td>${debt.to_whom}</td>
                        <td>${numberFormat.format(debt.sum)}</td>
                    </tr>
                `);
            }
            return trs;
        }
    });
    $("#debts-history-table").smartTableWithVirtualScroll({
        name: "all-debts",
        csrfToken,
        firstShowRows: "intersected",
        unloadTypes: [
            {
                html: `<i class="fa-solid fa-file-excel"></i> ДМП`,
                type: "interdivisional-debts-xlsx-1"
            }
        ],
        unloadUrl: "/p1/finance-module/unload",
        defaultOrder: [{ "field": "datetime", "sort": "desc" }],
        numberFormat: new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
        lastRowTarget: "#debts-history-last-row",
        rowsTarget: "#debts-history-table-rows",
        getValuesUrl: "/p1/finance-module/debts-get-values",
        getRowsUrl: "/p1/finance-module/debts-get-rows",
        getSubtotalsUrl: "/p1/finance-module/debts-get-subtotals",
        loadingHtml: `
            <tr>
                <td class="text-center" colspan="5">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,
        getTr(row) {
            return `
                <tr>
                    <td>${row.from_whom}</td>
                    <td>${row.to_whom}</td>
                    <td>${balanceNumberFormat.format(row.sum)}</td>
                    <td>${new Date(row.datetime).toLocaleDateString()}</td>
                    <td>${row.status || ""}</td>
                </tr>
            `;
        }
    });
    $("#unpaid-invoices-table").smartTableWithVirtualScroll({
        name: "all-unpaid-invoices",
        csrfToken,
        canReload: false,
        firstShowRows: "intersected",
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
        rowsTarget: "#unpaid-invoices-rows",
        getValuesUrl: "/p1/finance-module/all-unpaid-invoices-get-values",
        getRowsUrl: "/p1/finance-module/all-unpaid-invoices-get-rows",
        getSubtotalsUrl: "/p1/finance-module/all-unpaid-invoices-get-subtotals",
        loadingHtml: `
            <tr>
                <td class="text-center p-2" colspan="52">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,
        getTr(row) {
            const $tr = $(`
                <tr data-number="${row.number}" class="unpaid-invoice-row" id="unpaid-invoice-row-${row.id}">
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
                    <td>
                        <input type="number" min="0" max="${row.allowed_payment_amount}" step="0.01" class="form-control form-control-sm unpaid-invoice-sum-input" aria-describedby="sum-input-validation-${row.number}">
                    </td> 
                    <td><div class="td-payment-decision td-content">${row.payment_decision}</div></td>
                    <td><div class="td-content">${row.bank}</div></td>
                </tr>
            `);
            unpaidInvoices[row.number] = row;
            row.allowed_payment_amount = parseFloat(row.allowed_payment_amount).toFixed(2);
            const $sumInput = $(".unpaid-invoice-sum-input", $tr);
            
            row.remainder = parseFloat(row.remainder) || 0;
            
            
            if (!row.has_exception) {
                if (!row.remainder) {
                    $sumInput.prop("title", "Оплачено");
                    $sumInput.prop("disabled", true);
                } else {
                    if (row.payment_decision != "OK") {
                        $sumInput.prop("title", row.payment_decision);
                        $sumInput.prop("disabled", true);
                        if (row.payment_decision == "Отказ! Заполнить статус работ") {
                            $(".td-payment-decision", $tr).html(`<a href="https://docs.google.com/spreadsheets/d/1nT3voM4t7BI2NKfotHS1TQqvGmXwuPl3zERE_wGaaw0/edit#gid=0&fvid=1576463693" target="_blank">${row.payment_decision}</a>`);
                        }
                    } else {
                        unpaidInvoiceCheckCanPay($tr);
                    }
                }
            }
            $sumInput.val(unpaidInvoiceNumberSum[row.number]);
            function clamp() {
                const value = Math.min(row.allowed_payment_amount, Math.max(parseFloat($sumInput.val()) || 0, 0));
                $sumInput.val(value);
            }
            $sumInput.on("input", function () {
                clamp();
                const value = parseFloat($(this).val());
                if (value) {
                    unpaidInvoiceNumberSum[row.number] = value;
                } else {
                    delete unpaidInvoiceNumberSum[row.number];
                }
                displayTotalUnpaidInvoices();
                checkCanSubmit();
            });
            return $tr;
        }
    });
    let sutochnyeIndex = 1;
    $("#sutochnye-history-table").smartTableWithVirtualScroll({
        name: "all-sutochnye-history-table",
        csrfToken,
        firstShowRows: "intersected",
        numberFormat,
        unload: [
            {
                html: `<i class="fa-solid fa-file-excel"></i> XLSX`,
                async onUnload(fieldValuesList, order) {
                    console.log(123);
                }
            }
        ],
        lastRowTarget: "#sutochnye-history-table-last-row",
        rowsTarget: "#sutochnye-history-table-rows",
        getValuesUrl: "/p1/finance-module/sutochnye-get-values",
        getRowsUrl: "/p1/finance-module/sutochnye-get-rows",
        getSubtotalsUrl: "/p1/finance-module/sutochnye-get-subtotals",
        loadingHtml: `
            <tr>
                <td class="text-center" colspan="11">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,

        getTr(row) {
            const $tr = $(`
                <tr>
                    <td class="smart-table__always-shown">
                        <button class="btn btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#sutochnye-collapse-${sutochnyeIndex}" aria-expanded="false" aria-controls="sutochnye-collapse-${sutochnyeIndex}">
                            <i class="fa-solid fa-square-minus"></i>
                        </button>
                    </td> 
                    <td>${row.name}</td> 
                    <td>${row.days}</td> 
                    <td>${numberFormat.format(row.sum)}</td> 
                    <td>${row.subdivision.name}</td> 
                    <td>${row.project}</td> 
                    <td>${row.responsible}</td> 
                    <td>${`${new Date(row.business_trip_start_date).toLocaleDateString()}-${new Date(row.business_trip_end_date).toLocaleDateString()}`}</td> 
                    <td>${row.destination_point}</td> 
                    <td>${row.project_region.name}</td> 
                    <td>${row.account.name}</td> 
                    <td>${new Date(row.created_at).toLocaleDateString()}</td> 
                    <td>${row.status.name}</td> 
                </tr>
                <tr>
                    <td class="p-0 smart-table__always-shown" colspan="11">
                        <div id="sutochnye-collapse-${sutochnyeIndex}" class="collapse">
                            <div class="p-2">
                                <h5>Файлы</h5>
                                <ul class="files-ul list-group list-group-flush">

                                </ul>
                            </div>
                        </div>
                    </td>
                </tr>
            `);
            if (row.files.length) {
                for (const file of row.files) {
                    $tr.find(".files-ul").append(`
                        <li class="list-group-item">
                            <div class="row">
                                <div class="col">
                                    ${file.file.name}
                                </div>
                                <div class="col">
                                    <button class="show-sutochnie-file btn btn-primary" data-name="${file.file.name}" data-url="${file.file.url}">Показать</button>
                                </div>
                            </div>
                        </li>
                    `);
                }
            } else {
                $tr.find(".files-ul").append(`
                    <li class="list-group-item">Файлов нету</li>
                `);
            }
            sutochnyeIndex++;
            return $tr;
        }
    });
}

function getActiveSubdivision() {
    return $("#project-region-accounts-subdivisions .nav-link.active").data("subdivision");
}

/**
 * - `activeTab` - текущая вкладка,
 * - Расчётные счета сохраняются в переменную `selectedAccounts[activeTab]`  при каждом выборе,
 * - При изменение вкладки, все галочки расчётных счетов убираются, и загружается выбранные расчётные счета конкретной вкладки
 */



$(async function () {
    smartTables();
    displayTotalTransfers();
    displayTotalMandatoryPayments();
    displayTotalUnpaidInvoices();
    displayTotalInterdivisionalDebts();
    displayTotalSutochnye();
    checkCanSubmit();
    $(".payment-tab").on("shown.bs.tab", async function (event) {
        const tab = $(this).attr("aria-controls");
        await onTabChange(tab);
    });
    accountsTable.changeToggleViewButtonText();
    accountsTable.addEventListener("accounts-displayed", function () {
        accountSelection(activeTab);
        loadSelectedAccounts(activeTab);
        filterMandatoryPaymentsTableWithSubdivision();

        $(".unpaid-invoice-row-check-can-pay").each(function() {
            unpaidInvoiceCheckCanPay(this);
        });
    });
    const $filterMandatoryPaymentsTableWithSubdivision = $("#filter-mandatory-payments-table-with-subdivision");
    mandatoryPaymentsFilterWithSubdivision = localStorage.getItem("mandatory-payments-filter-with-subdivision") == null || localStorage.getItem("mandatory-payments-filter-with-subdivision") === "true";
    $filterMandatoryPaymentsTableWithSubdivision.prop("checked", mandatoryPaymentsFilterWithSubdivision);
    projectRegionMandatoryPaymentsPaid = await getProjectRegionMandatoryPaymentsPaid();

    $(document).on("change", ".account-radio", function () {
        if (activeTab) {
            saveSelectedAccounts(activeTab);
            checkCanSubmit();
        }
    });
    
    $filterMandatoryPaymentsTableWithSubdivision.on("change", async function () {
        mandatoryPaymentsFilterWithSubdivision = $(this).prop("checked");
        localStorage.setItem("mandatory-payments-filter-with-subdivision", $(this).prop("checked") ? "true" : "false");
        await filterMandatoryPaymentsTableWithSubdivision(getActiveSubdivision());
    });
    $("#project-region-accounts-subdivisions").on("shown.bs.tab", ".nav-link", async function (event) {
        await filterMandatoryPaymentsTableWithSubdivision($(this).data("subdivision"));
    });
    $("#sync-button").on("click", sync.bind(null, true));
    $("#form").on("submit", async function (event) {
        event.preventDefault();
        submit();
    });
    $("#project-region-accounts-table-setoff-button").on("click", async function () {
        const response = await fetch(`/p1/finance-module/api/setoff`, { method: "POST", body: JSON.stringify({ subdivision: getActiveSubdivision() }), headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/json" } });
        const json = await response.json();
        await accountsTable.reload();
    });

    $(document).on("click", ".show-sutochnie-file", function () {
        const url = $(this).data("url");
        const name = $(this).data("name");
        const $modal = $(`
            <div class="modal  modal-fade" tabindex="-1">
                <div class="modal-dialog my-0 mx-0 px-5" style="max-width: 100vw">
                    <div class="modal-content rounded-0 vh-100">
                        <div class="modal-header">
                        <h5 class="modal-title">Суточные - Файл - ${name}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <iframe src="${url}" class="w-100 h-100"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        `);
        $modal.appendTo(document.body);
        $modal.modal("show");
        $modal.on("hidden.bs.modal", function () {
            $modal.remove();
        });
    });

    $(document).on("click", "#unload-1-button", async function() {
        const date = new Date();
        const defaultHtml = $(this).html();
        let time = 0;
        const timeNumberFormat = Intl.NumberFormat("ru-RU", {maximumFractionDigits: 2})
        $(this).html(`
            <div class="d-flex align-items-center gap-1">
                <div>
                    Выгрузка...
                </div>
                <div id="unload-1-time"></div>
                <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
            </div>
        `);
        const $unloadTime = $(this).find("#unload-1-time");
        const timer = setInterval(() => {
            time += 0.01;
            $unloadTime.html(`${timeNumberFormat.format(time)} с`)
        }, 10);
        $(this).prop("disabled", true);
        try {
            const response = await fetch("/p1/finance-module/unload", {
                method: "POST",
                csrfToken,
                body: JSON.stringify({
                    type: "unload-1"
                })
            });
            const blob = await response.blob();
            const objectUrl = URL.createObjectURL(blob);
            const a = $(`<a href="${objectUrl}" download="ДДС ${date.toLocaleString()}.xlsx"></a>`).appendTo(document.body)[0];
            a.click();
            a.remove();
            URL.revokeObjectURL(objectUrl);
        } catch (error) {
            console.error(error);
        }
        clearInterval(timer);
        $(this).html(defaultHtml);
        $(this).prop("disabled", false);
    });

    await Promise.all([
        accountsTable.reload(),
        onTabChange("mandatory-payments")
    ]);
});


$(async function() {

});
