# Jellyfin Newsletter - Your recent additions in your users' inbox

<p align="center">
<img src="https://raw.githubusercontent.com/SeaweedbrainCY/jellyfin-newsletter/refs/heads/main/assets/jellyfin_newsletter.png" width=100>
</p>

A simple newsletter python script for Jellyfin to notify your users of your last additions. Based on your jellyfin API it will retrieve the last added items and send them to your users. 

It is fully customizable and can be run on a schedule using a cron job or a task scheduler.

## What it looks like ? 
<p align="center">
<img src="https://raw.githubusercontent.com/SeaweedbrainCY/jellyfin-newsletter/refs/heads/main/assets/new_media_notification_preview.png" width=500>
</p>

## Features
- Retrieve the last added movies and TV shows from your Jellyfin server
- Send a newsletter to your users with the last added items
- Retrieve the movie details from TMDB, including its poster
- Group TV shows by seasons
- Fully customizable and responsive email template
- Easy to maintain, extend, setup and run
- Support for multiple languages (English and French for now)
- Configure the list of recipients
- Configure specific folders to watch for new items

## Installation
### Requirements
- Python 3.9+ 
- Jellyfin API key - [How to generate an API key](https://github.com/SeaweedbrainCY/jellyfin-newsletter?tab=readme-ov-file#requirements)
- A TMDB API key (free) - [How to generate a TMDB API key]()
- A SMTP server 

### Installation and setup
1. Clone the repository on your machine
```bash
git clone https://github.com/SeaweedbrainCY/jellyfin-newsletter
```
2. Install the required packages 
```bash
# Unix : 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows :
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
3.  Copy the `config/config-example.yml` to `config/config.yml` ([direct download](https://raw.githubusercontent.com/SeaweedbrainCY/jellyfin-newsletter/refs/heads/main/config/config-example.yml)) and fill in the required fields. **All fields are required**.
```yaml
jellyfin:
    # URL of your jellyfin server
    url: "" 

    # API token of your jellyfin server. See requirements for more info
    api_token: ""

    # List of folders to watch for new movies. 
    # You can find them in your Jellyfin Dashboard -> Libraries -> Select a library -> Folder **WITHOUT THE TRAILING /**
    watched_film_folders:
        - ""
        # example for /movies folder add "movies"


    # List of folders to watch for new movies. 
    # You can find them in your Jellyfin Dashboard -> Libraries -> Select a library -> Folder **WITHOUT THE TRAILING /**
    watched_tv_folders:
        - ""
        # example for /movies folder add "movies"
  
  # Number of days to look back for new items
  observed_period_days: 30

tmdb:
    # TMDB API key. See requirements for more info.
    api_key: ""

# Email template to use for the newsletter
email_template:
    # Language of the email. Supported languages are "en" and "fr".
    language: "en"
    # Subject of the email
    subject: ""
    # Title of the email
    title: ""
    # Subtitle of the email
    subtitle: ""
    # Will be used to redirect the user to your Jellyfin instance
    jellyfin_url: ""
    # Used in the footer. This is a legal notice.
    unsubscribe_email: ""
    # Used in the footer
    jellyfin_owner_name: ""


email:
    # SMTP server configuration. TLS is required for now.
    smtp_server: ""
    smtp_port: 
    smtp_username: ""
    smtp_password: ""
    smtp_sender_email: ""


# List of users to send the newsletter to.
recipients:
  - ""
  # Example : "fname@email.com" or "fname <fname@email.com">
```

4. Run the script
```bash
python main.py
```

5. (Optional) Schedule the script to run on a regular basis. 
```bash
# Unix :
crontab -e
# Add the following line to run the script every 1st of the month at 8am
0 8 1 * * /path/to/project/venv/bin/python /path/to/main.py
```

## Current limitations
- Only supports English and French languages for the email template
- Only supports TLS for the SMTP server
- Only supports movies and TV shows for now
- Not included as a Jellyfin plugin yet. It required to be run manually or scheduled

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribution
Feel free to contribute to this project by opening an issue or a pull request.

If you like this project, consider giving it a ⭐️.

If you encounter any issues, please let me know by opening an issue.

## How to 
### How to generate a Jellyfin API key
1. Go to your Jellyfin dashboard
2. Scroll to advanced section and click on API keys
3. Click on the `+` button to create a new API key
4. Fill in the required fields and click on save
5. Copy the generated API key
6. Paste it in the `config.yml` file under `jellyfin.api_token`

### How to generate a TMDB API key
1. Go to the [TMDB website](https://www.themoviedb.org/)
2. Create an account or log in
3. Go to your account settings
4. Click on the API section
5. Click on the `Create` button to create a new API key
6. Copy the API key named "API Read Access Token"
7. Paste it in the `config.yml` file under `tmdb.api_key`
