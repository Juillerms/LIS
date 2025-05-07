import streamlit as st
import pandas as pd

st.title("Exemplo de LIS (Longest Increasing Subsequence)")

st.markdown(
    "Este aplicativo demonstra o algoritmo de Programação Dinâmica para encontrar a Longest Increasing Subsequence (LIS)."
)

seq_input = st.text_area(
    "Insira a sequência de números (separados por vírgula)",
    "3,10,2,1,20"
)

if st.button("Calcular LIS"):
    try:
        # Parse da sequência de entrada
        seq = [int(x.strip()) for x in seq_input.split(',') if x.strip()]
        n = len(seq)

        # Inicialização dos arrays DP
        dp = [1] * n           # dp[i] = comprimento da LIS terminando em i
        prev = [-1] * n        # prev[i] = índice anterior na LIS até i

        # Parte central do algoritmo: cálculo do dp
        for i in range(n):
            for j in range(i):
                if seq[j] < seq[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    prev[i] = j

        # Reconstrução da subsequência crescente máxima
        length = max(dp)
        idx = dp.index(length)
        lis = []
        while idx != -1:
            lis.append(seq[idx])
            idx = prev[idx]
        lis.reverse()

        # Montagem de tabela para exibir passo a passo
        df = pd.DataFrame({
            'Índice': list(range(n)),
            'Valor': seq,
            'Comprimento LIS até aqui': dp,
            'Prev (índice anterior)': prev
        })

        st.subheader("Tabela de Computação do DP")
        st.dataframe(df)

        st.subheader(f"Comprimento da LIS: {length}")
        st.subheader("Subsequência Crescente Máxima Encontrada")
        st.write(lis)

    except Exception as e:
        st.error(f"Erro ao processar a entrada: {e}")

# Para executar:
# 1. Instale dependências: pip install streamlit pandas
# 2. Rode: streamlit run app.py
