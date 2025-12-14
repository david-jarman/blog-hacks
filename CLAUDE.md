# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains standalone browser-based utility tools for davidjarman.net blog. Each tool is a self-contained single HTML file with embedded CSS and JavaScript - no build process or dependencies required.

## Project Structure

- Root directory contains standalone HTML tools
- Tools are deployed to GitHub Pages at https://hacks.davidjarman.net/
- No backend, no frameworks, no build step - pure client-side HTML/CSS/JS

## Deployment

Automated via GitHub Actions workflow (.github/workflows/jekyll-gh-pages.yml):
- Triggers on push to main branch
- Uses Jekyll to build from root directory
- Deploys to GitHub Pages

## Development Workflow

Since tools are self-contained HTML files with no build process:
1. Edit HTML files directly
2. Test by opening in browser
3. Commit and push to main - deployment is automatic

No test commands, no build commands, no package managers needed.

## Adding New Tools

When creating a new tool, ALWAYS:
1. Create the standalone HTML file in the root directory
2. Add the tool to README.md following the existing format:
   - Tool name as heading (###)
   - Brief description
   - Link in format: `[tool-name](https://hacks.davidjarman.net/tool-name)`
3. Test by opening the HTML file directly in browser (use `open` command on macOS)
