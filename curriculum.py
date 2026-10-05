"""Original starter lessons in French; edit this file to extend the catalogue."""


def numeric(title, prompt, answer, unit, solution, hint, tolerance=0.01):
    return dict(title=title, prompt=prompt, kind="numeric", answer=answer,
                unit=unit, solution=solution, hint=hint, tolerance=tolerance)


def text(title, prompt, answers, solution, hint):
    return dict(title=title, prompt=prompt, kind="text", answers=answers,
                solution=solution, hint=hint)


def written(title, prompt, solution, hint):
    return dict(title=title, prompt=prompt, kind="written", solution=solution, hint=hint)


def question(prompt, options, answer, explanation):
    return dict(prompt=prompt, options=options, answer=answer, explanation=explanation)


LESSONS = [
    dict(
        id="mouvement", subject="Physique", level="Collège", minutes=12,
        title="Mouvement et vitesse", icon="↗", tag="Mécanique",
        description="Relier une distance, une durée et une vitesse moyenne.",
        objectives=["Calculer une vitesse moyenne", "Convertir des unités", "Distinguer mouvement uniforme et mouvement accéléré"],
        body=r"""
### Décrire un mouvement
Un mouvement se décrit par rapport à un **référentiel**, par exemple le sol.
Un passager assis est immobile par rapport au train et en mouvement par rapport au sol.
La **trajectoire** est l'ensemble des positions occupées : elle peut être rectiligne,
circulaire ou plus généralement curviligne.

### Calculer une vitesse moyenne
La vitesse moyenne sur un trajet est la distance totale parcourue divisée par la durée totale :

$$v_{\mathrm{moy}} = \frac{d}{\Delta t}$$

Avec $d$ en mètres et $\Delta t$ en secondes, la vitesse s'exprime en m/s.
Avec des kilomètres et des heures, elle s'exprime en km/h. Une durée doit être strictement positive.

### Convertir et interpréter
Pour passer des m/s aux km/h, **multiplier par 3,6**. Pour faire l'inverse, diviser par 3,6.
Un mouvement est uniforme si la valeur de la vitesse reste constante. Il est accéléré
si cette valeur augmente et ralenti si elle diminue. La vitesse moyenne ne décrit pas,
à elle seule, chaque instant du trajet.
""",
        example="Un cycliste parcourt 600 m en 120 s. Sa vitesse moyenne vaut 600 ÷ 120 = **5 m/s**, soit **18 km/h**.",
        takeaway="Choisis des unités cohérentes avant de calculer : v = d / Δt et 1 m/s = 3,6 km/h.",
        exercises=[
            numeric("Un trajet à vélo", "Un cycliste parcourt 900 m en 180 s. Quelle est sa vitesse moyenne en m/s ?", 5, "m/s", "v = 900 / 180 = **5 m/s**.", "Divise la distance par la durée."),
            numeric("Changer d'unité", "Convertis 72 km/h en m/s.", 20, "m/s", "72 / 3,6 = **20 m/s**.", "Pour passer de km/h à m/s, divise par 3,6."),
            numeric("Combien de temps ?", "Un mobile parcourt 1 200 m à une vitesse constante de 6 m/s. Calcule la durée en secondes.", 200, "s", "Δt = d / v = 1 200 / 6 = **200 s**.", "Isole la durée dans la relation v = d / Δt."),
        ],
        quiz=[
            question("L'unité SI de vitesse est…", ["m/s", "km", "s", "kg"], "m/s", "La vitesse est une distance divisée par une durée : m/s."),
            question("Un mouvement uniforme a…", ["une vitesse de valeur constante", "une vitesse qui augmente", "une distance nulle", "une durée nulle"], "une vitesse de valeur constante", "Uniforme signifie que la valeur de la vitesse ne change pas."),
            question("10 m/s correspondent à…", ["2,78 km/h", "36 km/h", "10 km/h", "360 km/h"], "36 km/h", "10 × 3,6 = 36 km/h."),
            question("Un passager assis est immobile par rapport…", ["au train", "au sol lorsque le train roule", "à tous les référentiels", "au Soleil dans tous les cas"], "au train", "La description du mouvement dépend du référentiel choisi."),
        ],
    ),
    dict(
        id="electricite", subject="Physique", level="Collège", minutes=15,
        title="Électricité et loi d'Ohm", icon="ϟ", tag="Électricité",
        description="Comprendre tension, intensité et résistance dans un circuit.",
        objectives=["Identifier U, I et R", "Appliquer U = R × I", "Calculer une puissance électrique"],
        body=r"""
### Trois grandeurs à connaître
La **tension** $U$ se mesure en volts (V). L'**intensité** $I$ se mesure en ampères (A).
La **résistance** $R$ se mesure en ohms ($\Omega$).
Un ampèremètre se branche en série ; un voltmètre se branche en dérivation aux bornes du composant.

### La loi d'Ohm
Pour un conducteur ohmique à température constante :

$$U = R I \qquad I = \frac{U}{R} \qquad R = \frac{U}{I}$$

Sa tension est proportionnelle à l'intensité qui le traverse. Cette loi ne décrit pas
tous les composants : une diode ou une lampe à filament ne se comportent pas comme
une résistance constante sur toute leur plage de fonctionnement.

### Puissance électrique
En courant continu, la puissance reçue par un composant est $P = U I$, en watts (W).
Pour une résistance, on peut aussi écrire $P = R I^2$.
Avant de calculer, convertis les milliampères : **1 000 mA = 1 A**.
""",
        example="Une résistance de 100 Ω est soumise à 5 V. I = 5 / 100 = **0,05 A**, soit **50 mA**. Sa puissance vaut 5 × 0,05 = **0,25 W**.",
        takeaway="La loi d'Ohm s'applique aux conducteurs ohmiques : U = R × I. Utilise des ampères dans les calculs.",
        exercises=[
            numeric("Trouver une tension", "Une résistance de 20 Ω est traversée par 0,3 A. Calcule la tension à ses bornes.", 6, "V", "U = R × I = 20 × 0,3 = **6 V**.", "Multiplie la résistance par l'intensité."),
            numeric("Trouver une intensité", "Une résistance de 60 Ω est soumise à 12 V. Calcule I en ampères.", 0.2, "A", "I = U / R = 12 / 60 = **0,2 A**.", "I = U / R.", 0.001),
            numeric("Calculer une puissance", "Un appareil reçoit 12 V et est traversé par 0,5 A. Calcule sa puissance.", 6, "W", "P = U × I = 12 × 0,5 = **6 W**.", "En courant continu, P = U × I."),
        ],
        quiz=[
            question("L'intensité se mesure en…", ["volts", "ampères", "ohms", "watts"], "ampères", "L'ampère est l'unité d'intensité électrique."),
            question("Pour une résistance constante, si U double, I…", ["double", "est divisée par deux", "reste inchangée", "devient nulle"], "double", "I = U / R : l'intensité est proportionnelle à la tension."),
            question("250 mA valent…", ["0,25 A", "2,5 A", "25 A", "250 A"], "0,25 A", "On divise les milliampères par 1 000."),
            question("Un voltmètre se branche…", ["en dérivation", "en série uniquement", "à la place du générateur", "sans contact électrique"], "en dérivation", "Il mesure la tension entre les deux bornes d'un composant."),
        ],
    ),
    dict(
        id="poids", subject="Physique", level="Collège", minutes=12,
        title="Forces, masse et poids", icon="↓", tag="Mécanique",
        description="Distinguer la masse d'un objet de son poids.",
        objectives=["Exprimer une force en newtons", "Utiliser P = m × g", "Expliquer la différence entre masse et poids"],
        body=r"""
### Qu'est-ce qu'une force ?
Une force modélise une action mécanique. Elle peut modifier un mouvement ou déformer un objet.
On la représente par une flèche qui précise son point d'application, sa direction,
son sens et sa valeur. Sa valeur se mesure en **newtons (N)** avec un dynamomètre.

### Masse et poids
La **masse** $m$, en kilogrammes, ne dépend pas du lieu dans les situations étudiées ici.
Le **poids** est la force d'attraction gravitationnelle exercée par un astre sur l'objet.
Près de sa surface :

$$P = m g$$

$g$ est l'intensité de la pesanteur, en N/kg. Près de la surface terrestre,
on utilise souvent $g \approx 9{,}81$ N/kg. Un exercice peut choisir 10 N/kg pour simplifier.
Le poids dépend donc du lieu, alors que la masse reste la même.

### Faire attention aux unités
Convertis la masse en kilogrammes avant de multiplier : **500 g = 0,5 kg**.
Près de la surface de la Terre, la direction du poids est verticale et son sens est vers le bas.
""",
        example="Avec g = 10 N/kg, un objet de masse 0,5 kg a un poids P = 0,5 × 10 = **5 N**. Sur la Lune, son poids est plus faible ; sa masse reste 0,5 kg.",
        takeaway="La masse se mesure en kg, le poids en N. Le poids se calcule avec P = m × g.",
        exercises=[
            numeric("Un cartable", "Un cartable a une masse de 3 kg. Avec g = 10 N/kg, calcule son poids.", 30, "N", "P = 3 × 10 = **30 N**.", "P = m × g."),
            numeric("Retrouver la masse", "Un objet pèse 45 N dans un lieu où g = 10 N/kg. Quelle est sa masse ?", 4.5, "kg", "m = P / g = 45 / 10 = **4,5 kg**.", "Isole m dans P = m × g."),
            numeric("Sur la Lune", "Une masse de 5 kg se trouve sur la Lune, où l'on prend g = 1,6 N/kg. Calcule son poids.", 8, "N", "P = 5 × 1,6 = **8 N**.", "La masse reste 5 kg ; utilise la pesanteur lunaire."),
        ],
        quiz=[
            question("Le poids est…", ["une force", "une masse", "un volume", "une vitesse"], "une force", "Le poids est une force gravitationnelle."),
            question("L'unité SI de masse est…", ["le newton", "le kilogramme", "le watt", "le volt"], "le kilogramme", "La masse s'exprime en kilogrammes."),
            question("La masse d'un objet sur la Lune…", ["reste la même", "devient nulle", "est divisée par six exactement", "se mesure en newtons"], "reste la même", "Changer d'astre change le poids, pas la masse dans ce cadre."),
            question("Pour m = 2 kg et g = 10 N/kg, P vaut…", ["5 N", "12 N", "20 N", "200 N"], "20 N", "P = 2 × 10 = 20 N."),
        ],
    ),
    dict(
        id="energie", subject="Physique", level="Lycée", minutes=18,
        title="Énergie cinétique et conservation", icon="∿", tag="Énergie",
        description="Relier énergie, vitesse et hauteur dans un modèle simple.",
        objectives=["Calculer une énergie cinétique", "Calculer une énergie potentielle de pesanteur", "Préciser les conditions de conservation"],
        body=r"""
### L'énergie du mouvement
Dans le cadre de la mécanique classique, l'énergie cinétique d'un objet de masse $m$
dont le centre de masse se déplace à la vitesse $v$ s'écrit, pour le modèle du point matériel :

$$E_c = \frac{1}{2} m v^2$$

Avec $m$ en kg et $v$ en m/s, l'énergie s'exprime en joules (J).
Si la vitesse double, l'énergie cinétique est multipliée par quatre.

### L'énergie liée à la hauteur
Dans un champ de pesanteur supposé uniforme, l'énergie potentielle peut s'écrire :

$$E_p = m g h$$

Le niveau $h = 0$ est une référence choisie. Ce sont les différences d'énergie
potentielle qui interviennent dans les échanges d'énergie.

### Conservation de l'énergie mécanique
L'énergie mécanique est $E_m = E_c + E_p$ dans le modèle étudié.
Elle reste constante lorsque seules des forces conservatives travaillent, par exemple
le poids sans frottement. Avec des frottements, l'énergie mécanique peut diminuer et
être transférée notamment sous forme d'énergie thermique. L'énergie totale se conserve
si l'on tient compte de tous les échanges.
""",
        example="Une balle de 0,2 kg se déplace à 10 m/s : Ec = ½ × 0,2 × 10² = **10 J**. À 20 m/s, Ec = **40 J**.",
        takeaway="Ec = ½mv² ; Ep = mgh. La conservation de l'énergie mécanique exige des conditions explicites.",
        exercises=[
            numeric("Énergie d'un mobile", "Un mobile de 2 kg se déplace à 3 m/s. Calcule son énergie cinétique.", 9, "J", "Ec = ½ × 2 × 3² = **9 J**.", "Élève d'abord la vitesse au carré."),
            numeric("Prendre de la hauteur", "Une masse de 2 kg est à h = 5 m au-dessus de la référence. Avec g = 10 N/kg, calcule Ep.", 100, "J", "Ep = mgh = 2 × 10 × 5 = **100 J**.", "Utilise Ep = m × g × h."),
            numeric("Une chute idéale", "Un objet part du repos à 5 m au-dessus du sol. Sans frottement, avec g = 10 N/kg, quelle est sa vitesse juste avant de toucher le sol ?", 10, "m/s", "mgh = ½mv², donc v = √(2gh) = √100 = **10 m/s**.", "La perte d'énergie potentielle devient un gain d'énergie cinétique."),
        ],
        quiz=[
            question("L'énergie se mesure en…", ["joules", "newtons", "mètres", "ampères"], "joules", "Le joule est l'unité SI d'énergie."),
            question("Si la vitesse triple à masse constante, Ec est multipliée par…", ["3", "6", "9", "1"], "9", "L'énergie cinétique est proportionnelle au carré de la vitesse."),
            question("Sans frottement, une chute transforme surtout…", ["Ep en Ec", "Ec en masse", "la masse en vitesse", "la tension en résistance"], "Ep en Ec", "La perte d'énergie potentielle correspond à un gain d'énergie cinétique."),
            question("Avec des frottements, l'énergie mécanique…", ["peut diminuer", "est toujours conservée", "augmente toujours", "est toujours nulle"], "peut diminuer", "Une partie peut être transférée sous forme thermique ; l'énergie totale reste conservée si tous les échanges sont inclus."),
        ],
    ),
    dict(
        id="accords", subject="Français", level="Collège", minutes=12,
        title="Les accords dans le groupe nominal", icon="Aa", tag="Grammaire",
        description="Accorder le déterminant, le nom et l'adjectif.",
        objectives=["Repérer le nom principal", "Identifier le genre et le nombre", "Accorder un adjectif qualificatif"],
        body="""
### Repérer le groupe nominal
Un groupe nominal se construit autour d'un **nom principal**, souvent appelé le noyau.
Dans « les petites maisons », le noyau est « maisons ». Le déterminant « les » et
l'adjectif « petites » se rapportent à ce nom.

### Faire les accords
Le déterminant et l'adjectif s'accordent en **genre** (masculin ou féminin) et en
**nombre** (singulier ou pluriel) avec le nom. On écrit « un livre intéressant »,
« une histoire intéressante » et « des histoires intéressantes ».
Le féminin et le pluriel ne se forment pas toujours par un simple ajout :
« beau » devient « belle », « nouveau » devient « nouvelle ».

### Une méthode de relecture
1. Souligne le nom principal.
2. Détermine son genre et son nombre.
3. Vérifie le déterminant et chaque adjectif qui s'y rapporte.

Les exercices de cette leçon portent sur des adjectifs courants. Certains accords,
notamment les adjectifs de couleur composés, demandent des règles supplémentaires.
""",
        example="« Une petite maison » devient au pluriel **« des petites maisons »** : le déterminant, l'adjectif et le nom changent ensemble.",
        takeaway="Pars du nom : son genre et son nombre commandent les accords du déterminant et de l'adjectif.",
        exercises=[
            text("Un adjectif au pluriel", "Complète avec la forme de « vert » : des feuilles _____. Écris seulement le mot manquant.", ["vertes"], "« Feuilles » est féminin pluriel : **vertes**.", "L'adjectif s'accorde avec « feuilles »."),
            text("Un féminin particulier", "Complète avec la forme de « nouveau » : une _____ histoire. Écris seulement le mot manquant.", ["nouvelle"], "Au féminin singulier, « nouveau » devient **nouvelle**.", "Le nom « histoire » est féminin singulier."),
            text("Tout au pluriel", "Mets au pluriel le groupe nominal « un petit chat ».", ["des petits chats"], "**Des petits chats** : les trois mots portent la marque du pluriel.", "Change aussi le déterminant."),
        ],
        quiz=[
            question("Dans « les grandes fenêtres », le noyau est…", ["les", "grandes", "fenêtres", "le groupe entier"], "fenêtres", "Le nom principal est « fenêtres »."),
            question("Quelle forme est correcte ?", ["des robes bleues", "des robes bleu", "des robe bleues", "des robes bleus"], "des robes bleues", "« Bleues » s'accorde au féminin pluriel avec « robes »."),
            question("Le féminin de « beau » est…", ["beau", "beaus", "belle", "beaux"], "belle", "Le féminin de « beau » est « belle »."),
            question("Le groupe « une histoire intéressante » est…", ["féminin singulier", "masculin singulier", "féminin pluriel", "masculin pluriel"], "féminin singulier", "Le nom « histoire » est féminin et employé au singulier."),
        ],
    ),
    dict(
        id="conjugaison", subject="Français", level="Collège", minutes=15,
        title="Présent, imparfait et passé composé", icon="Ab", tag="Conjugaison",
        description="Choisir et former trois temps fréquents de l'indicatif.",
        objectives=["Conjuguer les verbes réguliers du premier groupe", "Former l'imparfait", "Construire le passé composé"],
        body="""
### Le présent de l'indicatif
Le présent peut exprimer une action actuelle, une habitude ou une vérité générale.
Pour un verbe régulier du premier groupe comme « parler », les terminaisons sont
**-e, -es, -e, -ons, -ez, -ent**. Le verbe « aller » est une exception : il n'appartient
pas au premier groupe malgré sa terminaison en -er.

### L'imparfait
L'imparfait sert souvent à décrire, à raconter une habitude passée ou à présenter
une action en cours dans le passé. On part généralement du radical de « nous »
au présent, sans -ons, puis on ajoute **-ais, -ais, -ait, -ions, -iez, -aient**.
« Nous finissons » donne « je finissais ». Le verbe « être » utilise le radical « ét- ».

### Le passé composé
Il se construit avec **avoir ou être au présent + participe passé** :
« j'ai parlé », « elle est arrivée ». Avec « être », le participe passé s'accorde
généralement avec le sujet : « elles sont arrivées ». Avec « avoir », il ne s'accorde
pas avec le sujet ; un complément d'objet direct placé avant peut imposer un accord.

### Choisir un temps
« Il pleuvait quand le bus est arrivé » associe une situation en cours à un événement.
Le choix dépend du contexte : évite d'associer un temps à une seule valeur dans tous les textes.
""",
        example="Présent : **nous parlons**. Imparfait : **nous parlions**. Passé composé : **nous avons parlé**.",
        takeaway="Le passé composé possède deux éléments. À l'imparfait, repère le radical et la terminaison.",
        exercises=[
            text("Au présent", "Conjugue « parler » au présent avec « nous ». Écris le verbe seul.", ["parlons"], "Nous **parlons** : radical parl- et terminaison -ons.", "La terminaison de « nous » est -ons."),
            text("À l'imparfait", "Conjugue « finir » à l'imparfait avec « je ». Écris le verbe seul.", ["finissais"], "Nous finissons → finiss- → je **finissais**.", "Pars de « nous finissons » au présent."),
            text("Au passé composé", "Complète : « Elles _____ tôt. » Utilise « arriver » au passé composé et écris les deux mots manquants.", ["sont arrivées", "sont arrivees"], "Elles **sont arrivées**. L'auxiliaire est « être » et le participe s'accorde au féminin pluriel.", "Ce verbe utilise ici l'auxiliaire « être »."),
        ],
        quiz=[
            question("Quel verbe est à l'imparfait ?", ["parlait", "parle", "a parlé", "parlera"], "parlait", "La terminaison -ait indique ici l'imparfait."),
            question("Quel est le passé composé de « je mange » ?", ["j'ai mangé", "je mangeais", "je mangerai", "je manger"], "j'ai mangé", "Le passé composé associe l'auxiliaire au présent et le participe passé."),
            question("Quelle phrase est correcte ?", ["Elles sont parties.", "Elles sont parti.", "Elles est parties.", "Elles ont partir."], "Elles sont parties.", "Avec être, le participe passé s'accorde ici avec « elles »."),
            question("Dans « Quand j'étais petit, je jouais dehors », l'imparfait exprime notamment…", ["une habitude passée", "un ordre", "un futur certain", "une question"], "une habitude passée", "Le contexte présente une action habituelle dans le passé."),
        ],
    ),
    dict(
        id="lecture", subject="Français", level="Collège", minutes=15,
        title="Lire et comprendre un texte", icon="≡", tag="Lecture",
        description="Repérer les informations et justifier une interprétation.",
        objectives=["Repérer les informations explicites", "Faire une inférence justifiée", "Distinguer auteur et narrateur"],
        body="""
### Lire en deux passages
Une première lecture permet de comprendre la situation : qui agit, où et quand ?
Une seconde lecture sert à repérer les détails utiles et les mots qui relient les idées.

### Information explicite et inférence
Une information **explicite** est directement présente dans le texte.
Une **inférence** est une conclusion tirée de plusieurs indices. Elle doit pouvoir être
justifiée ; elle ne doit pas ajouter des faits sans appui.

### Auteur et narrateur
L'auteur est la personne qui écrit le texte. Le narrateur est la voix qui raconte.
Un récit à la première personne ne prouve pas, à lui seul, que le narrateur est l'auteur.

### Texte d'entraînement
> Lina referma son parapluie avant d'entrer dans la bibliothèque. Ses chaussures
> laissaient de petites traces sur le sol. Elle regarda l'horloge : dix-sept heures.
> « J'ai encore une heure », pensa-t-elle, puis elle chercha le rayon des romans.

Le lieu est explicitement donné. Le parapluie et les chaussures mouillées suggèrent
qu'il pleut ou qu'il a plu. Le texte ne donne pas directement l'heure de fermeture
de la bibliothèque : Lina peut avoir une autre raison de disposer d'une heure.
""",
        example="Question : où se trouve Lina ? Réponse : **dans une bibliothèque**. Justification : le texte dit « avant d'entrer dans la bibliothèque ».",
        takeaway="Appuie chaque réponse sur le texte et distingue ce qui est dit de ce qui est seulement suggéré.",
        exercises=[
            text("Repérer le lieu", "D'après le texte de la leçon, dans quel lieu Lina entre-t-elle ?", ["une bibliothèque", "la bibliothèque", "bibliothèque", "dans une bibliothèque", "dans la bibliothèque"], "Lina entre **dans une bibliothèque**. Le lieu est explicitement nommé.", "Relis la première phrase."),
            text("Repérer une heure", "Quelle heure Lina lit-elle sur l'horloge ? Écris sous la forme 17 h ou 17:00.", ["17 h", "17h", "17:00", "17 heures", "dix-sept heures"], "L'horloge indique **17 h**.", "L'heure est donnée juste après le mot « horloge »."),
            written("Justifier une inférence", "Pourquoi peut-on penser qu'il pleut ou qu'il a plu ? Cite deux indices du texte.", "Le **parapluie** et les **traces laissées par les chaussures** suggèrent de la pluie. Le texte ne précise pas directement si elle tombe encore.", "Repère les objets et les détails qui évoquent l'eau."),
        ],
        quiz=[
            question("Une information explicite est…", ["directement écrite dans le texte", "inventée par le lecteur", "toujours fausse", "toujours une opinion"], "directement écrite dans le texte", "Elle apparaît directement dans le texte."),
            question("L'auteur et le narrateur…", ["ne sont pas nécessairement la même personne", "sont toujours la même personne", "n'existent que dans la poésie", "sont tous les personnages"], "ne sont pas nécessairement la même personne", "L'auteur écrit ; le narrateur est la voix du récit."),
            question("Quel rayon Lina cherche-t-elle ?", ["les romans", "les dictionnaires", "les revues", "les sciences"], "les romans", "La dernière phrase mentionne le rayon des romans."),
            question("Le texte permet-il d'affirmer que la bibliothèque ferme à 18 h ?", ["Non, ce n'est pas précisé.", "Oui, c'est écrit.", "Oui, toute bibliothèque ferme à 18 h.", "Non, elle ferme forcément à 17 h."], "Non, ce n'est pas précisé.", "Lina dispose d'une heure, mais la raison n'est pas indiquée."),
        ],
    ),
    dict(
        id="argumentation", subject="Français", level="Lycée", minutes=20,
        title="Construire un paragraphe argumenté", icon="¶", tag="Expression écrite",
        description="Défendre une idée avec une raison et un exemple précis.",
        objectives=["Formuler une thèse", "Distinguer argument et exemple", "Écrire un paragraphe cohérent et nuancé"],
        body="""
### Thèse, argument et exemple
La **thèse** est l'idée que l'on défend. Un **argument** explique pourquoi on la défend.
Un **exemple** illustre l'argument par un cas concret. Un exemple isolé ne suffit pas
nécessairement à établir une conclusion générale.

### Construire le paragraphe
Commence par une idée claire, donne une raison, puis ajoute un exemple pertinent.
Termine en expliquant ce que cet exemple apporte. Les connecteurs (« car », « par exemple »,
« cependant ») aident à suivre le raisonnement lorsqu'ils expriment le bon lien logique.

### Nuancer sans perdre sa position
Reconnaître une limite rend une position plus précise. « Les outils numériques peuvent
aider à réviser, à condition de choisir des ressources fiables » est plus défendable
que « tous les outils numériques améliorent toujours les résultats ».

### Relire
Vérifie que chaque phrase sert l'idée principale, que l'exemple est précis et que les
accords sont corrects. Une formulation simple vaut mieux qu'un mot compliqué utilisé
sans nécessité. Plusieurs réponses bien construites sont possibles en expression écrite.
""",
        example="**Idée :** les exercices réguliers aident à apprendre. **Argument :** ils obligent à utiliser les notions. **Exemple :** résoudre plusieurs problèmes de vitesse permet de repérer les erreurs de conversion.",
        takeaway="Une idée, une raison, un exemple, puis une explication : chaque élément doit servir la même thèse.",
        exercises=[
            text("Nommer l'idée défendue", "Comment appelle-t-on l'idée principale que l'on défend dans une argumentation ? Écris un seul mot.", ["thèse", "these"], "L'idée défendue est la **thèse**.", "Le mot apparaît au début de la leçon."),
            written("Du général au concret", "Propose un exemple précis pour soutenir l'argument : « Lire régulièrement enrichit le vocabulaire. »", "Exemple possible : « En lisant un roman chaque mois et en notant les mots inconnus, un élève découvre des mots qu'il peut ensuite réutiliser dans ses rédactions. » D'autres exemples cohérents sont possibles.", "Décris une situation concrète plutôt que de répéter l'argument."),
            written("Rédiger un paragraphe", "En 4 à 6 phrases, défends l'intérêt de travailler en groupe. Donne un argument, un exemple et une limite.", "Exemple possible : « Travailler en groupe peut aider à comprendre une difficulté. Chaque élève peut expliquer sa méthode aux autres. Dans un exercice de physique, comparer deux calculs permet de repérer une erreur d'unité. Toutefois, chacun doit participer pour que ce travail soit utile. » Vérifie la présence d'une idée, d'une raison, d'un exemple et d'une limite.", "Commence par « Travailler en groupe peut… » et ajoute une réserve avec « toutefois »."),
        ],
        quiz=[
            question("Un argument sert à…", ["justifier une idée", "remplacer toute preuve par un mot", "nommer un personnage", "indiquer seulement un lieu"], "justifier une idée", "Il apporte une raison pour soutenir la thèse."),
            question("Quel connecteur introduit généralement une opposition ?", ["cependant", "donc", "par exemple", "car"], "cependant", "« Cependant » signale une opposition ou une réserve."),
            question("Quelle phrase est la plus nuancée ?", ["Ces outils peuvent aider si les ressources sont fiables.", "Ces outils fonctionnent toujours.", "Ces outils sont tous inutiles.", "Personne ne se trompe avec ces outils."], "Ces outils peuvent aider si les ressources sont fiables.", "La phrase précise une possibilité et une condition."),
            question("Un exemple pertinent doit…", ["illustrer l'argument", "changer complètement de sujet", "être toujours inventé comme un fait réel", "remplacer la thèse"], "illustrer l'argument", "Il rend l'argument concret et doit rester lié à l'idée défendue."),
        ],
    ),
]

LESSON_BY_ID = {lesson["id"]: lesson for lesson in LESSONS}
SUBJECTS = ("Physique", "Français")
LEVELS = ("Collège", "Lycée")
