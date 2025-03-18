import os
import pandas as pd
from datetime import datetime

def process_uf_file(file_path):
    year = int(file_path.split('UF ')[-1].split('.')[0])

    if year < 2013:
        # Intentar primero con coma como separador
        df = pd.read_csv(file_path)
    else:
        # Si falla, intentar con punto y coma
        df = pd.read_csv(file_path, sep=';')
    
    # Imprimir información de diagnóstico
    print(f"Procesando archivo: {file_path}")
    print("Nombres de columnas:", df.columns.tolist())
    
    # Crear lista para almacenar los datos procesados
    processed_data = []
    
    # Mapeo de nombres de meses según el formato
    month_mapping = {
        'pre-2013': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                     'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    }
    
    # Determinar qué formato de mes usar
    if any(mes in df.columns for mes in month_mapping['pre-2013']):
        months = month_mapping['pre-2013']
    
    # Procesar cada fila
    for _, row in df.iterrows():
        try:
            # Intentar diferentes variantes del nombre de la columna
            day = int(row['Día'])
            
            # Procesar cada mes
            for i, month in enumerate(months, 1):
                if pd.notna(row[month]):  # Verificar si el valor no es NA
                    try:
                        # Limpiar el valor (quitar puntos y comas)
                        value = str(row[month]).replace('.', '').replace(',', '.').strip('"')
                        
                        date = f"{year}-{i:02d}-{day:02d}"
                        
                        processed_data.append({
                            'date': date,
                            'clfclp': float(value)
                        })
                    except Exception as e:
                        print(f"Error procesando valor para {month}, día {day}: {e}")
                        print(f"Valor problemático: {row[month]}")
        except Exception as e:
            print(f"Error al procesar la fila: {row}")
            print(f"Error: {e}")
    
    return pd.DataFrame(processed_data)

def generate_combined_uf_file():
    # Lista para almacenar todos los dataframes
    all_data = []
    
    # Procesar cada archivo en el directorio
    directory = "UF data"  # Ajusta esto a tu directorio
    for filename in sorted(os.listdir(directory)):
        if filename.startswith("UF ") and filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            df = process_uf_file(file_path)
            all_data.append(df)
    
    # Combinar todos los dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Ordenar por fecha
    combined_df = combined_df.sort_values('date')
    
    # Guardar el archivo combinado
    combined_df.to_csv('UF 1990-2025.csv', index=False)

# Ejecutar la función principal
generate_combined_uf_file()