import streamlit as st
import pandas as pd
# Importar locale para tentar formatar datas, embora não seja estritamente necessário para esta lógica
import locale 

# Tentar configurar o locale para português (melhor para nomes de meses, se usado no futuro)
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252') # Windows
    except locale.Error:
        pass # Se falhar, usa o padrão do sistema

# Carregar e preparar os dados
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('dados_consolidados.csv')
        # Converter colunas de data, tratando possíveis erros
        data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce')
        data['completed_at'] = pd.to_datetime(data['completed_at'], errors='coerce')
        # Remover linhas onde a data de inscrição é inválida (NaT)
        data = data.dropna(subset=['created_at'])
        
        # --- Novas colunas para o filtro simplificado ---
        data['year'] = data['created_at'].dt.year
        # Criar uma coluna de data (sem hora) para o filtro de dia
        data['date_only'] = data['created_at'].dt.date
        
        return data
    except FileNotFoundError:
        st.error("Arquivo 'data/dados_consolidados.csv' não encontrado. Verifique o caminho.")
        return pd.DataFrame() # Retorna um DataFrame vazio para evitar mais erros

data = load_data()

# Título da aplicação
st.title('Visualizador de Projetos de Negócios do Paraná')

if not data.empty:
    # --- Filtro de Data de Inscrição Simplificado ---
    st.sidebar.header('Filtros')
    
    # 1. Filtro de Ano
    # Ordena os anos disponíveis, do mais recente para o mais antigo
    available_years = sorted(data['year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox(
        'Selecione o Ano da Inscrição:',
        available_years
    )
    
    # Filtrar dados pelo ano selecionado
    data_filtered_by_year = data[data['year'] == selected_year]
    
    # 2. Filtro de Dia (baseado no ano selecionado)
    # Pega apenas os dias únicos onde houve inscrições naquele ano
    available_dates = sorted(data_filtered_by_year['date_only'].unique())
    
    # DataFrame para os dados finais filtrados
    filtered_data = pd.DataFrame()
    
    if not available_dates:
        st.sidebar.warning(f"Não há dados de inscrição para o ano {selected_year}.")
    else:
        # Seletor para o dia exato
        selected_date = st.sidebar.selectbox(
            'Selecione o Dia da Inscrição:',
            available_dates,
            # Formata a data no seletor para ficar amigável (ex: 05/10/2023)
            format_func=lambda date: date.strftime('%d/%m/%Y') 
        )
        
        # Filtrar dados pela data exata selecionada
        if selected_date:
            mask = (data['date_only'] == selected_date)
            filtered_data = data[mask] # 'data' já contém 'date_only'
        
    # --- Seleção de Projeto (baseado nos dados filtrados) ---
    if not filtered_data.empty:
        project = st.selectbox(
            'Selecione um projeto (filtrado por data):', 
            filtered_data['proposal_id'].unique()
        )

        # Exibir informações do projeto selecionado (buscando do DataFrame original)
        if project:
            # Usamos o DataFrame 'data' original para obter todos os detalhes
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
                # Formatando as datas para exibição
                st.metric('Data de inscrição', project_data['created_at'].strftime('%d/%m/%Y') if pd.notna(project_data['created_at']) else 'N/A')
                st.metric('Data de Finalização', project_data['completed_at'].strftime('%d/%m/%Y') if pd.notna(project_data['completed_at']) else 'N/A')
            
            st.subheader('Informações da Empresa')
            st.write(f'**Nome da Empresa:** {project_data["company_name"]}')
            st.write(f'**Cidade:** {project_data["city_id"]}')
            st.write('**CNPJ**:', project_data["federal_tax_id"])
    else:
        # Se available_dates não estava vazio, significa que o filtro de dia não retornou nada
        if available_dates:
             st.warning("Nenhum projeto encontrado para a data selecionada.")
        # Se available_dates estava vazio, o aviso já foi dado na sidebar
else:
    st.error("Não foi possível carregar os dados para exibição.")

