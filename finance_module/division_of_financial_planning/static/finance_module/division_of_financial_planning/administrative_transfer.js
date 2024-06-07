const accountsTable = new AccountsTable({
  url: "/p1/finance-module/api/project-region-accounts-table?filter=none",
});

async function loadNameDateList() {
  const response = await fetch(
    `/p1/finance-module/division-of-financial-planning/api/daily-table?show=per-day&date=${new Date()
      .toISOString()
      .slice(0, 10)}`
  );
  const json = await response.json();
  const $nameDataList = $("#name-datalist");
  $nameDataList.empty();
  for (const row of json.rows) {
    $nameDataList.append(`
            <option value="${row.name}"></option>
        `);
  }
}
const numberFormat = new Intl.NumberFormat("ru-RU", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
$(async function () {
  const $administrativeTransfersTable = $("#administrative-transfers-table");
  $administrativeTransfersTable.smartTableWithVirtualScroll({
    name: "division-of-financial-planning-administrative-transfers-table",
    csrfToken,
    defaultOrder: [{ field: "created_at", sort: "desc" }],
    firstShowRows: "intersected",
    numberFormat,
    lastRowTarget: "#administrative-transfers-table-last-row",
    rowsTarget: "#administrative-transfers-table-rows",
    getValuesUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/administrative-transfers-get-values",
    getRowsUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/administrative-transfers-get-rows",
    getSubtotalsUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/administrative-transfers-get-subtotals",
    loadingHtml: `
            <tr>
                <td class="text-center" colspan="7">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,
    getTr(row) {
      return `
                <tr>
                    <td class="text-center">${new Date(
                      row.created_at
                    ).toLocaleDateString("ru-RU")}</td>
                    <td>${row.project_region.name}</td>
                    <td>${row.account ? row.account.name : ""}</td>
                    <td>${row.name}</td>
                    <td class="text-end">${numberFormat.format(row.sum)}</td>
                    <td>${row.note}</td>
                    <td>${row.status.name}</td>
                </tr>
            `;
    },
  });

  const $form = $("#form");
  const $accountNameInput = $("#account-name-input");
  const $projectRegionNameInput = $("#project-region-name-input");
  const $projectRegionIdInput = $("#project-region-id-input");
  $(document).on("change", ".account-radio", function () {
    const accountId = $(this).val();
    const projectRegionId = $(this).data("projectRegionId");
    const account = accountsTable.getAccount(accountId);
    $accountNameInput.val(account.name);
    const projectRegion = accountsTable.getProjectRegion(projectRegionId);
    $projectRegionNameInput.val(projectRegion.name);
    $projectRegionIdInput.val(projectRegionId);
  });
  $form.on("submit", async function (event) {
    event.preventDefault();
    accountsTable.canSelectAnyAccount({
      form: "form",
      name: "account-id",
      required: true,
    });
    if (!this.checkValidity()) {
      this.reportValidity();
      return;
    }
    const response = await fetch(
      "/p1/finance-module/division-of-financial-planning/api/create-administrative-transfer",
      {
        method: "POST",
        body: new FormData(this),
        headers: {
          "X-CSRFToken": csrfToken,
        },
      }
    );
    const json = await response.json();
    this.reset();
    accountsTable.reload();
    $administrativeTransfersTable.smartTableReload();
  });
  accountsTable.addEventListener("accounts-displayed", function () {});
  const $chsiRows = $("#chsi-rows");
  let chsiRows = [];
  function showChsiTotalSum() {
    const $totalSum = $("#chsi-total-sum");
    $totalSum.text(
      numberFormat.format(
        chsiRows.reduce((sum, chsiRow) => sum + parseFloat(chsiRow.sum), 0)
      )
    );
  }
  showChsiTotalSum();
  const $addChsiForm = $("#add-chsi-form");
  function chsiAddRow(row) {
    chsiRows.push(row);
    const $tr = $(`
        <tr class="chsi-row">
            <td class="align-middle text-center">${row.llc}</td>
            <td class="align-middle">${row.recipient}</td>
            <td class="align-middle">${row.binOrIin}</td>
            <td class="align-middle">${row.iik}</td>
            <td class="align-middle">${row.executiveInscription}</td>
            <td class="align-middle">${row.retentionType}</td>
            <td class="align-middle">${row.collaborator}</td>
            <td class="align-middle">${row.iin}</td>
            <td class="align-middle text-center">${row.actualRetentionRate}</td>
            <td class="align-middle text-end">${numberFormat.format(
              row.sum
            )}</td>
            <td class="align-middle text-center">${row.executiveOrderReceiptDate.toLocaleDateString(
              "ru-RU"
            )}</td>
            <td class="text-center align-middle aling-middle"><button class="btn btn-sm btn-danger chsi-remove-row-button">Удалить</button></td>
        </tr>
    `);
    $tr.on("click", ".chsi-remove-row-button", function () {
      chsiRows.splice(chsiRows.indexOf(row), 1);
      $tr.remove();
      showChsiTotalSum();
    });
    showChsiTotalSum();
    $chsiRows.append($tr);
  }
  $addChsiForm.on("submit", function (event) {
    event.preventDefault();
    const row = {
      llc: this.elements["llc"].value,
      recipient: this.elements["recipient"].value,
      binOrIin: this.elements["iin-or-bin"].value,
      iik: this.elements["iik"].value,
      executiveInscription: this.elements["executive-inscription"].value,
      retentionType: this.elements["retention-type"].value,
      collaborator: this.elements["collaborator"].value,
      iin: this.elements["iin"].value,
      actualRetentionRate: this.elements["actual-retention-rate"].value,
      sum: this.elements["sum"].valueAsNumber,
      executiveOrderReceiptDate:
        this.elements["executive-order-receipt-date"].valueAsDate,
    };
    chsiAddRow(row);
    this.reset();
  });
  $addChsiForm.on("dragover", function (event) {
    event.preventDefault();
  });
  $addChsiForm.on("drop", function (event) {
    event.preventDefault();
    const $table = $(event.originalEvent.dataTransfer.getData("text/html"));
    chsiDeleteAllRows();
    let lastActualRetentionRate = null;
    $table.find("tr").each(function () {
        
        const $td = $(this).find("td");
        console.log(this);
        if ($td.length !== 11 && $td.length !== 10) {
            return;
        }
        
        
        let sum = null;
        let executiveOrderReceiptDate = null;
        let actualRetentionRate = null;
        console.log(actualRetentionRate);
        if ($td.length === 11) {
            actualRetentionRate = $($td[8]).text().trim();
            lastActualRetentionRate = actualRetentionRate;
            sum = $td[9];
            executiveOrderReceiptDate = $td[10];
        } else {
            actualRetentionRate = lastActualRetentionRate;
            sum = $td[8];
            executiveOrderReceiptDate = $td[9];
        }
        const dateMatch = $(executiveOrderReceiptDate).text().trim().match(/(\d+)\.(\d+)\.(\d+)/);
        if (!dateMatch) return;
        sum = parseFloat($(sum).text().trim().replace(/\s+/, "").replace(",", "."));
        executiveOrderReceiptDate = new Date(parseInt(dateMatch[3]), parseInt(dateMatch[2]), parseInt(dateMatch[1]));
        const row = {
            llc: $($td[0]).text().trim(),
            recipient: $($td[1]).text().trim(),
            binOrIin: $($td[2]).text().trim(),
            iik: $($td[3]).text().trim(),
            executiveInscription: $($td[4]).text().trim(),
            retentionType: $($td[5]).text().trim().split(/\s+/).join(" "),
            collaborator: $($td[6]).text().trim(),
            iin: $($td[7]).text().trim(),
            actualRetentionRate,
            sum,
            executiveOrderReceiptDate,
        };
        console.log($($td[10]).text().trim(), $($td[9]).text().replace(/\s+/, "").replace(",", "."))
        if (row.llc.toLowerCase() === "тоо") {
            return;
        }
        console.log(row);
        chsiAddRow(row);
    });
  });
  function chsiDeleteAllRows() {
    chsiRows = [];
    $chsiRows.find(".chsi-row").remove();
    showChsiTotalSum();
  }
  $("#chsi-delete-all-rows").on("click", chsiDeleteAllRows);
  $("#chsi-form").on("submit", async function (event) {
    event.preventDefault();
    accountsTable.canSelectAnyAccount({ form: "chsi-form", required: true });
    if (!this.checkValidity()) {
      this.reportValidity();
      return;
    }

    const response = await fetch(
      "/p1/finance-module/division-of-financial-planning/api/pay-chsi",
      {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
          rows: chsiRows,
          accountId: this.elements["account-id"].value,
          projectRegionId: this.elements["project-region-id"].value,
          date: this.elements["date"].valueAsDate,
        }),
      }
    );
    const json = await response.json();

    chsiDeleteAllRows();
  });

  $("#chsi-groups-table").smartTableWithVirtualScroll({
    name: "division-of-financial-planning-administrative-chsi-groups-table",
    csrfToken,
    defaultOrder: [{ field: "created_at", sort: "desc" }],
    firstShowRows: "intersected",
    numberFormat,
    lastRowTarget: "#chsi-groups-table-last-row",
    rowsTarget: "#chsi-groups-table-rows",
    getValuesUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/chsi-groups-get-values",
    getRowsUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/chsi-groups-get-rows",
    getSubtotalsUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/chsi-groups-get-subtotals",
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
        const $tr = $(`
            <tr>
                <td class="smart-table__always-shown align-middle text-center">
                    <button class="chsi-collapse-button btn btn-sm">
                        <i class="fa-solid fa-caret-up"></i>
                    </button>
                </td>
                <td>${row.project_region.name}</td>
                <td>${row.account.name}</td>
                <td>${numberFormat.format(row.sum)}</td>
                <td>${row.status.name}</td>
            </tr>
            <tr class="chsi-tr d-none">
                <td class="smart-table__always-shown" colspan="5">
                    <table class="table" id="chsi-${row.id}-table">
                        <thead class="table-light">
                            <tr>
                                <th scope="col">
                                    <label for="chsi-llc-input">ТОО</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-recipient-input">Получатель</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-iin-or-bin-input">ИИН/БИН</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-iik-input">ИИК</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-executive-inscription-input">Исполнительная надпись</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-retention-type-input">Вид удержания</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-collaborator-input">Сотрудник</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-iin-input">ИИН</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-actual-retention-rate-input">Фактическая ставка удержания</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-sum-input">Сумма</label>
                                </th>
                                <th scope="col">
                                    <label for="chsi-executive-order-receipt-date-input">Дата получения исполнительного</label>
                                </th>
                            </tr>
                        </thead>
                        <tbody class="chsi-table-rows">
                        </tbody>
                    </table>
                </td>
            </tr>
        `);
        const $chsiTr = $tr.closest(".chsi-tr");
        $tr.find(".chsi-collapse-button").on("click", function() {
            $chsiTr.toggleClass("d-none");
        });
        const $chsiRows = $chsiTr.find(".chsi-table-rows");
        for (const chsi of row.chsi_set) {
            $chsiRows.append(`
                <tr>
                    <td class="align-middle text-center">${chsi.llc}</td>
                    <td class="align-middle">${chsi.recipient}</td>
                    <td class="align-middle">${chsi.bin_or_iin}</td>
                    <td class="align-middle">${chsi.iik}</td>
                    <td class="align-middle">${chsi.executive_inscription}</td>
                    <td class="align-middle">${chsi.retention_type}</td>
                    <td class="align-middle">${chsi.collaborator}</td>
                    <td class="align-middle">${chsi.iin}</td>
                    <td class="align-middle text-center">${chsi.actual_retention_rate}</td>
                    <td class="align-middle text-end">${numberFormat.format(chsi.sum)}</td>
                    <td class="align-middle text-center">${new Date(chsi.executive_order_receipt_date).toLocaleDateString("ru-RU")}</td>
                </tr>
            `);
        }
        return $tr.add($chsiTr);
    },
  });
  const $raschetnyeTable = $("#raschetnye-table");
  $raschetnyeTable.smartTableWithVirtualScroll({
    name: "division-of-financial-planning-raschetnye-table",
    csrfToken,
    defaultOrder: [{ field: "created_at", sort: "desc" }],
    firstShowRows: "intersected",
    numberFormat,
    lastRowTarget: "#raschetnye-table-last-row",
    rowsTarget: "#raschetnye-table-rows",
    getValuesUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/raschetnye-get-values",
    getRowsUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/raschetnye-get-rows",
    getSubtotalsUrl:
      "/p1/finance-module/division-of-financial-planning/smart-tables/raschetnye-get-subtotals",
    loadingHtml: `
            <tr>
                <td class="text-center" colspan="9">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `,
    getTr(row) {
        return `
            <tr>
                <td class="text-center">${new Date(
                    row.created_at
                ).toLocaleDateString("ru-RU")}</td>
                <td>${row.project_region.name}</td>
                <td>${row.account.name}</td>
                <td>${row.name}</td>
                <td>${row.layoff_date}</td>
                <td class="text-end">${numberFormat.format(row.raschetnye_by_1c)}</td>
                <td class="text-end">${numberFormat.format(row.subreport)}</td>
                <td class="text-end">${numberFormat.format(row.percent_15)}</td>
                <td>${row.status.name}</td>
            </tr>
        `;
    },
  });
  $("#raschetnye-form").on("submit", async function (event) {
    event.preventDefault();
    accountsTable.canSelectAnyAccount({
      form: "raschetnye-form",
      required: true,
    });
    if (!this.checkValidity()) {
      this.reportValidity();
      return;
    }
    const response = await fetch(
      "/p1/finance-module/division-of-financial-planning/api/create-raschetnye",
      {
        method: "POST",
        body: new FormData(this),
        headers: {
          "X-CSRFToken": csrfToken,
        },
      }
    );
    const json = await response.json();
    this.reset();
    accountsTable.reload();
    $raschetnyeTable.smartTableReload();
  });

  $("#send-raschetnye-mail-button").on("click", async function() {
    const response = await fetch("/p1/finance-module/division-of-financial-planning/api/mail-raschetnye", {
      method: "POST",
      body: JSON.stringify({}),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      }
    });
    const json = await response.json();
  });
  const $transfersTable = $('#transfers-table');
  $transfersTable.smartTableWithVirtualScroll({
    name: 'division-of-financial-planning-transfers-table',
    defaultOrder: [{ field: 'datetime', sort: 'desc' }],
    lastRowTarget: '#transfers-table-last-row',
    firstShowRows: "intersected",
    rowsTarget: '#transfers-table-rows',
    getValuesUrl: '/p1/finance-module/division-of-financial-planning/smart-tables/transfers-get-values',
    getRowsUrl: '/p1/finance-module/division-of-financial-planning/smart-tables/transfers-get-rows',
    getSubtotalsUrl: '/p1/finance-module/division-of-financial-planning/smart-tables/transfers-get-subtotals',
    loadingHtml: `
        <tr>
          <td class="text-center text-primary" colspan="10">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </td>
        </tr>
      `,
    getTr(row) {
      const $tr = $(/*html*/`
        <tr class="border-black">
          <td class="align-middle text-center">${new Date(row.datetime).toLocaleDateString()}</td>
          <td class="align-middle">${row.responsible ? `${row.responsible.first_name} ${row.responsible.last_name}` : ""}</td>
          <td class="align-middle">${row.from_whom.name}</td>
          <td class="align-middle">${row.from_account.name}</td>
          <td class="align-middle">${row.from_account.number}</td>
          <td class="align-middle">${row.to_whom.name}</td>
          <td class="align-middle">${row.to_account.name}</td>
          <td class="align-middle">${row.to_account.number}</td>
          <td class="align-middle text-end">${numberFormat.format(row.sum)}</td>
          <td class="align-middle confirmation-td"></td>
        </tr>
      `);
      return $tr;
    }
  });
  const $transfersToWhomSelect = $("#transfers-to-whom-select");
  async function transfersUpdateProjectRegions() {
    $transfersToWhomSelect.prop("disabled", true);
    $transfersToWhomSelect.find(":not(:first-child)").remove();
    const response  = await fetch("/p1/finance-module/api/all-project-regions");
    const json = await response.json();
    for (const projectRegion of json.project_regions) {
      $transfersToWhomSelect.append(`
        <option value="${projectRegion.id}">
          ${projectRegion.name}
        </option>
      `);
    }
    $transfersToWhomSelect.prop("disabled", false);

  }
  $transfersToWhomSelect.on("change", async function() {
    const id = $(this).val();
    await transfersUpdateAccounts(id);
  });
  const $transfersToAccountSelect = $("#transfers-to-account-select");
  async function transfersUpdateAccounts(projectRegionId) {
    $transfersToAccountSelect.prop("disabled", true);

    $transfersToAccountSelect.find(":not(:first-child)").remove();
    const response = await fetch(`/p1/finance-module/api/project-region-accounts?project-region-id=${projectRegionId}`);
    const json = await response.json();
    for (const account of json.accounts) {
      $transfersToAccountSelect.append(`
        <option value="${account.id}">
          ${account.name}
        </option>
      `);
    }
    $transfersToAccountSelect.prop("disabled", false);

  }
  $("#transfers-form").on("submit", async function (event) {
    event.preventDefault();
    accountsTable.canSelectAnyAccount({
      form: "transfers-form",
      name: "from-account-id",
      projectRegionName: "from-whom-id",
      required: true,
    });
    if (!this.checkValidity()) {
      this.reportValidity();
      return;
    }
    const response = await fetch(
      "/p1/finance-module/division-of-financial-planning/api/create-transfers",
      {
        method: "POST",
        body: new FormData(this),
        headers: {
          "X-CSRFToken": csrfToken,
        },
      }
    );
    const json = await response.json();
    this.reset();
    accountsTable.reload();
    $transfersTable.smartTableReload();
  });
  transfersUpdateProjectRegions();
  await Promise.all([loadNameDateList(), accountsTable.reload()]);
});
