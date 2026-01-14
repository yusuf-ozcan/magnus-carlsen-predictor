import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(page_title="Magnus Carlsen Win Predictor", page_icon="♟️")
st.title("♟️ Magnus Carlsen Win Predictor")
st.write("Enter the game parameters to estimate the probability of winning against the World Champion!")

# --- Model Loading Section ---
# Yeni dosya ismin olan 'magnus_model.pkl' kullanıldı.
try:
    model = joblib.load('magnus_model.pkl')
    # Model yüklendiğinde kullanıcıyı sessizce doğrula (İsteğe bağlı st.success eklenebilir)
except Exception as e:
    st.error(f"Model file 'magnus_model.pkl' not found! Please ensure the file is in the same directory. Error: {e}")
    st.stop()  # Model yoksa burada durur, böylece aşağıda 'NameError' almazsın.

# --- Sidebar Input Fields ---
st.sidebar.header("Match Parameters")

opponent_rating = st.sidebar.number_input("Your (Opponent) Rating", min_value=1000, max_value=4000, value=2800)
magnus_rating = st.sidebar.number_input("Magnus Carlsen's Rating", min_value=1000, max_value=4000, value=2855)

color = st.sidebar.selectbox("Magnus's Color", ["White", "Black"])
color_numeric = 1 if color == "White" else 0

prev_result = st.sidebar.selectbox("Magnus's Previous Result", ["Win", "Loss", "Draw"])
# Mapping must match your LabelEncoder used during training
result_map = {"Draw": 0, "Loss": 1, "Win": 2}
prev_result_numeric = result_map[prev_result]

# --- Prediction and Results ---
if st.button("Calculate Probability"):
    # Prepare input data for the model
    input_data = pd.DataFrame([[magnus_rating, opponent_rating, color_numeric, prev_result_numeric]], 
                              columns=['player_rating', 'opponent_rating', 'color_numeric', 'prev_result_numeric'])
    
    # Perform prediction
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    # Extract probabilities based on model classes
    classes = list(model.classes_)
    magnus_win_prob = probabilities[classes.index('Win')] * 100
    your_win_prob = probabilities[classes.index('Loss')] * 100
    draw_prob = probabilities[classes.index('Draw')] * 100

    # Display Results
    st.subheader(f"Predicted Outcome: {prediction}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Magnus Win %", f"{magnus_win_prob:.1f}%")
    col2.metric("Your Win %", f"{your_win_prob:.1f}%")
    col3.metric("Draw %", f"{draw_prob:.1f}%")

    # Feedback messages based on win probability
    if your_win_prob > 25:
        st.balloons()
        st.success("You have a decent chance! Prepare for a tough fight.")
    elif your_win_prob > 10:
        st.info("It's a long shot, but anything can happen in chess!")
    else:
        st.warning("It looks tough. Magnus is likely to dominate this match.")