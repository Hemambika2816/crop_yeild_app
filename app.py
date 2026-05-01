import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Page Setup ----------
st.set_page_config(page_title="Crop Yield Predictor", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #2e7d32;
}
.stButton>button {
    background-color: #2e7d32;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# ---------- Title ----------
st.title("🌾 Crop Yield Prediction System")
st.markdown("#### Smart Agriculture Assistant for Farmers")

# ---------- Sidebar ----------
st.sidebar.header("📌 Input Parameters")

states = sorted(df["State"].unique())
crops = sorted(df["Crop"].unique())

state = st.sidebar.selectbox("🌍 Select State", states)
crop = st.sidebar.selectbox("🌱 Select Crop", crops)

rainfall = st.sidebar.slider("🌧️ Rainfall", 0, 2000, 800)
temperature = st.sidebar.slider("🌡️ Temperature", 0, 50, 30)
humidity = st.sidebar.slider("💧 Humidity", 0, 100, 60)

nitrogen = st.sidebar.slider("🧪 Nitrogen", 0, 150, 60)
phosphorus = st.sidebar.slider("🧪 Phosphorus", 0, 150, 40)
potassium = st.sidebar.slider("🧪 Potassium", 0, 150, 40)

area = st.sidebar.number_input("📏 Area", min_value=1, value=1000)

# ---------- Recommendation Function ----------
def get_recommendation(rainfall, nitrogen, temperature):
    suggestions = []
    if rainfall < 500:
        suggestions.append("⚠️ Low rainfall: Consider irrigation")
    if nitrogen < 50:
        suggestions.append("🌱 Low nitrogen: Add fertilizers")
    if temperature > 35:
        suggestions.append("🔥 High temperature: Crop stress risk")
    if not suggestions:
        suggestions.append("✅ Conditions are optimal")
    return suggestions

# ---------- Prediction ----------
if st.sidebar.button("🚀 Predict Yield"):

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

    prediction = model.predict(input_data)

    # ---------- Layout ----------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Predicted Yield")
        st.metric(label="Yield (tons/hectare)", value=f"{prediction[0]:.2f}")

    with col2:
        st.subheader("🌱 Recommendations")
        recs = get_recommendation(rainfall, nitrogen, temperature)
        for r in recs:
            st.write(r)

# ---------- Visualization ----------
st.subheader("📈 Yield Trend")

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Yield")
ax.set_title("Yield Over Time")

st.pyplot(fig)

# ---------- Footer ----------
st.markdown("---")
st.markdown("Developed as a Data Science Project 🌾")
