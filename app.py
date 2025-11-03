
import streamlit as st
import pandas as pd

# Carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv('dados_consolidados.csv')
    return data

data = load_data()

# Título da aplicação
st.title('Visualizador de Projetos de Negócios do Paraná')

# Selecionar um projeto
project = st.selectbox('Selecione um projeto:', data['proposal_id'].unique())

# Exibir informações do projeto selecionado
if project:
    project_data = data[data['proposal_id'] == project].iloc[0]
    
    # Exibir informações
    st.subheader(project_data['name'])
    
    st.subheader('Descrição do Projeto')
    st.write(project_data['description_project'])
    
    st.subheader('Descrição do benefício')
    st.write(project_data['description_benefit'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Investimento Total', f'R$ {project_data["total"]:,.2f}')
        st.metric('Investimento Requerido', f'R$ {project_data["required_investment"]:,.2f}')
        st.metric('Tipo de projeto', project_data['type'])
        st.metric('Identificação do benefício', project_data['identification'])
    with col2:
        st.metric('Categoria', project_data['category'])
        st.metric('Status', project_data['status'])
        st.metric('Data de inscrição', project_data['created_at'])
        st.metric('Data de Finalização', project_data['completed_at'])
    
    st.subheader('Informações da Empresa')
    st.write(f'**Nome da Empresa:** {project_data["company_name"]}')
    st.write(f'**Cidade:** {project_data["city_id"]}')
    st.write('**CNPJ**:', project_data["federal_tax_id"])
    
   

