from flask import Flask, render_template, request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/produits-non-livres", methods=["GET", "POST"])
def produits_non_livres():
    if request.method == "POST":
        text = request.form.get("raw_text")
        print(text)
        return "Form submitted!"
    return render_template("produits_non_livres.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")  # no debug in production