# Contribution Guidelines for Mediaserver Newsletter Project

> **Based on [SeaweedbrainCY/jellyfin-newsletter](https://github.com/SeaweedbrainCY/jellyfin-newsletter) — original Jellyfin newsletter project**

Thank you for your interest in contributing to Mediaserver Newsletter!  
We appreciate your willingness to help improve the project.  
This document outlines the guidelines and processes for contributing, ensuring a smooth and collaborative experience for everyone.

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
    - [Fork the Repository](#fork-the-repository)
    - [Set up the Project](#set-up-the-project)
3. [Contribution Process](#contribution-process)
    - [Issue Tracker](#issue-tracker)
    - [Branching](#branching)
    - [Code Style](#code-style)
    - [Testing](#testing)
4. [Submitting Pull Requests](#submitting-pull-requests)
5. [Security](#security)
6. [Community and Communication](#community-and-communication)
7. [Acknowledgements](#acknowledgements)
8. [License](#license)

## Introduction

Mediaserver Newsletter is an open-source project that provides a newsletter system for Jellyfin **and Emby** users.  
We welcome contributions from developers, designers, and anyone interested in improving the project.

## Getting Started

### Fork the Repository

Before you start contributing, fork the Mediaserver Newsletter repository to your GitHub account.  
You will be working on your forked repository and submitting pull requests from there.

### Requirements
- Python 3.9+
- Jellyfin or Emby API key - see [How to generate an API key](https://github.com/SeaweedbrainCY/jellyfin-newsletter?tab=readme-ov-file#how-to-generate-a-jellyfin-api-key)
- A TMDB API key (free) - see [How to generate a TMDB API key](https://github.com/SeaweedbrainCY/jellyfin-newsletter?tab=readme-ov-file#how-to-generate-a-tmdb-api-key)
- A SMTP server

### Installation and Setup

1. Install required packages:
    ```bash
    # Unix:
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Windows:
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  Copy the example config and fill it in:
    ```bash
    cp config/config-example.yml config/config.yml
    ```
    Edit `config/config.yml` for **Jellyfin or Emby**, and fill in all fields.

3. Make sure these locales are enabled:
    - `en_US.UTF-8 UTF-8`
    - `fr_FR.UTF-8 UTF-8`

    On Debian-based systems:
    ```bash
    sudo locale-gen
    ```
    For other systems, please refer to your system documentation.

4. Run the script:
    ```bash
    python main.py
    ```

## Contribution Process

### Issue Tracker

Check the [Issue Tracker](https://github.com/ldoctoru/mediaserver-newsletter/issues) before starting new features or bugfixes.  
If you find a new issue or want to suggest an enhancement, open a new issue with details and steps to reproduce.

### Commit Signature

**All commits must be signed.**  
[How to sign commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits):

```bash
git commit -S -m "Your commit message"