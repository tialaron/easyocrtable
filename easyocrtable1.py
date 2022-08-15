import streamlit as st
import spacy
import spacy_streamlit
import numpy as np
import PIL
import easyocr
import matplotlib.pyplot as plt
import cv2
import boxesdrawer
import ast

from PIL import Image,ImageDraw
from spacy import displacy

image11 = Image.open('pipesegm.png')
path_pict = '/app/easyocrtable/pictures/'

st.markdown('''<h1 style='text-align: center; color: #F64A46;'
            >Распознавание таблиц с помощью Spacy.</h1>''',
            unsafe_allow_html=True)

st.write("""
Лабораторная работа *"Распознавание таблиц с помощью библиотеки [Spacy](https://spacy.io/)"* позволяет продемонстрировать 
работу библиотеки с открытым исходным кодом для расширенной обработки естественного языка, написанной на языках программирования [Python](https://ru.wikipedia.org/wiki/Python) и [Cython](https://ru.wikipedia.org/wiki/Cython) для распознавания "сущностей" в тексте.
""")


with st.expander("Общая схема"):
      st.image(image11)
      st.markdown(
        '''
        \n**Этапы:**
        \n1. База данных типовых договоров:
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
            >Задача лабораторной работы.</h1>''',
            unsafe_allow_html=True)
st.write('Нейронная сеть, представленная здесь, обучена распзнавать документы в виде JPG файлов.')
st.write('Вы можете выбрать любой документ из представленных в списке для распознавания.')
option1 = st.selectbox('Какой документ Вы выбираете?',('ИНН','СНИЛС','полис','регистрация','договор'))
full_path = path_pict+option1+'_ЧБ.jpg'
img = Image.open(full_path)
st.image(full_path)
st.write('Теперь нужно разметить документ таким образом, чтобы выделить из него текст.')
st.write('Для этого нажмите на кнопку "Распознать" и дождитесь когда появится документ с выделенными участками текста')
is_clicked1 = st.button("Распознать")
if is_clicked1:
            image1 = open(full_path,'rb')
            f = image1.read()
            file_bytes = np.asarray(bytearray(f),dtype=np.uint8)
            bytearray_img = cv2.imdecode(file_bytes, 1)
            image1.close()
            reader1 = easyocr.Reader(['ru'])
            bounds = reader1.readtext(bytearray_img)
            image2 = boxesdrawer.draw_boxes(full_path, bounds)
            image2.save('out111.jpg')
            st.image('out111.jpg')
            file_list = open('bounds_list.txt', 'wt')
            file_list.write(str(bounds))
            file_list.close()

st.write('Далее необходимо сделать так, чтобы нейронка "поняла" текст и выделила в нем главное.')
st.write('Данную проблему обычно называют [NER-задачей](https://sysblok.ru/glossary/named-entity-recognition-ner/) или Named Entity Recognition.')
st.write('В ее решении может помочь библиотека [Spacy](https://spacy.io/). Это промышленная библиотека по выделению именованных сущностей из текста.')
st.write('Нажмите на кнопку "Найти" и дождитесь результата.')
is_clicked2 = st.button("Найти")
if is_clicked2:
            file_reader = open('bounds_list.txt', 'rt')
            text_bounds = file_reader.read()
            file_reader.close()
            bounds = ast.literal_eval(text_bounds)
            text1 = ''
            for i in range(len(bounds)):
                        text1 = text1 + bounds[i][1] + '\n'
            nlp1 = spacy.load('ru_core_news_sm')
            doc1 = nlp1(text1)
            ent_html = displacy.render(doc1, style="ent", jupyter=False)
            st.markdown(ent_html, unsafe_allow_html=True)
st.write('Ключевые обозначения: PER - личные данные (Personal), ORG - название организации (Organisation), LOC - локация, географическое положение (Location), DATE - дата')
st.write('А теперь, ответьте на вопросы:')
st.write('1. Как расшифровывается аббревиатура OCR?')
st.write('2. Как расшифровывается аббревиатура NER?')
st.write('3. Подсчитайте выделенные разноцветные поля (PER,ORG,LOC). Сколько их всего?')
st.write('4. Подсчитайте количество полей каждого типа (сколько PER, сколько ORG, сколько LOC).')
