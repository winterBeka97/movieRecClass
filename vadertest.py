import os
import json
import pandas as pd
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

data_folder = "Data"

good_comments = []
bad_comments = []

def classify_sentiment(comment):
    """
    Classifies the sentiment of a comment as good, neutral, or bad using VADER.
    """
    vs = analyzer.polarity_scores(comment)
    compound = vs['compound']
    if compound >= 0.05:
        return "good"
    elif compound <= -0.05:
        return "bad"
    else:
        return "neutral"

for filename in os.listdir(data_folder):
    if filename.endswith(".json"):  
        filepath = os.path.join(data_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reviews = json.load(f)  

                if isinstance(reviews, list):
                    for review in reviews:
                        if 'content' in review:
                            comment = review['content']
                            sentiment = classify_sentiment(comment)
                            print(f"File: {filename}, Comment: '{comment[:50]}...', Sentiment: {sentiment}")
                            
                            if sentiment == "good":
                            # Append the good comment to the dictionary
                                good_comments.append({
                                    'file': filename,
                                    'comment': comment,
                                    'sentiment': sentiment
                                }) 
                            elif sentiment == "bad":
                                # Append the bad comment to the dictionary
                                bad_comments.append({
                                    'file': filename,
                                    'comment': comment,
                                    'sentiment': sentiment
                                })
                        else:
                            print(f"Warning: File '{filename}' contains a review without a 'content' key.")
                else:
                    print(f"Warning: File '{filename}' does not contain a list of reviews.")

        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON in file: {filepath}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {filepath}: {e}")

print("\nSentiment analysis complete.")

# Export classified comments to a CSV file
df = pd.DataFrame(good_comments)
output_file = "good_comments.csv"
df.to_csv(output_file, index=False)

df = pd.DataFrame(bad_comments)
output_file = "bad_comments.csv"
df.to_csv(output_file, index=False)

print(f"\nClassified comments saved to csv file.")
