from flask import Flask, flash, render_template, request, session
import pandas as pd
from prompting import format_dataframe, map_headers

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
    table_html = None
    if request.method == "POST":
        file = request.files.get("data_file")
        if file and file.filename:
            df = pd.read_csv(file)
            table_html = table_html = df.to_html(index=False, classes="table table-striped table-bordered")
    return render_template("produits_non_livres.html", table_html=table_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
