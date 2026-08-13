#!/bin/sh

set -e

if [ -z "$GITHUB_TOKEN" ]; then
    echo "GITHUB_TOKEN is not set."
    exit 1
fi

git config --global user.name "CI/CD Intelligence Agent"
git config --global user.email "ci-agent@users.noreply.github.com"

git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"

if [ ! -d "/workspace/.git" ]; then
    git clone "https://github.com/pruthviraj-m/ci-cd-intelligence-agent.git" /workspace
fi

cd /workspace

echo "Repository ready."
echo "Starting CI remediation worker..."

exec python -m app.worker