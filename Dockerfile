FROM python:3.12.2

ENV PROMETHEUS_MULTIPROC_DIR=/var/tmp/prometheus_multiproc_dir
RUN mkdir $PROMETHEUS_MULTIPROC_DIR \
    && chown www-data $PROMETHEUS_MULTIPROC_DIR \
    && chmod g+w $PROMETHEUS_MULTIPROC_DIR

WORKDIR /srv/service
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV GDC_ID= \
    GDC_TITLE= \
    GDC_DESCRIPTION= \
    GDC_STAC_API=

ADD . .

USER www-data
EXPOSE 8000

CMD ["uvicorn", "--host=0.0.0.0", "--port=8000", "datacube-access.app:app"]
