import streamlit as st

EUROPEAN_ROULETTE = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10,
    5, 24, 16, 33, 1, 20, 14, 31,
    9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎰 Modelo Condicional Ruleta Europea")

num = st.number_input("Número (0–36)", 0, 36, step=1)

if st.button("Agregar"):
    st.session_state.history.append(num)

history = st.session_state.history
st.write("Últimos 6 números:", history[-6:])

def vecinos_extendidos(n):
    idx = EUROPEAN_ROULETTE.index(n)
    vecinos = set()
    for i in range(-3, 4):
        vecinos.add(EUROPEAN_ROULETTE[(idx + i) % len(EUROPEAN_ROULETTE)])
    return vecinos

def ultimas_apariciones(num, history, k=3):
    idxs = [i for i in range(len(history)-1) if history[i] == num]
    return idxs[-k:]

if len(history) >= 51:
    st.subheader("🔍 Análisis activo")

    last_number = history[-1]
    vecinos = vecinos_extendidos(last_number)

    st.write("Último número:", last_number)
    st.write("Vecinos extendidos:", vecinos)

    candidatos = history[-6:-1]

    st.divider()

    for n in reversed(candidatos):
        idxs = ultimas_apariciones(n, history)

        if len(idxs) < 3:
            continue

        siguientes = [history[i+1] for i in idxs]

        coincidencias = [x for x in siguientes if x in vecinos]
        faltantes = [x for x in siguientes if x not in coincidencias]

        if coincidencias:
            st.markdown(f"### ✅ Coincidencia con {n}")
            st.write("Números posteriores:", siguientes)
            st.write("Coinciden con vecinos:", coincidencias)
            st.write("❗ Faltan por aparecer:", faltantes)
def vecinos_ruleta(num, rango=2):
    idx = EUROPEAN_ROULETTE.index(num)
    vecinos = set()
    for i in range(-rango, rango + 1):
        vecinos.add(EUROPEAN_ROULETTE[(idx + i) % len(EUROPEAN_ROULETTE)])
    return vecinos

if len(history) >= 10:
    st.subheader("🔥 Terminales calientes (últimos 10 tiros)")

    ultimos_10 = history[-10:]

    # Agrupar por terminal
    terminales = {}
    for n in ultimos_10:
        t = n % 10
        terminales.setdefault(t, []).append(n)

    scores = {}

    for terminal, nums in terminales.items():
        score = 0
        for n in nums:
            vecinos = vecinos_ruleta(n, 2)
            score += sum(1 for x in ultimos_10 if x in vecinos)
        scores[terminal] = score

    max_score = max(scores.values())
    calientes = {t: s for t, s in scores.items() if s >= max_score - 1}

    st.write("Últimos 10 números:", ultimos_10)

    for t, s in calientes.items():
        st.markdown(f"### 🔥 Terminal {t}")
        st.write("Score térmico:", s)
        st.write("Números:", terminales[t])
