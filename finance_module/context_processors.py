def finance_sections(request):
    sections = {
        'Платежи': {
            'url': '/p1/finance-module/all',
            'icon': 'fas fa-file-invoice',
            'subsections': {}
        },
        'Импорт поступлений': {
            'url': '/p1/finance-module/import-inflows',
            'icon': 'fas fa-people-arrows',
            'subsections': {}
        },
        'Обязательные платежи': {
            'url': '/p1/finance-module/mandatory-payments/import-mandatory-payments',
            'icon': 'fa-solid fa-asterisk',
            'subsections': {
                'Импорт обязательных платежей': {'url': '/p1/finance-module/mandatory-payments/import-mandatory-payments', 'icon': 'fa-solid fa-file-import'},
                'Калькулятор начислений': {'url': '/p1/finance-module/mandatory-payments/accrual-calculator', 'icon': 'fa-solid fa-calculator'},
                'Список начислений': {'url': '/p1/finance-module/mandatory-payments/accrual-list', 'icon': 'fa-solid fa-list'},
                'Список обязательных платежей': {'url': '/p1/finance-module/mandatory-payments/list', 'icon': 'fa-solid fa-list-alt'},
                'Создать исключение для ПМ': {'url': '/p1/finance-module/mandatory-payments/create-access-to-others-exception-for-project-manager', 'icon': 'fa-solid fa-exclamation-circle'},
                'Выгрузка': {'url': '/p1/finance-module/mandatory-payments/unloading', 'icon': 'fa-solid fa-download'},
            }
        },
        'Долги между подразделениями': {
            'url': '/p1/finance-module/interdivisional-debts/import',
            'icon': 'fa-solid fa-arrow-right-arrow-left',
            'subsections': {
                'Импорт': {'url':'/p1/finance-module/interdivisional-debts/import', 'icon': 'fa-solid fa-file-import'},
                'Таблица "Долги между подразделениями"': {'url': '/p1/finance-module/interdivisional-debts/table', 'icon': 'fa-solid fa-table'},
                'Дать долг от имени компании': {'url': '/p1/finance-module/lend-company', 'icon': 'fa-solid fa-hand-holding-usd'},
                'Выгрузка': {'url': '/p1/finance-module/unload_debts', 'icon': 'fa-solid fa-download'},
            }
        },
        'Отдел финансового планирования': {
            'url': '/p1/finance-module/division-of-financial-planning/confirmation',
            'icon': 'fa-solid fa-scale-balanced',
            'subsections': {
                'Подтверждение платежей': {'url': '/p1/finance-module/division-of-financial-planning/confirmation', 'icon': 'fa-solid fa-check-circle'},
                'Ежедневно': {'url': '/p1/finance-module/division-of-financial-planning/daily', 'icon': 'fa-solid fa-calendar-day'},
                'Ежемесячные платежи': {'url': '/p1/finance-module/division-of-financial-planning/monthly-payments', 'icon': 'fa-solid fa-calendar-alt'},
                'Переводы': {'url': '/p1/finance-module/division-of-financial-planning/transfers', 'icon': 'fa-solid fa-exchange-alt'},

            }
        },
        'Для казначеев': {
            'url': '/p1/finance-module/for-treasurers/confirmation',
            'icon': 'fa-solid fa-money-bill-transfer',
            'subsections': {
                'Подтверждение платежей': {'url': '/p1/finance-module/for-treasurers/confirmation', 'icon': 'fa-solid fa-check-circle'},
            }
        },
        'Бегунок/Касса': {
            'url': '/p1/finance-module/runner-and-cash-register',
            'icon': 'fa-solid fa-cash-register',
            'subsections': {}
        },
        'Реестр неоплаченных счетов': {
            'url': '/p1/finance-module/unpaid-invoices/import',
            'icon': 'fas fa-upload',
            'subsections': {
                'Импорт': {'url': '/p1/finance-module/unpaid-invoices/import', 'icon': 'fa-solid fa-file-import'},
                'Список реестра неоплаченных счетов': {'url': '/p1/finance-module/unpaid-invoices/list', 'icon': 'fa-solid fa-list'},
                'Реестр оплат': {'url': '/p1/finance-module/unpaid-invoices/paid-invoices', 'icon': 'fa-solid fa-list-check'},
                'Выгрузка': {'url': '/p1/finance-module/unpaid-invoices/unloading', 'icon': 'fa-solid fa-download'},
                'Сумма от ПМ': {'url': '/p1/finance-module/unpaid-invoices/pm-sum', 'icon': 'fa-solid fa-dollar-sign'},
            }
        },
        'Сверка реестра оплат с выписками из банка': {
            'url': '/p1/finance-module/statement-reconciliation',
            'icon': 'fa-solid fa-not-equal',
            'subsections': {}
        },
        'Приход 71п': {
            'url': '/p1/finance-module/income-71-p',
            'icon': 'fa-solid fa-piggy-bank',
            'subsections': {}
        },
    }

    return {'sections': sections}
