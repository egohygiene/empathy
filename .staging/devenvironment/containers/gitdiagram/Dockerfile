######################################################################
# gitdiagram – interactive architecture diagram generator
# https://github.com/ahmedkhaleel2004/gitdiagram
#
# This image clones the gitdiagram Next.js application at the ref
# specified by GITDIAGRAM_REF, installs its Bun dependencies and
# runs the Next.js development server on port 3000.
#
# Required runtime environment variables (pass via docker-compose):
#   AI_PROVIDER          – "openai" or "openrouter"
#   OPENAI_API_KEY       – OpenAI API key (when AI_PROVIDER=openai)
#   OPENROUTER_API_KEY   – OpenRouter API key (when AI_PROVIDER=openrouter)
#
# Optional but recommended:
#   GITHUB_PAT           – GitHub PAT; raises API rate limit from 60→5000/hr
######################################################################
# hadolint global ignore=DL3008,DL3006
FROM oven/bun:1.3.11

WORKDIR /app

USER root

# Install git (needed to clone the source) and ca-certificates for HTTPS
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Pin the gitdiagram source to a specific branch or tag for reproducibility.
# Override at build time with --build-arg GITDIAGRAM_REF=<branch|tag>.
ARG GITDIAGRAM_REF=main
RUN git clone --depth 1 --branch "${GITDIAGRAM_REF}" \
        https://github.com/ahmedkhaleel2004/gitdiagram.git . \
    && rm -rf .git

# Install root JavaScript/TypeScript dependencies
RUN bun install --frozen-lockfile

EXPOSE 3000

ENV NEXT_TELEMETRY_DISABLED=1 \
    NODE_ENV=development \
    PORT=3000 \
    HOSTNAME=0.0.0.0 \
    NEXT_PUBLIC_GENERATION_BACKEND=next

CMD ["bun", "--bun", "next", "dev", "--turbo"]
