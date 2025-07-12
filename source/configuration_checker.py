from source.configuration import conf
from source.configuration import logging
from urllib.parse import urlparse


def check_server_base_config(server_conf, label="server"):
    # Server URL
    parsed_url = urlparse(server_conf.url)
    assert parsed_url.scheme != '', f"[FATAL] Invalid {label} URL. It must include scheme (http/https). Got: {server_conf.url}"
    assert parsed_url.netloc != '', f"[FATAL] Invalid {label} URL. Must contain valid host (e.g. example.com). Got: {server_conf.url}"

    # API token
    assert isinstance(server_conf.api_token, str), f"[FATAL] Invalid {label} API token. It must be a string."
    assert server_conf.api_token != '', f"[FATAL] Invalid {label} API token. It cannot be empty."

    # watched folders
    assert isinstance(server_conf.watched_film_folders, list), f"[FATAL] {label} watched_film_folders must be a list."
    assert isinstance(server_conf.watched_tv_folders, list), f"[FATAL] {label} watched_tv_folders must be a list."

    # observed period
    assert isinstance(server_conf.observed_period_days, int), f"[FATAL] {label} observed_period_days must be an integer."


def check_tmdb_configuration():
    assert isinstance(conf.tmdb.api_key, str), "[FATAL] Invalid TMDB API key. Must be a string."
    assert conf.tmdb.api_key != '', "[FATAL] TMDB API key cannot be empty."


def email_template_configuration():
    assert isinstance(conf.email_template.language, str), "[FATAL] Invalid email language. Must be a string."
    assert conf.email_template.language in ['en', 'fr'], "[FATAL] Email language must be 'en' or 'fr'."

    assert isinstance(conf.email_template.subject, str), "[FATAL] Email subject must be a string."
    assert isinstance(conf.email_template.title, str), "[FATAL] Email title must be a string."
    assert isinstance(conf.email_template.subtitle, str), "[FATAL] Email subtitle must be a string."
    assert isinstance(conf.email_template.jellyfin_url, str), "[FATAL] jellyfin_url must be a string."
    assert isinstance(conf.email_template.unsubscribe_email, str), "[FATAL] unsubscribe_email must be a string."
    assert isinstance(conf.email_template.jellyfin_owner_name, str), "[FATAL] jellyfin_owner_name must be a string."


def check_email_configuration():
    assert isinstance(conf.email.smtp_server, str), "[FATAL] SMTP server must be a string."
    assert conf.email.smtp_server != '', "[FATAL] SMTP server cannot be empty."

    assert isinstance(conf.email.smtp_port, int), "[FATAL] SMTP port must be an integer."
    assert conf.email.smtp_port > 0, "[FATAL] SMTP port must be greater than 0."

    assert isinstance(conf.email.smtp_user, str), "[FATAL] SMTP username must be a string."
    assert conf.email.smtp_user != '', "[FATAL] SMTP username cannot be empty."

    assert isinstance(conf.email.smtp_password, str), "[FATAL] SMTP password must be a string."
    assert conf.email.smtp_password != '', "[FATAL] SMTP password cannot be empty."


def check_recipients_configuration():
    assert isinstance(conf.recipients, list), "[FATAL] Recipients must be a list."


def check_scheduler_configuration():
    if conf.scheduler.enabled:
        assert isinstance(conf.scheduler.cron, str), "[FATAL] Scheduler cron must be a string."


def check_configuration():
    """
    Top-level configuration check for both server types.
    """
    if conf.server_type == "jellyfin":
        check_server_base_config(conf.jellyfin, label="Jellyfin")
    elif conf.server_type == "emby":
        check_server_base_config(conf.emby, label="Emby")
    else:
        raise Exception(f"[FATAL] Invalid server_type '{conf.server_type}' in config. Must be 'jellyfin' or 'emby'.")

    check_tmdb_configuration()
    email_template_configuration()
    check_email_configuration()
    check_recipients_configuration()
    check_scheduler_configuration()