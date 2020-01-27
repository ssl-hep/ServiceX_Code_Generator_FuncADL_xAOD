FROM python:3.7

RUN useradd -ms /bin/bash servicex

WORKDIR /home/servicex
RUN mkdir ./servicex

COPY setup.cfg setup.cfg
COPY requirements.txt requirements.txt
COPY README.md README.md
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY boot.sh ./
COPY app.conf ./
COPY servicex/ ./servicex
COPY scripts/from_ast_to_zip.py .
RUN chmod +x boot.sh

USER servicex
ENV APP_CONFIG_FILE "/home/servicex/app.conf"

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
