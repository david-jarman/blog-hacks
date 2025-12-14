# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains standalone browser-based utility tools for davidjarman.net blog. Each tool is a self-contained single HTML file with embedded CSS and JavaScript - no build process or dependencies required.

## Project Structure

- Root directory contains standalone HTML tools
- Tools are deployed to GitHub Pages at https://hacks.davidjarman.net/
- No backend, no frameworks, no build step - pure client-side HTML/CSS/JS

## Current Tools

### guitar-tuner.html
Browser-based guitar tuner using Web Audio API. Uses autocorrelation pitch detection to identify guitar string frequencies (E A D G B E standard tuning). Requires microphone access.

### clipboard-inspector.html
Diagnostic tool for examining clipboard contents. Shows all MIME types present in clipboard data via Clipboard API. Useful for debugging copy/paste issues. Displays text, images, and binary data grouped by type with tabbed interface.

### base64.html
Simple Base64 encoder/decoder with UTF-8 support. Uses btoa/atob with proper Unicode handling via encodeURIComponent/decodeURIComponent.

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
