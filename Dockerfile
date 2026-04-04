FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install pydantic openai

CMD ["python", "inference.py"]