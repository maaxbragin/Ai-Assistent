import requests


class AIClient:
    def __init__(self, api_key: str, api_url: str, model: str):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        

    def get_answer(self, prompt: str) -> str:
        # Формат запроса теперь точно такой же, как у OpenAI
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            response = requests.post(
                self.api_url, headers=self.headers, json=payload, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            return "Ошибка: Превышено время ожидания ответа от OpenRouter."
        except requests.exceptions.HTTPError as e:
            error_details = e.response.text if e.response is not None else "Нет деталей"
            return f"Ошибка API (HTTP {e.response.status_code}): {error_details}"
        except Exception as e:
            return f"Неизвестная ошибка: {e}"
