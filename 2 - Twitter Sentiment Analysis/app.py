import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import json
import numpy as np

class SentimentAnalyzer:
    def __init__(self, config, model, tokenizer):
        self.config = config
        self.model = model
        self.tokenizer = tokenizer
    
    def preprocess_text(self, text):
        tokens = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(
            tokens,
            maxlen=self.config['max_sequence_length'],
            padding=self.config['padding_strategy'],
            truncating=self.config['truncating_strategy']
        )
        return padded
    
    def predict_sentiment(self, text):
        preprocessed = self.preprocess_text(text)
        prediction = self.model.predict(preprocessed)[0][0]
        return float(prediction)

@st.cache_resource
def load_model_and_tokenizer():
    model = load_model('sentiment_v2/sentiment_model_v2.h5')
    with open('sentiment_v2/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open('sentiment_v2/model_config.json') as f:
        config = json.load(f)
    return SentimentAnalyzer(config, model, tokenizer)

st.set_page_config(
    page_title="Sentiment Analysis Model",
    layout="wide",
    menu_items={
        "About": "https://github.com/SalvatoreLS"
    }
)

st.title("Sentiment Analysis Model")
st.write("This is a simple sentiment analysis model that uses a LSTM neural network to predict the sentiment of a given text. The model was trained on the sentiment140 dataset sourced by Kaggle.")

analyzer = load_model_and_tokenizer()

text = st.text_area("Enter some text to analyze", "I love this product!")
analyze_button = st.button("Analyze")

if analyze_button:
    try:
        prediction = analyzer.predict_sentiment(text)
        if prediction > 0.5:
            st.write(f"Prediction: {prediction:.3f} - Positive sentiment")
        else:
            st.write(f"Prediction: {prediction:.3f} - Negative sentiment")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

sample_sentences = [
    'This movie is fantastic. I love it',
    'I did not like the way you talked about it',
    'You are horrible when you sing',
    'That song is the worst I have ever heard',
    'I love the way she dances in the video',
    'If you are ten years old, you will love this terrible cartoon'
]

st.markdown('## Suggested sentences')
cols = st.columns(3)
for i, col in enumerate(cols):
    for sentence in sample_sentences[i*2:(i+1)*2]:
        col.markdown('- ' + sentence)

st.markdown('---')
st.markdown('## About the project')
st.markdown('This is my first model that involves LSTMs and Embeddings to predict the sentiment of a text.')
st.markdown('Since it is a simple model and it is my first project in the field of NLP, the performance and accuracy of the model are not the best.')
st.markdown('In addition, I decided not to use Transformers or advanced techniques.')
st.markdown('The scope of this project is to document my learning process.')
st.markdown('## About the model')
st.markdown('The model was trained on the sentiment140 dataset sourced by Kaggle. '
            'The dataset contains 1.6M tweets, labeled with 0 for negative sentiment and 4 for positive sentiment.')
st.markdown('The model uses a LSTM neural network and an embedding layer. I decided to use a bidirectional LSTM in order to give the model more context and give it the ability to consider the entire sequence of words in the text.')
st.markdown('Further information about the project can be found on my [GitHub](https://www.github.com/SalvatoreLS), or on the notebook that I used to train the model.')
