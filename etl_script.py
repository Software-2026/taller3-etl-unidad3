import pandas as pd

# 1. Cargar archivo original
df_raw = pd.read_excel('Datos_Reto.xlsx')

rows = []
current_area = None

# 2. Extracción y filtrado
for idx, row in df_raw.iterrows():
    val1 = str(row['Unnamed: 1']).strip()
    val2 = str(row['Unnamed: 2']).strip()

    if val1 == 'Área' or 'Total' in val1 or 'Empleados' in val2:
        continue

    if val1 != 'nan' and val1.isdigit():
        current_area = int(val1)

    id_val = row['Unnamed: 2']

    if pd.notna(id_val) and str(id_val).replace('.', '').isdigit():
        rows.append({
            'Área': current_area,
            'ID': int(id_val),
            'Nombre_Raw': str(row['Unnamed: 3']),
            'Título profesional': str(row['Unnamed: 4']).strip(),
            'Nivel organizacional': row['Unnamed: 5'],
            'Estado civil': str(row['Unnamed: 6']).strip(),
            'Género': str(row['Unnamed: 7']).strip(),
            'Fecha de contratación': row['Unnamed: 8'],
            'Bono (USD)': row['Unnamed: 9']
        })

df = pd.DataFrame(rows)

# 3. Separación de nombres y formato
def separar_nombre_apellido(nombre_completo):
    texto_limpio = nombre_completo.replace('.', ' ')
    partes = [p.strip() for p in texto_limpio.split() if p.strip()]
    if not partes:
        return "", ""
    nombre = partes[0].title()
    apellidos = " ".join(partes[1:]).title() if len(partes) > 1 else ""
    return nombre, apellidos

df[['Nombre', 'Apellidos']] = df['Nombre_Raw'].apply(lambda x: pd.Series(separar_nombre_apellido(x)))
df = df.drop(columns=['Nombre_Raw'])

# 4. Limpieza de datos y formato de fechas
df['Bono (USD)'] = df['Bono (USD)'].fillna(0)
df['Fecha de contratación'] = pd.to_datetime(df['Fecha de contratación']).dt.strftime('%Y-%m-%d')
df = df.drop_duplicates(subset=['ID'], keep='first')

# 5. Guardar el resultado depurado
cols_order = [
    'Área', 'ID', 'Nombre', 'Apellidos', 'Título profesional',
    'Nivel organizacional', 'Estado civil', 'Género',
    'Fecha de contratación', 'Bono (USD)'
]
df_final = df[cols_order]
df_final.to_excel('Datos_Reto_Limpio.xlsx', index=False)

print("¡Proceso ETL completado exitosamente! Se ha generado 'Datos_Reto_Limpio.xlsx'.")