# CREATED BY LIAM O'KANE
#
# THIS APP TELLS YOU YOUR FAVOURITE GENRES
# IN 5 LEVELS OF SPECIFICITY
#
# RUN THE FOLLOWING COMMAND TO INITIALISE
#
# pip install spotipy
#
# 21/08/2020

import spotipy, json
from collections import Counter

def authenticate(): 
    token = spotipy.util.prompt_for_user_token(
        username="",
        scope='user-top-read',
        client_id='9a69b46d15f24488b9d852fe9de5c301',
        client_secret='1d6dfaea6a0741a3bd9e0b321105d4c2',
        redirect_uri='http://localhost:8888/callback'
    )

    return spotipy.Spotify(auth=token)


def generateTiers():
    sp = authenticate()
    results = sp.current_user_top_artists(limit=50, time_range='short_term')

    top_genres = []
    for idx, item in enumerate(results['items']):
        top_genres += item['genres']

    with open("static/genreData.json", 'r') as infile:
        genreData = json.load(infile)

    parent = genreData[0]
    specifier = genreData[1]

    top_both = []

    # SORT FAVS INTO TOP GENRES
    for name in top_genres:
        for genre in parent.keys():
            for adj in specifier.keys():
                if genre in name and adj in name:
                    top_both.append(name)
                    break
                else:
                    if genre in name:   
                        parent[genre].append(name)
                    if adj in name:
                        specifier[adj].append(name)


    # REMOVE IRRELEVANT GENRES
    relevant_genres = []
    for genre in parent.keys():
        relevant_genres += [genre] * len(parent[genre])

    # SORT GENRES BASED ON RELEVANCE
    counts = Counter(relevant_genres)
    ordered_genres = sorted(counts, key=counts.get, reverse=True)
    tier_1 = [genre.replace(" ", "-") for genre in ordered_genres]

    # SORT TOP_BOTH BASED ON RELEVANCE
    counts = Counter(top_both)
    top_both = sorted(counts, key=counts.get, reverse=True)

    # INIT TIER 2 AND 3
    tier_2 = []
    tier_3 = []

    # SORT GENRES INTO TIER 2 AND 3
    for name in top_both:

        # REMOVE ONES THAT ARE SUBSETS OF ANOTHER
        arr = []
        for second in top_both:
            if name in second:
                arr.append(second)
        if len(arr) > 1:
            arr.sort(key=len)
            for item in range(1,len(arr)):
                tier_3.append(arr[item])
                top_both.remove(arr[item])

    for name in range(len(top_both)):
        # REMOVE ONES WITH TOO MANY KEYWORDS
        count = 0
        length = 0
        for adj in specifier.keys():
            if adj in top_both[name]:
                length += len(adj)
                count += 1
        for genre in parent.keys():
            if genre in top_both[name]:
                length += len(genre)
                count += 1
        if (count > 2) or (length+3 < len(top_both[name])):
            tier_3.append(top_both[name])
        else:
            tier_2.append(top_both[name])


    # SORT ALL OF THE TOP GENRES
    # BASED ON RELEVANCE
    counts = Counter(top_genres)
    top_genres = sorted(counts, key=counts.get, reverse=True)

    # CREATE A PRELIMINARY GROUP CONTAINING GENRES WITH
    # ONLY 1 OF EITHER THE PARENT GENRE OR ADJECTIVE
    prelim_4 = []
    for name in top_genres:
        for adj in specifier.keys():
            for genre in parent.keys():
                if (adj in name) ^ (genre in name):
                    if genre == adj:
                        tier_2.append(name)
                    else:
                        prelim_4.append(name)

    # MAKE SURE THE GENRE HASNT BEEN USED YET
    tier_4 = []
    for genre in prelim_4:
        if genre not in ordered_genres:
            if genre not in tier_2:
                if genre not in tier_3:
                    if len(genre.split()) < 3:
                        if genre not in tier_4: 
                            tier_4.append(genre)


    # PUT ALL REMAINING UNUSED GENRES INTO TIER 5
    tier_5 = []
    for five in top_genres:
        if five not in ordered_genres:
            if five not in tier_2:
                if five not in tier_3:
                    if five not in tier_4:
                        tier_5.append(five)

    # Return all
    return [top_genres[:5], tier_1, tier_2, tier_3, tier_4, tier_5]

a = generateTiers()
for tier in a:
    print(tier)