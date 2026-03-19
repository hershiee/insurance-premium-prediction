import streamlit as st
import requests

# --- Config ---
API_URL = "http://15.206.91.116:8000/predict"

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🛡️",
    layout="centered"
)

# --- Header ---
st.title("🛡️ Insurance Premium Category Predictor")
st.markdown("Fill in your details below to predict your insurance premium category.")
st.divider()

# --- Input Form ---
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("🎂 Age", min_value=1, max_value=119, value=30)
    weight = st.number_input("⚖️ Weight (kg)", min_value=1.0, value=65.0, step=0.5)
    height = st.number_input("📏 Height (m)", min_value=0.5, max_value=2.49, value=1.70, step=0.01)
    income_lpa = st.number_input("💰 Annual Income (LPA)", min_value=0.1, value=10.0, step=0.5)

with col2:
    smoker = st.selectbox(
        "🚬 Are you a smoker?",
        options=[False, True],
        format_func=lambda x: "Yes" if x else "No"
    )
    city = st.text_input("🏙️ City", value="Mumbai")
    occupation = st.selectbox(
        "💼 Occupation",
        options=[
            'retired', 'freelancer', 'student',
            'government_job', 'business_owner',
            'unemployed', 'private_job'
        ],
        format_func=lambda x: x.replace("_", " ").title()
    )

# --- BMI Preview ---
bmi = weight / (height ** 2)
st.divider()

bmi_col, _ = st.columns([1, 2])
with bmi_col:
    st.metric("📊 Your BMI", f"{bmi:.1f}")

st.divider()

# --- Predict Button ---
if st.button("🔍 Predict Premium Category", use_container_width=True, type="primary"):

    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    with st.spinner("Predicting..."):
        try:
            response = requests.post(API_URL, json=input_data, timeout=10)
            result = response.json()

            # ✅ FIX: API returns data nested inside "response" key
            if response.status_code == 200 and "response" in result:
                data = result["response"]  # unwrap the nested response
                category = data["predicted_category"]
                confidence = data.get("confidence", 0)
                class_probs = data.get("class_probabilities", {})

                # Color-coded result
                color_map = {
                    "Low": "#28a745",
                    "Medium": "#fd7e14",
                    "High": "#dc3545"
                }
                color = color_map.get(category, "#007bff")

                st.success("✅ Prediction successful!")

                # --- Result Card ---
                st.markdown(
                    f"""
                    <div style="
                        background-color: {color}22;
                        border-left: 5px solid {color};
                        padding: 24px;
                        border-radius: 8px;
                        text-align: center;
                        margin: 16px 0;
                    ">
                        <h2 style="color: {color}; margin: 0;">
                            {category} Premium
                        </h2>
                        <p style="color: gray; margin-top: 8px; margin-bottom: 0;">
                            Confidence: {confidence:.0%}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # --- Class Probabilities ---
                if class_probs:
                    st.divider()
                    st.subheader("📊 Class Probabilities")
                    prob_col1, prob_col2, prob_col3 = st.columns(3)

                    with prob_col1:
                        st.metric(
                            "🟢 Low",
                            f"{class_probs.get('Low', 0):.0%}"
                        )
                    with prob_col2:
                        st.metric(
                            "🟠 Medium",
                            f"{class_probs.get('Medium', 0):.0%}"
                        )
                    with prob_col3:
                        st.metric(
                            "🔴 High",
                            f"{class_probs.get('High', 0):.0%}"
                        )

                # --- Input Summary ---
                st.divider()
                st.subheader("📋 Input Summary")
                summary_col1, summary_col2 = st.columns(2)

                with summary_col1:
                    st.write(f"**Age:** {age}")
                    st.write(f"**Weight:** {weight} kg")
                    st.write(f"**Height:** {height} m")
                    st.write(f"**BMI:** {bmi:.2f}")

                with summary_col2:
                    st.write(f"**Income:** ₹{income_lpa} LPA")
                    st.write(f"**Smoker:** {'Yes' if smoker else 'No'}")
                    st.write(f"**City:** {city}")
                    st.write(f"**Occupation:** {occupation.replace('_', ' ').title()}")

            else:
                st.error(f"⚠️ Unexpected response from API (status {response.status_code})")
                st.json(result)

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the API server. Make sure EC2 is running.")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The server took too long to respond.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# --- Footer ---
st.divider()
st.caption("Powered by FastAPI (AWS EC2) + Streamlit | Insurance Premium Predictor")