import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import pycountry
import streamlit as st

df = pd.read_csv(
    "https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

# Dicionário de renomeação
novos_nomes = {
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda',
    'salary_in_usd': 'usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'modalidade_trabalho',
    'company_location': 'empresa',
    'company_size': 'tamanho_empresa'
}

# Aplicando renomeação
df.rename(columns=novos_nomes, inplace=True)

# Verificando resultado
print(df.head())

# Mudando os nomes das categorias de senioridade
# SE = Senior, MI = Mid-level, EN = Entry-level, EX = Executive
senioridade = {
    'SE': 'senior',
    'MI': 'pleno',
    'EN': 'junior',
    'EX': 'executivo'
}
df['senioridade'] = df['senioridade'].replace(senioridade)
print(df['senioridade'].value_counts())
# Mudando os nomes dos tipos de contrato
# FT = Full-time, PT = Part-time, CT = Contract, FL = Freelance
contrato = {
    'FT': 'integral',
    'PT': 'parcial',
    'CT': 'contrato',
    'FL': 'freelancer'
}
df['contrato'] = df['contrato'].replace(contrato)
df['contrato'].value_counts()

# Mudando os nomes dos tamanhos de empresa
# L = Large, S = Small, M = Medium
tamanho_empresa = {
    'L': 'grande',
    'S': 'pequena',
    'M':	'media'

}
df['tamanho_empresa'] = df['tamanho_empresa'].replace(tamanho_empresa)
df['tamanho_empresa'].value_counts()

# Mudando os nomes dos tipos de trabalho remoto
# 0 = Presencial, 100 = Remoto, 50 = Híbrido
mapa_trabalho = {
    0: 'presencial',
    100: 'remoto',
    50: 'hibrido'
}

df['modalidade_trabalho'] = df['modalidade_trabalho'].replace(mapa_trabalho)
df['modalidade_trabalho'].value_counts()
print(df.head())

# Preparação e limpeza dos Dados

print(df.isnull().sum())

print(df['ano'].unique())

print(df[df.isnull().any(axis=1)])

df_limpo = df.dropna()

df_limpo.isnull().sum()

df_limpo = df_limpo.assign(ano=df_limpo['ano'].astype('Int64'))

df_limpo.to_csv('dados-imersao.csv', index=False)

print(df_limpo.head())

# Criação de Dashboards
senioridade_media_salario = df_limpo.groupby(
    'senioridade')['usd'].mean().sort_values(ascending=False).reset_index()

fig = px.bar(senioridade_media_salario,
             x='senioridade',
             y='usd',
             title='Média Salarial por Senioridade',
             labels={'senioridade': 'Nível de Senioridade', 'usd': 'Média Salarial (USD)'})
fig.write_html('media_salarial_por_senioridade.html')

remoto_contagem = df_limpo['modalidade_trabalho'].value_counts().reset_index()
remoto_contagem.columns = ['tipo_trabalho', 'quantidade']

fig = px.pie(remoto_contagem,
             names='tipo_trabalho',
             values='quantidade',
             title='Proporção dos tipos de trabalho',
             hole=0.5
             )
fig.update_traces(textinfo='percent+label')
fig.write_html('proporcao_trabalho.html')

df_data_scientist = df_limpo[df_limpo['cargo'] == 'Data Scientist']
salarios_por_pais = df_data_scientist.groupby(
    'residencia')['usd'].mean().sort_values(ascending=False).reset_index()

fig = px.bar(salarios_por_pais,
             x='residencia',
             y='usd',
             title='Média Salarial de Data Scientists por País',
             labels={'residencia': 'País', 'usd': 'Média Salarial (USD)'})

fig.write_html('media_salarial_data_scientist.html')

# Função para converter ISO-2 para ISO-3


def iso2_to_iso3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None


# Criar nova coluna com código ISO-3 no DataFrame limpo
df_limpo['residencia_iso3'] = df_limpo['residencia'].apply(iso2_to_iso3)
# O DataFrame principal para o Streamlit deve ser o df_limpo, que já foi preparado
df = df_limpo

# MAPA MUNDI SALARIO DATA SCIENTIST POR PAIS
# Calcular média salarial por país (ISO-3)
df_ds = df_limpo[df_limpo['cargo'] == 'Data Scientist']
media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()

# Gerar o mapa
fig = px.choropleth(media_ds_pais,
                    locations='residencia_iso3',
                    color='usd',
                    color_continuous_scale='rdylgn',
                    title='Salário médio de Cientista de Dados por país',
                    labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
fig.write_html('media_ds_pais.html')

# MAPA MUNDI SALARIO SOFTWARE ENGINEER POR PAIS
# Calcular média salarial por país (ISO-3)
df_se = df_limpo[df_limpo['cargo'] == 'Software Engineer']
media_se_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()

# Gerar o mapa
fig = px.choropleth(media_se_pais,
                    locations='residencia_iso3',
                    color='usd',
                    color_continuous_scale='rdylgn',
                    title='Salário médio de Engenheiro de Software por país',
                    labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
fig.write_html('media_se_pais.html')

# MAPA MUNDI SALARIO SOFTWARE ENGINEER POR PAIS
# Calcular média salarial por país (ISO-3)
df_pm = df_limpo[df_limpo['cargo'] == 'Product Manager']
media_se_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()

# Gerar o mapa
fig = px.choropleth(media_se_pais,
                    locations='residencia_iso3',
                    color='usd',
                    color_continuous_scale='rdylgn',
                    title='Salário médio de Product Manager por país',
                    labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
fig.write_html('media_pm_pais.html')

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect(
    "Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect(
    "Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect(
    "Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# Filtro de Residência
residencias_disponiveis = sorted(
    [code for code in df['residencia_iso3'].unique() if code is not None])
residencias_selecionados = st.sidebar.multiselect(
    "Residências", residencias_disponiveis, default=residencias_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados)) &
    (df['residencia_iso3'].isin(residencias_selecionados))
]

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio = 0
    salario_mediano = 0  # ou None, se preferir
    salario_maximo = 0
    total_registros = 0
    cargo_mais_frequente = ""  # Use o mesmo nome da variável que está no bloco 'if'

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(
            10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(
            title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['modalidade_trabalho'].value_counts(
        ).reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')[
            'usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
                                       locations='residencia_iso3',
                                       color='usd',
                                       color_continuous_scale='rdylgn',
                                       title='Salário médio de Cientista de Dados por país',
                                       labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
