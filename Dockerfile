# ==================================== BASE ====================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-3.7}
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS compile-image

RUN apt-get update
RUN apt-get install -y \
    curl \
    gcc

ARG INSTALL_NODE_VERSION=${INSTALL_NODE_VERSION:-12}
RUN curl -sL https://deb.nodesource.com/setup_${INSTALL_NODE_VERSION}.x | bash -
RUN apt-get install -y \
    nodejs \
    && apt-get -y autoclean

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements requirements
RUN pip install -r requirements/dev.txt

# ================================= SERVER ================================
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS server
COPY --from=compile-image /opt/venv /opt/venv

WORKDIR /app

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid

COPY . .

EXPOSE 5000

ENV PATH="/opt/venv/bin:$PATH"
CMD [ "gunicorn", "-b", ":5000", "flask_fsm_test.app:create_app()"]

# # ================================= PRODUCTION =================================
# FROM base AS production
# RUN pip install --user -r requirements/prod.txt
# COPY supervisord.conf /etc/supervisor/supervisord.conf
# COPY supervisord_programs /etc/supervisor/conf.d
# EXPOSE 5000
# ENTRYPOINT ["/bin/bash", "shell_scripts/supervisord_entrypoint.sh"]
# CMD ["-c", "/etc/supervisor/supervisord.conf"]

# =================================== MANAGE ===================================
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS manage
COPY --from=compile-image /opt/venv /opt/venv

WORKDIR /app

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid

COPY . .
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT [ "flask" ]
