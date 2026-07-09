import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Page configuration
st.set_page_config(
    page_title="ML Prediction App",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 Machine Learning Prediction System")
st.markdown("Upload your data or input values to get predictions")

# Load model
@st.cache_resource
def load_model():
    try:
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        st.error("Model file not found. Please ensure model.pkl exists.")
        return None

model = load_model()

# Sidebar for input methods
st.sidebar.header("Input Method")
input_method = st.sidebar.radio(
    "Choose input method:",
    ["Manual Input", "Upload CSV"]
)

if input_method == "Manual Input":
    st.subheader("Enter Values Manually")
    
    # Create input fields based on your features
    col1, col2 = st.columns(2)
    
    with col1:
        feature1 = st.number_input("Feature 1", value=0.0)
        feature2 = st.number_input("Feature 2", value=0.0)
    
    with col2:
        feature3 = st.number_input("Feature 3", value=0.0)
        feature4 = st.number_input("Feature 4", value=0.0)
    
    if st.button("Predict", type="primary"):
        if model is not None:
            input_data = np.array([[feature1, feature2, feature3, feature4]])
            prediction = model.predict(input_data)
            
            # Display prediction
            st.success(f"Prediction: {prediction[0]}")
            
            # Additional visualization
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(input_data)
                st.write("Prediction Probabilities:", proba)

else:
    st.subheader("Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file with your features"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(df.head())
            
            if st.button("Run Predictions", type="primary"):
                if model is not None:
                    predictions = model.predict(df)
                    df['Predictions'] = predictions
                    st.success("Predictions completed!")
                    st.dataframe(df)
                    
                    # Download results
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Predictions",
                        data=csv,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Built with Streamlit")
