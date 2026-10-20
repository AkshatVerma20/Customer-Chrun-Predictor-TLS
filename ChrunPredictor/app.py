import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

model_path = Path(__file__).parent / "final_churn_model.pkl"

try:
    model = joblib.load(model_path)
except Exception as e:
    st.error("Unable to load the churn prediction model.")
    st.exception(e)
    st.stop()

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f4f8ff 0%, #f8f6ff 100%);
        color: #172554;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #14264e;
    }

    .hero {
        background: linear-gradient(110deg, #e4efff, #f0eaff);
        padding: 25px 30px;
        border-radius: 18px;
        margin-bottom: 22px;
        border: 1px solid #dce7ff;
    }

    .hero h1 {
        margin: 0;
        font-size: 2rem;
    }

    .hero p {
        color: #53678e;
        margin: 8px 0 0 0;
        font-size: 1.05rem;
    }

    .panel {
        background: #ffffff;
        border: 1px solid #e1e9f6;
        border-radius: 20px;
        padding: 25px;
        min-height: 100%;
        box-shadow: 0 5px 20px rgba(30, 64, 120, 0.05);
    }

    .panel-subtitle {
        color: #64748b;
        margin-top: -8px;
        margin-bottom: 22px;
    }

    .result-card {
        padding: 22px;
        border-radius: 16px;
        margin: 12px 0 22px 0;
    }

    .low-risk {
        background: #effcf3;
        border: 1px solid #b8efc7;
    }

    .high-risk {
        background: #fff1f2;
        border: 1px solid #fecdd3;
    }

    .result-title {
        font-size: 1.45rem;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .result-description {
        color: #475569;
        line-height: 1.6;
    }

    .info-card {
        background: #eff6ff;
        border: 1px solid #dbeafe;
        padding: 17px;
        border-radius: 14px;
        margin-top: 20px;
        margin-bottom: 18px;
    }

    .recommendation-card {
        background: #fff5f8;
        border: 1px solid #fce0e9;
        padding: 18px;
        border-radius: 14px;
        margin-top: 16px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background: linear-gradient(100deg, #1674ed, #7045f6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-weight: 650;
        min-height: 48px;
        width: 100%;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        color: white;
        border: none;
        filter: brightness(1.05);
    }

    div[data-testid="stMetric"] {
        background: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }

    label {
        color: #263653 !important;
        font-weight: 550 !important;
    }

    /* Force all inputs, number fields, and selectboxes to have white background */
    input, 
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"],
    [data-baseweb="input"] {
        background-color: #ffffff !important;
        color: #172554 !important;
        border-color: #cbd5e1 !important;
    }

    /* Dropdown menus and popovers */
    div[data-baseweb="menu"], 
    div[data-baseweb="popover"],
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        color: #172554 !important;
    }

    div[data-baseweb="menu"] div, 
    ul[data-baseweb="menu"] li,
    ul[data-baseweb="menu"] div {
        background-color: #ffffff !important;
        color: #172554 !important;
    }

    ul[data-baseweb="menu"] li:hover {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }

    hr {
        border-color: #e2e8f0;
    }

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1> Customer Churn Prediction</h1>
    <p>Understand customer churn risk early and take action to improve retention.</p>
</div>
""", unsafe_allow_html=True)

left_panel, right_panel = st.columns([1.05, 1], gap="large")

with left_panel:
    st.subheader(" Customer Information")
    st.markdown(
        '<p class="panel-subtitle">Enter the customer details to estimate their churn risk.</p>',
        unsafe_allow_html=True
    )

    with st.form("customer_details_form"):

        st.markdown("#### Personal Information")

        c1, c2, c3 = st.columns(3)

        with c1:
            gender = st.selectbox(
                "Gender",
                ["Female", "Male"],
                key="gender"
            )

        with c2:
            senior_citizen = st.selectbox(
                "Senior Citizen",
                [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
                key="senior_citizen"
            )

        with c3:
            partner = st.selectbox(
                "Partner",
                ["Yes", "No"],
                key="partner"
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            dependents = st.selectbox(
                "Dependents",
                ["Yes", "No"],
                key="dependents"
            )

        with c2:
            tenure = st.number_input(
                "Tenure (months)",
                min_value=0,
                max_value=72,
                value=12,
                step=1,
                key="tenure"
            )

        with c3:
            phone_service = st.selectbox(
                "Phone Service",
                ["Yes", "No"],
                key="phone_service"
            )

        st.divider()
        st.markdown("#### Services")

        c1, c2, c3 = st.columns(3)

        with c1:
            multiple_lines = st.selectbox(
                "Multiple Lines",
                ["No", "Yes", "No phone service"],
                key="multiple_lines"
            )

        with c2:
            internet_service = st.selectbox(
                "Internet Service",
                ["DSL", "Fiber optic", "No"],
                key="internet_service"
            )

        with c3:
            online_security = st.selectbox(
                "Online Security",
                ["Yes", "No", "No internet service"],
                key="online_security"
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            online_backup = st.selectbox(
                "Online Backup",
                ["Yes", "No", "No internet service"],
                key="online_backup"
            )

        with c2:
            device_protection = st.selectbox(
                "Device Protection",
                ["Yes", "No", "No internet service"],
                key="device_protection"
            )

        with c3:
            tech_support = st.selectbox(
                "Tech Support",
                ["Yes", "No", "No internet service"],
                key="tech_support"
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            streaming_tv = st.selectbox(
                "Streaming TV",
                ["Yes", "No", "No internet service"],
                key="streaming_tv"
            )

        with c2:
            streaming_movies = st.selectbox(
                "Streaming Movies",
                ["Yes", "No", "No internet service"],
                key="streaming_movies"
            )

        with c3:
            contract = st.selectbox(
                "Contract",
                ["Month-to-month", "One year", "Two year"],
                key="contract"
            )

        st.divider()
        st.markdown("#### Billing Information")

        c1, c2, c3 = st.columns(3)

        with c1:
            paperless_billing = st.selectbox(
                "Paperless Billing",
                ["Yes", "No"],
                key="paperless_billing"
            )

        with c2:
            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)"
                ],
                key="payment_method"
            )

        with c3:
            monthly_charges = st.number_input(
                "Monthly Charges",
                min_value=0.0,
                value=70.0,
                step=1.0,
                key="monthly_charges"
            )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=840.0,
            step=10.0,
            key="total_charges"
        )

        submitted = st.form_submit_button(
            " Predict Customer Churn",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
    if submitted:
        customer_data = pd.DataFrame([{
            "SeniorCitizen": senior_citizen,
            "tenure": tenure,
            "MonthlyCharges": monthly_charges,
            "gender": gender,
            "Partner": partner,
            "Dependents": dependents,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "TotalCharges": str(total_charges)
        }])

        try:
            prediction = model.predict(customer_data)[0]
            probabilities = model.predict_proba(customer_data)[0]

            classes = list(model.classes_)
            churn_index = classes.index(1)
            churn_probability = float(probabilities[churn_index])

            st.session_state["churn_result"] = {
                "prediction": int(prediction),
                "probability": churn_probability
            }

        except Exception as e:
            st.session_state.pop("churn_result", None)
            st.error("We couldn't calculate the prediction. Please check the customer details.")
            with st.expander("Technical details"):
                st.exception(e)

with right_panel:
    st.subheader(" Prediction Result")
    st.markdown(
        '<p class="panel-subtitle">Your customer retention insights.</p>',
        unsafe_allow_html=True
    )

    result = st.session_state.get("churn_result")

    if result is None:
        st.info(
            " Enter the customer details on the left, then select "
            "**Predict Customer Churn** to see the result here."
        )

        st.markdown("""
        <div class="info-card">
            <strong> What you'll get</strong>
            <p>A churn-risk estimate, a simple explanation, and practical suggestions
            for improving customer retention.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        prediction = result["prediction"]
        churn_probability = result["probability"]

        if prediction == 1:
            st.markdown(f"""
            <div class="result-card high-risk">
                <div style="font-size: 1.1rem; font-weight: 700; color: #be123c;">
                     At Risk of Churning
                </div>
                <div class="result-title">This customer may leave</div>
                <div class="result-description">
                    The model identifies this customer as being at risk.
                    Consider proactive outreach to understand their needs.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card low-risk">
                <div style="font-size: 1.1rem; font-weight: 700; color: #15803d;">
                     Lower Churn Risk
                </div>
                <div class="result-title">This customer is likely to stay</div>
                <div class="result-description">
                    The model predicts a lower likelihood of churn for this customer.
                    Continue building a positive customer relationship.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Estimated Churn Probability")

        st.markdown(
            f"<div style='font-size:2.4rem;font-weight:800;color:"
            f"{'#dc3655' if churn_probability >= 0.5 else '#159957'};'>"
            f"{churn_probability:.2%}</div>",
            unsafe_allow_html=True
        )

        st.progress(churn_probability)
        st.caption("0% = lower estimated risk · 100% = higher estimated risk")

        st.markdown(f"""
        <div class="info-card">
            <strong> What does this mean?</strong>
            <p>
                The model estimates a {churn_probability:.2%} probability of churn
                for the details provided. This is an estimate, not a guarantee
                of what the customer will do.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="recommendation-card">
            <h4 style="margin-top:0;color:#9d174d;">📣 Recommended Actions</h4>
            <p style="color:#475569;">Use these suggestions to support customer retention:</p>
            <p> Provide responsive, helpful customer support</p>
            <p> Offer plans that fit the customer's needs</p>
            <p> Monitor service satisfaction and engagement</p>
            <p> Explain relevant benefits and available services</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption(
    "Customer Churn Prediction Dashboard · Predictions are estimates "
    "and should support—not replace—business judgment."
)

