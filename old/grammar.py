
modes = {
    "Nominative" : {
        "Usage" : "The nominative case (der Nominativ) is used to express the subject of a sentence who performs the action of the verb.",
        "Personal pronouns": {
            "1st": "ich",
            "2nd": "du",
            "3rd Masculine":"er",
            "3rd Feminine":"sie",
            "3rd Neutral":"es",
            "1st Plural":"wir",
            "2nd Plural": "ihr",
            "3rd Plural:":"sie",
            "2nd Formal": "Sie"
        },
        "Articles": {
            "Definite": {
                "Masculine":"der",
                "Feminine": "die",
                "Neutral": "das",
                "Plural": "die"
            },
            "Indefinite": {
                "Masculine":"ein",
                "Feminine": "eine",
                "Neutral": "ein"
            }
        }
    },
     "Accusative" : {
        "Usage" : "The accusative case (der Akkusativ) is used to express the direct object of the sentence. It’s the “receiver” of the subject’s actions and is influenced by them.",
        "Personal pronouns": {
            "1st": "mich",
            "2nd": "dich",
            "3rd Masculine":"ihn",
            "3rd Feminine":"sie",
            "3rd Neutral":"es",
            "1st Plural":"uns",
            "2nd Plural": "euch",
            "3rd Plural:":"sie",
            "2nd Formal": "Sie"
        },
        "Articles": {
            "Definite": {
                "Masculine":"den",
                "Feminine": "die",
                "Neutral": "das",
                "Plural": "die"
            },
            "Indefinite": {
                "Masculine":"einen",
                "Feminine": "eine",
                "Neutral": "ein"
            }
        }
    },
     "Dative" : {
        "Usage" : "The dative case (der Dativ) is used to express the indirect object of the sentence. This would be the noun that receives or is acted upon by the direct object.",
        "Personal pronouns": {
            "1st": "mir",
            "2nd": "dir",
            "3rd Masculine":"ihm",
            "3rd Feminine":"ihr",
            "3rd Neutral":"ihm",
            "1st Plural":"uns",
            "2nd Plural": "euch",
            "3rd Plural:":"ihnen",
            "2nd Formal": "Ihnen"
        },
        "Articles": {
            "Definite": {
                "Masculine":"dem",
                "Feminine": "der",
                "Neutral": "dem",
                "Plural": "den"
            },
            "Indefinite": {
                "Masculine":"einem",
                "Feminine": "einer",
                "Neutral": "einem"
            }
        }
    },
    "Genitive" : {
        "Usage" : """The genitive case (der Genitiv) is used to express possession or association. In English, we indicate possession by saying something is 'of' someone or by adding -‘s to nouns. In German, the approach is a bit similar.
Typically, you’ll have to change the “possessor” noun’s article. Then, for masculine and neuter nouns, you must add –es (for short, one-syllable nouns) or –s (for multi-syllable nouns).
The genitive possessive articles depend on the gender of the possessor noun as well.
Here’s an example of the genitive case in action:
Das Haus meiner Schwester ist sehr groß. 
The house of my sister is very interesting. / My sister’s house is very big. The dative case (der Dativ) is used to express the indirect object of the sentence. This would be the noun that receives or is acted upon by the direct object.""",
        "Personal pronouns": {
            "1st": "meiner",
            "2nd": "deiner",
            "3rd Masculine":"seiner",
            "3rd Feminine":"ihrer",
            "3rd Neutral":"seiner",
            "1st Plural":"unser",
            "2nd Plural": "eurer",
            "3rd Plural:":"ihrer",
            "2nd Formal": "Ihrer"
        },
        "Articles": {
            "Definite": {
                "Masculine":"des",
                "Feminine": "der",
                "Neutral": "des",
                "Plural": "der"
            },
            "Indefinite": {
                "Masculine":"eines",
                "Feminine": "einer",
                "Neutral": "eines"
            }
        }
    }

}

def mode_decoder (mode:str) -> str:
    match mode:
        case "r": 
            return "Masculine"
        case "e":
            return "Feminine"
        case "s":
            return "Neutral"
        case "pl":
            return "Plural"
        case _:
            return ""

