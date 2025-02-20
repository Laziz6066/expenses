from PIL import Image, ImageDraw, ImageFont


def generate_remains_png(remains, file_path="/app/app/png/remains_report.png"):
    """
    Генерирует PNG-отчёт по остаткам.
    Аргументы:
        remains: список объектов, каждый из которых
         имеет атрибуты cash и plastic.
        file_path: путь для сохранения изображения.
    Возвращает:
        file_path, по которому сохранено изображение.
    """
    # Если передан список, суммируем значения
    if isinstance(remains, list):
        if not remains:
            raise ValueError("Список остатков пустой")
        total_cash = sum(r.cash for r in remains)
        total_plastic = sum(r.plastic for r in remains)
    else:
        total_cash = remains.cash
        total_plastic = remains.plastic

    total_overall = total_cash + total_plastic

    # Размеры изображения
    img_width = 501
    img_height = 225
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Загружаем шрифты (убедитесь, что файлы
    # шрифтов доступны по указанному пути)
    try:
        font = ImageFont.truetype("/app/app/png/DejaVuSans.ttf", 20)
        font_bold = ImageFont.truetype("/app/app/png/DejaVuSans-Bold.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font

    # Заголовок отчёта
    title = "Отчет по остаткам"
    bbox = draw.textbbox((0, 0), title, font=font_bold)
    title_w = bbox[2] - bbox[0]
    draw.text(((img_width - title_w) / 2, 10),
              title, fill="black", font=font_bold)

    # Определяем размеры таблицы
    headers = ["Тип", "Сумма"]
    col_widths = [250, 250]
    row_height = 40
    start_y = 60
    x_margin = 0

    # Рисуем заголовок таблицы
    current_y = start_y
    current_x = x_margin
    for i, header in enumerate(headers):
        draw.rectangle([current_x, current_y, current_x
                        + col_widths[i], current_y + row_height],
                       outline="black", fill="lightgrey")
        bbox = draw.textbbox((0, 0), header, font=font_bold)
        header_w = bbox[2] - bbox[0]
        draw.text((current_x + (col_widths[i] - header_w) / 2, current_y + 10),
                  header, fill="black", font=font_bold)
        current_x += col_widths[i]
    current_y += row_height

    # Данные для таблицы: Наличные, Пластик картой, Общий итог
    data = [
        ("Наличные", f"{total_cash:,.0f} UZS"),
        ("Пластик картой", f"{total_plastic:,.0f} UZS"),
        ("Общий итог", f"{total_overall:,.0f} UZS")
    ]
    for row in data:
        current_x = x_margin
        for i, cell in enumerate(row):
            draw.rectangle([current_x, current_y, current_x
                            + col_widths[i], current_y + row_height],
                           outline="black")
            bbox = draw.textbbox((0, 0), cell, font=font)
            cell_w = bbox[2] - bbox[0]
            draw.text((current_x + (col_widths[i] - cell_w)
                       / 2, current_y + 10),
                      cell, fill="black", font=font)
            current_x += col_widths[i]
        current_y += row_height

    # Сохраняем изображение
    img.save(file_path)
    return file_path
