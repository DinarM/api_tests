import pandas as pd
from openpyxl.utils import get_column_letter

path1 = "vniirice_ogly/"
path2 = "vniirice_korotenko/"

filename = '2024_Pitomnik_kollektsionnyy_Krasnodarskiy_kray'

file1 = f"{path1}{filename}.xlsx"
file2 = f"{path2}{filename}.xlsx" 

# Загружаем оба файла
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Убедимся, что размеры совпадают
if df1.shape != df2.shape:
    print("Размеры файлов не совпадают")
else:
    differences = []

    for row in range(df1.shape[0]):
        for col in range(df1.shape[1]):
            val1 = df1.iat[row, col]
            val2 = df2.iat[row, col]
            if pd.isna(val1) and pd.isna(val2):
                continue
            if val1 != val2:
                cell_address = f"{get_column_letter(col+1)}{row+1}"
                differences.append((cell_address, val1, val2))

    if not differences:
        print(f"Файлы {filename} полностью совпадают")
    else:
        print("Найдены отличия:")
        for cell, v1, v2 in differences:
            print(f"{cell}: '{v1}' != '{v2}'")