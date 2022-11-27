FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /code/docker
#
# pull official base image
#FROM python:3.8.3-alpine
#
## create directory for the app user
#RUN mkdir -p /home/app
#
## create the app user
#RUN addgroup -S app && adduser -S app -G app
#
## create the appropriate directories
#ENV HOME=/home/app
#ENV APP_HOME=/home/app/stationsApp
#RUN mkdir $APP_HOME
#RUN mkdir $APP_HOME/static
#RUN mkdir $APP_HOME/media
#WORKDIR $APP_HOME
#
## install dependencies
#RUN apk update && apk add libpq jpeg-dev zlib-dev libjpeg
#COPY --from=builder /usr/src/app/wheels /wheels
#COPY --from=builder /usr/src/app/requirements.txt .
#RUN pip install --no-cache /wheels/*
#
## copy entrypoint.sh
#COPY ./entrypoint.sh $APP_HOME
#
## copy project
#COPY . $APP_HOME
#
## chown all the files to the app user
#RUN chown -R app:app $APP_HOME
#
## change to the app user
#USER app
#
## run entrypoint.sh
#ENTRYPOINT ["/home/app/stationsApp/entrypoint.sh"]
