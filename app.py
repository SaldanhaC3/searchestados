import streamlit as st
import pandas as pd

# Carregar o arquivo CSV com as capitais, TCI e UULE
capitals_df = pd.read_csv("tci_capitais_brasil_completo_atualizado.csv")

# Função para construir a URL de busca
def build_search_url(keyword, tci, uule):
    base_url = "https://www.google.com.br/search"
    search_url = (
        f"{base_url}?q={keyword.replace(' ', '%20')}"
        f"&glp=1&adtest=on&hl=PT&tci=g:{tci}"
        f"&uule={uule}&cr=countryBR&safe=images"
    )
    return search_url

# Configurações da página
st.set_page_config(page_title="Busca por Capitais", layout="centered")

# Título da página
st.title("Busca por Capitais")

# Campo de entrada para a palavra-chave
keyword = st.text_input("Digite a palavra-chave para a busca:")

# Verifica se uma palavra-chave foi inserida
if keyword:
    # Gerar a lista de links de busca para cada capital
    results = []
    for _, row in capitals_df.iterrows():
        capital = row['Capital']
        tci = row['TCI']
        uule = row['UULE']
        search_url = build_search_url(keyword, tci, uule)
        # Criar link clicável
        clickable_link = f"[Ver busca]({search_url})"
        results.append({"Capital": capital, "Link de Busca": clickable_link})
    
    # Exibir os resultados em uma tabela
    results_df = pd.DataFrame(results)
    st.write("### Resultados")
    st.write(results_df.to_markdown(), unsafe_allow_html=True)
    
    # Botão para download do CSV
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="resultados_busca_capitais.csv",
        mime="text/csv",
    )
