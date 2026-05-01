import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ---------- Page Setup ----------
st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

# ---------- Theme Toggle ----------
theme = st.sidebar.selectbox("🎨 Theme", ["Light", "Dark"])

if theme == "Dark":
    bg_color = "#0E1117"
    card_color = "#1c1f26"
    text_color = "white"
else:
    bg_color = "#f5f7fa"
    card_color = "white"
    text_color = "black"

# ---------- Custom CSS ----------
st.markdown(f"""
<style>
.main {{
    background-color: {bg_color};
    color: {text_color};
}}
.card {{
    padding: 15px;
    border-radius: 12px;
    background-color: {card_color};
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}}
</style>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# ---------- Language ----------
text = {
    "English": {
        "title": "🌾 Crop Yield Dashboard",
        "predict": "Predict Yield",
        "result": "Predicted Yield",
        "suggest": "Suggestions",
        "trend": "Yield Trend",
        "category": "Yield Category",
        "rain": "Rainfall",
        "temp": "Temperature",
        "hum": "Humidity",
        "nit": "Nitrogen",
        "area": "Area",
        "good": "Good conditions",
        "low_rain": "Use irrigation",
        "low_n": "Add fertilizer",
        "high_temp": "High temperature risk"
    },
    "हिन्दी": {
        "title": "🌾 फसल डैशबोर्ड",
        "predict": "पूर्वानुमान करें",
        "result": "अनुमानित उत्पादन",
        "suggest": "सुझाव",
        "trend": "उत्पादन प्रवृत्ति",
        "category": "उत्पादन श्रेणी",
        "rain": "वर्षा",
        "temp": "तापमान",
        "hum": "आर्द्रता",
        "nit": "नाइट्रोजन",
        "area": "क्षेत्रफल",
        "good": "स्थिति अच्छी है",
        "low_rain": "सिंचाई करें",
        "low_n": "खाद डालें",
        "high_temp": "अधिक तापमान खतरा"
    },
    "తెలుగు": {
        "title": "🌾 పంట డాష్‌బోర్డ్",
        "predict": "అంచనా వేయండి",
        "result": "అంచనా దిగుబడి",
        "suggest": "సూచనలు",
        "trend": "దిగుబడి ట్రెండ్",
        "category": "దిగుబడి స్థాయి",
        "rain": "వర్షపాతం",
        "temp": "ఉష్ణోగ్రత",
        "hum": "ఆర్ద్రత",
        "nit": "నైట్రోజన్",
        "area": "ప్రాంతం",
        "good": "పరిస్థితులు బాగున్నాయి",
        "low_rain": "నీటిపారుదల చేయండి",
        "low_n": "ఎరువు వేయండి",
        "high_temp": "అధిక ఉష్ణోగ్రత ప్రమాదం"
    }
}

lang = st.sidebar.selectbox("🌐 Language", ["English", "हिन्दी", "తెలుగు"])
t = text[lang]

# ---------- Header ----------
st.image(
    "https://images.unsplash.com/photo-1625246333195-78d9c38ad449",
    use_column_width=True
)

st.markdown(f"<h1 style='text-align:center'>{t['title']}</h1>", unsafe_allow_html=True)

# ---------- Inputs Card ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

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

# ---------- Category ----------
def yield_category(y):
    if y < 2:
        return "🔴 Low"
    elif y < 4:
        return "🟡 Medium"
    else:
        return "🟢 High"

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

    # ---------- Result Cards ----------
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric(t["result"], f"{pred[0]:.2f} t/ha")
        st.info(f"{t['category']}: {yield_category(pred[0])}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(t["suggest"])
        for r in get_recommendation(rainfall, nitrogen, temperature):
            st.write("•", r)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Graph ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("📈 " + t["trend"])

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Yield")

st.pyplot(fig)

st.markdown("</div>", unsafe_allow_html=True)
