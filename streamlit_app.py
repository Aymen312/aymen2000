"""Moha El Idrissi: physics and French lessons, exercises and revision tools."""

import html
import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from curriculum import LESSONS, LESSON_BY_ID, LEVELS, SUBJECTS
from learning import check_answer, default_progress, validate_progress

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Moha El Idrissi · Apprendre et pratiquer", page_icon="📚", layout="wide")
st.markdown(f"<style>{(ROOT / 'assets' / 'style.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

NAVIGATION = ["Accueil", "Cours", "Exercices", "Quiz", "Laboratoire", "Ma progression", "À propos"]
NAV_LABELS = {"Accueil": "⌂  Accueil", "Cours": "▤  Cours", "Exercices": "✎  Exercices",
              "Quiz": "✓  Quiz", "Laboratoire": "⚗  Laboratoire", "Ma progression": "↗  Ma progression",
              "À propos": "ⓘ  À propos"}

if "progress" not in st.session_state:
    st.session_state.progress = default_progress()
if "nav" not in st.session_state:
    st.session_state.nav = "Accueil"


def navigate(page, subject=None, lesson=None):
    st.session_state.nav = page
    if subject:
        st.session_state.subject_filter = subject
        st.session_state.level_filter = "Tous les niveaux"
    if lesson:
        st.session_state.subject_filter = LESSON_BY_ID[lesson]["subject"]
        st.session_state.level_filter = "Tous les niveaux"
        st.session_state.lesson_picker = lesson


def intro(eyebrow, title, description):
    st.markdown(f'<div class="eyebrow">{html.escape(eyebrow)}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="page-intro">{html.escape(description)}</p>', unsafe_allow_html=True)


def progress_stats():
    progress = st.session_state.progress
    correct = sum(result["correct"] is True for result in progress["exercises"].values())
    written = sum(result["correct"] is None and result["practiced"] for result in progress["exercises"].values())
    quizzes = progress["quizzes"]
    average = round(100 * sum(value["score"] for value in quizzes.values()) /
                    sum(value["total"] for value in quizzes.values())) if quizzes else None
    return len(progress["completed_lessons"]), correct, written, average


def lesson_card(lesson, index):
    subject_class = "physics" if lesson["subject"] == "Physique" else "french"
    st.markdown(f'''<div class="lesson-card {subject_class}">
      <span class="lesson-symbol" aria-hidden="true">{html.escape(lesson['icon'])}</span>
      <div class="card-meta">{html.escape(lesson['subject'])} · {html.escape(lesson['level'])} · {lesson['minutes']} min</div>
      <h3>{html.escape(lesson['title'])}</h3><p>{html.escape(lesson['description'])}</p>
      <span class="topic-tag">{html.escape(lesson['tag'])}</span></div>''', unsafe_allow_html=True)
    st.button("Découvrir le cours →", key=f"open_{index}_{lesson['id']}",
              on_click=navigate, args=("Cours", None, lesson["id"]), use_container_width=True)


def select_lesson():
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Matière", ["Toutes les matières", *SUBJECTS], key="subject_filter")
    with col2:
        level = st.selectbox("Niveau", ["Tous les niveaux", *LEVELS], key="level_filter")
    filtered = [item for item in LESSONS if (subject == "Toutes les matières" or item["subject"] == subject)
                and (level == "Tous les niveaux" or item["level"] == level)]
    if not filtered:
        st.info("Aucun cours ne correspond à ces filtres. Essaie une autre matière ou un autre niveau.")
        return None
    ids = [item["id"] for item in filtered]
    if st.session_state.get("lesson_picker") not in ids:
        st.session_state.lesson_picker = ids[0]
    selected = st.selectbox("Choisir un chapitre", ids, format_func=lambda key: LESSON_BY_ID[key]["title"], key="lesson_picker")
    return LESSON_BY_ID[selected]


def render_home():
    left, right = st.columns([1.6, 1], gap="large")
    with left:
        st.markdown('<div class="eyebrow">PHYSIQUE & FRANÇAIS · COLLÈGE ET LYCÉE</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Comprendre.<br>Pratiquer.<br><span>Progresser.</span></h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-description">Une notion à la fois. Des cours clairs, des exercices corrigés et des outils pour apprendre à ton rythme.</p>', unsafe_allow_html=True)
        a, b = st.columns(2)
        a.button("Explorer les cours →", type="primary", on_click=navigate, args=("Cours",), use_container_width=True)
        b.button("M'entraîner", on_click=navigate, args=("Exercices",), use_container_width=True)
    with right:
        st.markdown((ROOT / "assets" / "learning.svg").read_text(encoding="utf-8"), unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.metric("Cours à découvrir", len(LESSONS))
    b.metric("Exercices avec correction", sum(len(item["exercises"]) for item in LESSONS))
    c.metric("Questions pour réviser", sum(len(item["quiz"]) for item in LESSONS))
    st.divider()
    st.subheader("Deux matières, la même envie d'apprendre")
    a, b = st.columns(2, gap="large")
    with a:
        st.markdown('<div class="subject-panel physics"><span class="subject-number">01 / PHYSIQUE</span><h2>Observer. Calculer. Expliquer.</h2><p>Mouvement, électricité, forces et énergie : comprendre les phénomènes grâce à des exemples concrets.</p></div>', unsafe_allow_html=True)
        st.button("Découvrir la physique →", on_click=navigate, args=("Cours", "Physique"), use_container_width=True)
    with b:
        st.markdown('<div class="subject-panel french"><span class="subject-number">02 / FRANÇAIS</span><h2>Lire. Écrire. Argumenter.</h2><p>Grammaire, conjugaison, compréhension et expression : trouver les mots et construire ses idées.</p></div>', unsafe_allow_html=True)
        st.button("Découvrir le français →", on_click=navigate, args=("Cours", "Français"), use_container_width=True)
    st.subheader("Pour bien commencer")
    a, b = st.columns(2, gap="large")
    with a:
        lesson_card(LESSONS[0], "home")
    with b:
        lesson_card(LESSONS[4], "home")
    st.info("Ton parcours : lire une leçon → essayer les exercices → vérifier avec le quiz. Les corrections sont là pour t'aider à comprendre.")


def render_courses():
    intro("LE CATALOGUE", "Un cours, une idée claire.", "Choisis une matière et un chapitre. Chaque leçon comprend des objectifs, un exemple et l'essentiel à retenir.")
    lesson = select_lesson()
    if not lesson:
        return
    st.divider()
    st.caption(f"{lesson['subject']} / {lesson['tag']} · {lesson['level']} · environ {lesson['minutes']} minutes")
    st.header(lesson["title"])
    with st.expander("Ce que tu vas apprendre", expanded=True):
        for objective in lesson["objectives"]:
            st.markdown(f"- {objective}")
    st.markdown(lesson["body"])
    st.subheader("Un exemple pour comprendre")
    st.info(lesson["example"])
    st.success(lesson["takeaway"])
    completed = lesson["id"] in st.session_state.progress["completed_lessons"]
    if st.button("✓ Cours déjà lu" if completed else "Marquer ce cours comme lu", key=f"complete_{lesson['id']}", disabled=completed):
        st.session_state.progress["completed_lessons"].append(lesson["id"])
        st.rerun()
    a, b = st.columns(2)
    a.button("Passer aux exercices →", type="primary", on_click=navigate, args=("Exercices", None, lesson["id"]), use_container_width=True)
    b.button("Faire le quiz", on_click=navigate, args=("Quiz", None, lesson["id"]), use_container_width=True)
    download = f"# {lesson['title']}\n\n{lesson['body']}\n\n## Exemple\n\n{lesson['example']}\n\n## À retenir\n\n{lesson['takeaway']}"
    st.download_button("Télécharger la fiche de cours", download, file_name=f"cours_{lesson['id']}.md", mime="text/markdown")


def render_exercises():
    intro("À TOI DE JOUER", "Essayer, puis comprendre.", "Réponds avant d'ouvrir la correction. Tu peux demander un indice et recommencer autant que nécessaire.")
    lesson = select_lesson()
    if not lesson:
        return
    st.header(lesson["title"])
    for index, exercise in enumerate(lesson["exercises"]):
        key = f"{lesson['id']}:{index}"
        with st.container(border=True):
            st.subheader(f"{index + 1:02d} · {exercise['title']}")
            st.write(exercise["prompt"])
            with st.expander("Un petit indice"):
                st.write(exercise["hint"])
            with st.form(f"exercise_{key}"):
                if exercise["kind"] == "written":
                    answer = st.text_area("Ta réponse", key=f"answer_{key}", placeholder="Écris ta proposition ici…")
                    submitted = st.form_submit_button("Comparer avec une proposition de correction")
                else:
                    label = f"Ta réponse (en {exercise['unit']}, nombre seul)" if exercise["kind"] == "numeric" else "Ta réponse"
                    answer = st.text_input(label, key=f"answer_{key}", placeholder="Ex. : 0,5" if exercise["kind"] == "numeric" else "Écris ta réponse…")
                    submitted = st.form_submit_button("Vérifier ma réponse", type="primary")
            if submitted:
                if not answer.strip():
                    st.warning("Écris une réponse avant de la vérifier.")
                else:
                    correct = check_answer(exercise, answer)
                    previous = st.session_state.progress["exercises"].get(key, {})
                    st.session_state.progress["exercises"][key] = {
                        "correct": None if correct is None else bool(correct or previous.get("correct")), "practiced": True}
                    st.session_state[f"feedback_{key}"] = {"correct": correct, "answer": answer}
            feedback = st.session_state.get(f"feedback_{key}")
            if feedback:
                if feedback["correct"] is True:
                    st.success("Bonne réponse !")
                elif feedback["correct"] is False:
                    st.error("Cette réponse ne correspond pas à la correction. Utilise l'indice, puis essaie à nouveau.")
                else:
                    st.info("Plusieurs réponses sont possibles. Compare ta proposition avec le modèle ; cet exercice n'est pas noté automatiquement.")
                    st.markdown(exercise["solution"])
            with st.expander("Voir la correction expliquée"):
                st.markdown(exercise["solution"])
    st.caption("Pour les nombres, le point et la virgule sont acceptés. Les exercices de rédaction sont à comparer au modèle, sans note automatique.")
    st.button("Vérifier mes connaissances avec le quiz →", on_click=navigate, args=("Quiz", None, lesson["id"]), type="primary")


def render_quiz():
    intro("LE TEST DE RÉVISION", "Quatre questions pour faire le point.", "Choisis une réponse pour chaque question, puis découvre ton score et les explications.")
    lesson = select_lesson()
    if not lesson:
        return
    lesson_id = lesson["id"]
    st.header(lesson["title"])
    attempt = st.session_state.get(f"attempt_{lesson_id}", 0)
    with st.form(f"quiz_{lesson_id}_{attempt}"):
        answers = [st.radio(f"{index + 1}. {item['prompt']}", item["options"], index=None,
                            key=f"quiz_answer_{lesson_id}_{attempt}_{index}")
                   for index, item in enumerate(lesson["quiz"])]
        submitted = st.form_submit_button("Corriger mon quiz", type="primary")
    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Réponds aux quatre questions avant de corriger le quiz.")
        else:
            score = sum(answer == item["answer"] for answer, item in zip(answers, lesson["quiz"]))
            previous = st.session_state.progress["quizzes"].get(lesson_id, {"score": 0})
            st.session_state.progress["quizzes"][lesson_id] = {"score": max(score, previous["score"]), "total": len(answers)}
            st.session_state[f"quiz_feedback_{lesson_id}"] = {"score": score, "answers": answers, "attempt": attempt}
    feedback = st.session_state.get(f"quiz_feedback_{lesson_id}")
    if feedback and feedback["attempt"] == attempt:
        total = len(lesson["quiz"])
        st.metric("Ton résultat", f"{feedback['score']} / {total}")
        st.progress(feedback["score"] / total)
        for index, (answer, item) in enumerate(zip(feedback["answers"], lesson["quiz"])):
            if answer == item["answer"]:
                st.success(f"Question {index + 1} · Bonne réponse. {item['explanation']}")
            else:
                st.error(f"Question {index + 1} · Réponse attendue : {item['answer']}. {item['explanation']}")
        if st.button("Recommencer le quiz", key=f"retry_{lesson_id}"):
            st.session_state[f"attempt_{lesson_id}"] = attempt + 1
            st.rerun()
        st.caption("Ta progression conserve ton meilleur score pour chaque chapitre.")


def render_lab():
    intro("LE LABORATOIRE", "Et si on changeait une valeur ?", "Fais varier les paramètres pour comprendre les relations entre les grandeurs physiques.")
    tool = st.selectbox("Choisir une expérience", ["Mouvement uniforme", "Loi d'Ohm", "Masse et poids", "Énergie cinétique"], key="lab_tool")
    if tool == "Mouvement uniforme":
        st.latex(r"d(t)=v\,t")
        speed = st.slider("Vitesse constante (m/s)", 0.0, 30.0, 5.0, 0.5, key="speed")
        duration = st.slider("Durée (s)", 1, 120, 20, key="duration")
        a, b = st.columns(2)
        a.metric("Distance parcourue", f"{speed * duration:g} m")
        b.metric("Vitesse en km/h", f"{speed * 3.6:g} km/h")
        times = [duration * index / 40 for index in range(41)]
        st.line_chart({"Temps (s)": times, "Distance (m)": [speed * time for time in times]}, x="Temps (s)", y="Distance (m)", color="#176B57")
        st.info("La pente de cette droite correspond à la vitesse. Modèle : mouvement rectiligne uniforme, distance initiale nulle.")
    elif tool == "Loi d'Ohm":
        st.latex(r"U=RI \qquad P=RI^2")
        resistance = st.slider("Résistance (Ω)", 1, 200, 20, key="resistance")
        current = st.slider("Intensité (A)", 0.0, 2.0, 0.3, 0.05, key="current")
        a, b = st.columns(2)
        a.metric("Tension", f"{resistance * current:g} V")
        b.metric("Puissance dissipée", f"{resistance * current**2:.2f} W")
        currents = [index / 20 for index in range(41)]
        st.line_chart({"Intensité (A)": currents, "Tension (V)": [resistance * value for value in currents]}, x="Intensité (A)", y="Tension (V)", color="#176B57")
        st.info("La pente correspond à la résistance. Modèle : conducteur ohmique à température constante, en courant continu.")
    elif tool == "Masse et poids":
        st.latex(r"P=mg")
        mass = st.slider("Masse (kg)", 0.1, 20.0, 3.0, 0.1, key="weight_mass")
        place = st.selectbox("Lieu", ["Terre · g = 9,81 N/kg", "Lune · g = 1,62 N/kg", "Mars · g = 3,71 N/kg"], key="place")
        gravity = {"Terre · g = 9,81 N/kg": 9.81, "Lune · g = 1,62 N/kg": 1.62, "Mars · g = 3,71 N/kg": 3.71}[place]
        st.metric("Poids", f"{mass * gravity:.2f} N")
        st.bar_chart({"Astre": ["Terre", "Lune", "Mars"], "Poids (N)": [mass * value for value in [9.81, 1.62, 3.71]]}, x="Astre", y="Poids (N)", color="#176B57")
        st.info("La masse reste identique dans cette comparaison. Les valeurs de pesanteur sont des approximations près de la surface de chaque astre.")
    else:
        st.latex(r"E_c=\frac12 mv^2")
        mass = st.slider("Masse (kg)", 0.1, 20.0, 2.0, 0.1, key="energy_mass")
        speed = st.slider("Vitesse (m/s)", 0.0, 30.0, 3.0, 0.5, key="energy_speed")
        st.metric("Énergie cinétique", f"{0.5 * mass * speed**2:.2f} J")
        speeds = [index / 2 for index in range(61)]
        st.line_chart({"Vitesse (m/s)": speeds, "Énergie (J)": [0.5 * mass * value**2 for value in speeds]}, x="Vitesse (m/s)", y="Énergie (J)", color="#176B57")
        st.info("Doubler la vitesse multiplie l'énergie par quatre. Modèle : point matériel en mécanique classique.")
    st.caption("Les graphiques explorent un modèle idéal. Le laboratoire ne demande aucune manipulation électrique ou mécanique réelle.")


def render_progress():
    intro("TON PARCOURS", "Chaque étape compte.", "Retrouve les cours lus, les exercices réussis et tes meilleurs résultats aux quiz.")
    completed, correct, written, average = progress_stats()
    a, b, c, d = st.columns(4)
    a.metric("Cours lus", f"{completed} / {len(LESSONS)}")
    b.metric("Exercices réussis", correct)
    c.metric("Rédactions travaillées", written)
    d.metric("Meilleurs scores moyens", f"{average} %" if average is not None else "—")
    st.progress(completed / len(LESSONS), text="Part des cours marqués comme lus")
    rows = []
    for lesson in LESSONS:
        score = st.session_state.progress["quizzes"].get(lesson["id"])
        results = [st.session_state.progress["exercises"].get(f"{lesson['id']}:{index}", {}) for index in range(len(lesson["exercises"]))]
        rows.append({"Matière": lesson["subject"], "Chapitre": lesson["title"],
                     "Cours": "Lu" if lesson["id"] in st.session_state.progress["completed_lessons"] else "À découvrir",
                     "Exercices réussis": sum(result.get("correct") is True for result in results),
                     "Quiz": f"{score['score']} / {score['total']}" if score else "À faire"})
    st.dataframe(rows, hide_index=True, use_container_width=True)
    st.info("La progression est conservée pendant cette session. Télécharge une sauvegarde pour la retrouver après une fermeture ou un redémarrage, puis importe-la ici.")
    data = dict(st.session_state.progress, exported_at=datetime.now(timezone.utc).isoformat())
    st.download_button("Télécharger ma progression", json.dumps(data, ensure_ascii=False, indent=2), file_name="moha_progression.json", mime="application/json", type="primary")
    with st.expander("Restaurer une sauvegarde"):
        uploaded = st.file_uploader("Fichier de progression (.json)", type="json", key="progress_upload")
        st.caption("L'import remplace la progression de la session actuelle.")
        if st.button("Importer cette progression", disabled=uploaded is None):
            try:
                if uploaded.size > 300_000:
                    raise ValueError("Le fichier est trop volumineux.")
                restored = validate_progress(json.loads(uploaded.getvalue().decode("utf-8")))
            except (ValueError, UnicodeError) as error:
                st.error(f"Import impossible : {error}")
            else:
                st.session_state.progress = restored
                for key in list(st.session_state):
                    if key.startswith(("feedback_", "quiz_feedback_")):
                        del st.session_state[key]
                st.session_state.restore_notice = True
                st.rerun()
    if st.session_state.pop("restore_notice", False):
        st.success("Ta progression a été restaurée.")
    with st.expander("Recommencer mon parcours"):
        confirmed = st.checkbox("Je souhaite effacer la progression de cette session.", key="confirm_reset")
        if st.button("Réinitialiser ma progression", disabled=not confirmed):
            for key in list(st.session_state):
                if key != "nav":
                    del st.session_state[key]
            st.rerun()


def render_about():
    intro("LE PROJET", "Apprendre avec Moha El Idrissi.", "Un espace simple pour comprendre une notion, la pratiquer et revenir sur ses erreurs.")
    st.markdown("""
Ce site propose un **premier catalogue de ressources en français**, pour le collège et le lycée.
Les niveaux sont indicatifs : les chapitres ne constituent pas un programme scolaire officiel complet.

**Comment l'utiliser ?** Lis le cours, essaie les exercices, puis passe au quiz.
Les exercices de rédaction proposent une correction possible plutôt qu'une réponse unique.
Le laboratoire permet d'explorer des modèles simples de physique.

**Ta progression.** Aucun compte élève n'est nécessaire. La progression appartient à la session
en cours et peut être téléchargée puis restaurée. L'application n'enregistre pas de profils
ou de réponses dans une base de données. L'hébergement peut toutefois produire ses propres
journaux techniques.

**Faire évoluer les cours.** Le catalogue est organisé par chapitre. Il peut être enrichi avec
de nouvelles notions, des exercices et des questions de révision.
""")
    st.link_button("Voir le projet sur GitHub ↗", "https://github.com/Aymen312/Moha-El-idrissi")
    st.caption("Le dépôt GitHub est privé ; son accès dépend des autorisations de son propriétaire.")


with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">M<span>.</span></span><div>Moha El Idrissi<small>Apprendre & pratiquer</small></div></div>', unsafe_allow_html=True)
    st.caption("TON ESPACE D'APPRENTISSAGE")
    page = st.radio("Navigation", NAVIGATION, format_func=lambda value: NAV_LABELS[value], key="nav", label_visibility="collapsed")
    st.divider()
    read, solved, _, average = progress_stats()
    st.markdown("**Un pas après l'autre.**")
    st.progress(read / len(LESSONS))
    st.caption(f"{read} cours lus · {solved} exercices réussis")
    st.markdown('<div class="sidebar-note">Comprendre une erreur,<br>c’est déjà progresser.</div>', unsafe_allow_html=True)

{"Accueil": render_home, "Cours": render_courses, "Exercices": render_exercises,
 "Quiz": render_quiz, "Laboratoire": render_lab, "Ma progression": render_progress,
 "À propos": render_about}[page]()
st.divider()
st.markdown('<div class="footer">MOHA EL IDRISSI <span>Physique & français · Apprendre à ton rythme.</span></div>', unsafe_allow_html=True)
