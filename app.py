import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Horácios e Curiácios", layout="centered")
st.title("Jogo: Os Horácios e os Curiácios")

# Inicializa variáveis de sessão
if 'historico_curiacio' not in st.session_state:
    st.session_state.historico_curiacio = []
    st.session_state.vitorias_c = 0
    st.session_state.vitorias_h = 0
    st.session_state.empates = 0

def estado_inicial():
    pecas = {
        'C8': '🌹', 'D8': '🌹', 'E8': '🌹',
        'C7': '🗡️', 'D7': '🗡️', 'E7': '🗡️',
        'C6': '⚔️', 'D6': '⚔️', 'E6': '⚔️',
        'C1': '🌹', 'D1': '🌹', 'E1': '🌹',
        'C2': '🗡️', 'D2': '🗡️', 'E2': '🗡️',
        'C3': '⚔️', 'D3': '⚔️', 'E3': '⚔️'
    }
    donos = {}
    for pos in pecas:
        donos[pos] = 'C' if int(pos[1]) >= 6 else 'H'
    return pecas, donos

def gerar_movimentos_validos(origem, pecas, donos):
    tipo = pecas[origem]
    movimentos = []
    col0 = ord(origem[0])
    row0 = int(origem[1])
    alcance = 3 if tipo == '🌹' else 2 if tipo == '🗡️' else 1
    for dx in range(-alcance, alcance + 1):
        for dy in range(-alcance, alcance + 1):
            if dx == 0 and dy == 0:
                continue
            col = chr(col0 + dx)
            row = row0 + dy
            destino = col + str(row)
            if 'A' <= col <= 'G' and 1 <= row <= 8:
                if destino not in pecas or donos.get(destino) != donos[origem]:
                    movimentos.append(destino)
    return movimentos

def jogada_ia(dono, pecas, donos):
    melhor = None
    melhor_peso = -1
    for pos in list(pecas):
        if donos[pos] != dono:
            continue
        for destino in gerar_movimentos_validos(pos, pecas, donos):
            peso = random.random() + (1 if destino in pecas else 0)
            if peso > melhor_peso:
                melhor = (pos, destino)
                melhor_peso = peso
    if melhor:
        origem, destino = melhor
        pecas[destino] = pecas[origem]
        donos[destino] = donos[origem]
        del pecas[origem]
        del donos[origem]

def verificar_fim(pecas, donos):
    vivos_h = sum(1 for d in donos.values() if d == 'H')
    vivos_c = sum(1 for d in donos.values() if d == 'C')
    if vivos_h == 0:
        st.session_state.vitorias_c += 1
        st.session_state.historico_curiacio.append(st.session_state.vitorias_c)
        return 'C'
    elif vivos_c == 0:
        st.session_state.vitorias_h += 1
        return 'H'
    elif vivos_h == 1 and vivos_c == 1:
        st.session_state.empates += 1
        return 'E'
    return None

def simular_treinamento(n):
    for _ in range(n):
        pecas, donos = estado_inicial()
        for _ in range(20):
            jogada_ia('C', pecas, donos)
        verificar_fim(pecas, donos)

def plotar_grafico():
    fig, ax = plt.subplots()
    ax.plot(range(1, len(st.session_state.historico_curiacio)+1),
            st.session_state.historico_curiacio, marker='o', color='red')
    ax.set_title("Vitórias dos Curiácios")
    ax.set_xlabel("Treinamentos")
    ax.set_ylabel("Vitórias acumuladas")
    st.pyplot(fig)

# Botoes
col1, col2, col3 = st.columns(3)
if col1.button("📊 Treinamento 100 jogos"):
    simular_treinamento(100)

if col2.button("🔄 Reiniciar o Jogo"):
    st.session_state.vitorias_c = 0
    st.session_state.vitorias_h = 0
    st.session_state.empates = 0
    st.session_state.historico_curiacio = []

if col3.button("🧹 Zerar Treinamento"):
    st.session_state.vitorias_c = 0
    st.session_state.historico_curiacio = []

# Placar
total = st.session_state.vitorias_c + st.session_state.vitorias_h + st.session_state.empates
st.markdown(f"""
### Placar:
- 🔵 Horácios: {st.session_state.vitorias_h} 
- 🔴 Curiácios: {st.session_state.vitorias_c} 
- 🤝 Empates: {st.session_state.empates} 
- Total: {total}
""")

# Gráfico
plotar_grafico()
