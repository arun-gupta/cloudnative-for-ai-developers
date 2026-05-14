#!/usr/bin/env bash
# Build the image. With --push, also tag and push to GHCR.
#
# Usage:
#   bash build.sh           Build locally as embedder:latest
#   bash build.sh --push    Build, tag as ghcr.io/<GHCR_USERNAME>/embedder:latest, and push
#
# Push requires:
#   docker login ghcr.io -u <user> -p <GitHub PAT with write:packages>

set -euo pipefail

GHCR_USERNAME="${GHCR_USERNAME:-arun-gupta}"
IMAGE_NAME="${IMAGE_NAME:-embedder}"
TAG="${TAG:-latest}"

docker build -t "${IMAGE_NAME}:${TAG}" .
echo
echo "Built ${IMAGE_NAME}:${TAG}"

if [[ "${1:-}" == "--push" ]]; then
    REMOTE="ghcr.io/${GHCR_USERNAME}/${IMAGE_NAME}:${TAG}"
    docker tag "${IMAGE_NAME}:${TAG}" "${REMOTE}"
    docker push "${REMOTE}"
    echo
    echo "Pushed ${REMOTE}"
fi
