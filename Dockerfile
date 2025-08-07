FROM python:3.13-slim AS build

WORKDIR /tmp
RUN pip install uv
COPY pyproject.toml uv.lock /tmp/
RUN uv export --no-dev --format requirements-txt > requirements.txt
RUN uv export --format requirements-txt > dev-requirements.txt


FROM python:3.13-slim AS test

WORKDIR /backend
COPY --from=build /tmp/dev-requirements.txt /backend/dev-requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/dev-requirements.txt
COPY ./app /backend/app
COPY ./tests /backend/tests
COPY ./pytest.ini /backend/


FROM python:3.13-slim

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN addgroup --gid $GROUP_ID nonroot && adduser --uid $USER_ID --ingroup nonroot nonroot

WORKDIR /backend

COPY --from=build /tmp/requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
# TODO: Uncomment when we have a database
# COPY ./alembic.ini /backend/
# COPY ./migrations /backend/migrations
COPY ./app /backend/app

USER nonroot

CMD ["python", "-m", "app"]
