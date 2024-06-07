$(function() {
    const numberFormat = new Intl.NumberFormat("ru-RU", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
    const $statementReconciliationFormSubmitButton = $("#statement-reconciliation-form-submit-button");
    const $statementReconciliationFormLoading = $(".statement-reconciliation-form-loading");
    const $paidInvoicesTableRows = $("#paid-invoices-table-rows");
    const $notFoundTableRows = $("#not-found-table-rows");
    const $refundTableRows = $("#refund-table-rows");
    const $statementReconciliationFormErrorMessage = $("#statement-reconciliation-form-error-message");
    const $statementsTableRows = $("#statements-table-rows");
    const $statementReconciliationSavedResults = $("#statement-reconciliation-saved-results");
    let loading = false;
    let data = null;
    $("#statement-reconciliation-form").on("submit", function(event) {
        event.preventDefault();
        if (loading) {
            return;
        }
        try {
            $statementReconciliationFormSubmitButton.prop("disabled", true);
            $statementReconciliationFormErrorMessage.empty();
            $paidInvoicesTableRows.html(`
                <tr>
                    <td class="text-center" colspan="6">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </td>    
                </tr>
            `);
            $notFoundTableRows.html(`
                <tr>
                    <td class="text-center" colspan="5">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </td>    
                </tr>
            `);
            $refundTableRows.html(`
                <tr>
                    <td class="text-center" colspan="6">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </td>    
                </tr>
            `);
            $statementsTableRows.html(`
                <tr>
                    <td class="text-center" colspan="8">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </td>    
                </tr>
            `);
    
            $statementReconciliationFormLoading.removeClass("d-none");
            const formData = new FormData(this);
            const xmlHttpRequest = new XMLHttpRequest();
            xmlHttpRequest.addEventListener("readystatechange", function() {
                if (this.readyState === XMLHttpRequest.DONE) {
                    const json = JSON.parse(this.response);
                    
                    if (this.statusText == "OK") {
                        showResult(json);
                        showStatementReconciliationSavedResults();
                    } else {
                        showError(json.detail);
                    }
                    $statementReconciliationFormSubmitButton.prop("disabled", false);
                    $statementReconciliationFormLoading.addClass("d-none");
                }
                loading = false;
            });
            xmlHttpRequest.open("POST", "/p1/finance-module/get-statement-reconciliation-result");
            loading = true;
            xmlHttpRequest.send(formData);
        } catch (error) {
            $statementReconciliationFormSubmitButton.prop("disabled", false);
            $statementReconciliationFormLoading.addClass("d-none");
            loading = false;
            console.error(error);
            showError(error);
        }
    });

    const $paidInvoicesTable = $("#paid-invoices-table");
    $paidInvoicesTable.smartTable({
        name: "statement-reconciliation-paid-invoices-table",
        canReload: false,
        defaultOrder: [{field: "checked", sort: "asc"}],
        getValues(field, fieldType, fieldValuesList) {
            return smartTableGetValues(data ? data.paidInvoices : null, field, fieldType, fieldValuesList);
        },
        showRows(fieldValuesList, fieldType, order) {
            const paidInvoices = smartTableGetRows(data ? data.paidInvoices : null, fieldValuesList, fieldType, order);
            $paidInvoicesTableRows.empty();
            if (paidInvoices.length === 0) {
                $paidInvoicesTableRows.append(`
                    <tr>
                        <td class="text-center" colspan="6">Оплаты не найдены</td>    
                    </tr>
                `);
            } else {
                for (const paidInvoice of paidInvoices) {
                    const $tr = $(`
                        <tr class="border-black">
                            <th class="align-middle text-center" scope="row">
                                <input type="hidden" name="paid-invoice-id" value="${paidInvoice.id}"/>
                                <button title="Показать связанные документы" type="button" data-bs-toggle="collapse" data-bs-target="#related-document-${paidInvoice.id}" aria-expanded="false" aria-controls="related-document-${paidInvoice.id}" class="btn btn-sm btn-link show-related-documents-button">${paidInvoice.number}</button>
                            </th>
                            <td class="align-middle">${paidInvoice.contractor}</td>
                            <td class="align-middle text-end">${numberFormat.format(paidInvoice.paid)}</td>
                            <td class="align-middle text-end">
                                <input type="hidden" name="paid-invoice-commission-${paidInvoice.id}" value="${paidInvoice.commissionDocument ? paidInvoice.commissionDocument.debit : 0}"/>
                                ${paidInvoice.commissionDocument ? numberFormat.format(paidInvoice.commissionDocument.debit) : "-"}
                            </td>
                            <td class="align-middle">${paidInvoice.account}</td>
                            <td class="align-middle">
                                <div class="d-flex justify-content-center">
                                    <input type="checkbox" class="form-check complete-checkbox" name="paid-invoice-complete-${paidInvoice.id}"/>
                                </div>
                            </td>
                        </tr>
                    `);
                    const $collapseTr = $(`
                        <tr class="border-black">
                            <td class="p-0" colspan="6">
                                <div class="collapse" id="related-document-${paidInvoice.id}">
                                    <div class="p-2">
                                        <div class="commission-document">
                                            <h5>
                                            Документ комиссий
                                            </h5>
                                            <table class="table table-bordered border-black commission-document-table">
                                                <thead class="table-light border-black">
                                                    <tr>
                                                        <th class="text-center" scope="col">№ п/п</th>
                                                        <th class="text-center" scope="col">Дата</th>
                                                        <th class="text-center" scope="col">Корреспондент</th>
                                                        <th class="text-center text-primary" scope="col">Дебет</th>
                                                        <th class="text-center text-primary" scope="col">Кредит</th>
                                                        <th class="text-center text-primary" scope="col">Назначение</th>
                                                        <th class="text-center" scope="col">Файл</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr class="commission-document-table-row">
                                                    </tr>
                                                </tody>
                                            </table>
                                        </div>
                                        <div class="related-documents">
                                            <h5>
                                            Документы
                                            </h5>
                                            <table class="table table-bordered border-black related-documents-table">
                                                <thead class="table-light border-black">
                                                    <tr>
                                                        <th class="text-center" scope="col">№ п/п</th>
                                                        <th class="text-center" scope="col">Дата</th>
                                                        <th class="text-center" scope="col">Корреспондент</th>
                                                        <th class="text-center text-primary" scope="col">Дебет</th>
                                                        <th class="text-center text-primary" scope="col">Кредит</th>
                                                        <th class="text-center text-primary" scope="col">Назначение</th>
                                                        <th class="text-center" scope="col">Файл</th>
                                                    </tr>
                                                </thead>
                                                <tbody class="related-documents-table-rows">
                                                </tody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    `);
                    const $showRelatedDocumentButton = $tr.find(".show-related-documents-button");
                    $tr.find(".complete-checkbox").prop("checked", paidInvoice.matched).on("change", function() {
                        paidInvoice.checked = $(this).prop("checked");
                    });
                    $showRelatedDocumentButton.prop("disabled", !paidInvoice.matched);
                    if (paidInvoice.matched) {
                        $tr.addClass("table-success");
                    } else {
                        $tr.addClass("table-danger");
                    }
                    const $relatedDocumentsTableRows = $collapseTr.find(".related-documents-table-rows");
                    let hasRelatedDocuments = paidInvoice.relatedDocuments && paidInvoice.relatedDocuments.length !== 0;
                    $collapseTr.find(".related-documents-table").toggleClass("d-none", !hasRelatedDocuments);
                    if (hasRelatedDocuments) {
                        for (const document of paidInvoice.relatedDocuments) {
                            $relatedDocumentsTableRows.append(`
                                <tr class="border-black">
                                    <th class="align-middle" scope="row">${document.id}</th>
                                    <td class="align-middle">${new Date(document.datetime).toLocaleDateString()}</td>
                                    <td class="align-middle">${document.correspondent}</td>
                                    <td class="align-middle text-end">${numberFormat.format(document.debit)}</td>
                                    <td class="align-middle text-end">${numberFormat.format(document.credit)}</td>
                                    <td class="align-middle">${document.purposeOfPayment}</td>
                                    <td class="align-middle">${document.uploadedFile}</td>
                                </tr>
                            `);
                        }
                    }
                    $collapseTr.find(".commission-document").toggleClass("d-none", !paidInvoice.commissionDocument);

                    if (paidInvoice.commissionDocument) {
                        $collapseTr.find(".commission-document-table-row").html(`
                            <th class="align-middle" scope="row">${paidInvoice.commissionDocument.id}</th>
                            <td class="align-middle">${new Date(paidInvoice.commissionDocument.datetime).toLocaleDateString()}</td>
                            <td class="align-middle">${paidInvoice.commissionDocument.correspondent}</td>
                            <td class="align-middle text-end">${numberFormat.format(paidInvoice.commissionDocument.debit)}</td>
                            <td class="align-middle text-end">${numberFormat.format(paidInvoice.commissionDocument.credit)}</td>
                            <td class="align-middle">${paidInvoice.commissionDocument.purposeOfPayment}</td>
                            <td class="align-middle">${paidInvoice.commissionDocument.uploadedFile}</td>
                        `);
                    }
                    $paidInvoicesTableRows.append($tr);
                    if (hasRelatedDocuments || paidInvoice.commissionDocument) {
                        $collapseTr.addClass("border-top-0");
                        $tr.addClass("border-bottom-0");
                        $paidInvoicesTableRows.append($collapseTr);
                    }
                }
            }
        },
        getSubtotals(fieldValuesList, fieldType, fieldSubtotal) {
            return smartTableGetSubtotals(data ? data.paidInvoices : null, fieldValuesList, fieldType, fieldSubtotal);
        }
    });
    const $statementsTable = $("#statements-table");
    function getDocuments() {
        if (!data) {
            return [];
        }
        let result = [];
        for (const statement of data.statements) {
            for (const [, documents] of Object.entries(statement.correspondentDocuments)) {
                for (const document of documents) {
                    result.push(document)
                }
            }
        }
        return result;
    }
    $statementsTable.smartTable({
        name: "statement-reconciliation-statements-table",
        canReload: false,
        getValues(field, fieldType, fieldValuesList) {
            return smartTableGetValues(getDocuments(), field, fieldType, fieldValuesList);
        },
        showRows(fieldValuesList, fieldType, order) {
            const documents = smartTableGetRows(getDocuments(), fieldValuesList, fieldType, order);
            $statementsTableRows.empty();
            if (documents.length === 0) {
                $statementsTableRows.append(`
                    <tr>
                        <td class="text-center" colspan="8">Выписки не найдены</td>    
                    </tr>
                `);
            } else {
                let index = 0;
                for (const document of documents) {
                    const $tr = $(`
                        <tr class="border-black">
                            <th class="align-middle" scope="row">
                                <button title="Показать связанные документы и оплаты" type="button" data-bs-toggle="collapse" data-bs-target="#statement-collapse-${index}" aria-expanded="false" aria-controls="statement-collapse-${index}" class="btn btn-sm btn-link collapse-button">${document.id}</button>
                            </th>
                            <td class="align-middle">${new Date(document.datetime).toLocaleDateString()}</td>
                            <td class="align-middle">${document.correspondent}</td>
                            <td class="align-middle text-end">${numberFormat.format(document.debit)}</td>
                            <td class="align-middle text-end">${numberFormat.format(document.credit)}</td>
                            <td class="align-middle">${document.ppc}</td>
                            <td class="align-middle">${document.purposeOfPayment}</td>
                            <td class="align-middle">${document.uploadedFile}</td>
                        </tr>
                    `);
                    const $collapseTr = $(`
                        <tr class="border-black">
                            <td class="p-0" colspan="8">
                                <div class="collapse" id="statement-collapse-${index}">
                                    <div class="p-2">
                                        <div class="commission-document">
                                            <h5>
                                            Документ комиссий
                                            </h5>
                                            <table class="table table-bordered border-black commission-document-table">
                                                <thead class="table-light border-black">
                                                    <tr>
                                                        <th class="text-center" scope="col">№ п/п</th>
                                                        <th class="text-center" scope="col">Дата</th>
                                                        <th class="text-center" scope="col">Корреспондент</th>
                                                        <th class="text-center text-primary" scope="col">Дебет</th>
                                                        <th class="text-center text-primary" scope="col">Кредит</th>
                                                        <th class="text-center text-primary" scope="col">Назначение</th>
                                                        <th class="text-center" scope="col">Файл</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr class="commission-document-table-row">
                                                    </tr>
                                                </tody>
                                            </table>
                                        </div>
                                        <div class="related-paid-invoices">
                                            <h5>
                                            Список оплат
                                            </h5>
                                            <table class="table table-bordered border-black related-paid-invoices-table">
                                                <thead class="table-light border-black">
                                                    <tr>
                                                        <th class="text-center" scope="col">ДО</th>
                                                        <th class="text-center" scope="col">Контрагент</th>
                                                        <th class="text-center text-primary" scope="col">Сумма</th>
                                                        <th class="text-center text-primary" scope="col">Коммисия</th>
                                                        <th class="text-center" scope="col">Расчётный счёт</th>
                                                    </tr>
                                                </thead>
                                                <tbody class="related-paid-invoices-table-rows">
                                                </tody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    `);
                    const $relatedPaidInvoicesTableRows = $collapseTr.find(".related-paid-invoices-table-rows");
                    let hasRelatedPaidInvoices = document.relatedPaidInvoices && document.relatedPaidInvoices.length !== 0;
                    $collapseTr.find(".related-paid-invoices").toggleClass("d-none", !hasRelatedPaidInvoices);
                    if (hasRelatedPaidInvoices) {
                        for (const paidInvoice of document.relatedPaidInvoices) {
                            $relatedPaidInvoicesTableRows.append(`
                                <tr class="border-black">
                                    <th class="align-middle" scope="row">${paidInvoice.number}</th>
                                    <td class="align-middle">${paidInvoice.contractor}</td>
                                    <td class="align-middle text-end">${numberFormat.format(paidInvoice.paid)}</td>
                                    <td class="align-middle">${paidInvoice.commissionDocument ? paidInvoice.commissionDocument.debit : "-"}</td>
                                    <td class="align-middle">${paidInvoice.account}</td>
                                </tr>
                            `);
                        }
                    }
    
                    $collapseTr.find(".commission-document").toggleClass("d-none", !document.commissionDocument);
                    if (document.commissionDocument) {
                        $collapseTr.find(".commission-document-table-row").html(`
                            <th class="align-middle" scope="row">${document.commissionDocument.id}</th>
                            <td class="align-middle">${new Date(document.commissionDocument.datetime).toLocaleDateString()}</td>
                            <td class="align-middle">${document.commissionDocument.correspondent}</td>
                            <td class="align-middle text-end">${numberFormat.format(document.commissionDocument.debit)}</td>
                            <td class="align-middle text-end">${numberFormat.format(document.commissionDocument.credit)}</td>
                            <td class="align-middle">${document.commissionDocument.purposeOfPayment}</td>
                            <td class="align-middle">${document.commissionDocument.uploadedFile}</td>
                        `);
                    }
                    $statementsTableRows.append($tr);
                    if (document.commissionDocument || hasRelatedPaidInvoices) {
                        $collapseTr.addClass("border-top-0");
                        $tr.addClass("border-bottom-0");
                        $statementsTableRows.append($collapseTr);
                    } else {
                        $tr.find(".collapse-button").prop("disabled", true);
                    }
                    index++;
                }
            }
        },
        getSubtotals(fieldValuesList, fieldType, fieldSubtotal) {
            return smartTableGetSubtotals(getDocuments(), fieldValuesList, fieldType, fieldSubtotal);
        }
    });

    function showResult(result) {
        data = result;
        if (data) {
            for(const paidInvoice of data.paidInvoices) {
                paidInvoice.checked = paidInvoice.matched;
                paidInvoice.commission = paidInvoice.commissionDocument ? paidInvoice.commissionDocument.debit : 0;
            }
        }
        $paidInvoicesTable.smartTableReload();
        $statementsTable.smartTableReload();
        $notFoundTableRows.empty();
        $refundTableRows.empty();
        let hasRefundDocument = false;
        let hasNotFoundDocument = false;
        let hasDocuments = false;
        for (const statement of result.statements) {
            for (const [correspondent, documents] of Object.entries(statement.correspondentDocuments)) {
                for (const document of documents) {
                    hasDocuments = true;
                    if (document.matched || document.excluded) {
                        continue;
                    }
                    if (document.refund) {
                        hasRefundDocument = true;
                        $refundTableRows.append(`
                            <tr class="border-black">
                                <th class="align-middle" scope="row">${document.id}</th>
                                <td class="align-middle">${new Date(document.datetime).toLocaleDateString()}</td>
                                <td class="align-middle">${document.correspondent}</td>
                                <td class="align-middle text-end">${numberFormat.format(document.credit)}</td>
                                <td class="align-middle">${document.purposeOfPayment}</td>
                                <td class="align-middle">${statement.uploadedFile}</td>
                            </tr>
                        `);
                    } else {
                        hasNotFoundDocument = true;
                        const $tr = $(`
                            <tr class="border-black">
                                <th class="align-middle" scope="row">${document.id}</th>
                                <td class="align-middle">${new Date(document.datetime).toLocaleDateString()}</td>
                                <td class="align-middle">${document.correspondent}</td>
                                <td class="align-middle text-end">${numberFormat.format(document.debit)}</td>
                                <td class="align-middle">${statement.uploadedFile}</td>
                            </tr>
                        `);
                        if (document.commission) {
                            $tr.addClass("table-light");
                        }
                        $notFoundTableRows.append($tr);
                    }
                }
            }
        }
        if (!hasRefundDocument) {
            $refundTableRows.html(`
                <tr>
                    <td class="text-center" colspan="6">
                        Ничего не найдено
                    </td>    
                </tr>
            `);
        }
        if (!hasNotFoundDocument) {
            $notFoundTableRows.html(`
                <tr>
                    <td class="text-center" colspan="5">
                        Ничего не найдено
                    </td>    
                </tr>
            `);
        }
        console.log(result);
    }

    function showError(error) {
        $paidInvoicesTableRows.html(`
            <tr>
                <td class="text-center text-danger" colspan="6">
                    Произошла ошибка при сверке выпесек. См. консоль
                </td>    
            </tr>
        `);
        $notFoundTableRows.html(`
            <tr>
                <td class="text-center text-danger" colspan="5">
                    Произошла ошибка при сверке выпесек. См. консоль
                </td>    
            </tr>
        `);
        $refundTableRows.html(`
            <tr>
                <td class="text-center text-danger" colspan="6">
                    Произошла ошибка при сверке выпесек. См. консоль
                </td>    
            </tr>
        `);
        $statementsTableRows.html(`
            <tr>
                <td class="text-center text-danger" colspan="8">
                    Произошла ошибка при сверке выпесек. См. консоль
                </td>    
            </tr>
        `);
        $statementReconciliationFormErrorMessage.text(error);
    }

    $statementReconciliationSavedResults.on("click", ".saved-result-load-button", async function() {
        const savedResultId = $(this).data("savedResultId");
        const response = await fetch(`/p1/finance-module/api/statement-reconciliation-saved-result?id=${savedResultId}`);
        const json = await response.json();
        showResult(json);
    });

    async function showStatementReconciliationSavedResults() {
        $statementReconciliationSavedResults.html(`
            <li class="list-group-item text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </li>
        `);
        const response = await fetch("/p1/finance-module/api/statement-reconciliation-saved-results");
        const json = await response.json();
        if (json.length) {
            $statementReconciliationSavedResults.empty();
            for (const savedResult of json) {
                $statementReconciliationSavedResults.append(`
                    <li class="list-group-item">
                        <div class="row">
                            <div class="col-8">
                                <div>Сверка на дату ${new Date(savedResult.date).toLocaleDateString()},</div>
                                <div>Создан ${new Date(savedResult.created_date).toLocaleDateString()}.</div>
                            </div>
                            <div class="col-4 d-flex align-items-center"><button type="button" class="btn btn-primary saved-result-load-button" data-saved-result-id="${savedResult.id}">Показать</button></div>
                        </div>
                    </li>
                `);
            }
        } else {
            $statementReconciliationSavedResults.html(`
                <li class="list-group-item text-center">Пока здесь ничего нет</li>
            `);
        }
    }
    showStatementReconciliationSavedResults();

    const $statementReconciliationCompleteFormLoading = $("#statement-reconciliation-complete-form-loading");
    const $statementReconciliationCompleteFormInfo = $("#statement-reconciliation-complete-form-info");
    $("#statement-reconciliation-complete-form").on("submit", async function(event) {
        event.preventDefault();
        $statementReconciliationCompleteFormInfo.empty();
        $statementReconciliationCompleteFormLoading.removeClass("d-none");
        const response = await fetch("/p1/finance-module/api/complete-paid-invoices", {
            method: "POST",
            body: new FormData(this),
            headers: {
                "X-CSRFToken": csrfToken,
            }
        });
        const json = await response.json();
        $statementReconciliationCompleteFormInfo.html(`
            ${json.notFoundPaidInvoices.length !== 0 ? `<div>Не найдено оплат: ${json.notFoundPaidInvoices.join(", ")};</div>` : ""}
            <div>Отправлено на подтверждение ${json.completeCount}, подтверждено ${json.realCompletedCount};</div>
            <div>Отправлено на отклонение ${json.rejectCount}, отколнено ${json.realRejectedCount};</div>
        `);
        $statementReconciliationCompleteFormLoading.addClass("d-none");
    });
});