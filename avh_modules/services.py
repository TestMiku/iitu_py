import re
from datetime import datetime

import xlsxwriter
import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render


class TransformXLSXFileService:
    def __init__(self, xlsx_file):
        self.xlsx_file = xlsx_file
        self.dfs = pd.read_excel(xlsx_file, sheet_name=None)
        self.output_filename = 'output.xlsx'

    def transform(self, request, template_name):
        try:
            with pd.ExcelWriter(self.output_filename, engine='xlsxwriter') as writer:
                for sheet_name, df in self.dfs.items():
                    df.columns = [re.sub(r'\s+', ' ', col.strip()) for col in df.columns]
                    required_columns = ['ДО', 'Дата', 'Сумма от ПМ']
                    available_columns = [col for col in required_columns if
                                         any(re.match(col, col_df) for col_df in df.columns)]
                    if available_columns:
                        selected_columns = df[available_columns]
                        selected_columns = selected_columns.applymap(
                            lambda x: x.strftime('%d.%m.%Y') if isinstance(x, pd.Timestamp) else x
                            )
                        selected_columns = selected_columns.applymap(
                            lambda x: x.replace(' ', '').replace(',', '.') if isinstance(x, str) else x)

                        for column in selected_columns.columns:
                            selected_columns = selected_columns.dropna()

                            if column == 'ДО':
                                selected_columns[column] = selected_columns[column].apply(
                                    lambda x: x.strip() if isinstance(x, str) else x)
                                selected_columns.loc[:, column] = selected_columns[column].astype(str)
                            if column == 'Дата':
                                selected_columns.loc[:, column] = pd.to_datetime(datetime.now(), format='%d.%m.%Y',
                                                                                 errors='coerce').date()
                            if column == 'Сумма от ПМ':
                                selected_columns[column] = selected_columns[column].apply(
                                    lambda x: float(x.replace(',', '').replace('\xa0', '')) if isinstance(x,
                                                                                                          str) else x)
                                selected_columns.loc[:, column] = selected_columns[column].astype(float)

                        selected_columns.to_excel(writer, sheet_name=sheet_name, index=False)

            return self.output_filename
        except Exception as e:
            return self.get_error(request, template_name, e)

    def get_response(self):
        with open(self.output_filename, 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="output.xlsx"'
            return response

    @staticmethod
    def get_error(request, template_name, error):
        return render(request, template_name, {'error': error})


"""
    Save the third column to csv file.
    Change type of the first column to string.
    Change type of the second column to date.
    Change type of the third column to int.
    Save csv file to xlsx file.
    Return response.
"""
