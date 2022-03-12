FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /ace_api
COPY requirements.txt /ace_api/
RUN pip install -r requirements.txt
COPY . /ace_api/

CMD ["sh", "ops/backend_start.sh"]