import os

# Укажите путь к папке с файлами
folder_path = 'labels'

# Проходим по всем файлам в папке
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):  # Проверяем, чтобы файл был текстовым
        file_path = os.path.join(folder_path, file_name)

        # Читаем содержимое файла
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Обрабатываем строки
        processed_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0:
                class_id = int(parts[0])  # Получаем первое число (ID класса)
                if class_id == 0 or class_id == 1:
                    continue  # Пропускаем строки с ID 0 и 1
                elif class_id == 2:
                    parts[0] = "0"  # Заменяем ID 2 на 0
                elif class_id == 3:
                    parts[0] = "1"  # Заменяем ID 3 на 1
                processed_lines.append(" ".join(parts))

        # Записываем изменения обратно в файл
        with open(file_path, "w") as file:
            file.write("\n".join(processed_lines))
