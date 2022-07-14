import csv, sys
import requests, re
from datetime import datetime
from bs4 import BeautifulSoup

def trim(text):
    return re.sub("\s+", " ", text.strip())

def f(s):
    arr = re.split("/", re.split(" ", s)[1])
    dt = datetime(int("20" + arr[2]), int(arr[1]), int(arr[0]))
    date = dt.strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d")
    return date >= now

def format_string(regex, text):
    arr = re.findall(regex, text)
    for i in arr:
        a = i[0:5] + " | " + i[5:]
        text = re.sub(i, a, text)
    return text

def getTableData(table):
    # Get all th of the row
    th = table.thead.tr.find_all("th")

    # Get all headers
    table_header = [trim(i.text).upper() for i in th]

    table_rows =table.tbody.find_all("tr")

    data = []

    for tr in table_rows:
        td = tr.find_all("td")
        table_data = [trim(i.text) for i in td]
        data.append(dict(zip(table_header, table_data)))

    return data

def main():

    URL = "https://educacionales.mendoza.edu.ar/"

    # Init post request
    response = requests.get(URL)

    # Response encoding
    response.encoding = "utf-8"

    # Init soup
    soup = BeautifulSoup(response.text, "lxml")

    # Get table element by id
    table = soup.find(id="example")

    data = getTableData(table)

    filename = "educacionales"

    with open(filename + ".tsv", "w") as tsvfile:

        fieldnames = ['PUBLICADO', 'NIVEL', 'DEPARTAMENTO', 'ESCUELA', 'ZONA', 'CARGO', 'HORAS', 'TURNO', 'MATERIA', 'LLAMADO', 'DOMICILIO ESCUELA', 'ARTICULO', 'CURSO', 'HORARIO', 'PRESENTARSE EN', 'PRIORIDAD', 'CONDICIONES', 'OBSERVACIONES', 'MOVILIDAD', 'ESTADO', 'MOTIVO DE CANCELACIÓN']
        
        writer = csv.writer(tsvfile, delimiter="\t")

        writer.writerow(fieldnames)

        try:
            for row in data:
                if not f(row["LLAMADO"]):
                    continue
                row["LLAMADO"] = format_string("\d+:\d+\w+:", row["LLAMADO"])
                row["PUBLICADO"] = format_string("\d+:\d+[c|C]", row["PUBLICADO"])
                
                writer.writerow([row["PUBLICADO"], row["NIVEL"], row["DEPARTAMENTO"], row["ESCUELA"], row["ZONA"], row["CARGO"], row["HORAS"], row["TURNO"], row["MATERIA"], row["LLAMADO"], row["DOMICILIO ESCUELA"], row["ARTICULO"], row["CURSO"], row["HORARIO"], row["PRESENTARSE EN"], row["PRIORIDAD"], row["CONDICIONES"], row["OBSERVACIONES"], row["MOVILIDAD"], row["ESTADO"], row["MOTIVO DE CANCELACIÓN"]])

        except csv.Error as e:
            
            sys.exit('file {}, line {}: {}'.format(filename, writer.line_num, e))

if __name__ == "__main__":
    main()