# Study E local test environment (development scaffold; not a frozen artifact).
# Base image pinned by multi-platform index digest (pulled by the author 2026-11-19; reproducible across amd64/arm64, not byte-identical between them).
FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
ENV PYTHONDONTWRITEBYTECODE=1
RUN useradd --create-home --uid 10001 app
WORKDIR /work
COPY --chown=app:app study_e ./study_e
COPY --chown=app:app tests ./tests
USER app
CMD ["python", "-I", "-W", "error::ResourceWarning", "-m", "unittest", "discover", "-s", "tests", "-t", "."]
