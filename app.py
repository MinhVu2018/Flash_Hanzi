import streamlit as st
import pandas as pd
import random
from typing import List, Tuple

# Function to get a random word and 3 incorrect options
def get_flashcard_data(data_df) -> Tuple[str, str, List[str]]:
    # Select a random row for the question
    random_index = random.randint(0, len(data_df) - 1)
    question_row = data_df.iloc[random_index]
    
    # Get the correct word and meaning
    chinese_word = f'{question_row["Word"]} ({question_row["Pinyin"]})'
    correct_meaning = question_row['Meaning']
    
    # Get 3 random incorrect meanings (ensuring they're different from the correct one)
    incorrect_options = []
    while len(incorrect_options) < 3:
        random_idx = random.randint(0, len(data_df) - 1)
        if random_idx != random_index:  # Avoid selecting the correct answer
            meaning = data_df.iloc[random_idx]['Meaning']
            if meaning != correct_meaning and meaning not in incorrect_options:
                incorrect_options.append(meaning)
    
    # Combine correct and incorrect options
    all_options = incorrect_options + [correct_meaning]
    # Shuffle the options
    random.shuffle(all_options)
    
    return chinese_word, correct_meaning, all_options

def filter_df(raw_df, selected_topic):
    if selected_topic != "All Topics": 
        filtered_df = raw_df[raw_df["Topic"] == selected_topic]
    else:
        filtered_df = raw_df
    return filtered_df

def main():
    with st.sidebar:
        # Main flashcard game
        st.title("Flash_Hanzi")
        
        uploaded_file = st.file_uploader("Upload your vocabulary CSV file", type=["csv"])
        if uploaded_file:
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_csv("Chinese_Vocabulary_with_Specific_Topics.csv")
        
        st.session_state['data'] = raw_df.copy()
        
        # Get unique topics from the dataframe
        topics = [" * All Topics *"] + sorted(raw_df["Topic"].unique().tolist())
    
    # Create a dropdown for topic selection
    selected_topic = st.selectbox("Select a topic:", topics)
    if selected_topic != " * All Topics *": 
        st.session_state['data']  = raw_df[raw_df["Topic"] == selected_topic].copy()
        st.session_state['flashcard'] = get_flashcard_data(st.session_state['data'])

    if 'flashcard' not in st.session_state:
        st.session_state['flashcard'] = get_flashcard_data(st.session_state['data'])
        
    if st.button("Next word", key="next_flashcard"):
                st.session_state['flashcard'] = get_flashcard_data(st.session_state['data'])
    # Display the current flashcard
    chinese_word, correct_meaning, options = st.session_state['flashcard']

    st.subheader(f'What does " {chinese_word} " mean?')
    # Display the options as buttons
    selected_option = None
    for option in options:
        if st.button(option, key=f"option_{option}"):
            selected_option = option

    # Check the answer if an option was selected
    if selected_option:
        if selected_option == correct_meaning:
            st.success("Correct! 🎉")
        else:
            st.error(f"Incorrect! Please try again.")


if __name__ == "__main__":
    main()
