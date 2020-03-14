FROM python:3.7-slim

WORKDIR /usr/src/app

ENV APP_VERSION $CI_COMMIT_REF_NAME

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./app.py" ]