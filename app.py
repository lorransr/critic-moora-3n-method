from io import StringIO
from typing import List
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from method import apply_method

if 'init' not in st.session_state: st.session_state['init']=False
if 'store_d' not in st.session_state: st.session_state['store_d']={}
if 'store_a' not in st.session_state: st.session_state['store_a']=[]
if 'edit' not in st.session_state: st.session_state['edit']=True

if st.session_state.init == False:
    st.session_state.store_d = None
    st.session_state.init = True

# @st.cache(allow_output_mutation=True)
def fetch_data():
    if st.session_state.store_d is not None:
        return pd.DataFrame.from_dict(st.session_state.store_d)
    else:
        return get_df()

def get_df():
    df_method = st.selectbox("selecione uma opção",["formulario","csv"])
    if df_method == "formulario":
        return get_df_from_form()
    elif df_method == "csv":
        return get_df_from_csv()

def get_df_from_csv():
    uploaded_file = st.file_uploader("Selecione o arquivo csv compativel")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = df.set_index("alternatives")
        st.session_state.store_a = list(df.index)
        return df

def get_df_from_form():
    with st.form("meu_form"):
        n_alternativas = st.number_input("n de alternativas",min_value=2,step=1)
        n_criterios = st.number_input("n de criterios",min_value=2,step=1)
        nome_alternativas = st.text_input("nome alternativas separado por virgula")
        nome_criterios = st.text_input("nome criterios separado por virgula")
        submitted = st.form_submit_button("submit")
        if submitted:
            nome_alternativas = nome_alternativas.split(",")
            nome_criterios = nome_criterios.split(",")
            # nome_alternativas = [f"a{index}" for index in range(n_alternativas)]
            st.session_state.store_a = nome_alternativas
            # nome_criterios = [f"c{index}" for index in range(n_criterios)]
            return get_matrix_from_inputs(n_alternativas,n_criterios,nome_alternativas,nome_criterios)



def get_matrix_from_inputs(n_alternativas,n_criterios,nome_alternativas,nome_criterios):
    matrix = np.zeros((n_alternativas,n_criterios))
    df = pd.DataFrame(matrix,index = nome_alternativas,columns=nome_criterios)
    st.session_state.store_d = df.to_dict()
    print(df.to_dict())
    return df

def record_df(df):
    ag = AgGrid(df, editable=st.session_state.edit, height=200)
    df2=ag['data']
    df2.index = st.session_state.store_a
    st.session_state.store_d=df2.to_dict()
    return df2

def validate_criteria_type(criteria_type:List[str],df:pd.DataFrame) -> bool:
    is_same_len = len(criteria_type) == len(df.columns)
    is_max_or_min = True
    for criteria in criteria_type:
        if criteria not in ["MAX","MIN"]:
            is_max_or_min = False
            break
    return is_same_len and is_max_or_min

def criteria_type_form(decision_matrix):
    st.subheader("Insira os tipos dos critérios")
    submitted = None
    with st.form("Tipos de Critérios"):
        st.write("bla bla")
        criteria_types = st.text_input("insira o tipo dos critérios (MAX ou MIN) em ordem separados por virgula").split(",")
        criteria_type_list= [c.strip() for c in criteria_types]
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submeter")
    return submitted,criteria_type_list

def app():
    st.title("Critic-moora-3n")
    st.header("Explicação do  método")
    st.image("https://images.unsplash.com/photo-1620295153878-8e6026f3be98?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2574&q=80")
    st.write("""
    escreve o seu textao aqui
    """)
    st.subheader("Insira a matriz de decisão")
    df = fetch_data()
    ranking = None
    if df is not None:
        decision_matrix = record_df(df)
        submitted,criteria_type_list = criteria_type_form(decision_matrix)
        if submitted:
            validated = validate_criteria_type(criteria_type_list,decision_matrix)
            if not validated:
                raise ValueError("Input de critérios incorreto")
            criteria_names = list(decision_matrix.columns)
            criteria_dict = dict(zip(criteria_names,criteria_type_list))
            ranking = apply_method(decision_matrix,criteria_dict)

    if ranking is not None:
        st.write(ranking)
        st.balloons()

if __name__ == '__main__':
    app()