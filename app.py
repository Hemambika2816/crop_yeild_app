import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Crop Yield Predictor", layout="wide")

# Load data
df = pd.read_csv("crop_data_full.csv")
model = pickle.load(open("model.pkl", "rb"))

# Title
st.title("🌾 Crop Yield Prediction System")
st.markdown("### Smart Agriculture Assistant")

# Sidebar inputs
st.sidebar.header("Enter Input Features")

states = sorted(df["State"].unique())
crops = sorted(df["Crop"].unique())

state = st.sidebar.selectbox("State", states)
crop = st.sidebar.selectbox("Crop", crops)

rainfall = st.sidebar.number_input("Rainfall", min_value=0)
temperature = st.sidebar.number_input("Temperature", min_value=0)
humidity = st.sidebar.number_input("Humidity", min_value=0)
nitrogen = st.sidebar.number_input("Nitrogen", min_value=0)
phosphorus = st.sidebar.number_input("Phosphorus", min_value=0)
potassium = st.sidebar.number_input("Potassium", min_value=0)
area = st.sidebar.number_input("Area", min_value=0)

# Recommendation function
def get_recommendation(rainfall, nitrogen, temperature):
    suggestions = []

    if rainfall < 500:
        suggestions.append("⚠️ Low rainfall: Consider irrigation")

    if nitrogen < 50:
        suggestions.append("🌱 Low nitrogen: Add fertilizers")

    if temperature > 35:
        suggestions.append("🔥 High temperature: Risk of crop stress")

    if not suggestions:
        suggestions.append("✅ Conditions are good for crop growth")

    return suggestions

# Prediction
if st.sidebar.button("Predict"):

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

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Prediction Result")
        st.success(f"Predicted Yield: {prediction[0]:.2f}")

    with col2:
        st.subheader("🌱 Recommendations")
        recs = get_recommendation(rainfall, nitrogen, temperature)
        for r in recs:
            st.write(r)

# Graph section
st.subheader("📈 Yield Trend")

filtered = df[(df["State"] == state) & (df["Crop"] == crop)]

fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Yield"])
ax.set_xlabel("Year")
ax.set_ylabel("Yield")

st.pyplot(fig)
