import streamlit as st
import pandas as pd
import pickle

with open("streamlit_w_krisha/rf_model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Оценка квартиры", layout="centered")

st.markdown(
    """
    <style>
        /* Фон страницы */
        body {
            background-color: #F5F7FA;
        }

        /* Заголовок */
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #2C3E50;
        }

        /* Блок с ценой */
        .price-box {
            background-color: #E8F6FF;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2C3E50;
            margin-top: 20px;
        }

        /* Кастомные кнопки */
        .stButton>button {
            background-color: #1E90FF;
            color: white;
            padding: 12px;
            font-size: 18px;
            border-radius: 10px;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #0D6EFD;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>🏡 Оценка квартиры в Кокшетау</h1>", unsafe_allow_html=True)
st.write("Введите характеристики квартиры для предсказания её цены.")

with st.form("apartment_form"):
    col1, col2 = st.columns(2)

    with col1:
        area = st.number_input("📏 Площадь (кв.м):", min_value=10.0, max_value=1000.0, value=50.0, step=1.0)
        year = st.number_input("🏗️ Год постройки:", min_value=1800, max_value=2025, value=2000, step=1)
        current_floors = st.number_input("📶 Этаж квартиры:", min_value=1, max_value=100, value=5, step=1)
        ceiling = st.number_input("📏 Высота потолков (м):", min_value=1.0, max_value=10.0, value=2.5, step=0.1)

    with col2:
        total_floors = st.number_input("🏢 Всего этажей в доме:", min_value=1, max_value=100, value=10, step=1)
        balcony = st.selectbox("🚪 Балкон:", options=["нет", "да"])
        flat_toilets = st.selectbox("🚽 Туалет:", options=["нет", "да"])
        mortgage = st.selectbox("🏦 В залоге:", options=["нет", "В залоге"])
        dorm = st.selectbox("🏠 Бывшее общежитие:", options=["нет", "да"])

    submitted = st.form_submit_button("🔍 Предсказать цену")

if submitted:
    with st.spinner("🔄 Анализ данных..."):
        balcony_val = 0 if balcony == "нет" else 1
        flat_toilets_val = 0 if flat_toilets == "нет" else 1
        mortgage_val = 0 if mortgage == "нет" else 1
        dorm_val = 0 if dorm == "нет" else 1

        age_of_building = 2025 - year
        floor_ratio = current_floors / total_floors if total_floors > 0 else 0

        input_data = pd.DataFrame({
            "area": [area],
            "flat_toilets": [flat_toilets_val],
            "balcony": [balcony_val],
            "current_floors": [current_floors],
            "total_floors": [total_floors],
            "ceiling": [ceiling],
            "dorm": [dorm_val],
            "mortgage": [mortgage_val],
            "year": [year],
            "age_of_building": [age_of_building],
            "floor_ratio": [floor_ratio]
        })

        predicted_price = model.predict(input_data)[0]

    st.markdown(f"<div class='price-box'>💰 Предполагаемая цена квартиры: {predicted_price:,.0f} KZT</div>", unsafe_allow_html=True)
