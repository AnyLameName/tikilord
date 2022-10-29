FROM python
LABEL maintainer="jay.gagnon@gmail.com"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install poetry
COPY ./fonts/* /fonts/
WORKDIR /code/
COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-interaction --no-ansi
COPY . /code/
EXPOSE 9000
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:9000"]
