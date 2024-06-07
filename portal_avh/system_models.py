from django.core.files.storage import FileSystemStorage
import os

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            # Получаем путь к директории и имя файла без расширения
            directory, file_name = os.path.split(name)
            file_root, file_ext = os.path.splitext(file_name)
            
            # Добавляем (1) к имени файла
            file_root += ' (1)'
            name = os.path.join(directory, file_root + file_ext)
            
            # Проверяем, существует ли файл с новым именем
            while self.exists(name):
                # Если существует, увеличиваем число в скобках
                file_root = file_root[:-3]  # Удаляем текущий номер в скобках
                number_str = file_root.split(' ')[-1]  # Получаем текущее число
                if number_str.isdigit():
                    number = int(number_str)
                    number += 1
                    file_root = file_root.split(' ')[0] + f' ({number})'
                else:
                    file_root += ' (1)'
                name = os.path.join(directory, file_root + file_ext)
            
        return name
