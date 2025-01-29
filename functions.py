import os, csv

def get_universidades(estado: str) -> list[str]:
    path = f"C://Users//HP Victus//Desktop//Python//testes//31-45//test_41_sisu//documents//{estado}"
    path = os.listdir(path)

    universidades: list[str] = []

    for universidade in path:
        universidades.append(universidade.split(".")[0].upper())

    universidades.sort()

    return universidades


def get_campi(universidade: str, estado: str) -> list[str]:
    path = f"documents//{estado}//{universidade}.csv"

    campi: list[str] = []

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            if row["NO_CAMPUS"] not in campi:
                campi.append(row["NO_CAMPUS"])

    campi.sort()

    return campi


def get_cursos(campus: str, universidade: str, estado: str) -> list[str]:
    path = f"documents//{estado}//{universidade}.csv"

    cursos: list[str] = []

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            if row["NO_CURSO"] not in cursos and row["NO_CAMPUS"] == campus:
                cursos.append(row["NO_CURSO"])

    cursos.sort()

    return cursos


def get_results(curso: str, campus: str, universidade: str, estado: str) -> dict:
    path = f"documents//{estado}//{universidade}.csv"

    resultados: dict = {}

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            if row["TIPO_CONCORRENCIA"] not in resultados:
                resultados[row["TIPO_CONCORRENCIA"]] = {}

            if row["NO_INSCRITO"] and row["NO_CAMPUS"] == campus and row["NO_CURSO"] == curso:
                resultados[row["TIPO_CONCORRENCIA"]][row["NO_INSCRITO"]] = {"NU_CLASSIFICACAO": int(row["NU_CLASSIFICACAO"]), "NU_NOTA_CANDIDATO": row["NU_NOTA_CANDIDATO"]}

    sorted_data = {}

    for category, candidates in resultados.items():
        sorted_data[category] = dict(sorted(candidates.items(), key=lambda item: item[1]["NU_CLASSIFICACAO"]))
    
    return sorted_data
                