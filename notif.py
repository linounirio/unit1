import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Notificacao', layout='wide')

base = pd.read_csv('notif_jan_jun_2022.csv')
kpi_infra = pd.DataFrame(round(base['regulamento'].value_counts()/len(base)*100,2))
infracoes = kpi_infra.loc[kpi_infra['count']>9].rename(columns={'count':'%'})
#infracoes.loc['outras infrações (somadas)']= (100 - float(infracoes.sum()))

def main():
    st.title("Painel de dados dos Primeiros 6 meses de 2022")
    st.markdown('---')
    fig= px.pie(infracoes,values='%',names=infracoes.index)
    col1,col2 = st.columns([0.6,0.4])

    with col2:
        atributo = st.selectbox(label='Escolha a opção',options=base.columns[:2], index=None, placeholder='Escolha a análise')
        
    if not atributo:
        col1.plotly_chart(fig)
    if atributo:
        opcao = col2.radio(label='Escolha qual opção', options=sorted(base[atributo].unique()), index=None)
        if not opcao:
            col1.markdown(f'### Aguardando a escolha do(a) **{atributo}**!!!')
            col1.image("image_espera.png",caption="Aguardando")
        if opcao:            
            df_base = base.loc[base[atributo]==opcao]
            kpi_infra = pd.DataFrame(round(df_base['regulamento'].value_counts()/len(base)*100,2)).rename(columns={'count':'%'})
            fig= px.pie(kpi_infra,values='%',names=kpi_infra.index)
            col1.plotly_chart(fig)

if __name__=='__main__':
    main()