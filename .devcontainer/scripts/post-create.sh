#!/usr/bin/env bash

echo "▶ Installing project dependencies with pnpm..."
pnpm install

echo "▶ Installing Playwright Chromium browser..."
pnpm exec playwright install chromium

"update-submodules": ["git", "submodule", "update", "--recursive"]

// Example: Install Python dependencies with Poetry
// "install-python-deps": ["poetry", "install", "--no-root"],

// Example: Install Node.js dependencies
// "install-node-deps": ["npm", "install"],

// Example: Run database migrations
// "migrate-db": ["python", "manage.py", "migrate"]
