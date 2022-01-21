FROM python:3.10-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .
RUN mkdir app/data downloads
RUN gdown --id 1Hb9K3EyJ1VyX_NCFKik6l-GJPuruJ_cL -O downloads/indonesia-stocks.zip
RUN unzip -o downloads/indonesia-stocks.zip -d app/data

# ENV BOKEH_LOG_LEVEL=debug
ENV BOKEH_RESOURCES=cdn
ENV BOKEH_ALLOW_WS_ORIGIN=indostock-vizz.herokuapp.com

EXPOSE $PORT
# EXPOSE 5006

CMD bokeh serve app --port $PORT 