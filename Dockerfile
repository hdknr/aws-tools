FROM python:3
ARG BASE

WORKDIR ${BASE} 

# Debian
RUN apt-get update && \
    apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG=ja_JP.UTF-8  \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8 \
    TZ=JST-9 \
    TERM=xterm

# TOFU
# https://opentofu.org/docs/intro/install/deb/
RUN apt-get install -y apt-transport-https ca-certificates curl gnupg
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://get.opentofu.org/opentofu.gpg | tee /etc/apt/keyrings/opentofu.gpg >/dev/null
RUN curl -fsSL https://packages.opentofu.org/opentofu/tofu/gpgkey | gpg --no-tty --batch --dearmor -o /etc/apt/keyrings/opentofu-repo.gpg >/dev/null
RUN chmod a+r /etc/apt/keyrings/opentofu.gpg /etc/apt/keyrings/opentofu-repo.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/opentofu.gpg,/etc/apt/keyrings/opentofu-repo.gpg] https://packages.opentofu.org/opentofu/tofu/any/ any main"  >  /etc/apt/sources.list.d/opentofu.list
RUN echo "deb-src [signed-by=/etc/apt/keyrings/opentofu.gpg,/etc/apt/keyrings/opentofu-repo.gpg] https://packages.opentofu.org/opentofu/tofu/any/ any main"   >>/etc/apt/sources.list.d/opentofu.list
RUN chmod a+r /etc/apt/sources.list.d/opentofu.list
RUN apt-get update &&apt-get install -y tofu


# Poetry
COPY pyproject.toml poetry.lock README.md ${BASE}/
COPY awstools/ ${BASE}/awstools/
#
RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

