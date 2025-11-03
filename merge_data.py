import pandas as pd
import os

# Diretório onde os arquivos CSV estão localizados
data_dir = 'data'

# Nomes dos arquivos a serem carregados
files_to_load = {
    'proposal': 'Proposal_Data_proposal.csv',
    'project': 'Proposal_Data_proposal_project.csv',
    'company': 'Proposal_Data_proposal_project_company.csv',
    'address': 'Proposal_Data_proposal_address.csv',
    'benefit': 'Proposal_Data_proposal_benefit.csv',
    'contact': 'Proposal_Data_proposal_contact.csv',
    'multimedia': 'Proposal_Data_proposal_multimedia.csv',
    'benefit_address': 'Proposal_Data_proposal_benefit_address.csv'
}

# Carregar os dataframes
dataframes = {}
for key, filename in files_to_load.items():
    path = os.path.join(data_dir, filename)
    try:
        dataframes[key] = pd.read_csv(path)
        print(f"Arquivo {filename} carregado com sucesso.")
    except FileNotFoundError:
        print(f"Aviso: Arquivo {filename} não encontrado. Pulando.")
        dataframes[key] = pd.DataFrame()

# 1. Começar com 'project' como base
merged_df = dataframes.get('project', pd.DataFrame())

# 2. Merge com 'proposal'
if not dataframes.get('proposal', pd.DataFrame()).empty:
    merged_df = pd.merge(
        merged_df,
        dataframes['proposal'],
        left_on='proposal_id',
        right_on='id',
        how='left',
        suffixes=('_project', '_proposal')
    )

# 3. Merge com 'company'
if not dataframes.get('company', pd.DataFrame()).empty:
    merged_df = pd.merge(
        merged_df,
        dataframes['company'],
        on='project_id',
        how='left',
        suffixes=('', '_company')
    )

# 4. Merge com 'address'
if not dataframes.get('address', pd.DataFrame()).empty:
    merged_df = pd.merge(
        merged_df,
        dataframes['address'],
        left_on='proposal_id',
        right_on='proposal_id',
        how='left',
        suffixes=('', '_address')
    )

# 5. Merge com 'benefit'
if not dataframes.get('benefit', pd.DataFrame()).empty:
    merged_df = pd.merge(
        merged_df,
        dataframes['benefit'],
        left_on='proposal_id',
        right_on='proposal_id',
        how='left',
        suffixes=('', '_benefit')
    )

# 6. Merge com 'contact'
if not dataframes.get('contact', pd.DataFrame()).empty:
    merged_df = pd.merge(
        merged_df,
        dataframes['contact'],
        on='proposal_id',
        how='left',
        suffixes=('', '_contact')
    )


# 8. Merge com 'benefit_address'
if not dataframes.get('benefit_address', pd.DataFrame()).empty and 'id_benefit' in merged_df.columns:
    merged_df = pd.merge(
        merged_df,
        dataframes['benefit_address'],
        left_on='id_benefit',
        right_on='benefit_id',
        how='left',
        suffixes=('', '_benefit_address')
    )

# Limpeza e seleção de colunas
# Remover colunas de ID duplicadas e desnecessárias
cols_to_drop = [col for col in merged_df.columns if col.endswith('_proposal') or col == 'id_company' or col == 'id_address' or col == 'id_benefit' or col == 'id_contact' or col == 'id_multimedia']
merged_df.drop(columns=cols_to_drop, inplace=True, errors='ignore')


# Salvar o resultado
output_path = os.path.join(data_dir, 'dados_consolidados.csv')
merged_df.to_csv(output_path, index=False)

print(f"\nMerge concluído! Os dados foram salvos em '{output_path}'")
print("\nVisualizando as 5 primeiras linhas do resultado:")
print(merged_df.head())