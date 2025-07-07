from source import configuration
import re
from source import context
import os

# Define two translation blocks, one for each server type if you want!
translation = {
    "jellyfin": {
        "en": {
            "discover_now": "Discover now",
            "new_film": "New movies:",
            "new_tvs": "New shows:",
            "currently_available": "Currently available in Jellyfin:",
            "movies_label": "Movies",
            "episodes_label": "Episodes",
            "footer_label": "You are receiving this email because you are using ${owner_name}'s Jellyfin server. If you want to stop receiving these emails, you can unsubscribe by notifying ${unsubscribe_email}.",
            "added_on": "Added on"
        },
        "fr": {
            "discover_now": "Découvrir maintenant",
            "new_film": "Nouveaux films :",
            "new_tvs": "Nouvelles séries :",
            "currently_available": "Actuellement disponible sur Jellyfin :",
            "movies_label": "Films",
            "episodes_label": "Épisodes",
            "footer_label": "Vous recevez cet email car vous utilisez le serveur Jellyfin de ${owner_name}. Si vous ne souhaitez plus recevoir ces emails, vous pouvez vous désinscrire en notifiant ${unsubscribe_email}.",
            "added_on": "Ajouté le"
        }
    },
    "emby": {
        "en": {
            "discover_now": "Discover now",
            "new_film": "New movies:",
            "new_tvs": "New shows:",
            "currently_available": "Currently available in Emby:",
            "movies_label": "Movies",
            "episodes_label": "Episodes",
            "footer_label": "You are receiving this email because you are using ${owner_name}'s Emby server. If you want to stop receiving these emails, you can unsubscribe by notifying ${unsubscribe_email}.",
            "added_on": "Added on"
        },
        "fr": {
            "discover_now": "Découvrir maintenant",
            "new_film": "Nouveaux films :",
            "new_tvs": "Nouvelles séries :",
            "currently_available": "Actuellement disponible sur Emby :",
            "movies_label": "Films",
            "episodes_label": "Épisodes",
            "footer_label": "Vous recevez cet email car vous utilisez le serveur Emby de ${owner_name}. Si vous ne souhaitez plus recevoir ces emails, vous pouvez vous désinscrire en notifiant ${unsubscribe_email}.",
            "added_on": "Ajouté le"
        }
    }
}

def populate_email_template(movies, series, total_tv, total_movie) -> str:
    server_type = configuration.conf.server_type.lower()
    template_file = f"./template/new_media_notification_{server_type}.html"
    if not os.path.exists(template_file):
        raise Exception(f"Template for {server_type} not found: {template_file}")

    with open(template_file) as template_file_handle:
        template = template_file_handle.read()
        
        lang = configuration.conf.email_template.language
        if lang in ["fr", "en"]:
            for key in translation[server_type][lang]:
                template = re.sub(
                    r"\${" + key + "}", 
                    translation[server_type][lang][key], 
                    template
                )
        else:
            raise Exception(f"[FATAL] Language {lang} not supported. Supported languages are fr and en")

        # Pick the correct url and owner name based on server_type
        if server_type == "jellyfin":
            server_url = configuration.conf.email_template.jellyfin_url
            owner_name = configuration.conf.email_template.jellyfin_owner_name
        else:
            server_url = getattr(configuration.conf.email_template, "emby_url", configuration.conf.emby.url)
            owner_name = getattr(configuration.conf.email_template, "emby_owner_name", "Admin")

        custom_keys = [
            {"key": "title", "value": configuration.conf.email_template.title.format_map(context.placeholders)}, 
            {"key": "subtitle", "value": configuration.conf.email_template.subtitle.format_map(context.placeholders)},
            {"key": "server_url", "value": server_url},
            {"key": "owner_name", "value": owner_name.format_map(context.placeholders) if hasattr(owner_name, 'format_map') else owner_name},
            {"key": "unsubscribe_email", "value": configuration.conf.email_template.unsubscribe_email.format_map(context.placeholders)}
        ]
        
        for key in custom_keys:
            template = re.sub(r"\${" + key["key"] + "}", key["value"], template)

        # Movies section
        if movies:
            template = re.sub(r"\${display_movies}", "", template)
            movies_html = ""
            
            for movie_title, movie_data in movies.items():
                added_date = movie_data["created_on"].split("T")[0]
                movies_html += f"""
                <div class="movie_container" style="margin-bottom: 15px;">
                    <div class="movie_bg" style="background: url('{movie_data['poster']}') no-repeat center center; background-size: cover; border-radius: 10px;">
                        <table class="movie" width="100%" role="presentation" cellpadding="0" cellspacing="0" style="background: rgba(0, 0, 0, 0.7); border-radius: 10px; width: 100%;">
                            <tr>
                                <td class="movie-image" valign="top" style="padding: 15px; text-align: center; width: 120px;">
                                    <img src="{movie_data['poster']}" alt="{movie_title}" style="max-width: 100px; height: auto; display: block; margin: 0 auto;">
                                </td>
                                <td class="movie-content-cell" valign="top" style="padding: 15px;">
                                    <div class="mobile-text-container">
                                        <h3 class="movie-title" style="color: #ffffff !important; margin: 0 0 5px !important; font-size: 18px !important;">{movie_title}</h3>
                                        <div class="movie-date" style="color: #dddddd !important; font-size: 14px !important; margin: 0 0 10px !important;">
                                            {translation[server_type][lang]['added_on']} {added_date}
                                        </div>
                                        <div class="movie-description" style="color: #dddddd !important; font-size: 14px !important; line-height: 1.4 !important;">
                                            {movie_data['description']}
                                        </div>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
                """
                
            template = re.sub(r"\${films}", movies_html, template)
        else:
            template = re.sub(r"\${display_movies}", "display:none", template)

        # TV Shows section
        if series:
            template = re.sub(r"\${display_tv}", "", template)
            series_html = ""
            
            for serie_title, serie_data in series.items():
                added_date = serie_data["created_on"].split("T")[0]
                seasons_str = ", ".join(serie_data["seasons"])
                series_html += f"""
                <div class="movie_container" style="margin-bottom: 15px;">
                    <div class="movie_bg" style="background: url('{serie_data['poster']}') no-repeat center center; background-size: cover; border-radius: 10px;">
                        <table class="movie" width="100%" role="presentation" cellpadding="0" cellspacing="0" style="background: rgba(0, 0, 0, 0.7); border-radius: 10px; width: 100%;">
                            <tr>
                                <td class="movie-image" valign="top" style="padding: 15px; text-align: center; width: 120px;">
                                    <img src="{serie_data['poster']}" alt="{serie_title}" style="max-width: 100px; height: auto; display: block; margin: 0 auto;">
                                </td>
                                <td class="movie-content-cell" valign="top" style="padding: 15px;">
                                    <div class="mobile-text-container">
                                        <h3 class="movie-title" style="color: #ffffff !important; margin: 0 0 5px !important; font-size: 18px !important;">{serie_title} {seasons_str}</h3>
                                        <div class="movie-date" style="color: #dddddd !important; font-size: 14px !important; margin: 0 0 10px !important;">
                                            {translation[server_type][lang]['added_on']} {added_date}
                                        </div>
                                        <div class="movie-description" style="color: #dddddd !important; font-size: 14px !important; line-height: 1.4 !important;">
                                            {serie_data['description']}
                                        </div>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
                """
                
            template = re.sub(r"\${tvs}", series_html, template)
        else:
            template = re.sub(r"\${display_tv}", "display:none", template)

        # Statistics section
        template = re.sub(r"\${series_count}", str(total_tv), template)
        template = re.sub(r"\${movies_count}", str(total_movie), template)
        
        return template