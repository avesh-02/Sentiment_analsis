import io
import base64
from flask import Flask, render_template, request, Response
from textblob import TextBlob
import matplotlib.pyplot as plt

# Initialize the Flask application
app = Flask(__name__)


# Initialize sentiment counters
sentiment_counts = {
    "positive": 0,
    "negative": 0,
    "neutral": 0
}

# Route to display the homepage
@app.route('/')
def index():
    return render_template('index.html', sentiment_counts=sentiment_counts)

# Route to handle sentiment analysis and generate chart
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    # Get the input text from the form
    text = request.form['text']
    
    # Perform sentiment analysis using TextBlob
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # Get sentiment score
    
    # Determine sentiment type based on the score
    if sentiment_score > 0.1:
        sentiment = 'Positive'
        sentiment_counts['positive'] += 1
    elif sentiment_score < -0.1:
        sentiment = 'Negative'
        sentiment_counts['negative'] += 1
    else:
        sentiment = 'Neutral'
        sentiment_counts['neutral'] += 1

    # Create a bar chart to show sentiment distribution
    img = io.BytesIO()
    labels = ['Positive', 'Negative', 'Neutral']
    values = [sentiment_counts['positive'], sentiment_counts['negative'], sentiment_counts['neutral']]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['#4CAF50', '#F44336', '#FFC107'])
    plt.title('Sentiment Analysis Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.tight_layout()

    # Save the plot to the in-memory buffer
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image as base64
    chart_url = base64.b64encode(img.getvalue()).decode()

    # Return the result back to the frontend
    return render_template('index.html', sentiment=sentiment, score=sentiment_score, text=text, sentiment_counts=sentiment_counts, chart_url=chart_url)

if __name__ == '__main__':
    app.run(debug=True)
