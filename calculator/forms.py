from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DeleteOptionsForm(forms.Form):
    DELETE_ORDERS = 'delete_orders'
    DELETE_PRICES = 'delete_prices'
    DELETE_BOTH = 'delete_both'

    DELETE_CHOICES = [
        (DELETE_ORDERS, 'Удалить только заказы'),
        (DELETE_PRICES, 'Удалить только цены'),
        (DELETE_BOTH, 'Удалить и заказы, и цены'),
    ]

    delete_option = forms.ChoiceField(
        choices=DELETE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label='Выберите опцию удаления:'
    )
