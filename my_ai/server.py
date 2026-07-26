from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__)

knowledge_folder = "knowledge"

training_data = []


# -----------------------------
# LOAD ALL KNOWLEDGE FILES
# -----------------------------

for filename in os.listdir(knowledge_folder):

    if filename.endswith(".json"):

        file_path = os.path.join(
            knowledge_folder,
            filename
        )

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


            if isinstance(data, list):

                for item in data:

                    if isinstance(item, dict):

                        if (
                            "user_sentences" in item
                            and "answers" in item
                        ):

                            training_data.append(item)


            elif isinstance(data, dict):

                if (
                    "user_sentences" in data
                    and "answers" in data
                ):

                    training_data.append(data)


            print("Loaded:", filename)


        except Exception as error:

            print(
                "Could not load:",
                filename
            )

            print(error)


print()
print("AI KNOWLEDGE LOADED!")
print(
    "Number of knowledge categories:",
    len(training_data)
)
print()


# -----------------------------
# FIND AN ANSWER
# -----------------------------

def find_answer(message):

    message = message.lower().strip()


    for category in training_data:

        for sentence in category["user_sentences"]:

            if message == sentence.lower():

                return random.choice(
                    category["answers"]
                )


    return "I do not understand that yet."


# -----------------------------
# SHOW THE HTML BODY
# -----------------------------

@app.route("/")

def home():

    return send_from_directory(
        "body",
        "index.html"
    )


# -----------------------------
# RECEIVE QUESTIONS
# -----------------------------

@app.route(
    "/ask",
    methods=["POST"]
)

def ask_ai():

    data = request.get_json()

    user_message = data["message"]

    answer = find_answer(
        user_message
    )

    return jsonify({

        "answer": answer

    })


# -----------------------------
# START SERVER LOCALLY
# -----------------------------

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )