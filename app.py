import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import requests

# ---------- Page ----------
st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

# ---------- Theme ----------
theme = st.sidebar.selectbox("🎨 Theme", ["Light", "Dark"])

if theme == "Dark":
    bg = "#0E1117"
    card = "#1c1f26"
    text = "white"
else:
    bg = "#f5f7fa"
    card = "white"
    text = "black"

st.markdown(f"""
<style>
.main {{ background-color: {bg}; color: {text}; }}
.card {{
    padding: 15px;
    border-radius: 12px;
    background-color: {card};
    margin-bottom: 15px;
}}
</style>
""", unsafe_allow_html=True)

# ---------- Load ----------
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# ---------- API KEY ----------
API_KEY = "ae7cead3e3f14f2fec30cd58db6f47e4"

# ---------- Weather ----------
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()

    if res.status_code != 200:
        raise Exception(data.get("message", "API error"))

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return temp, humidity, rainfall

# ---------- Mapping ----------
state_city_map = {
    "Andhra Pradesh": "Vijayawada",
    "Telangana": "Hyderabad",
    "Tamil Nadu": "Chennai",
    "Karnataka": "Bangalore",
    "Maharashtra": "Mumbai",
    "Uttar Pradesh": "Lucknow",
    "Punjab": "Chandigarh",
    "Rajasthan": "Jaipur",
    "West Bengal": "Kolkata",
    "Gujarat": "Ahmedabad",
    "Kerala": "Thiruvananthapuram",
    "Madhya Pradesh": "Bhopal"
}

# ---------- Header ----------
st.image(
    "https://images.unsplash.com/photo-1625246333195-78d9c38ad449",
    use_column_width=True
)
st.markdown("<h1 style='text-align:center'>🌾 Crop Yield Dashboard</h1>", unsafe_allow_html=True)

# ---------- Inputs ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    state = st.selectbox("State", sorted(df["State"].unique()))

with col2:
    crop = st.selectbox("Crop", sorted(df["Crop"].unique()))

# ---------- Auto City ----------
default_city = state_city_map.get(state, "")
city = st.text_input("City (auto-filled, editable)", value=default_city)

# ---------- Session ----------
if "temperature" not in st.session_state:
    st.session_state.temperature = 30
    st.session_state.humidity = 60
    st.session_state.rainfall = 800

# ---------- Weather Button ----------
if st.button("🌦 Get Weather Data"):
    try:
        temp, hum, rain = get_weather(city)
        st.session_state.temperature = int(temp)
        st.session_state.humidity = int(hum)
        st.session_state.rainfall = int(rain)
        st.success(f"Weather loaded for {city}")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------- Sliders ----------
c1, c2, c3 = st.columns(3)

with c1:
    rainfall = st.slider("Rainfall", 0, 2000, st.session_state.rainfall)

with c2:
    temperature = st.slider("Temperature", 0, 50, st.session_state.temperature)

with c3:
    humidity = st.slider("Humidity", 0, 100, st.session_state.humidity)

c4, c5, c6 = st.columns(3)

with c4:
    nitrogen = st.slider("Nitrogen", 0, 150, 60)

with c5:
    phosphorus = st.slider("Phosphorus", 0, 150, 40)

with c6:
    potassium = st.slider("Potassium", 0, 150, 40)

area = st.number_input("Area", min_value=1, value=1000)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Recommendation ----------
def get_recommendation(r, n, t):
    recs = []
    if r < 500: recs.append("Use irrigation")
    if n < 50: recs.append("Add fertilizer")
    if t > 35: recs.append("High temperature risk")
    if not recs: recs.append("Good conditions")
    return recs

# ---------- Fertilizer ----------
def fertilizer_recommendation(n, p, k):
    recs = []
    if n < 50: recs.append("Add Urea")
    if p < 40: recs.append("Add DAP")
    if k < 40: recs.append("Add MOP")
    if not recs: recs.append("NPK balanced")
    return recs

# ---------- Category ----------
def yield_category(y):
    if y < 2: return "🔴 Low"
    elif y < 4: return "🟡 Medium"
    else: return "🟢 High"

# ---------- Predict ----------
if st.button("🚀 Predict Yield"):

    X = pd.DataFrame({
        "State":[state],
        "Crop":[crop],
        "Rainfall":[rainfall],
        "Temperature":[temperature],
        "Humidity":[humidity],
        "Nitrogen":[nitrogen],
        "Phosphorus":[phosphorus],
        "Potassium":[potassium],
        "Area":[area]
    })

    X = pd.get_dummies(X)
    X = X.reindex(columns=model.feature_names_in_, fill_value=0)

    pred = model.predict(X)

    colA, colB = st.columns(2)

    with colA:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("Yield", f"{pred[0]:.2f} t/ha")
        st.info(f"Category: {yield_category(pred[0])}")
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Suggestions")
        for r in get_recommendation(rainfall, nitrogen, temperature):
            st.write("•", r)

        st.subheader("🌿 Fertilizer")
        for f in fertilizer_recommendation(nitrogen, phosphorus, potassium):
            st.write("•", f)

        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Graph ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("📈 Yield Trend")

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Yield")

st.pyplot(fig)

st.markdown("</div>", unsafe_allow_html=True)
