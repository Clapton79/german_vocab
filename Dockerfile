FROM python:3.10-slim AS base

WORKDIR /german_vocab

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        mpg123 \
        gcc \
        libffi-dev \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY --link requirements.txt ./

RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

COPY --link . .

FROM base AS final

WORKDIR /german_vocab

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=base  /german_vocab/.venv /german_vocab/.venv
COPY --from=base  /german_vocab /german_vocab

ENV PATH="/german_vocab/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

USER appuser

CMD ["python", "browser.py"]


