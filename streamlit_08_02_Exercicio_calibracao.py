import streamlit as st
import pandas as pd

st.markdown("<h1 style='text-align: center;font-size:36px'><ins>CALIBRAÇÃO DE MANÔMETRO</ins></h1>", unsafe_allow_html=True)

def verif_calibracao(ent_aplicado_list, ent_leitura_asc_list, ent_leitura_des_list):
    st.write(ent_aplicado_list)
    st.write(ent_leitura_asc_list)
    st.write(ent_leitura_des_list)

def verif_aprovacao():
    
    if aprovado == 'Aprovado':
        resultado_aux.success('MANÔMETRO APROVADO', icon="✅")
        resultado.metric(label='MANÔMETRO :white_check_mark:', value=aprovado)
    elif aprovado == 'Reprovado' or num_medicoes<5: 
        resultado_aux.error('MANÔMETRO REPROVADO', icon="🔴")
        resultado.metric(label='MANÔMETRO :red_circle:', value=aprovado)
    if num_medicoes<5:
        resultado_menor_cinco.warning('FORNEÇA PELO MENOS 5 VALORES DE LEITURAS REALIZADAS', icon="⚠️")



with st.sidebar:
    st.title('ENTRADA DE DADOS')
    st.markdown("<h1 style='text-align: center;font-size:16px'>Range manômetro</h1>", unsafe_allow_html=True)
    menor_leitura, maior_leitura = st.columns(2)
    menor_leitura = menor_leitura.number_input('Manômetro: MENOR leit. possível', value=10)
    maior_leitura = maior_leitura.number_input('Manômetro: MAIOR leit. possível', value=160)

    st.markdown("<h1 style='text-align: center;font-size:16px'>Manômetro: especificações fabricante</h1>", unsafe_allow_html=True)
    exat_span, hist_span = st.columns(2)
    exat_span = exat_span.number_input('Manômetro: Exatidão %span (+-%)', value=0.4)
    hist_span = hist_span.number_input('Manômetro: Histerese %span (+-%)', value=1)

    st.markdown("<h1 style='text-align: center;font-size:16px'>Manômetro: valores aplicados x leitura</h1>", unsafe_allow_html=True)
    text_n_med, num_medicoes = st.columns(2)
    text_n_med = text_n_med.markdown("<h1 style='text-align: center;font-size:14px'>Selecione a quantidade de leituras realizadas</h1>", unsafe_allow_html=True)
    num_medicoes = num_medicoes.number_input('Selecione', value=1, min_value=1, step=1)


    num_medicoes = int(num_medicoes)
    ent_aplicado, ent_leitura_asc, ent_leitura_des = st.columns(3)
    ent_aplicado_list = []
    ent_leitura_asc_list = []
    ent_leitura_des_list = []
    for i in range(num_medicoes):
        Entrada1 = 'V_Aplicado_'+str(i+1)+'(psi)'
        Entrada2 = 'V_Leitura_asc_'+str(i+1)+'(psi)'
        Entrada3 = 'V_Leitura_des_'+str(i+1)+'(psi)'
        ent_aplicado_list.append(round(ent_aplicado.number_input(Entrada1), 2))
        ent_leitura_asc_list.append(round(ent_leitura_asc.number_input(Entrada2), 2))
        ent_leitura_des_list.append(round(ent_leitura_des.number_input(Entrada3), 2))
    b_verif_calib = st.button('VERIFICAR CALIBRAÇÃO')
    
#aprovado = 'Reprovado'
cond1 = False
cond2 = False

#########################################################
resultado_aux = st.empty()
resultado = st.empty() #Ver
resultado_menor_cinco = st.empty()


span_leit_monometro = maior_leitura - menor_leitura

psi_exat_span = (exat_span/100)*span_leit_monometro
psi_hist_span = (hist_span/100)*span_leit_monometro

per_apl_psi = []
leit_asc_erro_psi = []
leit_asc_span_per = []
leit_des_erro_psi = []
leit_des_span_per = []
hist_erro_psi = []
hist_span_per = []
hist_per = []
for i in range(num_medicoes):
    per_apl_psi.append(round((ent_aplicado_list[i] - menor_leitura)*100/span_leit_monometro, 2))
    leit_asc_erro_psi.append(round(ent_leitura_asc_list[i] - ent_aplicado_list[i], 2))
    leit_asc_span_per.append(round(leit_asc_erro_psi[i]*100/span_leit_monometro, 2))
    leit_des_erro_psi.append(round(ent_leitura_des_list[i] - ent_aplicado_list[i], 2))
    leit_des_span_per.append(round(leit_des_erro_psi[i]*100/span_leit_monometro, 2))
    hist_erro_psi.append(round(abs(leit_asc_erro_psi[i] - leit_des_erro_psi[i]), 2))
    hist_span_per.append(round(hist_erro_psi[i]*100/span_leit_monometro, 2))
    hist_per.append(round((leit_asc_erro_psi[i] - leit_des_erro_psi[i])*100/span_leit_monometro, 2))

tab_calib = []
tab_calib = pd.DataFrame(tab_calib)
tab_calib['Valor_aplicado'] = ent_aplicado_list
tab_calib['%_aplicado_psi'] = per_apl_psi
tab_calib['Leitura_ascendente'] = ent_leitura_asc_list
tab_calib['Leitura_ascendente_erro_psi'] = leit_asc_erro_psi
tab_calib['Leitura_ascendente_span_%'] = leit_asc_span_per
tab_calib['Leitura_descendente'] = ent_leitura_des_list
tab_calib['Leitura_descendente_erro_psi'] = leit_des_erro_psi
tab_calib['Leitura_descendente_span_%'] = leit_des_span_per
tab_calib['Histerese_erro_psi'] = hist_erro_psi
tab_calib['Histerese_span_%'] = hist_span_per
tab_calib['Histerese_%'] = hist_per


st.markdown("<h1 style='text-align: center;font-size:24px'><ins>TABELA DE CALIBRAÇÃO</ins></h1>", unsafe_allow_html=True)
st.write(tab_calib)

st.markdown("<h1 style='text-align: left;font-size:20px'><ins>LEITURA ASCENDENTE</ins></h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: left;font-size:16px'>Erro psi</h1>", unsafe_allow_html=True)
tit_mostrar_max_psi_asc, tit_mostrar_min_psi_asc = st.columns(2)
tit_mostrar_max_psi_asc.write('Máximo erro psi')
tit_mostrar_max_psi_asc.write(max(leit_asc_erro_psi))
tit_mostrar_min_psi_asc.write('Mínimo erro psi')
tit_mostrar_min_psi_asc.write(min(leit_asc_erro_psi))
st.markdown("<h1 style='text-align: left;font-size:16px'>Span %</h1>", unsafe_allow_html=True)
tit_mostrar_max_span_asc, tit_mostrar_min_span_asc = st.columns(2)
tit_mostrar_max_span_asc.write('Máximo span %')
tit_mostrar_max_span_asc.write(max(leit_asc_span_per))
tit_mostrar_min_span_asc.write('Mínimo span %')
tit_mostrar_min_span_asc.write(min(leit_asc_span_per))

st.markdown("<h1 style='text-align: left;font-size:20px'><ins>LEITURA DESCENDENTE</ins></h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: left;font-size:16px'>Erro psi</h1>", unsafe_allow_html=True)
tit_mostrar_max_psi_des, tit_mostrar_min_psi_des = st.columns(2)
tit_mostrar_max_psi_des.write('Máximo erro psi')
tit_mostrar_max_psi_des.write(max(leit_des_erro_psi))
tit_mostrar_min_psi_des.write('Mínimo erro psi')
tit_mostrar_min_psi_des.write(min(leit_des_erro_psi))
st.markdown("<h1 style='text-align: left;font-size:16px'>Span %</h1>", unsafe_allow_html=True)
tit_mostrar_max_span_des, tit_mostrar_min_span_des = st.columns(2)
tit_mostrar_max_span_des.write('Máximo span %')
tit_mostrar_max_span_des.write(max(leit_des_span_per))
tit_mostrar_min_span_des.write('Mínimo span %')
tit_mostrar_min_span_des.write(min(leit_des_span_per))


st.markdown("<h1 style='text-align: left;font-size:20px'><ins>RESULTADOS PARCIAIS</ins></h1>", unsafe_allow_html=True)
st.write('Máximo erro linear leitura ascentente')
max_erro_linear_asc = max(list(map(abs, leit_asc_span_per)))
st.write(max_erro_linear_asc)
st.write('Máximo erro linear leitura descentente')
max_erro_linear_des = max(list(map(abs, leit_des_span_per)))
st.write(max_erro_linear_des)
st.write('Máximo erro histerese')
max_erro_histerese_per = max(list(map(abs, hist_per)))
st.write(max_erro_histerese_per)

#cond1 = False
#cond2 = False
if max_erro_linear_asc < exat_span and num_medicoes>=5:
    cond1 = True
if max_erro_histerese_per < hist_span and num_medicoes>=5:
    cond2 = True
if num_medicoes<5:
    cond1 = False
    cond2 = False
if cond1 == True and cond2 == True:
    aprovado = 'Aprovado'
else:
    aprovado = 'Reprovado'
    
if b_verif_calib:
    verif_aprovacao()



##if aprovado == 'Aprovado':
##    st.write('Aprovado')
##    st.metric(label='MANÔMETRO', value='APROVADO', delta='-')
##elif (aprovado == False):
##    st.write('Reprovado')
##    st.metric(label='MANÔMETRO', value='REPROVADO', delta='-')
