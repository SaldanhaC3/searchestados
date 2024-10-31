import streamlit as st
import pandas as pd

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

# Configuração da interface
st.set_page_config(page_title="Busca por Capitais", layout="centered")

st.title("Busca por Capitais")
keyword = st.text_input("Digite a palavra-chave")

# Botão de busca
if st.button("Buscar") and keyword:
    results = []
    for _, row in capitals_df.iterrows():
        capital = row['Capital']
        tci = row['TCI']
        uule = row['UULE']
        search_url = build_search_url(keyword, tci, uule)
        results.append({"Capital": capital, "Link de Busca": search_url})

    # Exibindo resultados na tabela
    if results:
        results_df = pd.DataFrame(results)
        st.write(results_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        # Download dos resultados em CSV
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar resultados em CSV",
            data=csv,
            file_name="resultados_busca_capitais.csv",
            mime="text/csv",
        )
else:
    st.info("Digite uma palavra-chave e clique em 'Buscar' para ver os resultados.")
