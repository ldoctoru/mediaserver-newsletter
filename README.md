# Mediaserver Newsletter — keep your users updated (Jellyfin & Emby)

> **Based on [SeaweedbrainCY/jellyfin-newsletter](https://github.com/SeaweedbrainCY/jellyfin-newsletter) — original Jellyfin newsletter project**

<p align="center">
<img src="https://github.com/ldoctoru/mediaserver-newsletter/actions/workflows/build_and_deploy.yml/badge.svg?branch="/>
 <img src="https://img.shields.io/github/license/ldoctoru/mediaserver-newsletter"/>
<img src="https://img.shields.io/github/v/release/ldoctoru/mediaserver-newsletter"/>
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/ldoctoru/mediaserver-newsletter/main/assets/jellyfin_newsletter.png" width=100>
</p>

A self-hosted newsletter for **Jellyfin** and **Emby** to notify your users of your latest media additions.  
Mediaserver Newsletter connects to your media server API, retrieves new movies and shows, and emails your subscribers.  

It is fully customizable and can be run on a schedule using the built-in cron job or your own scheduler.

---

## Table of Contents
1. [What it looks like](#what-it-looks-like)
2. [Features](#features)
3. [Installation: Docker](#installation-docker)
4. [Current limitations](#current-limitations)
5. [License](#license)
6. [Contribution](#contribution)
7. [How to](#how-to)
   - [Generate a Jellyfin/Emby API key](#how-to-generate-a-jellyfin-emby-api-key)
   - [Generate a TMDB API key](#how-to-generate-a-tmdb-api-key)

---

## What it looks like 
<p align="center">
<img src="https://raw.githubusercontent.com/ldoctoru/mediaserver-newsletter/main/assets/new_media_notification_preview.png" width=500>
</p>

---

## Features
- Works with **Jellyfin** and **Emby** servers (auto-select via config)
- Retrieves newly added movies and TV shows
- Sends customizable, responsive newsletters to your users
- Movie/series details and posters from TMDB
- Groups TV shows by season
- Supports English and French
- Easy config for recipients and watched folders
- Docker-native (runs anywhere)

---

## Installation: Docker

### Requirements

- Docker or Docker Compose
- A Jellyfin **or** Emby API key (see below)
- A TMDB API key (free)
- An SMTP server for sending emails

### Quick Start

**docker-compose.yml:**
```yaml
services:
  mediaserver-newsletter:
    container_name: mediaserver-newsletter
    image: ghcr.io/ldoctoru/mediaserver-newsletter:1.0.0
    environment:
      USER_UID: 1000
      USER_GID: 1000
      TZ: 'Europe/Bucharest'
    volumes:
      - ./config:/app/config