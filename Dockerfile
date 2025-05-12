FROM python:3.11.2-slim as dependencies

ENV APP_PATH /usr/app
ENV TIMEZONE 'America/Manaus'

COPY . $APP_PATH/

WORKDIR $APP_PATH

RUN mkdir -p $APP_PATH \
  && apt-get update && apt-get install -y \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    build-essential \
    ncurses-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    gettext \
    libpq-dev \
    locales \
    python-dev \
    python3-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    openjdk-11-jdk \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* \
  && echo $TIMEZONE > /etc/timezone \
  && rm /etc/localtime \
  && ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime \
  && dpkg-reconfigure -f noninteractive tzdata \
  && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/'  /etc/locale.gen \
  && sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/'  /etc/locale.gen \
  && locale-gen

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

EXPOSE 8888

COPY requirements.txt .

RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt