from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Carregar o arquivo CSV com as capitais, códigos TCI e UULE atualizado
capitals_df = pd.read_csv("tci_capitais_brasil_completo_atualizado.csv")

# Função para construir a URL de busca com os parâmetros `tci` e `uule`
def build_search_url(keyword, tci, uule):
    base_url = "https://www.google.com.br/search"
    search_url = (
        f"{base_url}?q={keyword.replace(' ', '%20')}"
        f"&glp=1&adtest=on&hl=PT&tci=g:{tci}"
        f"&uule={uule}&cr=countryBR&safe=images"
    )
    return search_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        if not keyword:
            return redirect(url_for("index"))

        # Gerar a lista de links de busca para cada capital
        results = []
        for _, row in capitals_df.iterrows():
            capital = row['Capital']
            tci = row['TCI']
            uule = row['UULE']
            search_url = build_search_url(keyword, tci, uule)
            results.append({"capital": capital, "link": search_url})

        return render_template("index.html", keyword=keyword, results=results)

    return render_template("index.html", results=None)

if __name__ == "__main__":
    app.run(debug=True)
