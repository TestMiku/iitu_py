class AccountsTable extends EventTarget {
    constructor(options = { url: null, canSelectAccount: true }) {
        super();
        if (options.url == null) {
            throw new Error("url is required");
        }
        this.url = options.url;
        this.canSelectAccount = options.canSelectAccount == null ? true : options.canSelectAccount;
        this.loaded = false;
        this.data = null;
        this.accountBalance = {};
        this.numberFormat = Intl.NumberFormat("ru-RU", {
            maximumFractionDigits: 2,
            minimumFractionDigits: 2
        });
        this.projectRegionBalance = {};
        this._view = localStorage.getItem("accounts-table-view") || "project-region";

        $(document).on("click", "#project-region-accounts-table-toggle-view-button", () => {
            this.toggleView();
        });
        $(document).on("shown.bs.collapse", "#project-region-accounts-table-collapse", function () {
            const $projectRegionAccountsTableToggleCollapseButton = $("#project-region-accounts-table-toggle-collapse-button");
            $projectRegionAccountsTableToggleCollapseButton.html(`
                <i class="fa-regular fa-eye-slash"></i> Скрыть
            `);
            $projectRegionAccountsTableToggleCollapseButton.prop("title", "Скрыть таблицу расчётных счетов");
        }).on("hidden.bs.collapse", "#project-region-accounts-table-collapse", function () {
            const $projectRegionAccountsTableToggleCollapseButton = $("#project-region-accounts-table-toggle-collapse-button");
            $projectRegionAccountsTableToggleCollapseButton.html(`
                <i class="fa-regular fa-eye"></i> Показать
            `);
            $projectRegionAccountsTableToggleCollapseButton.prop("title", "Показать таблицу расчётных счетов");
        });
        $(document).on("click", "#project-region-accounts-table-reload-button", () => {
            this.reload();
        });
        $(document).on("change", ".account-radio", function() {
            $(this).next().prop("checked", true);
        });
    }
    changeToggleViewButtonText() {
        const $toggleViewButton = $("#project-region-accounts-table-toggle-view-button");
        if (this._view === "account") {
            $toggleViewButton.html(`<i class="fa-solid fa-arrow-right-arrow-left"></i> Расчётный счёт`);
        } else {
            $toggleViewButton.html(`<i class="fa-solid fa-arrow-right-arrow-left"></i> ПМ`);
        }
    }
    async _getData() {
        const response = await fetch(this.url);
        if (response.ok) {
            return await response.json();
        }
        return null;
    }
    async toggleView() {
        if (this._view === "project-region") {
            this._view = "account";
        } else {
            this._view = "project-region";
        }
        this.changeToggleViewButtonText();
        localStorage.setItem("project-region-accounts-table-view", this._view);
        await this._display({ viewToggled: true });
    }
    async _display(options = { viewToggled: false }) {
        const $projectRegionAccountsSubdivisions = $("#project-region-accounts-subdivisions");
        let activeSubdivision = $projectRegionAccountsSubdivisions.find(".nav-link.active").data("subdivision");
        const $projectRegionAccountsSubdivisionsLoading = $("#project-region-accounts-subdivisions-loading");
        $projectRegionAccountsSubdivisions.empty();
        $projectRegionAccountsSubdivisionsLoading.removeClass("d-none");

        const $container = $("#project-region-accounts-table-container");
        $container.html(`
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `);
        if (!options.viewToggled) {
            this.data = await this._getData();
        }
        $projectRegionAccountsSubdivisionsLoading.addClass("d-none");

        $container.empty();
        const subdivisions = Array.from(new Set(this.data.accounts.map(account => account.subdivision && account.subdivision.name)));
        subdivisions.sort((a, b) => {
            if (!a) {
                return 1;
            } else if (!b) {
                return -1;
            } else {
                return a.localeCompare(b);
            }
        });
        let index = 0;
        this.accountBalance = {};
        this.projectRegionBalance = {};
        for (const subdivision of subdivisions) {
            const accounts = this.data.accounts.filter(account => account.subdivision ? account.subdivision.name === subdivision : !subdivision)
            const projectRegions = this.data.project_regions.filter(projectRegion => projectRegion.subdivision ? projectRegion.subdivision.name === subdivision : !subdivision)
            if (accounts.length === 0 || projectRegions.length === 0) {
                continue;
            }
            if (activeSubdivision == null && index === 0) {
                activeSubdivision = subdivision;
            }
            const isCurrentSubdivisionActive = (!activeSubdivision && !subdivision) || activeSubdivision === subdivision;
            $projectRegionAccountsSubdivisions.append(`
                <li class="nav-item">
                    <a style="width: 8em" class="nav-link text-center text-truncate ${isCurrentSubdivisionActive ? "active" : ""}" id="project-region-accounts-subdivision-${index}-tab" data-bs-toggle="tab" href="#project-region-accounts-subdivision-${index}" role="tab" aria-controls="project-region-accounts-subdivision-${index}" aria-selected="${isCurrentSubdivisionActive ? "true" : "false"}" data-subdivision="${subdivision || ""}">${subdivision || `Не указан`}</a>
                </li>
            `);
            const $tabPane = $(`
                <div class="tab-pane ${isCurrentSubdivisionActive ? "active" : ""}" id="project-region-accounts-subdivision-${index}" role="tabpanel" aria-labelledby="project-region-accounts-subdivision-${index}-tab">
                    
                </div>
            `);
            const $table = $(`<table class="table mx-auto w-auto mb-0 table-bordered border-black"></table>`);
            const $tfoot = $(`
                <tfoot class="border-black">
                    <tr>
                        <th class="align-middle text-white" scope="row" style="background-color: #315496">Итого</th>
                    </tr>
                </tfoot>
            `).appendTo($table);
            const $tfootTr = $tfoot.children().first();
            let totalSum = 0;
            const getTd = (projectRegion, account, sum) => {
                let $td = null;
                if (this.canSelectAccount && !account.is_cash_register && this.data.project_region_accounts[projectRegion.id].find(projectRegionAccount => projectRegionAccount.id == account.id)) {
                    $td = $(`
                        <td class="align-middle text-end">
                            <div class="form-check">
                                <label class="form-check-label" for="project-region-${projectRegion.id}-account-${account.id}-radio">${this.numberFormat.format(sum)}</label>
                                <input class="account-radio form-check-input" type="radio" value="${account.id}" id="project-region-${projectRegion.id}-account-${account.id}-radio" data-project-region-id="${projectRegion.id}" data-account-id="${account.id}"/>
                                <input class="project-region-radio d-none" type="radio" value="${projectRegion.id}" id="account-${account.id}-project-region-${projectRegion.id}-radio" data-project-region-id="${projectRegion.id}" data-account-id="${account.id}"/>
                            </div>
                        </td>
                    `);
                } else {
                    $td = $(`<td class="align-middle text-end">${this.numberFormat.format(sum)}</td>`)
                }
                if (sum < 0) {
                    $td.addClass("text-danger");
                }
                return $td;
            };
            if (this._view === "project-region") {
                const $thead = $(`
                    <thead class="border-black">
                        <tr>
                            <th class="align-middle text-white" style="background-color: #315496" scope="col">ПМ</th>
                        </tr>
                    </thead>
                `).appendTo($table);
                const $theadTr = $thead.children().first();
                for (const account of accounts) {
                    $theadTr.append(`
                        <th class="text-end align-middle text-white" style="background-color: #315496; width: 10em" scope="col">               
                            ${account.name}
                        </th>
                    `);
                }
                $theadTr.append(`<th class="text-end align-middle text-white" style="background-color: #315496">Итого</th>`);
                const $tbody = $(`<tbody></tbody>`).appendTo($table);
                for (const projectRegion of projectRegions) {
                    const $tr = $(`<tr><th scope="row">${projectRegion.name}</th></tr>`);
                    let projectRegionTotalSum = 0;
                    for (const account of accounts) {
                        const sum = parseFloat(this.data.sums[projectRegion.id][account.id]);
                        if (account.id in this.accountBalance) {
                            this.accountBalance[account.id] += sum;
                        } else {
                            this.accountBalance[account.id] = sum;
                        }
                        projectRegionTotalSum += sum;
                        totalSum += sum;
                        $tr.append(getTd(projectRegion, account, sum));
                    }
                    this.projectRegionBalance[projectRegion.id] = projectRegionTotalSum;
                    const $td = $(`
                    <td class="align-middle text-end">
                        ${this.numberFormat.format(projectRegionTotalSum)}
                    </td>
                `);
                    if (projectRegionTotalSum < 0) {
                        $td.addClass("text-danger");
                    }
                    $tr.append($td);
                    $tbody.append($tr);
                }
                for (const account of accounts) {
                    const totalSum = this.accountBalance[account.id];
                    const $td = $(`<td class="text-end text-white align-middle" style="background-color: #315496">${this.numberFormat.format(totalSum)}</td>`);
                    if (totalSum < 0) {
                        $td.addClass("text-danger");
                    }
                    $tfootTr.append($td);
                }
            } else {
                const $thead = $(`
                    <thead class="border-black">
                        <tr>
                            <th class="align-middle text-white" scope="col" style="background-color: #315496">Расчётный счёт</th>
                        </tr>
                    </thead>
                `).appendTo($table);
                const $theadTr = $thead.children().first();
                for (const projectRegion of projectRegions) {
                    $theadTr.append(`
                        <th class="text-center text-white align-middle" scope="col" style="background-color: #315496; width: 8em">               
                            ${projectRegion.name}
                        </th>
                    `);
                }
                $theadTr.append(`<th class="text-end text-white align-middle" style="background-color: #315496">Итого</th>`);
                const $tbody = $(`<tbody></tbody>`).appendTo($table);
                for (const account of accounts) {
                    const $tr = $(`<tr><th scope="row">${account.name}</th></tr>`);
                    let accountTotalSum = 0;
                    for (const projectRegion of projectRegions) {
                        const sum = parseFloat(this.data.sums[projectRegion.id][account.id]);
                        if (projectRegion.id in this.projectRegionBalance) {
                            this.projectRegionBalance[projectRegion.id] += sum;
                        } else {
                            this.projectRegionBalance[projectRegion.id] = sum;
                        }
                        accountTotalSum += sum;
                        totalSum += sum;
                        $tr.append(getTd(projectRegion, account, sum));
                    }
                    this.accountBalance[account.id] = accountTotalSum;
                    const $td = $(`
                        <td class="align-middle text-end">
                            ${this.numberFormat.format(accountTotalSum)}
                        </td>
                    `);
                    if (accountTotalSum < 0) {
                        $td.addClass("text-danger");
                    }
                    $tr.append($td);
                    $tbody.append($tr);
                }
                for (const projectRegion of projectRegions) {
                    const totalSum = this.projectRegionBalance[projectRegion.id];
                    const $td = $(`<td class="text-end text-white align-middle" style="background-color: #315496">${this.numberFormat.format(totalSum)}</td>`);
                    if (totalSum < 0) {
                        $td.addClass("text-danger");
                    }
                    $tfootTr.append($td);
                }
            }
            const $td = $(`<td class="text-end text-white align-middle" style="background-color: #315496">${this.numberFormat.format(totalSum)}</td>`);
            if (totalSum < 0) {
                $td.addClass("text-danger");
            }
            $tfootTr.append($td);
            $tabPane.append($table)
            $container.append($tabPane);
            index++;
        }
        this.dispatchEvent(new Event("accounts-displayed"));
    }
    async reload() {
        this.loaded = false;
        const $reloadButton = $("#project-region-accounts-table-reload-button");
        $reloadButton.prop("disabled", true);
        await this._display();
        $reloadButton.prop("disabled", false);
        this.loaded = true;
    }

    getAccount(id) {
        if (!this.loaded) return null;
        return this.data.accounts.find(account => account.id == id);
    }

    getProjectRegion(id) {
        if (!this.loaded) return null;

        return this.data.project_regions.find(projectRegion => projectRegion.id == id);
    }

    getAccounts() {
        if (!this.loaded) return null;

        return this.data.accounts;
    }

    getProjectRegions() {
        if (!this.loaded) return null;

        return this.data.project_regions;
    }

    unselectAccounts() {
        const $accountRadio = $(".account-radio");
        const $projectRegionRadio = $(".project-region-radio");
        $accountRadio.prop("checked", false);
        $projectRegionRadio.prop("checked", false);
        console.log("Accounts unselected");
    }

    cantSelectAccount() {
        const $accountRadio = $(".account-radio");
        const $projectRegionRadio = $(".project-region-radio");

        $accountRadio.prop("disabled", true);
        $projectRegionRadio.prop("disabled", true);
        
        $accountRadio.attr("form", null);
        $projectRegionRadio.attr("form", null);
        
        $accountRadio.prop("name", null);
        $projectRegionRadio.prop("name", null);

        $accountRadio.prop("required", false);
        $projectRegionRadio.prop("required", false);
        
        console.log("Can't select account");
    }

    canSelectAnyAccount(options = { required: true, form: null, name: null, projectRegionName: null }) {
        const $accountRadio = $(".account-radio");
        const $projectRegionRadio = $(".project-region-radio");

        $accountRadio.prop("disabled", false);
        $projectRegionRadio.prop("disabled", false);

        $accountRadio.prop("name", options.name || `account-id`);
        $projectRegionRadio.prop("name", options.projectRegionName || `project-region-id`);

        $accountRadio.attr("form", options.form);
        $projectRegionRadio.attr("form", options.form);

        $accountRadio.prop("required", options.required);
        $projectRegionRadio.prop("required", options.required);

        console.log("Can select any account", options);
    }

    canSelectAnyProjectRegionAccount(options = { required: true, form: null}) {
        const $accountRadio = $(".account-radio");
        const $projectRegionRadio = $(".project-region-radio");

        $accountRadio.prop("disabled", false);
        $projectRegionRadio.prop("disabled", false);

        $accountRadio.attr("form", options.form);
        $projectRegionRadio.attr("form", options.form);

        $accountRadio.attr("required", options.required);
        $projectRegionRadio.attr("required", options.required);
        
        $accountRadio.prop("name", function () {
            const projectRegionId = $(this).data("projectRegionId");
            $(this).prop("name", `project-region-${projectRegionId}-account`);
            $(this).next().prop("name", `project-region-${projectRegionId}`);
        });

        console.log("Can select any project region account", options);
    }

    /**
     * 
     * @param {{projectRegionId: number | null, required: boolean, form: string | null, name: string | null}} options 
     * @returns {void}
     */
    canSelectOneProjectRegionAccount(options = { projectRegionId: null, required: true, form: null, name: null }) {
        const $accountRadio = $(".account-radio");
        const $projectRegionRadio = $(".project-region-radio");

        $accountRadio.prop("disabled", true);
        $projectRegionRadio.prop("disabled", true);

        $accountRadio.attr("form", null);
        $projectRegionRadio.attr("form", null);

        $accountRadio.attr("required", false);
        $projectRegionRadio.attr("required", false);

        $accountRadio.prop("name", null);
        $projectRegionRadio.prop("name", null);

        $accountRadio.prop("name", function () {
            const projectRegionId = $(this).data("projectRegionId");
            if (projectRegionId == options.projectRegionId) {
                $(this).prop("disabled", false);
                $(this).next().prop("disabled", false);

                $(this).attr("required", options.required);
                $(this).next().attr("required", options.required);

                $(this).attr("form", options.form);
                $(this).next().attr("form", options.form);

                $(this).prop("name", `project-region-${projectRegionId}-account`);
                $(this).next().prop("name", `project-region-${projectRegionId}`);
            }
        });
        console.log("Can select one project region account", options);
    }
}

