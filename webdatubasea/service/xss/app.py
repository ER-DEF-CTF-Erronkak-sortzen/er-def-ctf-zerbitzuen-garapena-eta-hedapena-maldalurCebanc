from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Almacenamiento temporal de comentarios
comments = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtiene el comentario del formulario
        comment = request.form.get("comment")
        # Agrega el comentario a la lista (sin filtrado de contenido)
        comments.append(comment)
        return redirect(url_for("index"))

    # Renderiza la página con los comentarios
    return render_template("index.html", comments=comments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)