import os
import pandas as pd
import requests
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu
import nltk

# Load .env file and API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Download tokenizer data (for BLEU score)
nltk.download('punkt')

# Define question categories and prompts
CATEGORIES = {
    "AI MEng Program": "Information about our AI MEng program at Duke University",
    "Duke/Pratt Info": "Information for prospective students about Duke and/or Pratt (including facts/figures)",
    "Campus Events": "Information about events on campus at Duke University"
}


def generate_questions(category_description, num_questions=10):
    """
    Generate a list of questions for a given category using GPT-4o.

    Args:
        category_description (str): Description of the category.
        num_questions (int): Number of questions to generate.

    Returns:
        List[str]: A list of cleaned questions.
    """
    prompt = f"Generate {num_questions} unique and relevant questions for the following topic:\n\n{category_description}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    raw_lines = response.choices[0].message.content.split("\n")
    cleaned_questions = [q.strip("0123456789). ").strip() for q in raw_lines if q.strip()]
    return cleaned_questions[:num_questions]


def create_question_set(filename="duke_questions.csv"):
    """
    Generate 30 questions across all categories and save them to a CSV.

    Args:
        filename (str): Output CSV filename.

    Returns:
        pd.DataFrame: The DataFrame of generated questions.
    """
    data = []
    for category, desc in CATEGORIES.items():
        questions = generate_questions(desc)
        for question in questions:
            data.append({
                "Category": category,
                "Question": question,
                "Chatbot_Response": "",
                "GPT4o_Response": "",
                "Cosine_Similarity": 0.0,
                "BLEU_Score": 0.0
            })
    df = pd.DataFrame(data)

    # Force correct dtypes to avoid warning
    df["Chatbot_Response"] = df["Chatbot_Response"].astype(str)
    df["GPT4o_Response"] = df["GPT4o_Response"].astype(str)

    df.to_csv(filename, index=False)
    return df


def query_custom_chatbot(question):
    """
    Query your deployed chatbot via HTTP GET and extract the 'answer' field.

    Args:
        question (str): The input question.

    Returns:
        str: Textual response from your chatbot or error fallback.
    """
    try:
        url = "https://duke-chatbot-service-518487429487.us-central1.run.app/ask"
        params = {"question": question}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("answer", "[No 'answer' key in response]")
    except Exception as e:
        print(f"Custom chatbot error for '{question}': {e}")
        return "[Error from custom chatbot]"


def query_gpt4o(question):
    """
    Query GPT-4o to get the official answer.

    Args:
        question (str): The input question.

    Returns:
        str: GPT-4o's response.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content.strip()


def evaluate_similarity(custom_response, gpt_response):
    """
    Compute cosine similarity and BLEU score between two responses.

    Args:
        custom_response (str): Response from your chatbot.
        gpt_response (str): Reference GPT-4o response.

    Returns:
        (float, float): Cosine similarity, BLEU score
    """
    try:
        tfidf = TfidfVectorizer().fit_transform([custom_response, gpt_response])
        cosine = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    except:
        cosine = 0.0
    try:
        bleu = sentence_bleu([gpt_response.split()], custom_response.split())
    except:
        bleu = 0.0
    return cosine, bleu


def populate_and_evaluate(filename="duke_questions.csv"):
    """
    Populate chatbot + GPT responses and evaluation scores in the CSV.

    Args:
        filename (str): Path to the CSV file to read and update.

    Returns:
        pd.DataFrame: Updated DataFrame with all columns populated.
    """
    df = pd.read_csv(filename)

    for i, row in df.iterrows():
        question = row["Question"]
        chatbot_resp = query_custom_chatbot(question)
        gpt4_resp = query_gpt4o(question)
        cosine, bleu = evaluate_similarity(chatbot_resp, gpt4_resp)

        df.at[i, "Chatbot_Response"] = chatbot_resp
        df.at[i, "GPT4o_Response"] = gpt4_resp
        df.at[i, "Cosine_Similarity"] = cosine
        df.at[i, "BLEU_Score"] = bleu

        print(f"[{i+1}/{len(df)}] Done: {question[:60]}...")

    df.to_csv(filename, index=False)
    print(f"\nEvaluation complete. Saved to: {filename}")
    return df


def main():
    """
    Run the full pipeline: generate questions, get responses, evaluate.
    """
    filename = "duke_questions.csv"
    print("Generating all questions...")
    create_question_set(filename)
    print("Populating responses and evaluating metrics...")
    populate_and_evaluate(filename)
    print("All results saved to duke_questions.csv")


if __name__ == "__main__":
    main()
