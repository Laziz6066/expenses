from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


def generate_expense_png(
        expenses,
        start_date: datetime,
        end_date: datetime,
        file_path="png/expense_report.png"):
    # Настройки таблицы
    headers = ["Название", "Сумма", "Тип", "Дата"]
    col_widths = [200, 150, 150, 200]  # ширина колонок в пикселях
    row_height = 30
    num_data_rows = len(expenses)
    summary_rows = 4  # пустая строка + 3 строки итогов

    # Определяем размеры изображения
    table_rows = 1 + num_data_rows + summary_rows
    img_width = sum(col_widths) + 20
    img_height = table_rows * row_height + 60  # +60 для заголовка отчёта
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Загружаем шрифты (убедитесь, что файлы
    # шрифтов находятся в доступном месте)
    try:
        font = ImageFont.truetype("png/DejaVuSans.ttf", 16)
        font_bold = ImageFont.truetype("png/DejaVuSans-Bold.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font

    # Заголовок отчёта
    title_text = (f"Отчет по расходам с {start_date.strftime('%d.%m.%Y')}"
                  f" по {end_date.strftime('%d.%m.%Y')}")
    bbox = draw.textbbox((0, 0), title_text, font=font_bold)
    title_w = bbox[2] - bbox[0]
    draw.text(((img_width - title_w) / 2, 10), title_text,
              fill="black", font=font_bold)

    # Начальные координаты для таблицы
    start_y = 40
    x_margin = 10

    # Рисуем заголовок таблицы
    current_y = start_y
    current_x = x_margin
    for i, header in enumerate(headers):
        # Рисуем ячейку
        draw.rectangle([current_x, current_y, current_x +
                        col_widths[i], current_y + row_height],
                       outline="black", fill="lightgrey")
        draw.text((current_x + 5, current_y + 5), header,
                  fill="black", font=font_bold)
        current_x += col_widths[i]
    current_y += row_height

    # Рисуем строки данных
    for expense in expenses:
        current_x = x_margin
        text_values = [
            expense.title,
            f"{expense.amount:,.0f} UZS",
            expense.type_expense,
            expense.created_at.strftime("%d.%m.%Y %H:%M")
        ]
        for i, text in enumerate(text_values):
            draw.rectangle([current_x, current_y, current_x +
                            col_widths[i], current_y + row_height],
                           outline="black")
            draw.text((current_x + 5, current_y + 5), text,
                      fill="black", font=font)
            current_x += col_widths[i]
        current_y += row_height

    # Расчёт итогов
    total_cash = sum(exp.amount for exp in expenses if
                     exp.type_expense.lower() == "наличными")
    total_plastic = sum(exp.amount for exp in expenses
                        if exp.type_expense.lower() == "пластик картой")
    total_overall = total_cash + total_plastic

    # Добавляем пустую строку между таблицей и итогами
    current_y += row_height // 2

    # Рисуем строки итогов
    summary_data = [
        ("Наличными:", f"{total_cash:,.0f} UZS"),
        ("Пластик картой:", f"{total_plastic:,.0f} UZS"),
        ("Общий итог:", f"{total_overall:,.0f} UZS")
    ]
    for label, value in summary_data:
        # Рисуем прямоугольник для строки итогов (на всю ширину)
        draw.rectangle([x_margin, current_y, img_width - x_margin,
                        current_y + row_height], outline="black")
        draw.text((x_margin + 5, current_y + 5), label,
                  fill="black", font=font_bold)
        # Выравнивание справа для суммы
        bbox_value = draw.textbbox((0, 0), value, font=font)
        value_w = bbox_value[2] - bbox_value[0]
        draw.text((img_width - x_margin - value_w - 5, current_y + 5),
                  value, fill="black", font=font)
        current_y += row_height

    # Сохраняем изображение
    img.save(file_path)
    return file_path
