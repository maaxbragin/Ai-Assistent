import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from ai_client import AIClient

load_dotenv()

app = Flask(__name__)

# Инициализируем клиент, передавая данные из .env
ai_bot = AIClient(
    api_key=os.getenv("AI_API_KEY"),
    api_url=os.getenv("AI_API_URL"),
    model=os.getenv("AI_MODEL"),
)


@app.route("/", methods=["GET", "POST"])
def index():
    response_text = None
    error_text = None

    if request.method == "POST":
        user_prompt = request.form.get("prompt", "").strip()

        if not user_prompt:
            error_text = "Вы отправили пустой запрос."
        else:
            response_text = ai_bot.get_answer(user_prompt)

            if response_text.startswith("Ошибка") or response_text.startswith(
                "Неизвестная"
            ):
                error_text = response_text
                response_text = None

    return render_template("index.html", response=response_text, error=error_text)


if __name__ == "__main__":
    app.run(debug=True)
