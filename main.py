import csv, sys
import re
import requests
from bs4 import BeautifulSoup

# centro
# 4003
# 4028
# 4108

# 4061

# Guaymallen
# 4115
# 4136
# 4133

# metodos de pago
# cheque en sus distintas denominaciones
# pagaré
# Factura C no tiene IVA
# preguntas, dudas, sugerencias

import time
# from datetime import datetime

# https://requests.readthedocs.io/en/latest/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

start_time = time.time()
# script_start_time = datetime.now()

def trim(text):
    return re.sub("\s+", " ", text.strip())

def getTableData(table):
    # Get all th of the row
    th = table.thead.tr.find_all("th")

    # Get all headers
    table_header = [trim(i.text).upper() for i in th]

    # Get all td of the row
    td = table.tbody.tr.find_all("td")

    # Get all values
    table_data = [trim(i.text) for i in td]

    # Convert lists to dictionary
    return dict(zip(table_header, table_data))

def main():

    url = "https://bases.mendoza.edu.ar/intranet2/portal_con_esc2.asp"
    
    data = {
        "formulario": "busqueda",
        "escnro": "",
        "cue": "",
        "nombre": "",
        "button": "Buscar+..."
    }

    school = {}
    school_numbers = []
    filename = "vacantes-area06-ingreso-2022"
    # filename = "depja-vacantes-ingreso-2022"

    with open(filename + ".csv", "r") as csvfile:

        reader = csv.DictReader(csvfile)
        
        with open(filename + ".tsv", "w") as tsvfile:

            fieldnames = ["ZONA","NUM. ESC.","NOM. ESC.","DOMICILIO ESC.","DEPARTAMENTO","CURSO","DIVISION","TURNO","HORAS","MA","MATERIA","DESI/ORI","BI"]

            writer = csv.writer(tsvfile, delimiter="\t")
            
            writer.writerow(fieldnames)

            try:
                for row in reader:

                    data["escnro"] = row["NUM. ESC."].replace("-", "")

                    if data["escnro"] not in school_numbers:

                        # Init post request
                        response = requests.post(url, data)

                        # Response encoding
                        response.encoding = "utf-8"

                        # Init soup
                        soup = BeautifulSoup(response.text, "lxml")

                        # Get table element by id
                        table = soup.find(id="example2")

                        school = getTableData(table)

                        # Write row
                        writer.writerow(
                            [row["ZONA"], row["NUM. ESC."], school["NOMBRE"], school["DOMICILIO"], row["DEPARTAMENTO"], row["CURSO"],
                            row["DIVISION"], row["TURNO"], row["HORAS"], row["MA"], row["MATERIA"], row["DESI/ORI"], row["BI"]]
                        )

                        # Add object to list
                        school_numbers.append(data["escnro"])
                    else:
                        # Write row
                        writer.writerow(
                            [row["ZONA"], row["NUM. ESC."], school["NOMBRE"], school["DOMICILIO"], row["DEPARTAMENTO"], row["CURSO"],
                            row["DIVISION"], row["TURNO"], row["HORAS"], row["MA"], row["MATERIA"], row["DESI/ORI"], row["BI"]]
                        )

            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

if __name__ == "__main__":
    main()

end_time = time.time()
# script_end_time = datetime.now()

final_time = end_time - start_time

print("### Total execution time:", round(final_time, 2), "seconds")