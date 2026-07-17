# paquetes ----------------------------------------------------------------
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

# definir estaciones ------------------------------------------------------
estaciones = ["INIA-4"]  # revisar csv estaciones_total

# definir variables -------------------------------------------------------
# variables disponibles: "TA_AVG", "TA_MIN", "TA_MAX",
# "HR_AVG", "HR_MIN", "HR_MAX", "PP_SUM", "PS_AVG",
# "RD_AVG", "TS00_AVG", "TS00_MIN", "TS00_MAX", "DV_AVG",
# "VV_AVG", "VV_MAX", "TS10_AVG", "TS10_MIN", "TS10_MAX",
variables = ["TS10_MIN", "TS10_MAX"]

# definir intervalo -------------------------------------------------------
anios = [2024, 2025]  # debe haber al menos un anio

# carpeta de salida (se crea si no existe)
carpeta_salida = Path("carpeta_datos_descargados")
carpeta_salida.mkdir(exist_ok=True)

for estacion in estaciones:
    for variable in variables:
        for anio in anios:
            entrada = {
                'estaciones[]': estacion,        # objeto estaciones
                'variables[]': variable,          # objeto variables
                'intervalo': 'day',               # intervalo: hour, day, month o year
                'desde': f"01-01-{anio}",
                'hasta': f"31-12-{anio}",
                'month_desde': 1,
                'month_hasta': 1,
                'yearMonth_desde': anio,
                'yearMonth_hasta': anio,
                'year_desde': f"{anio}-01-01",
                'year_hasta': f"{anio}-12-31",
                'vista[]': 'csv'
            }

            respuesta = requests.post('https://agrometeorologia.cl', data=entrada)
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            boton = soup.select_one("a.btn-danger")   # primer botón .btn-danger
            link = boton['href']
            csv = pd.read_csv(link)

            file_name = f"datos_{anio}_{estacion}_{variable}.csv"  # nombre archivo
            csv.to_csv(carpeta_salida / file_name, index=False)
