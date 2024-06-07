from django.core.management.base import BaseCommand
from openpyxl.reader.excel import load_workbook

from tester_atp_avr.models import TCP, TCPCategory, TCPFile
from tester_atp_avr.services import TCPCategoryRow, parsers


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            print("Choice: ")
            tcp_files = {}
            for index, tcp_file in enumerate(TCPFile.objects.all(), 1):
                tcp_files[index] = tcp_file
                print(f"{index}. {tcp_file}")
            selected_index = 1
            while True:
                selected_index = input("Enter index(default: 1): ")
                if not selected_index:
                    break
                try:
                    selected_index = int(selected_index)
                except ValueError:
                    print("You must enter a number.")
                else:
                    if selected_index <= 0:
                        print("The number must be equal to or greater than 1.")
                    elif selected_index not in tcp_files:
                        print("You entered the wrong number.")
                    else:
                        break
            print("\nOK...\n")
            tcp_file = tcp_files[selected_index]
            workbook = load_workbook(tcp_file.file.file, data_only=True)
            worksheet = workbook.active
            tcp_category_rows: list[TCPCategoryRow] | None = None
            for index, parse in enumerate(parsers):
                print(f"{index}. Applying the {parse.__qualname__} parser.")
                try:
                    tcp_category_rows = parse(worksheet)
                except Exception as exception:
                    print(str(exception))
                else:
                    break
            if tcp_category_rows is None:
                print("Failed to apply any parser.")
                return None
            elif not tcp_category_rows:
                print("No rows found.")
                return None
            print("\nOK...\n")
            for tcp_category_row in tcp_category_rows:
                print(
                    f"Creating TCPCategory with: {tcp_category_row.tcp_category_id} {tcp_category_row.name}, note={tcp_category_row.note}."
                )
                tcp_category = TCPCategory.objects.create(
                    tcp_category_id=tcp_category_row.tcp_category_id,
                    name=tcp_category_row.name,
                    note=tcp_category_row.note,
                    tcp_file=tcp_file,
                )

                for tcp_row in tcp_category_row.tcp_rows:
                    print(
                        f"Creating TCP with: {tcp_category_row.tcp_category_id}.{tcp_row.tcp_id} {tcp_row.name}, note={tcp_row.note}, base_price={tcp_row.base_price}, base_price_after_discount={tcp_row.base_price_after_discount}."
                    )
                    TCP.objects.create(
                        tcp_id=tcp_row.tcp_id,
                        tcp_category=tcp_category,
                        name=tcp_row.name,
                        note=tcp_row.note,
                        base_price=tcp_row.base_price,
                        base_price_after_discount=tcp_row.base_price_after_discount,
                    )
            print("\nFINISH.")
        except KeyboardInterrupt:
            print("Come back again.")
