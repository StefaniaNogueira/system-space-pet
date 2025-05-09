import streamlit as st
import pandas as pd
from backend import (
    listar_clientes, listar_pets_por_cliente,
    listar_prontuarios_por_pet, editar_prontuario, excluir_prontuario
)

st.title("📖 Histórico de Prontuário")

# Selecionar cliente
clientes = listar_clientes()
cliente_opcao = st.selectbox("Selecione o Tutor", clientes, format_func=lambda x: x[1])

if cliente_opcao:
    cliente_id = cliente_opcao[0]
    pets = listar_pets_por_cliente(cliente_id)
    pet_opcao = st.selectbox("Selecione o Pet", pets, format_func=lambda x: x[2])

    if pet_opcao:
        pet_id = pet_opcao[0]
        st.markdown(f"#### Tutor: **{cliente_opcao[1]}** | Pet: **{pet_opcao[2]}**")

        prontuarios = listar_prontuarios_por_pet(pet_id)
        prontuarios = sorted(prontuarios, key=lambda x: x[1], reverse=True)

        if not prontuarios:
            st.info("Nenhum prontuário registrado para este pet.")
        else:
            for prontuario in prontuarios:
                prontuario_id, data, anamnese, tratamento, exames = prontuario
                try:
                    data_formatada = pd.to_datetime(data).strftime("%d/%m/%Y")
                except Exception:
                    data_formatada = "Data inválida"

                with st.expander(f"🗓️ Prontuário de {data_formatada}"):
                    st.markdown("### ✏️ Editar Prontuário")

                    nova_data = st.date_input(
                        "Data",
                        value=pd.to_datetime(data).date() if data_formatada != "Data inválida" else pd.to_datetime("today"),
                        key=f"data_{prontuario_id}"
                    )
                    novo_anamnese = st.text_area("Anamnese", anamnese, key=f"anamnese_{prontuario_id}")
                    novo_tratamento = st.text_area("Tratamento", tratamento, key=f"tratamento_{prontuario_id}")
                    novo_exames = st.text_area("Exames", exames, key=f"exames_{prontuario_id}")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("💾 Salvar Alterações", key=f"editar_{prontuario_id}"):
                            editar_prontuario(prontuario_id, str(nova_data), novo_anamnese, novo_tratamento, novo_exames)
                            st.success("Prontuário atualizado com sucesso.")
                            st.experimental_rerun()

                    with col2:
                        st.markdown("**Exclusão**")
                        confirmar = st.checkbox("Confirmar exclusão", key=f"confirmar_{prontuario_id}")
                        if st.button("🗑 Excluir Prontuário", key=f"excluir_{prontuario_id}") and confirmar:
                            excluir_prontuario(prontuario_id)
                            st.warning("Prontuário excluído.")
                            st.experimental_rerun()
