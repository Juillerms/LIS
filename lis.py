import streamlit as st
import pandas as pd

st.set_page_config(layout="wide") # Utiliza mais espaço da tela

st.title("Exemplo de LIS (Longest Increasing Subsequence) com Passo a Passo")

st.markdown(
    """
    Este aplicativo demonstra o algoritmo de Programação Dinâmica para encontrar a
    Longest Increasing Subsequence (LIS) em uma sequência de números.
    Abaixo, você verá o detalhamento de cada passo do cálculo.
    """
)

# Mantém a última sequência válida em cache para repopular
if 'last_valid_sequence' not in st.session_state:
    st.session_state.last_valid_sequence = "3,10,2,1,20"

seq_input = st.text_area(
    "Insira a sequência de números (separados por vírgula)",
    st.session_state.last_valid_sequence
)

if st.button("Calcular LIS com Passo a Passo"):
    try:
        # Parse da sequência de entrada
        seq_str_list = [x.strip() for x in seq_input.split(',') if x.strip()]
        if not seq_str_list:
            st.warning("Por favor, insira uma sequência de números.")
            st.stop()

        seq = []
        for s_num in seq_str_list:
            if not s_num.lstrip('-').isdigit(): # Permite números negativos
                st.error(f"Entrada inválida: '{s_num}' não é um número inteiro. Por favor, use apenas números separados por vírgulas.")
                st.stop()
            seq.append(int(s_num))
        
        st.session_state.last_valid_sequence = seq_input # Salva a última sequência válida
        n = len(seq)

        if n == 0:
            st.warning("A sequência está vazia.")
            st.stop()

        # Inicialização dos arrays DP
        dp = [1] * n           # dp[i] = comprimento da LIS terminando em i
        prev = [-1] * n        # prev[i] = índice anterior na LIS até i

        all_steps_data = [] # Para armazenar os dados de cada passo i

        # Parte central do algoritmo: cálculo do dp
        for i in range(n):
            # Detalhes para o passo atual i
            current_step_details = {
                'i': i,
                'seq_i': seq[i],
                'initial_dp_i': 1, # dp[i] começa como 1
                'initial_prev_i': -1, # prev[i] começa como -1
                'comparisons': []
            }

            # Loop interno para comparações com elementos anteriores j < i
            for j in range(i):
                dp_i_before_this_j_comparison = dp[i] # Valor de dp[i] antes desta comparação específica

                condition1_seq_j_lt_seq_i = seq[j] < seq[i]
                # Avalia a condição 2 apenas se a condição 1 for verdadeira, para clareza na tabela
                condition2_dp_j_plus_1_gt_dp_i = (dp[j] + 1 > dp_i_before_this_j_comparison) if condition1_seq_j_lt_seq_i else None

                action_taken_str = "Nenhuma atualização"

                if condition1_seq_j_lt_seq_i and (dp[j] + 1 > dp[i]): # dp[i] aqui é o valor que pode ter sido atualizado por um j anterior
                    dp[i] = dp[j] + 1
                    prev[i] = j
                    action_taken_str = f"Atualizado: dp[{i}]={dp[i]}, prev[{i}]={prev[i]}"

                comparison_info = {
                    'j': j,
                    'seq_j': seq[j],
                    'dp_j': dp[j], # Este é o dp[j] finalizado de passos anteriores de i
                    'dp_i_before_check': dp_i_before_this_j_comparison,
                    'condition1_eval_str': f"{seq[j]} < {seq[i]} -> {condition1_seq_j_lt_seq_i}",
                    'condition1_bool': condition1_seq_j_lt_seq_i,
                    'condition2_eval_str': (f"{dp[j]+1} > {dp_i_before_this_j_comparison} -> {condition2_dp_j_plus_1_gt_dp_i}"
                                            if condition1_seq_j_lt_seq_i else "N/A (condição 1 não atendida)"),
                    'condition2_bool': condition2_dp_j_plus_1_gt_dp_i,
                    'action': action_taken_str
                }
                current_step_details['comparisons'].append(comparison_info)

            current_step_details['final_dp_i'] = dp[i]
            current_step_details['final_prev_i'] = prev[i]
            current_step_details['dp_array_snapshot'] = list(dp) # Cópia do array dp
            current_step_details['prev_array_snapshot'] = list(prev) # Cópia do array prev
            all_steps_data.append(current_step_details)

        st.divider()
        st.header("Passo a Passo da Computação do DP")

        for step_data in all_steps_data:
            i = step_data['i']
            st.subheader(f"Passo {i + 1}: Processando elemento seq[{i}] = {step_data['seq_i']}")
            st.markdown(f"Valores iniciais para este elemento: `dp[{i}] = {step_data['initial_dp_i']}`, `prev[{i}] = {step_data['initial_prev_i']}`")

            if not step_data['comparisons']:
                st.markdown("Nenhuma comparação interna (este é o primeiro elemento da sequência ou não há elementos anteriores).")
            else:
                st.markdown("**Comparações com elementos anteriores (`seq[j]`):**")
                comparison_df_list = []
                for comp in step_data['comparisons']:
                    comparison_df_list.append({
                        'j': comp['j'],
                        'seq[j]': comp['seq_j'],
                        'dp[j]': comp['dp_j'],
                        f'Condição 1: seq[j] < seq[{i}]?': comp['condition1_eval_str'],
                        f'Condição 2: dp[j]+1 > dp[{i}] (atual)?': comp['condition2_eval_str'],
                        'Ação Tomada / Resultado': comp['action']
                    })
                st.table(pd.DataFrame(comparison_df_list))

            st.markdown(f"**Valores finais para `seq[{i}]` após todas as comparações:** `dp[{i}] = {step_data['final_dp_i']}`, `prev[{i}] = {step_data['final_prev_i']}`")

            st.markdown(f"**Estado dos arrays `dp` e `prev` após o Passo {i+1}:**")
            current_arrays_df = pd.DataFrame({
                'Índice (k)': list(range(n)),
                'Valor (seq[k])': seq,
                'dp[k]': step_data['dp_array_snapshot'],
                'prev[k]': step_data['prev_array_snapshot']
            })
            st.dataframe(current_arrays_df)
            st.markdown("---") # Separador visual

        st.divider()
        st.header("Tabela de Computação Final do DP")
        final_df = pd.DataFrame({
            'Índice': list(range(n)),
            'Valor (seq[k])': seq,
            'Comprimento LIS (dp[k])': dp, # dp final
            'Índice Anterior (prev[k])': prev # prev final
        })
        st.dataframe(final_df)

        # Reconstrução da subsequência crescente máxima
        if not dp: # Caso de sequência vazia já tratado, mas para segurança
            length = 0
            lis = []
        else:
            length = max(dp) if dp else 0
            lis = []
            if length > 0:
                idx = dp.index(length)
                while idx != -1:
                    lis.append(seq[idx])
                    idx = prev[idx]
                lis.reverse()

        st.divider()
        st.header(f"Resultado Final")
        st.subheader(f"Comprimento da LIS: {length}")
        st.subheader("Subsequência Crescente Máxima Encontrada:")
        if lis:
            st.success(f"**{lis}**")
        else:
            st.info("Nenhuma subsequência crescente encontrada (ou sequência vazia).")

    except ValueError as ve: # Erro específico para conversão de int
        st.error(f"Erro de valor na entrada: {ve}. Certifique-se de que todos os números são inteiros válidos.")
    except Exception as e:
        st.error(f"Erro ao processar a entrada: {e}")
        st.exception(e) # Mostra o traceback para debugging

# Instruções para executar (se necessário, como comentário no final do script)
# Para executar:
# 1. Salve como app.py (ou outro nome .py)
# 2. Instale dependências: pip install streamlit pandas
# 3. No terminal, navegue até a pasta do arquivo e rode: streamlit run app.py