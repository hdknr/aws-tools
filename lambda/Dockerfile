FROM public.ecr.aws/lambda/python:3.12

ENV LANG=ja_JP.UTF-8  \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8 \
    TZ=JST-9 \
    TERM=xterm

#
RUN dnf install gcc-c++ -y
RUN pip install pip poetry -U 
RUN poetry config virtualenvs.create false
#

COPY lambda/handler.py ${LAMBDA_TASK_ROOT}
COPY pyproject.toml poetry.lock README.md ${LAMBDA_TASK_ROOT}/
COPY awstools/ ${LAMBDA_TASK_ROOT}/awstools/
#
RUN poetry install  --without dev

CMD ["handler.lambda_handler"]