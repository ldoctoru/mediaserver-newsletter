import sys 
from source import configuration, JellyfinAPI, TmdbAPI




if __name__ == "__main__":
    print("Welcome to jellyfin automatic newsletter !\n")
    print("Developped by Seaweedbrain, under MIT License.")
    print("##############################################\n\n")

    print(TmdbAPI.get_media_detail_from_title(title="L'Amour ouf", type="movie", year=2024))

    


    


