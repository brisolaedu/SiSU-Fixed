from functions import get_universidades, get_campi, get_cursos, get_results
from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = "0123456789"

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    session["estado"] = None
    session["universidade"] = None
    session["campus"] = None
    session["curso"] = None

    if request.method == "POST":
        estado = request.form.get("estado")
        session["estado"] = str(estado)
        return redirect("/estado")

    else:
        return render_template("estados.html")
    

@app.route("/estado", methods=["GET", "POST"])
def estado():
    estado = session.get("estado")
    universidade = session.get("universidade")
    campus = session.get("campus")
    curso = session.get("curso")

    universidades = None
    campi = None
    cursos = None

    if estado:
        universidades = get_universidades(estado)
    if universidade and estado:
        campi = get_campi(universidade, estado)
    if universidade and estado and campus:
        cursos = get_cursos(campus, universidade, estado)
    if curso and campus and universidade and estado:
        return redirect("/results")

    selected_university = universidade
    selected_campus = campus
    selected_curso = curso

    if request.method == "POST":
        if "back" in request.form:   
            if session.get("curso"):
                session["curso"] = None
                return redirect("/estado")
            elif session.get("campus"):
                session["campus"] = None
                return redirect("/estado")
            elif session.get("universidade"):
                session["universidade"] = None
                return redirect("/estado")
            
            session["estado"] = None
            session["universidade"] = None
            session["campus"] = None
            session["curso"] = None

            return redirect("/")  

        elif "submit1" in request.form:  
            selected_university = request.form.get("university").strip("--").lower()
            session["universidade"] = selected_university
            return redirect("/estado")
        
        elif "submit2" in request.form:
            selected_campus = request.form.get("campus").strip("--")
            session["campus"] = selected_campus
            return redirect("/estado")
        
        elif "submit3" in request.form:
            selected_curso = request.form.get("curso").strip("--")
            session["curso"] = selected_curso
            return redirect("/estado")

    return render_template(
        "busca.html", 
        universidades=universidades, 
        campi=campi, cursos=cursos, 
        selected_university=selected_university, 
        selected_campus=selected_campus, 
        selected_curso=selected_curso
    )


@app.route("/results", methods=["GET", "POST"])
def results():
    estado = session.get("estado")
    universidade = session.get("universidade")
    campus = session.get("campus")
    curso = session.get("curso")

    resultados, info = get_results(curso, campus, universidade, estado)

    if request.method == "POST":
        if "back" in request.form: 
            session["curso"] = None
            return redirect("/estado")  
    
    return render_template("resultados.html", resultados=resultados, info=info)


if __name__ == "__main__":
    app.run(debug=True)
