FROM ubuntu:latest

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    bash-completion \
    openjdk-17-jdk \
    fontconfig \
    fonts-dejavu-core \
    software-properties-common \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar ANTLR
COPY antlr-4.13.1-complete.jar /usr/local/lib/antlr-4.13.1-complete.jar

COPY ./commands/antlr /usr/local/bin/antlr
COPY ./commands/antlr /usr/bin/antlr

COPY ./commands/grun /usr/local/bin/grun
COPY ./commands/grun /usr/bin/grun

# Configurar permisos para los scripts
RUN chmod +x /usr/local/lib/antlr-4.13.1-complete.jar
RUN chmod +x /usr/local/bin/antlr
RUN chmod +x /usr/bin/antlr
RUN chmod +x /usr/local/bin/grun
RUN chmod +x /usr/bin/grun

# Configurar entorno virtual de Python
COPY python-venv.sh .
RUN chmod +x ./python-venv.sh
RUN ./python-venv.sh

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages

# Copiar archivos MiniLang.g4 y Driver.py al contenedor
COPY program/MiniLang.g4 /program/
COPY program/Driver.py /program/

# Crear usuario
ARG USER=appuser
ARG UID=1001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home /program \
    --no-create-home \
    --uid "${UID}" \
    "${USER}"

# Añadir appuser al grupo ubuntu
RUN usermod -aG ubuntu appuser

# Cambiar permisos del directorio de trabajo
RUN mkdir -p /program && chown -R ${UID}:${UID} /program

USER ${USER}
WORKDIR /program
