FROM rasa/rasa
ENV BOT_ENV=production
COPY . /var/www
WORKDIR /var/www
RUN pip install rasa
RUN pip install spacy
RUN rasa train
ENTRYPOINT ["rasa", "run", "actions"]
ENTRYPOINT ["rasa", "run", "--enable-api", "--cors", "*"]