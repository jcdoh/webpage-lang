from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import re
import copy

app = Flask(__name__)

languages = [
    {"id": "1",
     "language": "English",
     "video": "https://www.youtube.com/embed/bufxxxSBCHM",
     "review": "English is the untameable language. ‘It’s a hassle to kow-tow to soi-disant cognoscenti who think "
               "they’re the cat’s pyjamas, robotically issuing phoney diktats of grammatical rectitude. Ignore them! "
               "No one owns English.’ That plea for English liberation incorporates echoes of Latin, Greek, German, "
               "Irish, Czech, Persian, Italian, French, Chinese and Guarani.",
     "difficulty": "0",
     "speakers": "1300000000",
     "family": "Germanic",
     "countries": ["United Kingdom", "Ireland", "Malta"]},
    {"id": "2",
     "language": "German",
     "video": "https://www.youtube.com/embed/cDEwenlY9Xo",
     "review": "German is easy as pie. It’s one of the myths of our time that German is a difficult language. But all "
               "you have to do is link one noun to another noun to another noun, sprinkling a pinch of genitive over "
               "the whole thing, and abracadabra — Rindfleischetikettierungsüberwachungs-aufgabenübertragungsgesetz. "
               "Or Grundstücksverkehrsgenehmigungs-zuständigkeitsübertragungsverordnung. 63 characters, 67 characters, "
               "even 104 characters if you wish, neatly wrapped up in a single, simple word.",
     "difficulty": "2",
     "speakers": "135000000",
     "family": "Germanic",
     "countries": ["Germany", "Austria", "Belgium", "Luxembourg", "Switzerland", "Liechtenstein"]},
    {"id": "3",
     "language": "French",
     "video": "https://www.youtube.com/embed/F4sz5SbIkKU",
     "review": "French comes from Latin, but where is it going? While the French Academy has been the language council par excellence since 1635, the French people still can’t agree whether the pastry referred to as couque au chocolat in Belgium should be called pain au chocolat or chocolatine in France. And this is only one of many regional linguistic issues facing the over 270 million native French-speakers in France, Belgium, Luxembourg, Switzerland, Quebec, the Antilles, Oceania, the Indian Ocean, Lebanon and Africa.",
     "difficulty": "1",
     "speakers": "267000000",
     "family": "Romance",
     "countries": ["Belgium", "France", "Monaco", "Luxembourg", "Switzerland"]},
    {"id": "4",
     "language": "Finnish",
     "video": "https://www.youtube.com/embed/nmAud7EN3RA",
     "review": "Finnish is the odd one out. Traditionally, Finnish has contributed little to other European "
               "languages. Nevertheless, it has managed to export words such as sisu (a state of mind combining "
               "determination and tenacity), sauna, salmiakki (salty liquorice), rapakivi (a type of granite rock), "
               "aapa (a type of mire) and pulkka (pulk, a small toboggan).",
     "difficulty": "5",
     "speakers": "5000000",
     "family": "Uralic",
     "countries": ["Finland"]},
    {"id": "5",
     "language": "Greek",
     "video": "https://www.youtube.com/embed/0QF-CMhrPrU",
     "review": "Greek is a journey through the ages. Words such as logic, idea, theory, politics and democracy were "
               "crafted in Greek. It may also be argued that their meaning, too, was created through it. These words, "
               "and many more like them, were passed on like a torch from one generation to the next, helping human "
               "thinking to evolve. Greek is still used, along with Latin, to coin new scientific or technological "
               "terms whenever the need arises.",
     "difficulty": "4",
     "speakers": "13500000",
     "family": "Hellenic",
     "countries": ["Greece", "Cyprus"]},
    {"id": "6",
     "language": "Italian",
     "video": "https://www.youtube.com/embed/GtFbmk9ECNI",
     "review": "Italian is music to your ears. The Italian language has exported countless words to other European "
               "languages, mainly in the areas of gastronomy, music, fashion and architecture. The musical "
               "masterpieces of Monteverdi, Puccini, Rossini and Verdi have made a particularly significant "
               "contribution. Played all over the world for centuries, they continue to be sung in Italian.",
     "difficulty": "1",
     "speakers": "68000000",
     "family": "Romance",
     "countries": ["Italy", "San Marino", "Switzerland", "Vatican City"]},
    {"id": "7",
     "language": "Swedish",
     "video": "https://www.youtube.com/embed/ZpimWZluRh0",
     "review": "Swedish has a Viking heritage. In the 8th century, Old Norse was spoken in Scandinavia. Swedish developed from it, alongside Danish, "
               "as an East Scandinavian language. An early example can be found on the runes in Hagia Sofia in "
               "Istanbul, which date back to the 11th century. Although they were already quite worn down by the time "
               "of their discovery in 1964, they are decipherable as something like Halfdan was here.",
     "difficulty": "1",
     "speakers": "10000000",
     "family": "Germanic",
     "countries": ["Sweden", "Finland"]},
    {"id": "8",
     "language": "Spanish",
     "video": "https://www.youtube.com/embed/JaLUiwckjKI",
     "review": "Spanish is a standard born out of translation. Spanish astronomers could study the stars and use "
               "their own language to communicate their findings, while Copernicus and Newton still had to turn to "
               "Latin. Ever wondered why? In the 13th century, when most of Europe used Latin for higher learning, "
               "Alfonso X decided that the worlds of law, philosophy and science needed an abstract Castilian "
               "vocabulary. Arabic, Hebrew and Latin sources were all translated into written Castilian.",
     "difficulty": "1",
     "speakers": "143000000",
     "family": "Romance",
     "countries": ["Spain"]},
    {"id": "9",
     "language": "Bulgarian",
     "video": "https://www.youtube.com/embed/udWx-HcMjUQ",
     "review": "Bulgarian is not like other Slavic tongues. The Bulgarian language has undergone many changes at "
               "various stages in its history. It lost the Slavonic case system but — unlike the other Slavic "
               "languages — preserved its rich verb system. It also developed a definite article. Today it is the "
               "mother tongue of approximately 9 million people.",
     "difficulty": "4",
     "speakers": "9000000",
     "family": "Slavic",
     "countries": ["Bulgaria"]},
    {"id": "10",
     "language": "Croatian",
     "video": "https://www.youtube.com/embed/iXsv-UrMW-U",
     "review": "Croatian is the real delight for modern linguists. Modern Croatian has three major dialects: "
               "Čakavian, Kajkavian and Štokavian, named after the different ways of saying what in these dialects — "
               "ča, kaj and što respectively. The triune nature of Croatian is unique among the Slavic languages. In "
               "addition, Štokavian is the official dialect, yet it also has three variants (Ekavian, Ikavian and "
               "Ijekavian), with differing geographical distributions. Ijekavian forms the basis for Croatian.",
     "difficulty": "4",
     "speakers": "5600000",
     "family": "Slavic",
     "countries": ["Croatia", "Bosnia and Herzegovina", "Serbia", "Austria"]},
    {"id": "11",
     "language": "Czech",
     "video": "https://www.youtube.com/embed/nuZNFs5XCkE",
     "review": "Czech is a real tough one. Czech-speakers can create new words on the spot — and they will not even "
               "be considered particularly creative for doing so. Here’s why? Czech morphology has an abundance of "
               "affixes, which are more systematised than in other Slavic languages.",
     "difficulty": "4",
     "speakers": "10700000",
     "family": "Slavic",
     "countries": ["Czechia"]},
    {"id": "12",
     "language": "Danish",
     "video": "https://www.youtube.com/embed/EJuLq1FsxCI",
     "review": "Danish has left its mark on English, which contains hundreds of loan words from Old Norse brought by "
               "the Vikings. Of the 5,000 basic words in English, it’s estimated that as many as 20 per cent are loan "
               "words from Old Norse. English wouldn’t have such dramatic words as berserk, skull and hell had it not "
               "been for the Danes!",
     "difficulty": "1",
     "speakers": "6000000",
     "family": "Germanic",
     "countries": ["Denmark"]},
    {"id": "13",
     "language": "Dutch",
     "video": "https://www.youtube.com/embed/144m_3zvlOY",
     "review": "Dutch stands on its own two feet. Simon Stevin, born in Bruges in 1548, was a mathematician, "
               "scientist and engineer who thought Dutch was the most suitable language for science. He felt it lent "
               "itself easily to the development of new, self-explanatory scientific terms. Thanks to him, "
               "the Dutch language has its own words for terms that in most languages are borrowed from Greek, "
               "such as wiskunde (mathematics) and evenwijdig (parallel).",
     "difficulty": "1",
     "speakers": "25000000",
     "family": "Germanic",
     "countries": ["Netherlands", "Belgium"]},
    {"id": "14",
     "language": "Hungarian",
     "video": "https://www.youtube.com/embed/KbO_I9NyV4c",
     "review": "Hungarian is a peculiar one. Hungarian is not the only language to be influenced by other languages. "
               "But it has a few defence mechanisms. One is the bane of every Hungarian-learner’s life: vowel "
               "harmony. This is the reason in the house has the suffix -ban (a házban) but in the garden has the "
               "suffix -ben (a kertben). Partly because of this, Hungarian prefers to assimilate loan-words (which "
               "sound like the original foreign-language word) or to use a literal translation rather than a totally "
               "unaltered foreign word.",
     "difficulty": "5",
     "speakers": "13000000",
     "family": "Uralic",
     "countries": ["Hungary", "Serbia"]},
    {"id": "15",
     "language": "Irish",
     "video": "https://www.youtube.com/embed/e6JbUDBfY1E",
     "review": "Irish listens to the past and looks forward. When a language dies an untold wealth of cultural "
               "heritage disappears — stories, social relationships, ways of life. Irish has managed to stem the tide "
               "and appears to be turning a corner. Since the late 19th century a huge effort has been going on to "
               "preserve, revive and breathe new vigour and life into the language. Today it is an EU language, "
               "it is also being studied also outside Ireland, and there is a vibrant Irish‑language media sector.",
     "difficulty": "4",
     "speakers": "170000",
     "family": "Celtic",
     "countries": ["Ireland"]},
    {"id": "16",
     "language": "Latvian",
     "video": "https://www.youtube.com/embed/64MPDdJjT7c",
     "review": "Are you flexible enough for Latvian? If you have ever visited Latvia or had any contact with its "
               "culture, you may wonder why your name was transformed into Latvian text. You would be in good "
               "company, as Jean-Claude Juncker is referred to as Žans Klods Junkers! Words from other languages need "
               "to be modified so that they can be included in the Latvian grammar system.",
     "difficulty": "4",
     "speakers": "1800000",
     "family": "Baltic",
     "countries": ["Latvia"]},
    {"id": "17",
     "language": "Lithuanian",
     "video": "https://www.youtube.com/embed/YUfemdKSX84",
     "review": "Lithuanian is both young and old. Before Lithuania’s independence in 1918, Dr Jonas Basanavičius "
               "clandestinely and illegally published Aušra (“Dawn”), the first Lithuanian-language newspaper to use "
               "the Roman alphabet. Although short-lived, Aušra helped galvanise a national movement, "
               "igniting aspirations of independence. Dr Basanavičius is seen by Lithuanians as the man who gave them "
               "the freedom to read and write in Lithuanian — a language considered to be one of the oldest in the "
               "Indo-European language family.",
     "difficulty": "4",
     "speakers": "3000000",
     "family": "Baltic",
     "countries": ["Lithuania"]},
    {"id": "18",
     "language": "Maltese",
     "video": "https://www.youtube.com/embed/xmMI7uJCbp8",
     "review": "Maltese has survived and been revived. Maltese is the story of a language that has made it through the ages. More than a thousand years of influences — from a constant flow of conquerors, travellers and seafarers who settled on Malta — have created this unique hybrid of Semitic and Romance. The chequered travails of the Maltese language are a true example of European multilingualism, illustrating the dignity of different nations’ tongues and how cultures and their languages can meld harmoniously.",
     "difficulty": "1",
     "speakers": "520000",
     "family": "Semitic",
     "countries": ["Malta"]},
    {"id": "19",
     "language": "Polish",
     "video": "https://www.youtube.com/embed/VnuRmmGLnu4",
     "review": "Polish is certainly the affectionate language. The oldest written phrase in Polish dates from 1270 "
               "and expresses affection: Day, ut ia pobrusa, a ti poziwai (“Let me do the grinding, and you take a "
               "rest”). Perhaps, then, it’s not surprising that Polish has numerous terms of endearment or nicknames "
               "in the form of the diminutive. The name Agnieszka, for example, has variations such as Aga, Agusia, "
               "Agunia, Agniesia, Agnisia and Aguś.",
     "difficulty": "4",
     "speakers": "50000000",
     "family": "Slavic",
     "countries": ["Poland"]},
    {"id": "20",
     "language": "Portuguese",
     "video": "https://www.youtube.com/embed/stqMz9XjuNo",
     "review": "Portuguese loves its Arabic heritage. The Arabs came from North Africa to the Iberian Peninsula in "
               "711, and their language had a great influence on Portuguese vocabulary. Many words of Arabic origin "
               "begin with the Arabic article al. For example, the name of the Algarve region quite simply means the "
               "west in Arabic. An interesting example of Arabic influence is the expression oxalá, which in both "
               "form and meaning comes from law xâ Allâh (God willing).",
     "difficulty": "1",
     "speakers": "250000000",
     "family": "Romance",
     "countries": ["Portugal"]},
    {"id": "21",
     "language": "Romanian",
     "video": "https://www.youtube.com/embed/TcRWiz1PhKU",
     "review": "Romanian has a bit of everything. Like all Romance languages, Romanian is based on Latin. But it also "
               "has influences from many other languages, including Russian, German, Greek, Hungarian, Turkish, "
               "Bulgarian, Ukrainian, Serbo-Croat, French, Italian and, more recently, English. Romanian uses almost "
               "all the Latin cases, except the ablative. It has three genders — for a noun to be neuter, "
               "its singular form must be masculine and its plural form feminine. The definite article is attached to "
               "the end of a word.",
     "difficulty": "1",
     "speakers": "25000000",
     "family": "Romance",
     "countries": ["Romania", "Moldova", "Serbia"]},
    {"id": "22",
     "language": "Slovak",
     "video": "https://www.youtube.com/embed/ZVCDqZMU0Qg",
     "review": "Slovak is the language of the people. While standard Slovak is relatively young, Slovaks are rightly "
               "proud of their rich heritage of folklore. This is manifested in tales, dances, songs, lullabies and "
               "vinše — the personalised verse wishes that Slovaks still make the effort to craft to celebrate "
               "birthdays and other events.",
     "difficulty": "4",
     "speakers": "5200000",
     "family": "Slavic",
     "countries": ["Slovakia", "Serbia"]},
    {"id": "23",
     "language": "Slovenian",
     "video": "https://www.youtube.com/embed/ZdMA4yG5qOE",
     "review": "With Slovenian, you get two for the price of one. Slovenian, or Slovene, has around 2.2 million "
               "native speakers and no less than 37 dialects, which differ quite significantly from one another. In "
               "addition to the singular and plural, the language has preserved the grammatical number dual referring "
               "to precisely two objects or people. And it does come in handy in a romantic situation to have a "
               "specific word — midva — meaning the two of us.",
     "difficulty": "4",
     "speakers": "2500000",
     "family": "Slavic",
     "countries": ["Slovenia"]},
    {"id": "24",
     "language": "Estonian",
     "video": "https://www.youtube.com/embed/TFRbAhzrXps",
     "review": "Estonian has the culture heritage of a 100-year-old nation. The Estonian language goes back centuries "
               "in spoken form, but was successfully modernised after Estonia declared its independence in 1918. “Let "
               "us remain Estonians, but let us also become Europeans!” said the writer Gustav Suits, who was active "
               "in the first decades of the 20th century. Today, the percentage of Estonians translating for the EU "
               "is quite high — around 200, or 0.02% of the overall language community.",
     "difficulty": "5",
     "speakers": "1100000",
     "family": "Uralic",
     "countries": ["Estonia"]},
    {"id": "25",
     "language": "Ukrainian",
     "video": "https://www.youtube.com/embed/3wk6az6b9gg",
     "review": "Ukrainian is the beautiful language. Based on the results of the languages competition that took place in Paris "
               "in 1934, Ukrainian is the third most beautiful by its phonetics, vocabulary, phraseology, "
               "and sentence structure after French and Persian. Also, it's officially the second most melodic "
               "language in the world after Italian. So it comes as no surprise that many admit the Ukrainian "
               "language reminds them a nightingale’s song. To make sure it's true, you might want to listen to "
               "world-famous Summertime by George Gershwin and Carol of the Bells in their original language, "
               "which is... Ukrainian!",
     "difficulty": "4",
     "speakers": "45000000",
     "family": "Slavic",
     "countries": ["Ukraine"]},
]


# ROUTES

@app.route('/')
def hello():
    global languages

    new_lang = copy.deepcopy(languages)

    lang_sorted = (sorted(new_lang, key=lambda i: int(i["speakers"])))
    bottom = lang_sorted[:3]
    top = lang_sorted[-3:]
    top.reverse()

    for i in bottom:
        i["review"] = re.split('[.!?]', i["review"])[0]
    for j in top:
        j["review"] = re.split('[.!?]', j["review"])[0]

    return render_template('welcome.html', most=top, least=bottom)


@app.route('/search_results/<search>')
def search_results(search):
    global languages

    empty = False
    lang_results = []
    fam_results = []
    country_results = {}
    for item in languages:
        if search.lower() in item["language"].lower():
            lang_results.append(item)
        if search.lower() in item["family"].lower():
            fam_results.append(item)
        for i in item["countries"]:
            if search.lower() in i.lower():
                if item["id"] in country_results:
                    country_results[item["id"]].append(i)
                else:
                    country_results[item["id"]] = [item["language"], i]
    if len(lang_results) == 0 and len(fam_results) == 0 and len(country_results) == 0:
        empty = True

    return render_template('search_results.html', lang_results=lang_results, fam_results=fam_results,
                           country_results=country_results, search=search, empty=empty)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/view/<id>')
def view(id):
    global languages

    info = 0
    for item in languages:
        if id == item["id"]:
            info = item
    num = len(info["countries"])
    if (num % 2) == 0:
        halfway = int(num / 2)
    else:
        halfway = int((num + 1) / 2)
    return render_template('view.html', info=info, halfway=halfway)


@app.route('/edit/<id>')
def edit(id):
    global languages

    info = 0
    for item in languages:
        if id == item["id"]:
            info = item

    countries = ""
    for i in range(len(info["countries"])):
        countries += info["countries"][i]
        if i < len(info["countries"]) - 1:
            countries += ", "

    return render_template('edit.html', info=info, countries=countries)


# AJAX FUNCTIONS

@app.route('/save_new_entry', methods=['POST', 'GET'])
def save_new_entry():
    global languages

    json_data = request.get_json()
    new_entry = json_data
    new_id = int(languages[-1]["id"]) + 1
    new_entry["id"] = str(new_id)

    languages.append(new_entry)

    return jsonify(new_id)


@app.route('/edit_entry', methods=['POST', 'GET'])
def edit_entry():
    global languages

    json_data = request.get_json()
    new_data = json_data

    iden = ""
    for item in languages:
        if item["id"] == new_data["id"]:
            iden = item["id"]
            for key in item.keys():
                item[key] = new_data[key]

    return jsonify(iden)


if __name__ == '__main__':
    app.run(debug=True)
