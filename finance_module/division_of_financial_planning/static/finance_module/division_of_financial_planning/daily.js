$(function () {
  const numberFormat = new Intl.NumberFormat("ru-RU", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  const $mandatoryPaymentSeizuresTable = $("#mandatory-payment-seizures-table");
  $mandatoryPaymentSeizuresTable.smartTableWithVirtualScroll({
    name: "daily-mandatory-payment-seizures-table",
    defaultOrder: [{ field: "datetime", sort: "desc" }],
    lastRowTarget: "#daily-mandatory-payment-seizures-last-row",
    rowsTarget: "#daily-mandatory-payment-seizures-rows",
    getValuesUrl:
      "/p1/finance-module/daily-mandatory-payment-seizure-get-values",
    getRowsUrl: "/p1/finance-module/daily-mandatory-payment-seizure-get-rows",
    getSubtotalsUrl:
      "/p1/finance-module/daily-mandatory-payment-seizure-get-subtotals",
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
      return `
            <tr>
              <td class="align-middle">${row.project_region.director_display
        }</td>
              <td class="align-middle">${row.project_region.project_manager_display}</td>
              <td class="align-middle">${row.project_region.name}</td>
              <td class="align-middle">${row.mandatory_payment ? row.mandatory_payment.name : ""
        }</td>
              <td class="align-middle">${row.account ? row.account.name : ""
        }</td>
              <td class="align-middle">${row.responsible
          ? `${row.responsible.first_name} ${row.responsible.last_name}`
          : ""
        }</td>
              <td class="text-end align-middle">${numberFormat.format(
          row.sum
        )}</td>
              <td class="align-middle">${new Date(
          row.datetime
        ).toLocaleDateString()}</td>
            </tr>
          `;
    },
  });
  const $dailyTable = $("#daily-table");
  const $dailyTableRows = $dailyTable.find("tbody");
  const $showSelect = $("#show-select");
  const $loadingTr = $(`
    <tr>
      <td class="text-center border-start border-black border-bottom" colspan="7">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </td>
    </tr>
  `);
  const $loading = $(`
    <div>
      <div class="spinner-border spinner-border-sm text-primary ms-1" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  `);
  const $dayChange = $("#day-change");
  let dayChangeDate = null;
  const $dayChangeDateInput = $("#day-change-date-input");
  const $dayChangePreviousDate = $("#day-change-previous-date");
  const $dayChangeCurrentDate = $("#day-change-current-date");
  const $dayChangeNextDate = $("#day-change-next-date");

  function dayChangeNextDate() {
    const nextDate = new Date(dayChangeDate);
    nextDate.setDate(nextDate.getDate() + 1);
    return nextDate;
  }
  function dayChangePreviousDate() {
    const previousDate = new Date(dayChangeDate);
    previousDate.setDate(previousDate.getDate() - 1);
    return previousDate;
  }
  function dayChangeFormatDate(date) {
    return date.toLocaleDateString("ru-RU", {
      month: "long",
      year: "numeric",
      day: "2-digit",
    });
  }

  $dailyTable.on("st.rows.displayed", function () {
    $(".need-disable").prop("disabled", false);
  });

  async function dayChangeNewDate(date) {
    $(".need-disable").prop("disabled", true);
    dayChangeDate = new Date(date);
    $dayChangePreviousDate.text(dayChangeFormatDate(dayChangePreviousDate()));
    $dayChangeCurrentDate.text(dayChangeFormatDate(dayChangeDate));
    date = new Date();
    $("#day-change-next-button").toggleClass(
      "disabled",
      dayChangeDate.getFullYear() == date.getFullYear() &&
      dayChangeDate.getFullYear() == date.getFullYear() &&
      dayChangeDate.getDate() == date.getDate()
    );

    $dayChangeNextDate.text(dayChangeFormatDate(dayChangeNextDate()));
    $dailyTable.smartTableReload();
    saveState();
  }

  $("#day-change-form").on("submit", async function (event) {
    event.preventDefault();
    await dayChangeNewDate(this.elements.date.value);
  });

  $("#day-change-previous-button").on("click", async function () {
    await dayChangeNewDate(dayChangePreviousDate());
  });
  $("#day-change-next-button").on("click", async function () {
    await dayChangeNewDate(dayChangeNextDate());
  });

  const $monthChange = $("#month-change");
  let monthChangeDate = null;
  const $monthChangePreviousDate = $("#month-change-previous-date");
  const $monthChangeCurrentDate = $("#month-change-current-date");
  const $monthChangeMonthInput = $("#month-change-month-input");
  const $monthChangeNextDate = $("#month-change-next-date");

  function monthChangePreviousDate() {
    const previousDate = new Date(monthChangeDate);
    previousDate.setMonth(previousDate.getMonth() - 1);
    return previousDate;
  }
  function monthChangeNextDate() {
    const nextDate = new Date(monthChangeDate);
    nextDate.setMonth(nextDate.getMonth() + 1);
    return nextDate;
  }
  function monthChangeFormatDate(date) {
    return date.toLocaleDateString("ru-RU", { year: "numeric", month: "long" });
  }
  async function monthChangeNewDate(date) {
    $(".need-disable").prop("disabled", true);
    monthChangeDate = new Date(date);
    $monthChangePreviousDate.text(
      monthChangeFormatDate(monthChangePreviousDate())
    );
    $monthChangeCurrentDate.text(monthChangeFormatDate(monthChangeDate));
    date = new Date();
    $("#month-change-next-button").toggleClass(
      "disabled",
      monthChangeDate.getFullYear() == date.getFullYear() &&
      monthChangeDate.getMonth() == date.getMonth()
    );
    $monthChangeNextDate.text(monthChangeFormatDate(monthChangeNextDate()));
    $dailyTable.smartTableReload();
    saveState();
  }

  $("#month-change-previous-button").on("click", async function () {
    await monthChangeNewDate(monthChangePreviousDate());
  });
  $("#month-change-next-button").on("click", async function () {
    await monthChangeNewDate(monthChangeNextDate());
  });

  $(`#month-change-form`).on("submit", function (event) {
    event.preventDefault();
    monthChangeNewDate(new Date(this.elements.month.value));
  });

  const $yearChange = $("#year-change");
  let yearChangeDate = null;
  const $yearChangePreviousDate = $("#year-change-previous-date");
  const $yearChangeCurrentDate = $("#year-change-current-date");
  const $yearChangeNextDate = $("#year-change-next-date");

  function yearChangePreviousDate() {
    const previousDate = new Date(yearChangeDate);
    previousDate.setFullYear(previousDate.getFullYear() - 1);
    return previousDate;
  }
  function yearChangeNextDate() {
    const nextDate = new Date(yearChangeDate);
    nextDate.setFullYear(nextDate.getFullYear() + 1);
    return nextDate;
  }
  function yearChangeFormatDate(date) {
    return date.toLocaleDateString("ru-RU", { year: "numeric" });
  }
  async function yearChangeNewDate(date) {
    $(".need-disable").prop("disabled", true);
    yearChangeDate = new Date(date);
    $yearChangePreviousDate.text(
      yearChangeFormatDate(yearChangePreviousDate())
    );
    $yearChangeCurrentDate.text(yearChangeFormatDate(yearChangeDate));
    $("#year-change-next-button").toggleClass(
      "disabled",
      yearChangeDate.getFullYear() == new Date().getFullYear()
    );
    $yearChangeNextDate.text(yearChangeFormatDate(yearChangeNextDate()));
    $dailyTable.smartTableReload();
    saveState();
  }

  $("#year-change-previous-button").on("click", async function () {
    await yearChangeNewDate(yearChangePreviousDate());
  });
  $("#year-change-next-button").on("click", async function () {
    await yearChangeNewDate(yearChangeNextDate());
  });

  $(`#year-change-form`).on("submit", function (event) {
    event.preventDefault();
    const date = new Date();
    date.setFullYear(this.elements.year.valueAsNumber);
    yearChangeNewDate(date);
  });
  const $periodChange = $("#period-change");
  let periodChangeStartDate = null;
  let periodChangeEndDate = null;
  const $periodChangeDateRange = $("#period-change-date-range");

  function periodChangeFormatDate(date) {
    return date.toLocaleDateString("ru-RU", {
      month: "long",
      year: "numeric",
      day: "2-digit",
    });
  }
  async function periodChangeNewDate(startDate, endDate) {
    $(".need-disable").prop("disabled", true);
    periodChangeStartDate = startDate ? new Date(startDate) : null;
    periodChangeEndDate = endDate ? new Date(endDate) : null;
    let dateRange = null;
    if (periodChangeStartDate && periodChangeEndDate) {
      dateRange = `C ${periodChangeFormatDate(
        periodChangeStartDate
      )} по ${periodChangeFormatDate(periodChangeEndDate)}`;
    } else if (periodChangeStartDate) {
      dateRange = `C ${periodChangeFormatDate(periodChangeStartDate)}`;
    } else if (periodChangeEndDate) {
      dateRange = `До ${periodChangeFormatDate(periodChangeEndDate)}`;
    } else {
      dateRange = "За всё время";
    }
    $periodChangeDateRange.text(dateRange);
    $dailyTable.smartTableReload();
    saveState();
  }
  $(`#period-change-form`).on("submit", function (event) {
    event.preventDefault();
    periodChangeNewDate(
      this.elements["start-date"].value,
      this.elements["end-date"].value
    );
  });
  function getQueryParams() {
    switch ($showSelect.val()) {
      case "per-day":
        return `date=${dayChangeDate.toISOString().slice(0, 10)}`;
      case "per-month":
        return `month=${monthChangeDate.toISOString().slice(0, 7)}`;
      case "per-year":
        return `year=${yearChangeDate.getFullYear()}`;
      case "during-period":
        if (periodChangeStartDate && periodChangeEndDate) {
          return `start-date=${periodChangeStartDate
            .toISOString()
            .slice(0, 10)}&end-date=${periodChangeEndDate
              .toISOString()
              .slice(0, 10)}`;
        } else if (periodChangeStartDate) {
          return `start-date=${periodChangeStartDate
            .toISOString()
            .slice(0, 10)}`;
        } else if (periodChangeEndDate) {
          return `end-date=${periodChangeEndDate.toISOString().slice(0, 10)}`;
        } else {
          return "";
        }
    }
  }
  function getSearch() {
    const queryParams = getQueryParams();
    return `?show=${$showSelect.val()}${queryParams ? `&${queryParams}` : ""}`;
  }
  function saveState() {
    console.log("State saving");
    const search = getSearch();
    history.pushState({}, "", search);
    console.log("Search: ", search);
    console.log("State saved");
  }
  async function copyLink() {
    try {
      await navigator.clipboard.writeText(location.href);
      console.log("Link copied");
      return true;
    } catch (error) {
      console.error(error);
      console.log("Link copying error");
      return false;
    }
  }
  $(document).on("click", ".copy-link-button", async function () {
    $(this).prop("disabled", true);
    const successCopy = await copyLink();
    const defaultHtml = $(this).html();
    $(this).html(`
      <div class="d-flex align-items-center gap-2">
        <div>
          ${defaultHtml}
        </div>
        <div class="text-nowrap">
          ${successCopy ? `<span class="text-success">Скопировано</span>` : `<span class="text-danger">Ошибка при копирование, см. консоль</span>`}
        </div>
      </div>
    `);
    setTimeout(() => {
      $(this).html(defaultHtml);
      $(this).prop("disabled", false);
    }, 700);
  });
  $(document).on("click", ".unload-button", async function () {
    const defaultHtml = $(this).html();
    const defaultTitle = $(this).prop("title");
    $(this).prop("title", "Идёт выгрузка таблицы в xlsx...");
    const $icon = $(this).find(".fa-solid");
    $icon.addClass("fa-fade");
    $(".need-disable").prop("disabled", true);
    try {
      const search = getSearch();
      const response = await fetch(`/p1/finance-module/division-of-financial-planning/api/unload-daily-table${search}`);
      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      const a = $(`<a href="${objectUrl}" download="Ежедневно.xlsx"></a>`).appendTo(document.body)[0];
      a.click();
      a.remove();
    } catch (error) {
      console.log(error);
    }
    $(".need-disable").prop("disabled", false);
    $(this).html(defaultHtml);
    $(this).prop("title", defaultTitle);
  });
  let defaultDayDate = null;
  let defaultMonthDate = null;
  let defaultYearDate = null;
  let defaultPeriodDate = null;
  let $addNewDailyRowButton = null;
  function whatShow() {
    $dayChange.addClass("d-none");
    $monthChange.addClass("d-none");
    $yearChange.addClass("d-none");
    $periodChange.addClass("d-none");
    $addNewDailyRowButton?.addClass("d-none");
    $(".comment-th").addClass("d-none");
    switch ($showSelect.val()) {
      case "per-day":
        $dayChangeDateInput.prop("max", new Date().toISOString().slice(0, 10));
        dayChangeNewDate(defaultDayDate || new Date());
        $dayChange.removeClass("d-none");
        $addNewDailyRowButton?.removeClass("d-none");
        $(".comment-th").removeClass("d-none");
        break;
      case "per-month":
        $monthChangeMonthInput.prop(
          "max",
          new Date().toISOString().slice(0, 7)
        );
        monthChangeNewDate(defaultMonthDate || new Date());
        $monthChange.removeClass("d-none");
        break;
      case "per-year":
        yearChangeNewDate(defaultYearDate || new Date());
        $yearChange.removeClass("d-none");
        break;
      case "during-period":
        const [startDate, endDate] = defaultPeriodDate || [null, null];
        periodChangeNewDate(startDate, endDate);
        $periodChange.removeClass("d-none");
        break;
    }
  }
  function loadState() {
    console.log("State loading");
    const urlSearchParams = new URLSearchParams(location.search);
    const show = urlSearchParams.get("show");
    if (show) {
      console.log("Show: ", show);
      $showSelect.val(show);
    }
    const date = urlSearchParams.get("date");
    if (date) {
      defaultDayDate = new Date(date);
      console.log("Day: ", defaultDayDate);
    }
    const month = urlSearchParams.get("month");
    if (month) {
      defaultMonthDate = new Date(month);
      console.log("Month: ", defaultMonthDate);
    }
    const year = urlSearchParams.get("year");
    if (year) {
      defaultYearDate = new Date(year);
      console.log("Year: ", defaultYearDate);
    }
    let startDate = urlSearchParams.get("start-date");
    startDate = startDate ? new Date(startDate) : null;
    if (startDate) {
      console.log("Start date: ", startDate)
    }
    let endDate = urlSearchParams.get("end-date");
    endDate = endDate ? new Date(endDate) : null;
    if (endDate) {
      console.log("End date: ", endDate);
    }
    defaultPeriodDate = [startDate, endDate];
    console.log("State loaded");
  }

  $(window).on("popstate", function (event) {
    console.log(event);
    loadState();
    whatShow();
  });
  loadState();
  whatShow();
  $showSelect.on("change", function () {
    whatShow();
  });

  let rows = null;
  let filteredAndOrderedRows = null;

  async function saveValue(
    event,
    field,
    type,
    rows,
    options = {
      calculateOutgoingBalance: false,
      min: 0,
      calculateTotalDebt: false,
      calculateRemainder: false
    }
  ) {
    if (options.tableName === "Ежедневно" && $showSelect.val() !== "per-day") return;
    let value = $(event.target).val();
    if (type === "number") {
      value = parseFloat(value) || 0;
      if (options.min != null) {
        value = Math.max(value, options.min);
      }
    }
    if (event.type === "change") {
      $(event.target).val(value);
      const $tr = $(event.target).closest("tr");
      const id = $tr.data("id");
      $(event.target).prop("disabled", true);
      $(event.target).after($loading);
      try {
        const response = await fetch(
          `/p1/finance-module/division-of-financial-planning/api/tables/${options.tableName
          }${options.tableName === "Ежедневно" ? `/${dayChangeDate.toISOString().slice(0, 10)}` : ""}/rows/${id}/cells`,
          {
            method: "POST",
            body: JSON.stringify({
              field,
              type,
              value,
            }),
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
          }
        );
        $loading.remove();
        if (response.ok) {
          const json = await response.json();
          $(event.target).addClass("is-valid");
        } else {
          $(event.target).addClass("is-invalid");
        }
        const row = rows.find((row) => row.id == id);
        row[field] = value;
        if (type === "number") {
          if (options.calculateOutgoingBalance) {
            const parish = row["parish"];
            const incomingBalance = row["incoming_balance"];
            const outgoingBalance = incomingBalance + parish - row["expense"];
            $tr
              .find(".outgoing-balance-td")
              .html(numberFormat.format(outgoingBalance));
            row["outgoing_balance"] = outgoingBalance;
          }
          if (options.calculateTotalDebt) {
            const totalDebt =
              Math.max(row["previous_debts"] + row["debt"] - row["expense"], 0);
            $tr.find(".debt-td").html(numberFormat.format(totalDebt));
            row["total_debt"] = totalDebt;
          }
          if (options.calculateRemainder) {
            const remainder = row["remainder"] - row["mandatory_payment_seizures_sum"];
            $tr.find(".remainder-td").html(numberFormat.format(remainder));
          }
        }
      } catch (error) {
        console.error(error);
        $loading.remove();
        $(event.target).addClass("is-invalid");
      }
      setTimeout(() => {
        $(event.target).removeClass("is-valid");
        $(event.target).removeClass("is-invalid");
        $(event.target).prop("disabled", false);
        $(event.target).trigger("value-saved");
      }, 700);
    } else {
      $(event.target).val(value);
    }
    $dailyTable.smartTableUpdateSubtotals();
  }

  $dailyTable.on("change input", ".expense-input", async function (event) {
    await saveValue(event, "expense", "number", rows, {
      tableName: "Ежедневно",
      calculateOutgoingBalance: true,
      calculateTotalDebt: true,
    });
  });
  $dailyTable.on("change input", ".debt-input", async function (event) {
    await saveValue(event, "debt", "number", rows, {
      tableName: "Ежедневно",
      calculateTotalDebt: true,
    });
  });
  $dailyTable.on(
    "change input",
    ".incoming-balance-input",
    async function (event) {
      await saveValue(event, "incoming_balance", "number", rows, {
        tableName: "Ежедневно",
        calculateOutgoingBalance: true,
      });
    }
  );
  $dailyTable.on("change input", ".parish-input", async function (event) {
    await saveValue(event, "parish", "number", rows, {
      tableName: "Ежедневно",
      calculateOutgoingBalance: true,
      min: null,
      changeInputVal: false,
    });
  });
  $dailyTable.on("change input", ".comment-textarea", async function (event) {
    await saveValue(event, "comment", "string", rows, {
      tableName: "Ежедневно",
    });
  });
  function addNewDailyRow() {
    if ($showSelect.val() !== "per-day") return;
    const $tr = $(`
      <tr class="daily-row">
        <th class="border-start border-bottom sticky-relative sticky-relative-left border-black border-end table-light align-middle name-td text-truncate" scope="row" style="position: sticky; left: 0;">
          <form id="add-new-row-form">
            <input type="text" class="form-control" id="add-new-row-name-input" placeholder="Введите имя" required/>
          </form>
        </th>
        <td class="incoming-balance-td border-bottom border-black align-middle text-end">
          <div class="d-flex align-items-center">
            <input class="incoming-balance-input form-control" type="number" name="" id="" value="0" min="0" step="0.01" />
          </div>
        </td>
        <td class="border-start border-bottom parish-td border-black align-middle text-end">
          <div class="d-flex align-items-center">
            <input class="parish-input form-control" type="number" name="" id="" value="0" min="0" step="0.01" />
          </div>
        </td>
        <td class="border-start border-bottom border-black align-middle expense-td text-end">
          <div class="d-flex align-items-center">
            <input class="expense-input form-control" type="number" name="" id="" value="0" min="0" step="0.01" />
          </div>
        </td>
        <td class="border-start border-bottom border-black align-middle text-end outgoing-balance-td">
          ${numberFormat.format(0)}
        </td>
        <td class="border-start border-bottom border-black align-middle debt-td text-end">
          ${numberFormat.format(0)}
        </td>
        <td class="align-middle comment-td border-black border-start border-bottom text-end">
          <textarea class="form-control comment-textarea" rows="1"></textarea>
        </td>
      </tr>
    `);
    const $nameInput = $tr.find("#add-new-row-name-input");
    function onBlur() {
      $tr.remove();
    }
    $nameInput.on("blur", onBlur);
    $nameInput.on("input", function () {
      this.setCustomValidity("");
    });
    $tr.on("submit", "#add-new-row-form", function (event) {
      event.preventDefault();
      $nameInput.off("blur", onBlur);
      const name = $nameInput.val();
      $nameInput.prop("disabled", true);
      if ($(`tr[data-name="${name}"]`, $dailyTableRows).length !== 0) {
        $nameInput.addClass("is-invalid");
      } else {
        $nameInput.addClass("is-valid");
      }
      setTimeout(async () => {
        if ($nameInput.hasClass("is-valid")) {
          try {
            const response = await fetch(
              `/p1/finance-module/division-of-financial-planning/api/tables/Ежедневно/${dayChangeDate
                .toISOString()
                .slice(0, 10)}/rows`,
              {
                method: "POST",
                body: JSON.stringify({
                  name: name,
                }),
                headers: {
                  "X-CSRFToken": csrfToken,
                  "Content-Type": "application/json",
                },
              }
            );
            if (response.ok) {
              const json = await response.json();
              const row = {
                id: json.id,
                name,
                parish: 0,
                expense: 0,
                comment: null,
                previous_debts: 0,
                debt: 0,
                outgoing_balance: 0,
                incoming_balance: 0,
              };

              rows.push(row);
              $tr.attr("data-id", json.id);
              $tr.find(".name-td").html(`
                <div class="d-flex align-items-center justify-content-between gap-2">
                  <div class="flex-fill name-container">
                    ${name}
                  </div>
                  <div>
                    <button type="button" class="btn btn-sm btn-outline-danger delete-daily-row-button" style="text-align: right">
                      <i class="fa-solid fa-trash"></i>
                    </button>
                  </div>
                </div>
              `);
              if ($showSelect.val() === "per-day") {
                row.comment = null;
              }
              $dailyTable.smartTableUpdateSubtotals();
              return;
            }
            console.log(response);
          } catch (error) {
            console.error(error);
          }
          $nameInput.removeClass("is-valid");
          $nameInput.addClass("is-invalid");
          setTimeout(() => {
            $nameInput.removeClass("is-invalid");
            $nameInput.prop("disabled", false);
            $nameInput
              .get(0)
              .setCustomValidity(
                `Ошибка при добавлений строки: "${name}", см. консоль`
              );
            $nameInput.get(0).reportValidity();
            $nameInput.focus();
            $nameInput.on("blur", onBlur);
          }, 500);
        } else {
          $nameInput.removeClass("is-invalid");
          $nameInput.prop("disabled", false);
          $nameInput
            .get(0)
            .setCustomValidity(`Такое имя уже существует: "${name}"`);
          $nameInput.get(0).reportValidity();
          $nameInput.focus();
          $nameInput.on("blur", onBlur);
        }
      }, 700);
    });
    $dailyTableRows.append($tr);
    $nameInput.focus();
  }
  $dailyTable.on("dblclick", ".debt-td", async function () {
    const $tr = $(this).closest("tr");
    const id = $tr.data("id");
    const row = rows.find((row) => row.id == id);
    const debt = row.debt;
    $(this).html(`
      <div class="d-flex align-items-center">
        <input class="debt-input form-control" type="number" name="" id="" value="${row.debt}" min="0" step="0.01" />
      </div>
    `);
    const $debtInput = $(this).find(".debt-input");
    $debtInput.focus();
    await new Promise((resolve, reject) => {
      function x(event) {
        if (event.type === "blur" && debt != $debtInput.val()) {
          return;
        }
        resolve();
        $debtInput.off("blur value-saved", x);
      }
      $debtInput.on("blur value-saved", x);
    });
    $(this).html(`
      ${numberFormat.format(row.total_debt || 0)}
    `);
  });
  $dailyTable.on("click", ".delete-daily-row-button", async function () {
    if ($showSelect.val() !== "per-day") {
      return;
    }
    const $tr = $(this).closest("tr");
    const id = $tr.data("id");
    const row = rows.find(row => row.id == id);
    const date = dayChangeDate.toISOString().slice(0, 10);
    const $modal = $(`
      <div class="modal fade" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-body">
              <h5 class="modal-title">Вы точно хотите удалить строку "${row.name}"?</h5>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-link" data-bs-dismiss="modal">Отмена</button>
              <button type="button" class="btn btn-danger submit-delete-button">Удалить</button>
            </div>
          </div>
        </div>
      </div>
    `);
    $modal.on("hidden.bs.modal", function () {
      $modal.remove();
    });
    $modal.modal("show");
    $modal.on("click", ".submit-delete-button", async function () {
      try {
        const response = await fetch(
          `/p1/finance-module/division-of-financial-planning/api/tables/Ежедневно/${date}/rows/${id}`,
          {
            method: "DELETE",
            headers: {
              "X-CSRFToken": csrfToken,
              "Content-Type": "application/json",
            },
          }
        );
        const json = await response.json();
        if (response.ok) {
          rows = rows.filter((row) => row.id != id);
          $tr.remove();
          $dailyTable.smartTableUpdateSubtotals();
          $modal.modal("hide");
          return;
        }
        console.error(json.detail);
      } catch (error) {
        console.error(error);
      }
    });
  });

  $dailyTable.on("dblclick", ".name-container", async function() {
    const $tr = $(this).closest("tr");
    const id = $tr.data("id");
    const row = rows.find(row => row.id == id);
    const $nameContainer = $(this);

    $(this).html(`
      <form id="name-change-form">
        <input id="name-input" type="text" class="form-control" value="${row.name}" required/>
      </form>
    `);
    const $nameInput = $(this).find("#name-input");
    const $nameChangeForm = $(this).find("#name-change-form");
    $nameInput.focus();
    $nameInput.on("blur", function() {
      $nameContainer.html(row.name);
    });
    $nameChangeForm.on("submit", async function(event) {
      event.preventDefault();
      row.name = $nameInput.val();
      const response = await fetch(
        `/p1/finance-module/division-of-financial-planning/api/tables/Ежедневно/rows/${id}`,
        {
          method: "PATCH",
          body: JSON.stringify({
            name: row.name,
          }),
          headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
          },
        }
      );
      const json = await response.json();
      $nameContainer.html(row.name);
    });
    console.log(row);
  });

  $dailyTable.smartTable({
    name: "daily-table",
    async getValues(field, fieldType, fieldValuesList) {
      return smartTableGetValues(rows, field, fieldType, fieldValuesList);
    },
    async getSubtotals(fieldValuesList, fieldType, fieldSubtotal) {
      return smartTableGetSubtotals(
        rows,
        fieldValuesList,
        fieldType,
        fieldSubtotal
      );
    },
    async addTools($tools) {
      $addNewDailyRowButton = $(`
        <button id="add-new-daily-row-button" type="button" class="btn btn-sm" title="Добавить новую строку">
          <i class="fa-solid fa-plus"></i>
        </button>
      `);
      $addNewDailyRowButton.on("click", addNewDailyRow);
      $tools.append($addNewDailyRowButton);
      console.log($tools);
    },
    async showRows(fieldValuesList, fieldType, order, forceReload = false) {
      $dailyTableRows.empty();
      $dailyTableRows.append($loadingTr);
      if (!rows || forceReload) {
        const search = getSearch();
        const response = await fetch(
          `/p1/finance-module/division-of-financial-planning/api/daily-table${search}`
        );
        history.pushState(null, "", search);
        const json = await response.json();
        rows = json.rows.map((row) => {
          row["outgoing_balance"] =
            row["incoming_balance"] + row["parish"] - row["expense"];
          if (row["total_debt"] == null) {
            row["total_debt"] = Math.max(row["previous_debts"] + row["debt"] - row["expense"], 0);
          }
          return row;
        });
      } else {
        await new Promise((resolve, reject) => {
          setTimeout(resolve, 500);
        });
      }
      $dailyTableRows.empty();
      filteredAndOrderedRows = smartTableGetRows(
        rows,
        fieldValuesList,
        fieldType,
        order
      );
      let index = 0;
      for (const row of filteredAndOrderedRows) {
        const $tr = $(`
          <tr class="daily-row" data-id="${row.id}">
            <th class="table-light align-middle border-black sticky-relative sticky-relative-left border-start border-end border-bottom name-td text-truncate" scope="row" style="position: sticky; left: 0;">
              <div class="d-flex align-items-center justify-content-between gap-2">
                <div class="flex-fill name-container">
                  ${row.name}
                </div>
                  <button type="button" class="btn btn-sm btn-outline-danger delete-daily-row-button" style="text-align: right">
                    <i class="fa-solid fa-trash"></i>
                  </button>
              </div>
            </th>
            <td class="align-middle incoming-balance-td text-end border-black border-bottom">
              ${numberFormat.format(row.incoming_balance)}
            </td>
            <td class="align-middle parish-td text-end border-black border-start border-bottom">
              ${numberFormat.format(row.parish)}
            </td>
            <td class="align-middle expense-td text-end border-black border-start border-bottom">
              ${numberFormat.format(row.expense)}
            </td>
            <td class="align-middle text-end outgoing-balance-td border-black border-start border-bottom">
              ${numberFormat.format(row.outgoing_balance)}
            </td>
            <td class="align-middle debt-td border-black border-start border-bottom text-end">
              ${numberFormat.format(row.total_debt || 0)}
            </td>
            
          </tr>
        `);
        const $expenseTd = $tr.find(".expense-td");
        const $parishTd = $tr.find(".parish-td");
        const $incomingBalanceTd = $tr.find(".incoming-balance-td");
        const $nameTd = $tr.find(".name-td");
        const $debtTd = $tr.find(".debt-td");
        $dailyTableRows.append($tr);
        if ($showSelect.val() == "per-day") {
          $tr.append(`
            <td class="align-middle comment-td border-black border-start border-bottom text-end">
              <div class="d-flex align-items-center gap-2">
                <textarea class="form-control comment-textarea" rows="1"></textarea>
              </div>
            </td>
          `);
          const $commentTd = $tr.find(".comment-td");
          const $commentTextarea = $tr.find(".comment-textarea");
          $commentTextarea.val(row.comment);
          $expenseTd.html(`
            <div class="d-flex align-items-center">
              <input class="expense-input form-control" type="number" name="" id="" value="${row.expense}" min="0" step="0.01" />
            </div>
          `);
          let nameContainer = ".name-td";
          if (row.user_added) {
            nameContainer = ".name-container";
            $parishTd.html(`
              <div class="d-flex align-items-center">
                <input class="parish-input form-control" type="number" name="" id="" value="${row.parish}" min="0" step="0.01" />
              </div>
            `);
            if (
              new Date(row.created_date).toDateString() ===
              dayChangeDate.toDateString()
            ) {
              $incomingBalanceTd.html(`
                <div class="d-flex align-items-center">
                  <input class="incoming-balance-input form-control" type="number" name="" id="" value="${row.incoming_balance}" min="0" step="0.01" />
                </div>
              `);
            }
          }
          if (row.subrows && row.subrows.length !== 0) {
            $tr.find(nameContainer).html(function (_, html) {
              return `
                <div class="d-flex align-items-center w-100">
                  <button class="btn btn-sm subrows-collapse-button me-2" data-target=".subrows-${index}">
                    <i class="fa-solid fa-circle-chevron-up"></i>
                  </button>

                    ${html}
                   
                </div>
              `;
            });
            for (const subrow of row.subrows) {
              $dailyTableRows.append(`
                <tr class="d-none subrows-${index}">
                  <th class="align-middle sticky-relative sticky-relative-left border-start border-bottom border-black border-end text-secondary table-secondary" style="position: sticky; left: 0;"><div class="ms-5">${subrow.name}</div></th>
                  <td class="align-middle border-bottom border-black"></td>
                  <td class="text-end align-middle border-start border-bottom border-black">${numberFormat.format(subrow.parish)}</td>
                  <td class="border-start border-bottom border-black"></td>
                  <td class="border-start border-bottom border-black"></td>
                  <td class="border-start border-bottom border-black"></td>
                  <td class="border-start border-bottom border-black"></td>
                </tr>  
              `);
            }
          }
        }
        index++;
      }
    },
  });
  $dailyTable.on("click", ".subrows-collapse-button", function () {
    $(this).find(".fa-solid").toggleClass("fa-rotate-180");
    $($(this).data("target")).toggleClass("d-none");
  });

  const $accountsTable = $("#accounts-table");
  const $accountsTableRows = $("#accounts-table-rows");
  let accounts = null;
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
    yield [keyValue, group];
  }
  function addNewAccountRow() {
    const $tr = $(`
      <tr>
        <td class="name-td align-middle" colspan="2">
          <form id="add-new-account-row-form">
            <input type="text" placeholder="Введите имя" class="form-control add-new-account-row-name-input" required/>
          </form>
        </td>
        <td>
          <div class="d-flex align-items-center gap-2">
            <input type="number" min="0" class="form-control account-remainder-input" placeholder="" step="0.01"/>
          </div>
        </td>
        <td class="remainder-td text-end align-middle">
          ${numberFormat.format(0)}
        </td>
      </tr>
    `);
    const $nameInput = $tr.find(".add-new-account-row-name-input");
    const $form = $tr.find("#add-new-account-row-form");
    $nameInput.on("input", function () {
      this.setCustomValidity("");
    });
    $form.on("submit", function (event) {
      event.preventDefault();
      const name = $nameInput.val();
      $nameInput.off("blur", onBlur);

      $nameInput.prop("disabled", true);
      if ($accountsTableRows.find(`tr[data-name="${name}"]`).length === 0) {
        $nameInput.addClass("is-valid");
      } else {
        $nameInput.addClass("is-invalid");
      }
      setTimeout(async () => {
        async function reportError(error, wait) {
          if (wait) {
            await new Promise((resolve, reject) => {
              setTimeout(resolve, 500);
            });
          }
          $nameInput.prop("disabled", false);
          $nameInput.focus();
          $nameInput[0].setCustomValidity(error);
          $nameInput[0].reportValidity();
          $nameInput.on("blur", onBlur);
          $nameInput.removeClass("is-invalid");
        }
        if ($nameInput.hasClass("is-valid")) {
          try {
            const response = await fetch(
              "/p1/finance-module/division-of-financial-planning/api/tables/Расчётные счета/rows",
              {
                method: "POST",
                body: JSON.stringify({
                  name,
                }),
                headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": csrfToken,
                },
              }
            );
            const json = await response.json();
            if (response.ok) {
              $tr.attr("data-name", name);
              $tr.attr("data-id", json.id);
              $tr
                .find(".name-td")
                .html(
                  `<div class="d-flex align-items-center justify-content-between"><div>${name}</div><div><button type="button" class="btn btn-sm btn-outline-danger delete-account-row-button"><i class="fa-solid fa-trash"></i></button></div></div>`
                );
            } else {
              console.error(json.detail);
              $nameInput.removeClass("is-valid");
              $nameInput.addClass("is-invalid");
              reportError(
                "Ошибка при добавлений новой строки. См. консоль",
                true
              );
            }
          } catch (error) {
            console.error(error);
            $nameInput.removeClass("is-valid");
            $nameInput.addClass("is-invalid");
            reportError(
              "Ошибка при добавлений новой строки. См. консоль, возможно вы не подключены к интернету",
              true
            );
          }
        } else {
          reportError(`Имя "${name}" уже существует`);
        }
      }, 700);
    });

    $accountsTableRows.append($tr);
    $nameInput.focus();
    function onBlur() {
      $tr.remove();
    }
    $nameInput.on("blur", onBlur);
  }
  $accountsTable.smartTable({
    name: "division-of-financial-planning-daily-accounts-table",
    defaultOrder: [{ sort: "desc", field: "subdivision" }],
    async getValues(field, fieldType, fieldValuesList) {
      let values = smartTableGetValues(
        accounts == null ? [] : accounts,
        field,
        fieldType,
        fieldValuesList
      );
      return values;
    },
    async addTools($tools) {
      const $addNewAccountRowButton = $(`
        <button type="button" class="btn btn-sm" id="add-new-account-row-button" title="Добавить новую строку">
          <i class="fa-solid fa-plus"></i> 
        </button>
      `);
      $addNewAccountRowButton.on("click", addNewAccountRow);
      $tools.append($addNewAccountRowButton);
      console.log($tools);
    },
    async showRows(fieldValuesList, fieldType, order, forceReload = false) {
      $accountsTableRows.html(`
        <tr>
          <td colspan="5" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </td>
        </tr>
      `);

      if (forceReload) {
        try {
          const response = await fetch(
            "/p1/finance-module/division-of-financial-planning/api/accounts-table"
          );
          const json = await response.json();
          accounts = json.rows;
        } catch (error) {
          accounts = null;
          console.error(error);
        }
      }
      if (accounts && accounts.length !== 0) {
        $accountsTableRows.empty();
        let filteredAndOrderedAccounts = smartTableGetRows(
          accounts,
          fieldValuesList,
          fieldType,
          order
        );
        filteredAndOrderedAccounts = filteredAndOrderedAccounts.sort((a, b) => {
          if (a.is_cash_register && b.is_cash_register) {
            return b.name.localeCompare(a.name);
          } else if (a.is_cash_register) {
            return 1;
          } else if (b.is_cash_register) {
            return -1;
          }
          return 0;
        });
        for (const [key, group] of groupby(
          filteredAndOrderedAccounts,
          (x) => x.subdivision
        )) {
          let keyAdded = false;
          for (const account of group) {
            const $tr = $(`
              <tr data-id="${account.id}">
                <td class="name-td align-middle" ${key === undefined ? ` colspan="2"` : ``
              }>
                  ${account.name}  
                </td>
                <td class="text-end mandatory-payment-seizures-sum-td align-middle">
                  ${numberFormat.format(account.mandatory_payment_seizures_sum)}
                </td>
                <td class="remainder-td text-end align-middle">
                  ${numberFormat.format(
                account.remainder - account.mandatory_payment_seizures_sum
              )}
                </td>
              </tr>
            `);
            if (!keyAdded) {
              $tr.prepend(`
                <th scope="row" class="align-middle text-center border-black table-light" rowspan="${group.length
                }">
                  ${key || "-"}
                </th>
              `);
              keyAdded = true;
            }
            const $remainderTd = $tr.find(".remainder-td");
            const $mandatoryPaymentSeizuresSumTd = $tr.find(
              ".mandatory-payment-seizures-sum-td"
            );
            if (account.is_cash_register || account.user_added) {
              $mandatoryPaymentSeizuresSumTd.html(`
                <div class="d-flex align-items-center">
                  <input class="mandatory-payment-seizures-sum-input form-control" type="number" name="" id="" value="${account.mandatory_payment_seizures_sum}" min="0" step="0.01" />
                </div>
              `);
            }
            $accountsTableRows.append($tr);
          }
        }
      } else {
        $accountsTableRows.html(`
          <tr>
            <td colspan="5" class="text-center">
              Ничего не найдено
            </td>
          </tr>
        `);
      }
    },
  });
  $accountsTable.on("dblclick", ".remainder-td", async function () {
    const $tr = $(this).closest("tr");
    const id = $tr.data("id");
    const row = accounts.find((row) => row.id == id);
    if (!row.editable) {
      return;
    }
    const remainder = row.remainder;
    $(this).html(`
      <div class="d-flex align-items-center">
        <input class="remainder-input form-control" type="number" name="" id="" value="${remainder}" min="0" step="0.01" />
      </div>
    `);
    const $remainderInput = $(this).find(".remainder-input");
    $remainderInput.focus();
    await new Promise((resolve, reject) => {
      function x(event) {
        if (event.type === "blur" && remainder != $remainderInput.val()) {
          return;
        }
        resolve();
        $remainderInput.off("blur value-saved", x);
      }
      $remainderInput.on("blur value-saved", x);
    });
    $(this).html(`
      ${numberFormat.format(row.remainder - row.mandatory_payment_seizures_sum)}
    `);
  });
  $accountsTable.on("change input", ".remainder-input", async function (event) {
    await saveValue(event, "remainder", "number", accounts, {
      tableName: "Расчётные счета",
    });
  });
  $accountsTable.on("change input", ".reserve-input", async function (event) {
    await saveValue(event, "reserve", "number", accounts, {
      tableName: "Расчётные счета",
    });
  });
  $accountsTable.on(
    "change input",
    ".mandatory-payment-seizures-sum-input",
    async function (event) {
      await saveValue(
        event,
        "mandatory_payment_seizures_sum",
        "number",
        accounts,
        { tableName: "Расчётные счета", calculateRemainder: true }
      );
    }
  );
  $accountsTableRows.on("click", ".delete-account-row-button", function () {
    const $tr = $(this).closest("tr");
    const id = $tr.data("id");
    const row = accounts.find(account => account.id == id);
    const $modal = $(`
      <div class="modal fade" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-body">
              <h5 class="modal-title">Вы точно хотите удалить строку "${row.name}"?</h5>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-link" data-bs-dismiss="modal">Отмена</button>
              <button type="button" class="btn btn-danger submit-delete-button">Удалить</button>
            </div>
          </div>
        </div>
      </div>
    `);
    $modal.on("hidden.bs.modal", function () {
      $modal.remove();
    });
    $modal.modal("show");
    $modal.on("click", ".submit-delete-button", async function () {
      try {
        const response = await fetch(
          `/p1/finance-module/division-of-financial-planning/api/tables/Расчётные счета/rows/${id}`,
          {
            method: "DELETE",
            headers: {
              "X-CSRFToken": csrfToken,
            },
          }
        );
        const json = await response.json();
        if (response.ok) {
          accounts = accounts.filter((account) => account.id != id);
          $tr.remove();
          $accountsTable.smartTableUpdateSubtotals();
          $modal.modal("hide");
          return;
        }
        console.error(json.detail);
      } catch (error) {
        console.error(error);
      }
    });
  });

  const $projectRegionsTable = $("#project-regions-table");
  const $projectRegionsTableRows = $("#project-regions-table-rows");
  let projectRegions = null;
  $projectRegionsTable.smartTable({
    name: "division-of-financial-planning-daily-project-regions-table",
    defaultOrder: [{ sort: "asc", field: "director" }],
    async getValues(field, fieldType, fieldValuesList) {
      return smartTableGetValues(
        projectRegions || [],
        field,
        fieldType,
        fieldValuesList
      );
    },
    
    async showRows(fieldValuesList, fieldType, order, forceReload = false) {
      $projectRegionsTableRows.html(`
        <tr>
          <td colspan="5" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </td>
        </tr>
      `);
      if (forceReload) {
        projectRegions = null;
        try {
          const response = await fetch(
            "/p1/finance-module/division-of-financial-planning/api/project-regions"
          );
          const json = await response.json();
          if (response.ok) {
            projectRegions = json.projectRegions;
          } else {
            console.error(json.detail);
          }
        } catch (error) {
          console.error(error);
        }
      }
      if (projectRegions && projectRegions.length !== 0) {
        const filteredAndOrderedProjectRegions = smartTableGetRows(
          projectRegions,
          fieldValuesList,
          fieldType,
          order
        );
        if (filteredAndOrderedProjectRegions.length === 0) {
          $projectRegionsTableRows.html(`
            <tr>
              <td colspan="5" class="text-center">
                Ничего не найдено
              </td>
            </tr>
          `);
          return;
        }
        $projectRegionsTableRows.empty();
        let index = 0;
        for (const [director, directorProjectRegions] of groupby(filteredAndOrderedProjectRegions, projectRegion => projectRegion.director)) {
          let directorAdded = false;
          for (const projectRegion of directorProjectRegions) {
            const $tr = $(`
              <tr data-name="${projectRegion.name}">
                <td class="align-middle">
                  ${projectRegion.projectManager}
                </td>
                <td class="align-middle">
                  ${projectRegion.name}
                </td>
                <td class="align-middle text-end">
                  <div class="d-flex align-items-center justify-content-between">
                    <div>
                      <button type="button" class="btn btn-sm rounded-circle show-project-region-mandatory-payments-seizures-table-modal" title="Показать погашений" data-bs-toggle="modal" data-bs-target="#project-region-mandatory-payment-seizures-table-modal">
                        <i class="fa-regular fa-eye"></i>
                      </button>
                    </div>
                    ${numberFormat.format(projectRegion.mandatoryPaymentSeizuresSum)}
                  </div>
                </td>
                <td class="align-middle text-end">
                  ${numberFormat.format(projectRegion.inflowsSum - projectRegion.mandatoryPaymentSeizuresSum)}
                </td>
              </tr>
            `);
            if (!directorAdded) {
              $tr.prepend(`
                <th class="text-center align-middle" rowspan="${directorProjectRegions.length}">
                  ${director}
                </th>
              `);
              directorAdded = true;
            }
            $projectRegionsTableRows.append($tr);
          }
        }
      } else {
        $projectRegionsTableRows.html(`
          <tr>
            <td colspan="5" class="text-center text-danger">
              Нету приходов
            </td>
          </tr>
        `);
      }
    },
  });
  $projectRegionsTable.on(
    "click",
    ".show-project-region-mandatory-payments-seizures-table-modal",
    function () {
      const $tr = $(this).closest("tr");
      const name = $tr.data("name");
      $mandatoryPaymentSeizuresTable.smartTableResetFilters();
      $("#project-region-mandatory-payment-seizures-table-modal-label").text(
        `Погашений "${name}"`
      );
      $mandatoryPaymentSeizuresTable.smartTableUpdateFieldValues(
        "include",
        "project_region__name",
        [name]
      );
      $mandatoryPaymentSeizuresTable.smartTableUpdateFieldValues(
        "include",
        "datetime",
        [new Date().toISOString().slice(0, 10)]
      );
      $mandatoryPaymentSeizuresTable.smartTableReload();
    }
  );
  $projectRegionsTable.on(
    "show.bs.collapse",
    ".project-regions-collapse",
    function () {
      $(this)
        .closest("tr")
        .removeClass("border-top-0")
        .prev()
        .removeClass("border-bottom-0");
    }
  );
  $projectRegionsTable.on(
    "hidden.bs.collapse",
    ".project-regions-collapse",
    function () {
      $(this)
        .closest("tr")
        .addClass("border-top-0")
        .prev()
        .addClass("border-bottom-0");
    }
  );
});
