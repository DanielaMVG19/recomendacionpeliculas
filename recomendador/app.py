"""Recomendador escolar"""
import json
import os
from pathlib import Path
from flask import Flask, render_template, request

app = Flask(__name__, static_folder="public", static_url_path="")
NOMBRE = os.getenv("NOMBRE_ALUMNA", "Daniela Marlen Varilla Garcia ^^!")
GENEROS = ("Drama", "Comedia", "Musical", "Crimen")
CATALOGO = json.loads(Path(__file__).with_name("peliculas.json").read_text(encoding="utf-8"))


def grupo_edad(edad):
    """Devuelve una de las tres categorías del ejercicio."""
    if edad < 2:
        raise ValueError("Ingresa una edad de 2 años o más.")
    if edad <= 12:
        return "2 a 12"
    if edad <= 17:
        return "13 a 17"
    return "18 o más"


def recomendar(edad, genero):
    grupo = grupo_edad(edad)
    if genero not in GENEROS:
        raise ValueError("Selecciona un género válido.")
    return [p for p in CATALOGO if p["grupo"] == grupo and p["genero"] == genero]


@app.route("/", methods=["GET", "POST"])
def inicio():
    edad_texto, genero = "", ""
    peliculas, error, grupo = [], None, None
    if request.method == "POST":
        edad_texto = request.form.get("edad", "").strip()
        genero = request.form.get("genero", "")
        try:
            edad = int(edad_texto)
            grupo = grupo_edad(edad)
            peliculas = recomendar(edad, genero)
        except ValueError as exc:
            error = str(exc) if not edad_texto or edad_texto.lstrip("-").isdigit() else "Escribe tu edad con un número entero."
            if not edad_texto:
                error = "Escribe tu edad para continuar."
        except (OverflowError, TypeError):
            error = "Escribe una edad válida."
    return render_template("index.html", nombre=NOMBRE, generos=GENEROS,
                           edad=edad_texto, genero=genero, peliculas=peliculas,
                           error=error, grupo=grupo, enviado=request.method == "POST")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
