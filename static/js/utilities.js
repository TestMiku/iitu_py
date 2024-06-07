
function formatPrice(x) {
    return new Intl.NumberFormat("ru-RU", {
        minimumFractionDigits: 2,
        currency: "KZT",
        style: "currency",
        currencySign: "accounting"
    }).format(x)
}

function formatNumber(x) {
    return new Intl.NumberFormat("ru-RU", {maximumFractionDigits: 0}).format(x)
}

function formatNumber2(x) {
    return new Intl.NumberFormat("ru-RU", {maximumFractionDigits: 2}).format(x);
}


