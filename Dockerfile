FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

# install geospatial libraries and those on requirements.txt
RUN apt-get update && \
#    apt-get install software-properties-common -y && \
#    add-apt-repository ppa:ubuntugis/ppa && \
    apt-get install -y binutils libproj-dev gdal-bin  \
    libgeos++-dev libgeos-c1v5 libgeos-dev libgeos-doc && \
    # undo apt-update \
    rm -rf /var/lib/apt/lists/* && \
    # update pip and install requirements \
    pip install --upgrade pip && pip install -r requirements.txt
ADD . /app/