FROM public.ecr.aws/lambda/python:3.12

ENV LANG=ja_JP.UTF-8  \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8 \
    TZ=JST-9 \
    TERM=xterm \
    # UV
    UV_COMPILE_BYTCODE=1 \
    UV_CAHE_DIR=/root/.cache/uv \
    UV_LINK_MODE=copy \
    PATH="/root/.local/bin/:$PATH"

WORKDIR ${LAMBDA_TASK_ROOT}

# App
COPY lambda/handler.py pyproject.toml uv.lock README.md ${LAMBDA_TASK_ROOT}/
COPY src ${LAMBDA_TASK_ROOT}/src

RUN dnf install gcc-c++ tar -y

# UV
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# python setup
RUN uv sync --python-preference only-system
RUN uv pip install -e . 

CMD ["handler.lambda_handler"]
