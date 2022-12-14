import streamlit as st
import spacy
import spacy_streamlit
import numpy as np
import PIL


#import matplotlib.pyplot as plt

import pandas as pd
import ast

from numpy import math
from PIL import Image,ImageDraw
from spacy import displacy

image11 = Image.open('pipesegm.png')
path_pict = '/app/easyocrtable/tables/'
pictures_all = '/app/easyocrtable/pictures/'

st.markdown('''<h1 style='text-align: center; color: #F64A46;'
            >Распознавание таблиц с помощью Spacy.</h1>''',
            unsafe_allow_html=True)

st.write("""
Демонстрационная работа *"Распознавание таблиц с помощью библиотеки [Spacy](https://spacy.io/)"* позволяет продемонстрировать 
работу библиотеки с открытым исходным кодом для расширенной обработки естественного языка, написанной на языках программирования [Python](https://ru.wikipedia.org/wiki/Python) и [Cython](https://ru.wikipedia.org/wiki/Cython) для распознавания "сущностей" в тексте.
""") 


with st.expander("Общая схема"):
      st.image(image11)
      st.markdown(
        '''
        \n**Этапы:**
        \n1. База данных новостей:
        \nСодержит более 100 текстовых файлов типовых договоров купли, продажи, аренды, размещения вклада, банковского обслуживания и т.д.
        \n2. Библиотека слоев:
        \nСодержит набор слоев, используемых нейронной сетью.  [tensorflow](https://www.tensorflow.org/).
        \n3. Настройка модели:
        \nУстанавливается тип и количество слоев, а также количество нейронов в них.
        \n4. Обучение модели:
        \nВо время этого процесса нейросеть читает документы и обучается их воспроизводить.
        \n5. Проверка точности:
        \nНа этом этапе программист проверяет работу сети с помощью тестовых документов.
        \n6. Функция обработки текстового документа:
        \nПреобразует документ, который выдает нейронная сеть, в понятный для человека вид.
        \n7. Загрузка документа из нескольких предложенных:
        \nНа выбор студенту предлагается пять документов, которые можно отправить в нейронную сеть на обработку. В результате получается документ с выделенными цветными параграфами.
        \n8. Приложение Streamlit:
        \nОтображение документа.
        ''')
st.markdown('''<h1 style='text-align: center; color: black;'
            >Задача демонстрационной работы.</h1>''',
            unsafe_allow_html=True)
st.write('Нейронная сеть, представленная здесь, обучена выделять элементы текста и разделять их на категории (сущности).')
st.write('Вы можете выбрать любую таблицу из представленных в списке для распознавания.')
option1 = st.selectbox('Какой документ Вы выбираете?',('спецификация','спецификацияГОСТ','счет-фактура','товарная-накладная','платежная-ведомость'))
st.write('Вы выбрали документ - ' + option1)
st.write('Вот так выглядит документ')
st.image(pictures_all + option1 + '1.jpg')
st.write('Вот так его воспринимает программа (в виде таблицы). Пометка <NA> обозначает пустую ячейку.')            
full_path = path_pict+option1+'_1.xlsx'
data1 = pd.read_excel(full_path)
data1.to_csv('ttt.csv')
data2 = pd.read_csv('ttt.csv')

dataframe1 = st.table(data2.head(9))
st.write('Теперь попробуйте обнаружить в тексте ключевые элементы ("сущности") с помощью Spacy.')

is_clicked2 = st.button("Найти")
if is_clicked2:
            
            bounds = data2.values.tolist()      
            text1 = ''
            for i in range(len(bounds)):
                        for j in range(len(bounds[i])):
                                    if  bounds[i][j] :
                                                text1 = text1 + str(bounds[i][j]) + ','
            
            text2 = text1.split(',')           
            text3 = []
            for i in text2:
                        if i != "nan":
                                    text3.append(i)
            text4 = ''
            for i in text3:
                        text4 = text4 + i + ' '
            
            nlp1 = spacy.load('ru_core_news_sm')
            doc1 = nlp1(text4)
            
            ent_html = displacy.render(doc1, style="ent", jupyter=False)
                 
            st.markdown(ent_html, unsafe_allow_html=True)
