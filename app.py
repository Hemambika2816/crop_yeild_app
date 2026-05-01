import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ---------- Page Setup ----------
st.set_page_config(page_title="Crop Yield Predictor", layout="wide")

# ---------- Custom CSS (Responsive) ----------
st.markdown("""
<style>
.main {
    padding: 10px;
}
h1 {
    text-align: center;
    color: #2e7d32;
}
.block-container {
    padding-top: 1rem;
}
@media (max-width: 768px) {
    .block-container {
        padding: 0.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# ---------- Language ----------
text = {
    "English": {
        "title": "🌾 Crop Yield Predictor",
        "rain": "Rainfall",
        "temp": "Temperature",
        "hum": "Humidity",
        "nit": "Nitrogen",
        "area": "Area",
        "predict": "Predict Yield",
        "result": "Predicted Yield",
        "suggest": "Suggestions",
        "trend": "Yield Trend",
        "low_rain": "⚠️ Use irrigation",
        "low_n": "🌱 Add fertilizer",
        "high_temp": "🔥 High temperature risk",
        "good": "✅ Good conditions"
    },
    "हिन्दी": {
        "title": "🌾 फसल उत्पादन पूर्वानुमान",
        "rain": "वर्षा",
        "temp": "तापमान",
        "hum": "आर्द्रता",
        "nit": "नाइट्रोजन",
        "area": "क्षेत्रफल",
        "predict": "पूर्वानुमान करें",
        "result": "अनुमानित उत्पादन",
        "suggest": "सुझाव",
        "trend": "उत्पादन प्रवृत्ति",
        "low_rain": "⚠️ सिंचाई करें",
        "low_n": "🌱 खाद डालें",
        "high_temp": "🔥 अधिक तापमान खतरा",
        "good": "✅ स्थिति अच्छी है"
    },
    "తెలుగు": {
        "title": "🌾 పంట దిగుబడి అంచనా",
        "rain": "వర్షపాతం",
        "temp": "ఉష్ణోగ్రత",
        "hum": "ఆర్ద్రత",
        "nit": "నైట్రోజన్",
        "area": "ప్రాంతం",
        "predict": "అంచనా వేయండి",
        "result": "అంచనా దిగుబడి",
        "suggest": "సూచనలు",
        "trend": "దిగుబడి ట్రెండ్",
        "low_rain": "⚠️ నీటిపారుదల చేయండి",
        "low_n": "🌱 ఎరువు వేయండి",
        "high_temp": "🔥 అధిక ఉష్ణోగ్రత ప్రమాదం",
        "good": "✅ పరిస్థితులు బాగున్నాయి"
    }
}

lang = st.selectbox("🌐 Language", ["English", "हिन्दी", "తెలుగు"])
t = text[lang]

# ---------- Header ----------
st.image(
    "https://images.unsplash.com/photo-1625246333195-78d9c38ad449",
    use_column_width=True
)

st.markdown(f"<h1>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------- Inputs ----------
st.subheader("📌 Input Details")

# Responsive layout: auto adjusts columns
col1, col2, col3 = st.columns(3)

with col1:
    state = st.selectbox("State", sorted(df["State"].unique()))
    rainfall = st.slider(t["rain"], 0, 2000, 800)

with col2:
    crop = st.selectbox("Crop", sorted(df["Crop"].unique()))
    temperature = st.slider(t["temp"], 0, 50, 30)

with col3:
    humidity = st.slider(t["hum"], 0, 100, 60)
    nitrogen = st.slider(t["nit"], 0, 150, 60)

area = st.number_input(t["area"], min_value=1, value=1000)

st.markdown("---")

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

# ---------- Prediction ----------
if st.button("🚀 " + t["predict"]):

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

    # Responsive result layout
    r1, r2 = st.columns([1,1])

    with r1:
        st.success(f"{t['result']}: {pred[0]:.2f} tons/hectare")

    with r2:
        st.subheader("🌱 " + t["suggest"])
        for r in get_recommendation(rainfall, nitrogen, temperature):
            st.write(r)

st.markdown("---")

# ---------- Graph ----------
st.subheader("📈 " + t["trend"])

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Yield")

st.pyplot(fig)
