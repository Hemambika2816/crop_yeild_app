import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie

# ---------- Page ----------
st.set_page_config(page_title="Crop Yield App", layout="centered")

# ---------- Load ----------
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# ---------- Lottie Loader ----------
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_anim = load_lottie("https://assets10.lottiefiles.com/packages/lf20_2ks3pjua.json")

# ---------- Language Dictionary ----------
lang = st.selectbox("🌐 Select Language", ["English", "हिन्दी", "తెలుగు"])

text = {
    "English": {
        "title": "🌾 Crop Yield Predictor",
        "predict": "Predict Yield",
        "result": "Predicted Yield",
        "suggest": "Suggestions",
        "trend": "Yield Trend",
        "rain": "Rainfall",
        "temp": "Temperature",
        "hum": "Humidity",
        "nit": "Nitrogen",
        "pho": "Phosphorus",
        "pot": "Potassium",
        "area": "Area",
        "good": "Good conditions",
        "low_rain": "Low rainfall: Use irrigation",
        "low_n": "Low nitrogen: Add fertilizer",
        "high_temp": "High temperature risk"
    },
    "हिन्दी": {
        "title": "🌾 फसल उत्पादन भविष्यवाणी",
        "predict": "पूर्वानुमान करें",
        "result": "अनुमानित उत्पादन",
        "suggest": "सुझाव",
        "trend": "उत्पादन प्रवृत्ति",
        "rain": "वर्षा",
        "temp": "तापमान",
        "hum": "आर्द्रता",
        "nit": "नाइट्रोजन",
        "pho": "फॉस्फोरस",
        "pot": "पोटैशियम",
        "area": "क्षेत्रफल",
        "good": "स्थिति अच्छी है",
        "low_rain": "कम वर्षा: सिंचाई करें",
        "low_n": "कम नाइट्रोजन: खाद डालें",
        "high_temp": "अधिक तापमान का खतरा"
    },
    "తెలుగు": {
        "title": "🌾 పంట దిగుబడి అంచనా",
        "predict": "అంచనా వేయండి",
        "result": "అంచనా దిగుబడి",
        "suggest": "సూచనలు",
        "trend": "దిగుబడి ట్రెండ్",
        "rain": "వర్షపాతం",
        "temp": "ఉష్ణోగ్రత",
        "hum": "ఆర్ద్రత",
        "nit": "నైట్రోజన్",
        "pho": "ఫాస్పరస్",
        "pot": "పొటాషియం",
        "area": "ప్రాంతం",
        "good": "పరిస్థితులు బాగున్నాయి",
        "low_rain": "తక్కువ వర్షం: నీటిపారుదల చేయండి",
        "low_n": "నైట్రోజన్ తక్కువ: ఎరువు వేయండి",
        "high_temp": "అధిక ఉష్ణోగ్రత ప్రమాదం"
    }
}

t = text[lang]

# ---------- Title + Animation ----------
st.title(t["title"])
st_lottie(lottie_anim, height=200)

# ---------- Inputs ----------
states = sorted(df["State"].unique())
crops = sorted(df["Crop"].unique())

state = st.selectbox("State", states)
crop = st.selectbox("Crop", crops)

rainfall = st.slider(t["rain"], 0, 2000, 800)
temperature = st.slider(t["temp"], 0, 50, 30)
humidity = st.slider(t["hum"], 0, 100, 60)

nitrogen = st.slider(t["nit"], 0, 150, 60)
phosphorus = st.slider(t["pho"], 0, 150, 40)
potassium = st.slider(t["pot"], 0, 150, 40)

area = st.number_input(t["area"], min_value=1, value=1000)

# ---------- Recommendation ----------
def get_recommendation(rainfall, nitrogen, temperature):
    recs = []
    if rainfall < 500:
        recs.append(t["low_rain"])
    if nitrogen < 50:
        recs.append(t["low_n"])
    if temperature > 35:
        recs.append(t["high_temp"])
    if not recs:
        recs.append(t["good"])
    return recs

# ---------- Predict ----------
if st.button("🚀 " + t["predict"]):

    with st.spinner("Processing..."):
        input_data = pd.DataFrame({
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

        input_data = pd.get_dummies(input_data)
        input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

        pred = model.predict(input_data)

    st.success(f"{t['result']}: {pred[0]:.2f} tons/hectare")

    st.subheader("🌱 " + t["suggest"])
    for r in get_recommendation(rainfall, nitrogen, temperature):
        st.write(r)

# ---------- Graph ----------
st.subheader("📈 " + t["trend"])

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Yield")

st.pyplot(fig)
