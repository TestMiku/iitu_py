$(function () {
  const numberFormat = new Intl.NumberFormat("ru-RU", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  $("#paid-invoices-table").smartTableWithVirtualScroll({
    name: "unpaid-invoices-paid-invoices-table",
    csrfToken,
    firstShowRows: "intersected",
    unloadTypes: [
      {
        html: `<i class="fa-solid fa-file-excel"></i> 1C`,
        type: "unload-paid-invoices-xlsx-2",
      },
    ],
    unloadUrl: "/p1/finance-module/unload",
    defaultOrder: [{ field: "at", sort: "desc" }],
    numberFormat: new Intl.NumberFormat("ru-RU", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }),
    lastRowTarget: "#paid-invoices-table-last-row",
    rowsTarget: "#paid-invoices-table-rows",
    getValuesUrl:
      "/p1/finance-module/unpaid-invoices/smart-tables/paid-invoices-get-values",
    getRowsUrl:
      "/p1/finance-module/unpaid-invoices/smart-tables/paid-invoices-get-rows",
    getSubtotalsUrl:
      "/p1/finance-module/unpaid-invoices/smart-tables/paid-invoices-get-subtotals",
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
      const $tr = $(/*html*/ `
                <tr>
                    <td class="align-middle text-center">${row.number}</td>
                    <td class="align-middle text-center">${new Date(
                      row.date
                    ).toLocaleDateString("ru-RU")}</td>
                    <td class="align-middle">${row.invoice_number}</td>
                    <td class="align-middle text-center">${new Date(
                      row.invoice_date
                    ).toLocaleDateString("ru-RU")}</td>
                    <td class="align-middle thin-scrollbar" style="max-width: 12em; white-space: nowrap; overflow-x: scroll">${
                      row.project
                    }</span></td>
                    <td class="align-middle">${row.responsible_user_id}</td>
                    <td class="align-middle thin-scrollbar" style="max-width: 14em; white-space: nowrap; overflow-x: scroll">${
                      row.approver
                    }</td>
                    <td class="align-middle" style="white-space: nowrap;">${
                      row.llc
                    }</td>
                    <td class="align-middle thin-scrollbar" style="max-width: 14em; white-space: nowrap; overflow-x: scroll">${
                      row.contractor
                    }</td>
                    <td class="align-middle thin-scrollbar" style="max-width: 16em; white-space: nowrap; overflow-x: scroll">${
                      row.comment
                    }</td>
                    <td class="align-middle text-center">${row.currency}</td>
                    <td class="align-middle text-end">${numberFormat.format(
                      row.sum
                    )}</td>
                    <td class="align-middle" style="white-space: nowrap;">${
                      row.invoice_category || ""
                    }</td>
                    <td class="align-middle thin-scrollbar" style="max-width: 12em; white-space: nowrap; overflow-x: scroll">${
                      row.revenue_expense_articles || ""
                    }</td>
                    <td class="align-middle">${row.sales_order}</td>
                    <td class="align-middle text-center">${
                      row.bin_or_iin || ""
                    }</td>
                    <td class="align-middle text-end">${
                      row.document_amount
                        ? numberFormat.format(row.document_amount)
                        : ""
                    }</td>
                    <td class="align-middle">${row.account.number}</td>
                    <td class="align-middle text-center">${row.iic || ""}</td>
                    <td class="align-middle text-center">${
                      row.payment_destination_code || ""
                    }</td>
                    <td class="align-middle">${row.contract_number || ""}</td>
                    <td class="align-middle text-end">${numberFormat.format(
                      row.invoice_amount
                    )}</td>
                    <td class="align-middle text-end">${
                      row.paid_amount_1c
                        ? numberFormat.format(row.paid_amount_1c)
                        : ""
                    }</td>
                    <td class="align-middle text-end">${numberFormat.format(
                      row.sum
                    )}</td>
                    <td class="align-middle text-center">${new Date(
                      row.at
                    ).toLocaleDateString("ru-RU")}</td>
                    <td class="align-middle thin-scrollbar" style="max-width: 10em; white-space: nowrap; overflow-x: scroll">${
                      row.project_region.name
                    }</td>
                    <td class="align-middle">${
                      row.project_region.director_display
                    }</td>
                    <td class="align-middle">${
                      row.project_region.subdivision
                        ? row.project_region.subdivision.name
                        : ""
                    }</td>
                    <td class="align-middle" style="white-space: nowrap">${
                      row.account.name
                    }</td>
                    <td class="align-middle confirmation-td"></td>
                </tr>
            `);
      return $tr;
    },
  });
  const $mail1CStatus = $("#mail-1c-status");

  async function mail1C() {
    $(this).off("click", mail1C);

    const defaultHtml = $(this).html();
    $mail1CStatus.text(null);
    $(this).prop("disabled", true);
    $(this).html(
      `<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span> Отправка...`
    );
    try {
      const response = await fetch(
        "/p1/finance-module/unpaid-invoices/mail-1c", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            }
        }
      );
      const json = await response.json();
      if (response.ok) {
        $mail1CStatus.text(json.detail);
      } else {
        $mail1CStatus.text("Ошибка при отправке, см. консоль");
        console.error(response);
      }
    } catch (error) {
      $mail1CStatus.text(
        "Ошибка при отправке, возможно вы не подключены к интернету, см. консоль"
      );
      console.error(error);
    }
    setTimeout(() => {
        $mail1CStatus.text(null);
    }, 2000);
    $(this).prop("disabled", false);
    $(this).html(defaultHtml);
    $(this).on("click", mail1C);
  }

  $("#mail-1c-button").on("click", mail1C);
});
