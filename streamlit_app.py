import streamlit as st
import joblib
import numpy as np
import pandas as pd # Needed for creating DataFrame from user input

# --- 0. Configuration ---
MODEL_PATH = 'emotion_model.pkl'
LABEL_ENCODER_PATH = 'label_encoder.pkl'

# --- 1. Load Trained Model and LabelEncoder ---
@st.cache_resource # Cache the model and encoder to avoid reloading on every rerun
def load_resources():
    try:
        model = joblib.load(MODEL_PATH)
        le = joblib.load(LABEL_ENCODER_PATH)
        return model, le
    except FileNotFoundError:
        st.error(f"Error: Model or LabelEncoder file not found. Make sure '{MODEL_PATH}' and '{LABEL_ENCODER_PATH}' are in the same directory.")
        st.stop() # Stop the app if files are missing

model, le = load_resources()

# --- 2. Define Questions and their Mapping Logic ---
# These mappings MUST be identical to what you used during preprocessing!

# IMPORTANT: You need to review the `unique()` values you printed
# during preprocessing for each column and adjust these mappings if necessary.
# If a value from your actual data is not in these maps, it will cause errors
# when processing user input.

# Mappings for categorical/ordinal features
MOOD_MAPPING = {
    'Extreme sadness': 0, 'Very sad': 1, 'Somewhat sad': 2,
    'Irritability': 3, 'Fluctuating': 4, 'Neutral': 5,
    'Slightly anxious': 6, 'Somewhat anxious': 7, 'Mildly anxious': 8,
    'Slightly happy': 9, 'Happiness': 10, 'Very happy': 11
}

ANXIOUS_SOCIAL_MAPPING = {
    'Not at all anxious': 0, 'Rarely anxious': 1, 'Slightly anxious': 2,
    'Somewhat anxious': 3, 'Often anxious': 4, 'Very anxious': 5, 'Extremely anxious': 6
}

SLEEP_QUALITY_MAPPING = {
    'Difficulty staying asleep': 0, 'Early morning waking': 1, 'Interrupted': 2,
    'Restless': 3, 'Normal': 4, 'Restful': 5, 'Excellent': 6
}

APPETITE_CHANGE_MAPPING = {
    'Loss of appetite': 0, 'Decreased': 1, 'Fluctuates daily': 2,
    'No significant change': 3, 'Increased cravings': 4, 'Increased': 5
}

LACK_OF_INTEREST_MAPPING = {
    'Never': 0, 'Rarely': 1, 'Occasionally': 2, 'Frequently': 3, 'Always': 4
}

ENJOYABLE_ACTIVITIES_MAPPING = {
    'Never': 0, 'Rarely': 1, 'Once a week': 2, 'A few times a week': 3,
    'Daily': 4, 'Always': 5
}

PHYSICAL_ANXIETY_MAPPING = {
    'No': 0, 'Rarely': 1, 'Yes, occasionally': 2, 'Yes, frequently': 3, 'Always': 4
}

CONCENTRATION_DIFFICULTY_MAPPING = {
    'Never': 0, 'Rarely': 1, 'Occasionally': 2, 'Frequently': 3, 'Constantly': 4
}

# Questions to display in the UI
questions_data = [
    {'id': 'mood', 'text': '1. How would you describe your mood over the past two weeks?', 'type': 'radio', 'options': list(MOOD_MAPPING.keys())},
    {'id': 'anxious_social_scale', 'text': '2. On a scale of 0-6, how often have you felt anxious in social situations recently?', 'type': 'radio', 'options': list(ANXIOUS_SOCIAL_MAPPING.keys())},
    {'id': 'anxiety_triggers', 'text': '3. Have you experienced any of the following anxiety triggers in the past month?', 'type': 'multiselect', 'options': ['Family issues', 'Work-related stress', 'Financial concerns', 'Health issues', 'Social events', 'None of the above']},
    {'id': 'sleep_quality', 'text': '4. How would you rate the quality of your sleep over the past week?', 'type': 'radio', 'options': list(SLEEP_QUALITY_MAPPING.keys())},
    {'id': 'appetite_change', 'text': '5. Have you noticed any significant changes in your appetite?', 'type': 'radio', 'options': list(APPETITE_CHANGE_MAPPING.keys())},
    {'id': 'lack_of_interest', 'text': '6. How often have you felt a lack of interest or pleasure in daily activities?', 'type': 'radio', 'options': list(LACK_OF_INTEREST_MAPPING.keys())},
    {'id': 'enjoyable_activities', 'text': '7. How often do you engage in activities you enjoy or that help you relax?', 'type': 'radio', 'options': list(ENJOYABLE_ACTIVITIES_MAPPING.keys())},
    {'id': 'physical_anxiety_symptoms', 'text': '8. Have you had any physical symptoms of anxiety (e.g., heart palpitations, sweating, shortness of breath)?', 'type': 'radio', 'options': list(PHYSICAL_ANXIETY_MAPPING.keys())},
    {'id': 'concentration_difficulty', 'text': '9. How often do you find it difficult to concentrate on tasks?', 'type': 'radio', 'options': list(CONCENTRATION_DIFFICULTY_MAPPING.keys())},
    {'id': 'coping_strategies', 'text': '10. What coping strategies have you used when feeling stressed or anxious?', 'type': 'multiselect', 'options': ['Physical activity', 'Journaling or writing', 'Meditation/Mindfulness', 'Socializing', 'Seeking professional help', 'No coping strategies']},
]

# --- 3. Streamlit UI Layout ---
st.set_page_config(page_title="Emotional State Assessor", layout="centered")

st.title("💡 Emotional State Assessor")
st.markdown("Answer these 10 questions to get an assessment of your emotional state.")

user_inputs = {}

with st.form("emotion_assessment_form"):
    for q_data in questions_data:
        q_id = q_data['id']
        q_text = q_data['text']
        q_type = q_data['type']
        q_options = q_data['options']

        if q_type == 'radio':
            user_inputs[q_id] = st.radio(q_text, q_options, key=q_id)
        elif q_type == 'multiselect':
            user_inputs[q_id] = st.multiselect(q_text, q_options, key=q_id)

    submitted = st.form_submit_button("Assess My Emotion")

# --- 4. Process User Inputs and Make Prediction ---
if submitted:
    # Create a dictionary to hold the encoded features for the model
    processed_input = {}

    # Process each input based on the same logic used in preprocessing
    processed_input['mood_encoded'] = MOOD_MAPPING.get(user_inputs['mood'], MOOD_MAPPING['Neutral']) # Default if not found
    processed_input['anxious_social_scale_encoded'] = ANXIOUS_SOCIAL_MAPPING.get(user_inputs['anxious_social_scale'], ANXIOUS_SOCIAL_MAPPING['Somewhat anxious'])

    # Handle anxiety_triggers (One-Hot Encoding in preprocessing)
    # Get all possible trigger columns the model was trained on
    # (You would need to get these from your X.columns after training,
    # or ensure your list here covers all possibilities your model saw)
    all_triggers = ['Family issues', 'Work-related stress', 'Financial concerns', 'Health issues', 'Social events', 'None of the above']
    for trigger in all_triggers:
        col_name = f'trigger_{trigger.replace(" ", "_")}' # This assumes your get_dummies prefix was 'trigger'
        processed_input[col_name] = 1 if trigger in user_inputs['anxiety_triggers'] else 0
    # Special handling if 'None of the above' is selected
    if 'None of the above' in user_inputs['anxiety_triggers'] and len(user_inputs['anxiety_triggers']) > 1:
        st.warning("You selected 'None of the above' along with other triggers. Please choose only one.")
        st.stop()
    elif 'None of the above' in user_inputs['anxiety_triggers'] and len(user_inputs['anxiety_triggers']) == 1:
         for trigger in all_triggers:
             col_name = f'trigger_{trigger.replace(" ", "_")}'
             processed_input[col_name] = 0 # All other triggers are 0 if 'None of the above' is selected
         processed_input[f'trigger_{"None_of_the_above"}'] = 1


    processed_input['sleep_quality_encoded'] = SLEEP_QUALITY_MAPPING.get(user_inputs['sleep_quality'], SLEEP_QUALITY_MAPPING['Normal'])
    processed_input['appetite_change_encoded'] = APPETITE_CHANGE_MAPPING.get(user_inputs['appetite_change'], APPETITE_CHANGE_MAPPING['No significant change'])
    processed_input['lack_of_interest_encoded'] = LACK_OF_INTEREST_MAPPING.get(user_inputs['lack_of_interest'], LACK_OF_INTEREST_MAPPING['Occasionally'])
    processed_input['enjoyable_activities_encoded'] = ENJOYABLE_ACTIVITIES_MAPPING.get(user_inputs['enjoyable_activities'], ENJOYABLE_ACTIVITIES_MAPPING['Once a week'])
    processed_input['physical_anxiety_symptoms_encoded'] = PHYSICAL_ANXIETY_MAPPING.get(user_inputs['physical_anxiety_symptoms'], PHYSICAL_ANXIETY_MAPPING['No'])
    processed_input['concentration_difficulty_encoded'] = CONCENTRATION_DIFFICULTY_MAPPING.get(user_inputs['concentration_difficulty'], CONCENTRATION_DIFFICULTY_MAPPING['Occasionally'])

    # Handle coping_strategies (binary flag in preprocessing)
    processed_input['has_coping_strategies'] = 0 if 'No coping strategies' in user_inputs['coping_strategies'] else 1


    # Ensure all features from the trained model's X are present in the input for prediction.
    # This is crucial. Create a DataFrame from the processed_input dictionary.
    # The order of columns must match the order the model was trained on.
    # A robust way is to get the columns from your X_train used during model training.
    # For now, let's assume the column order is consistent.

    # Convert processed_input to a DataFrame row
    # This is a critical step to ensure column order and presence matches X_train
    # You should ideally save X.columns.tolist() during training and load it here.
    # For now, let's reconstruct the expected columns.
    # The easiest way is to use a dummy DataFrame and reindex.
    # Make sure this `feature_columns_order` list matches the exact `X.columns` list
    # after you did all the preprocessing for your model training.
    # You can get this by running `print(X.columns.tolist())` after your preprocessing script.
    # I'm providing a likely order based on the processing steps, but verify it.

    # Reconstruct the expected order of columns for the model
    # THIS LIST MUST EXACTLY MATCH THE COLUMNS IN YOUR X_TRAIN DATAFRAME!
    # A good practice is to save X_train.columns.tolist() after training and load it here.
    expected_feature_columns = [
        'mood_encoded', 'anxious_social_scale_encoded',
        'sleep_quality_encoded', 'appetite_change_encoded',
        'lack_of_interest_encoded', 'enjoyable_activities_encoded',
        'physical_anxiety_symptoms_encoded', 'concentration_difficulty_encoded',
        'has_coping_strategies',
        # One-hot encoded triggers - add all possible ones your model might have seen
        'trigger_Family_issues', 'trigger_Work-related_stress',
        'trigger_Financial_concerns', 'trigger_Health_issues',
        'trigger_Social_events', 'trigger_None_of_the_above'
    ]

    # Create a Pandas DataFrame from the processed input, ensuring correct column order
    input_df = pd.DataFrame([processed_input]).reindex(columns=expected_feature_columns, fill_value=0)

    # Make prediction
    prediction_encoded = model.predict(input_df)[0]
    predicted_emotion = le.inverse_transform([prediction_encoded])[0]

    # Display result
    st.markdown("---")
    st.subheader("Your Emotional State Assessment:")

    if predicted_emotion == 'Happy':
        st.success(f"🎉 Based on your answers, you seem to be feeling: **{predicted_emotion}!**")
        st.balloons()
    elif predicted_emotion == 'Normal':
        st.info(f"😊 Based on your answers, you seem to be feeling: **{predicted_emotion}.**")
    elif predicted_emotion == 'Sad':
        st.warning(f"😔 Based on your answers, you seem to be feeling: **{predicted_emotion}.**")
        st.write("If you're feeling down, remember it's okay to seek support. Consider talking to a trusted friend, family member, or a professional.")
    else:
        st.write(f"Your assessed emotional state is: **{predicted_emotion}**") # Fallback for unexpected labels

    st.markdown("---")
    st.caption("Disclaimer: This tool provides a basic assessment based on a machine learning model and is not a substitute for professional medical or psychological advice. If you have concerns about your mental health, please consult a qualified healthcare provider.")