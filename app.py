import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import requests

# ---------- Page Setup ----------
st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

# ---------- Load ----------
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# ---------- API KEY ----------
API_KEY = "import streamlit as st"
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import requests

# ---------- Page Setup ----------
st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

# ---------- Load ----------
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# ---------- API KEY ----------
API_KEY = "ae7cead3e3f14f2fec30cd58db6f47e4"

# ---------- Weather Function ----------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return temp, humidity, rainfall

# ---------- Header ----------
st.title("🌾 Crop Yield Dashboard")

# ---------- Input ----------
city = st.text_input("Enter City for Weather")

if "temperature" not in st.session_state:
    st.session_state.temperature = 30
    st.session_state.humidity = 60
    st.session_state.rainfall = 800

# ---------- Fetch Weather ----------
if st.button("🌦 Get Weather Data"):
    try:
        temp, hum, rain = get_weather(city)

        st.session_state.temperature = int(temp)
        st.session_state.humidity = int(hum)
        st.session_state.rainfall = int(rain)

        st.success("Weather data loaded!")
    except:
        st.error("Invalid city or API issue")

# ---------- Inputs ----------
col1, col2, col3 = st.columns(3)

with col1:
    state = st.selectbox("State", sorted(df["State"].unique()))
    rainfall = st.slider("Rainfall", 0, 2000, st.session_state.rainfall)

with col2:
    crop = st.selectbox("Crop", sorted(df["Crop"].unique()))
    temperature = st.slider("Temperature", 0, 50, st.session_state.temperature)

with col3:
    humidity = st.slider("Humidity", 0, 100, st.session_state.humidity)
    nitrogen = st.slider("Nitrogen", 0, 150, 60)

area = st.number_input("Area", min_value=1, value=1000)

# ---------- Recommendation ----------
def get_recommendation(rainfall, nitrogen, temperature):
    recs = []
    if rainfall < 500:
        recs.append("Use irrigation")
    if nitrogen < 50:
        recs.append("Add fertilizer")
    if temperature > 35:
        recs.append("High temperature risk")
    if not recs:
        recs.append("Good conditions")
    return recs

# ---------- Category ----------
def yield_category(y):
    if y < 2:
        return "🔴 Low"
    elif y < 4:
        return "🟡 Medium"
    else:
        return "🟢 High"

# ---------- Prediction ----------
if st.button("🚀 Predict Yield"):

    input_data = pd.DataFrame({
        "State":[state],
        "Crop":[crop],
        "Rainfall":[rainfall],
        "Temperature":[temperature],
        "Humidity":[humidity],
        "Nitrogen":[nitrogen],
        "Area":[area]
    })

    input_data = pd.get_dummies(input_data)
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    pred = model.predict(input_data)

    colA, colB = st.columns(2)

    with colA:
        st.success(f"Yield: {pred[0]:.2f} tons/hectare")
        st.info(f"Category: {yield_category(pred[0])}")

    with colB:
        st.subheader("Suggestions")
        for r in get_recommendation(rainfall, nitrogen, temperature):
            st.write("•", r)

# ---------- Graph ----------
st.subheader("📈 Yield Trend")

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Yield")

st.pyplot(fig)"

# ---------- Weather Function ----------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return temp, humidity, rainfall

# ---------- Header ----------
st.title("🌾 Crop Yield Dashboard")

# ---------- Input ----------
city = st.text_input("Enter City for Weather")

if "temperature" not in st.session_state:
    st.session_state.temperature = 30
    st.session_state.humidity = 60
    st.session_state.rainfall = 800

# ---------- Fetch Weather ----------
if st.button("🌦 Get Weather Data"):
    try:
        temp, hum, rain = get_weather(city)

        st.session_state.temperature = int(temp)
        st.session_state.humidity = int(hum)
        st.session_state.rainfall = int(rain)

        st.success("Weather data loaded!")
    except:
        st.error("Invalid city or API issue")

# ---------- Inputs ----------
col1, col2, col3 = st.columns(3)

with col1:
    state = st.selectbox("State", sorted(df["State"].unique()))
    rainfall = st.slider("Rainfall", 0, 2000, st.session_state.rainfall)

with col2:
    crop = st.selectbox("Crop", sorted(df["Crop"].unique()))
    temperature = st.slider("Temperature", 0, 50, st.session_state.temperature)

with col3:
    humidity = st.slider("Humidity", 0, 100, st.session_state.humidity)
    nitrogen = st.slider("Nitrogen", 0, 150, 60)

area = st.number_input("Area", min_value=1, value=1000)

# ---------- Recommendation ----------
def get_recommendation(rainfall, nitrogen, temperature):
    recs = []
    if rainfall < 500:
        recs.append("Use irrigation")
    if nitrogen < 50:
        recs.append("Add fertilizer")
    if temperature > 35:
        recs.append("High temperature risk")
    if not recs:
        recs.append("Good conditions")
    return recs

# ---------- Category ----------
def yield_category(y):
    if y < 2:
        return "🔴 Low"
    elif y < 4:
        return "🟡 Medium"
    else:
        return "🟢 High"

# ---------- Prediction ----------
if st.button("🚀 Predict Yield"):

    input_data = pd.DataFrame({
        "State":[state],
        "Crop":[crop],
        "Rainfall":[rainfall],
        "Temperature":[temperature],
        "Humidity":[humidity],
        "Nitrogen":[nitrogen],
        "Area":[area]
    })

    input_data = pd.get_dummies(input_data)
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    pred = model.predict(input_data)

    colA, colB = st.columns(2)

    with colA:
        st.success(f"Yield: {pred[0]:.2f} tons/hectare")
        st.info(f"Category: {yield_category(pred[0])}")

    with colB:
        st.subheader("Suggestions")
        for r in get_recommendation(rainfall, nitrogen, temperature):
            st.write("•", r)

# ---------- Graph ----------
st.subheader("📈 Yield Trend")

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Yield")

st.pyplot(fig)
