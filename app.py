import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ---------- Page Setup ----------
st.set_page_config(page_title="Crop Yield App", layout="centered")

# ---------- Load Data ----------
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# ---------- Title ----------
st.title("🌾 Crop Yield Predictor")
st.markdown("### Simple & Mobile-Friendly")

# ---------- Inputs (NO SIDEBAR) ----------
states = sorted(df["State"].unique())
crops = sorted(df["Crop"].unique())

state = st.selectbox("State", states)
crop = st.selectbox("Crop", crops)

rainfall = st.slider("Rainfall", 0, 2000, 800)
temperature = st.slider("Temperature", 0, 50, 30)
humidity = st.slider("Humidity", 0, 100, 60)

nitrogen = st.slider("Nitrogen", 0, 150, 60)
phosphorus = st.slider("Phosphorus", 0, 150, 40)
potassium = st.slider("Potassium", 0, 150, 40)

area = st.number_input("Area", min_value=1, value=1000)

# ---------- Recommendation ----------
def get_recommendation(rainfall, nitrogen, temperature):
    suggestions = []
    if rainfall < 500:
        suggestions.append("⚠️ Use irrigation")
    if nitrogen < 50:
        suggestions.append("🌱 Add fertilizer")
    if temperature > 35:
        suggestions.append("🔥 High heat risk")
    if not suggestions:
        suggestions.append("✅ Good conditions")
    return suggestions

# ---------- Button ----------
if st.button("📊 Predict Yield"):

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

    # ---------- Output ----------
    st.success(f"🌾 Yield: {prediction[0]:.2f} tons/hectare")

    st.subheader("🌱 Suggestions")
    recs = get_recommendation(rainfall, nitrogen, temperature)
    for r in recs:
        st.write(r)

# ---------- Graph ----------
st.subheader("📈 Yield Trend")

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Yield")

st.pyplot(fig)
