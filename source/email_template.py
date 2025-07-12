from source import configuration, context, utils
import re

translation = {
    "en": {
        "discover_now": "Discover now",
        "new_film": "New movies:",
        "new_tvs": "New shows:",
        "currently_available": "Currently available in {server_name}:",
        "movies_label": "Movies",
        "episodes_label": "Episodes",
        "footer_label": "You are receiving this email because you are using {jellyfin_owner_name}'s {server_name} server. If you want to stop receiving these emails, you can unsubscribe by notifying {unsubscribe_email}.",
        "added_on": "Added on",
        "episodes": "Episodes",
        "episode": "Episode",
    },
    "fr": {
        "discover_now": "Découvrir maintenant",
        "new_film": "Nouveaux films :",
        "new_tvs": "Nouvelles séries :",
        "currently_available": "Actuellement disponible sur {server_name} :",
        "movies_label": "Films",
        "episodes_label": "Épisodes",
        "footer_label": "Vous recevez cet email car vous utilisez le serveur {server_name} de {jellyfin_owner_name}. Si vous ne souhaitez plus recevoir ces emails, vous pouvez vous désinscrire en notifiant {unsubscribe_email}.",
        "added_on": "Ajouté le",
        "episodes": "Épisodes",
        "episode": "Épisode",
    }
}

def populate_email_template(movies, series, total_tv, total_movie) -> str:
    include_overview = True
    if len(movies) + len(series) > 10:
        include_overview = False
        configuration.logging.info("There are more than 10 new items; overview will not be included.")

    with open("./template/new_media_notification.html") as template_file:
        template = template_file.read()
        
        lang = configuration.conf.email_template.language
        server_name = configuration.conf.server_type.capitalize()

        if lang not in translation:
            raise Exception(f"[FATAL] Language {lang} not supported. Supported: {list(translation.keys())}")

        # Replace static translation keys
        for key, val in translation[lang].items():
            val_with_server = val.replace("{server_name}", server_name)
            template = re.sub(rf"\${{{key}}}", val_with_server, template)

        # Replace custom config-based placeholders
        custom_keys = [
            {"key": "title", "value": configuration.conf.email_template.title.format_map(context.placeholders)}, 
            {"key": "subtitle", "value": configuration.conf.email_template.subtitle.format_map(context.placeholders)},
            {"key": "jellyfin_url", "value": configuration.conf.email_template.jellyfin_url},
            {"key": "jellyfin_owner_name", "value": configuration.conf.email_template.jellyfin_owner_name.format_map(context.placeholders)},
            {"key": "unsubscribe_email", "value": configuration.conf.email_template.unsubscribe_email.format_map(context.placeholders)}
        ]
        for key in custom_keys:
            template = re.sub(rf"\${{{key['key']}}}", key["value"], template)

        # Movies section
        if movies:
            template = re.sub(r"\${display_movies}", "", template)
            movies_html = ""
            for movie_title, movie_data in movies.items():
                added_date = movie_data["created_on"].split("T")[0]
                item_overview_html = f"""
<div class="movie-description" style="color: #dddddd !important; font-size: 14px !important; line-height: 1.4 !important;">
    {movie_data['description']}
</div>""" if include_overview else ""
                movies_html += f"""
<div class="movie_container" style="margin-bottom: 15px;">
    <div class="movie_bg" style="background: url('{movie_data['poster']}') no-repeat center center; background-size: cover; border-radius: 10px;">
        <table class="movie" width="100%" cellpadding="0" cellspacing="0" style="background: rgba(0, 0, 0, 0.7); border-radius: 10px;">
            <tr>
                <td class="movie-image" style="padding: 15px; text-align: center; width: 120px;">
                    <img src="{movie_data['poster']}" alt="{movie_title}" style="max-width: 100px; height: auto;">
                </td>
                <td class="movie-content-cell" style="padding: 15px;">
                    <h3 class="movie-title" style="color: #ffffff; margin: 0 0 5px; font-size: 18px;">{movie_title}</h3>
                    <div class="movie-date" style="color: #dddddd; font-size: 14px; margin: 0 0 10px;">
                        {translation[lang]['added_on']} {added_date}
                    </div>
                    {item_overview_html}
                </td>
            </tr>
        </table>
    </div>
</div>
"""
            template = re.sub(r"\${films}", movies_html, template)
        else:
            template = re.sub(r"\${display_movies}", "display:none", template)

        # Series section
        if series:
            template = re.sub(r"\${display_tv}", "", template)
            series_html = ""
            for serie_title, serie_data in series.items():
                added_date = serie_data["created_on"].split("T")[0]
                if len(serie_data["seasons"]) == 1:
                    if len(serie_data["episodes"]) == 1:
                        added_items_str = f"{serie_data['seasons'][0]}, {translation[lang]['episode']} {serie_data['episodes'][0]}"
                    else:
                        ranges = utils.summarize_ranges(serie_data["episodes"])
                        added_items_str = f"{serie_data['seasons'][0]}, {translation[lang]['episodes']} {', '.join(ranges)}"
                else:
                    serie_data["seasons"].sort()
                    added_items_str = ", ".join(serie_data["seasons"])
                item_overview_html = f"""
<div class="movie-description" style="color: #dddddd; font-size: 14px; line-height: 1.4;">
    {serie_data['description']}
</div>""" if include_overview else ""
                series_html += f"""
<div class="movie_container" style="margin-bottom: 15px;">
    <div class="movie_bg" style="background: url('{serie_data['poster']}') no-repeat center center; background-size: cover; border-radius: 10px;">
        <table class="movie" width="100%" cellpadding="0" cellspacing="0" style="background: rgba(0, 0, 0, 0.7); border-radius: 10px;">
            <tr>
                <td class="movie-image" style="padding: 15px; text-align: center; width: 120px;">
                    <img src="{serie_data['poster']}" alt="{serie_title}" style="max-width: 100px; height: auto;">
                </td>
                <td class="movie-content-cell" style="padding: 15px;">
                    <h3 class="movie-title" style="color: #ffffff; margin: 0 0 5px; font-size: 18px;">{serie_title}: {added_items_str}</h3>
                    <div class="movie-date" style="color: #dddddd; font-size: 14px; margin: 0 0 10px;">
                        {translation[lang]['added_on']} {added_date}
                    </div>
                    {item_overview_html}
                </td>
            </tr>
        </table>
    </div>
</div>
"""
            template = re.sub(r"\${tvs}", series_html, template)
        else:
            template = re.sub(r"\${display_tv}", "display:none", template)

        # Stats
        template = template.replace("${series_count}", str(total_tv))
        template = template.replace("${movies_count}", str(total_movie))

        return template