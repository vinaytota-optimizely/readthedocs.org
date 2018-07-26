# Inherit from openresty for supervisor/nginx/lua/etc.
FROM debian:jessie

# Build args for PyPI Mirror.
ARG PIP_INDEX_URL=${PIP_INDEX_URL:-""}
ENV PIP_INDEX_URL ${PIP_INDEX_URL}

# Configure host.
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends make build-essential \
        texlive texlive-latex-recommended texlive-latex-extra \
        texlive-fonts-recommended locales git python-dev supervisor \
        libevent-dev libjpeg-dev libxml2-dev libxslt-dev libpq-dev libssl-dev \
        zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
        python python-setuptools python-pip ca-certificates nginx && \
    easy_install virtualenv && \
    export LANGUAGE=en_US.UTF-8 && \
    export LANG=en_US.UTF-8 && \
    export LC_ALL=en_US.UTF-8 && \
    locale-gen en_US.UTF-8 && \
    dpkg-reconfigure locales && \
    mkdir -p /app/readthedocs && \
    # clean up
    apt-get clean -yqq && \
    apt-get autoclean -y && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Set all pyenv version/paths.
ENV PY3_VERSION='3.6.5'
ENV PYENV_SHELL=sh

# pyenv-installer doesn't work right if the directory already exists.
ENV PYENV_ROOT=/opt/pyenv
ENV PYENV_BIN="${PYENV_ROOT}/bin"
ENV PYENV_SHIM="${PYENV_ROOT}/shims"
ENV PYENV_VENV_SHIM="${PYENV_ROOT}/plugins/pyenv-virtualenv/shims"
ENV PATH="${PYENV_BIN}:${PYENV_SHIM}:${PYENV_VENV_SHIM}:${PATH}"

# Install pyenv and set our version as global for this user.
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | sh && \
    # Install Python3 and set it as global python for this user.
    pyenv install ${PY3_VERSION} && pyenv global ${PY3_VERSION}

# Copy reqs.
COPY requirements /requirements
RUN pip install -r /requirements/deploy.txt

# Upgrade some of the deploy dependencies.
RUN pip install --upgrade pip && pip install -U psycopg2-binary gunicorn gevent

# Copy the supervisord config.
COPY configs/supervisord/readthedocs.conf /etc/supervisor/conf.d/

# Copy the nginx configs over.
RUN sed -i 's/www-data/root/g' /etc/nginx/nginx.conf
COPY configs/nginx/readthedocs.conf /etc/nginx/conf.d/readthedocs.conf

WORKDIR /app/readthedocs

# Copy app code.
COPY . /app/readthedocs

# Make sure app is available to runtime.
RUN python setup.py develop

# Make sure statics are collected.
RUN python manage.py collectstatic --noinput

# Make sure supervisor is running.
ENTRYPOINT ["supervisord", "-n"]
