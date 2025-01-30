import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_universidades(estado: str) -> list[str]:
    path = os.path.join(BASE_DIR, "documents", estado)

    if not os.path.exists(path):
        return []

    universidades: list[str] = [
        f.split(".")[0].upper() for f in os.listdir(path) if f.endswith(".csv")
    ]

    return sorted(universidades)


def get_campi(universidade: str, estado: str) -> list[str]:
    path = os.path.join(BASE_DIR, "documents", estado, f"{universidade}.csv")

    if not os.path.exists(path):
        return []

    campi: set[str] = set()

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            campi.add(row["NO_CAMPUS"])

    return sorted(campi)


def get_cursos(campus: str, universidade: str, estado: str) -> list[str]:
    path = os.path.join(BASE_DIR, "documents", estado, f"{universidade}.csv")

    if not os.path.exists(path):
        return []

    cursos: set[str] = set()

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            if row["NO_CAMPUS"] == campus:
                cursos.add(row["NO_CURSO"])

    return sorted(cursos)


def get_results(curso: str, campus: str, universidade: str, estado: str) -> dict:
    path = os.path.join(BASE_DIR, "documents", estado, f"{universidade}.csv")

    if not os.path.exists(path):
        return {}

    resultados: dict = {}

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            if row["NO_CAMPUS"] == campus and row["NO_CURSO"] == curso:
                tipo_concorrencia = row["TIPO_CONCORRENCIA"]
                inscrito = row["NO_INSCRITO"]

                if tipo_concorrencia not in resultados:
                    resultados[tipo_concorrencia] = {}

                resultados[tipo_concorrencia][inscrito] = {
                    "NU_CLASSIFICACAO": int(row["NU_CLASSIFICACAO"]),
                    "NU_NOTA_CANDIDATO": row["NU_NOTA_CANDIDATO"],
                }

    sorted_data = {
        category: dict(
            sorted(candidates.items(), key=lambda item: item[1]["NU_CLASSIFICACAO"])
        )
        for category, candidates in resultados.items()
    }

    return sorted_data
