from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
from datetime import datetime
import sys
import traceback

# Logging für Debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Bot-Token (ersetze diesen mit deinem tatsächlichen Token)
TOKEN = "8110397202:AAG-BUqDPgywugBWrMZWNgJ7xRX-GnIKbzk"

# Fehler-Handler hinzufügen
def log_exception(exc_type, exc_value, exc_tb):
    print(f"Fehler aufgetreten: {exc_type}, {exc_value}")
    traceback.print_tb(exc_tb)

sys.excepthook = log_exception

# Start-Kommando
async def start(update, context):
    print("Start-Befehl empfangen!")  # Debug-Ausgabe
    await update.message.reply_text("Willkommen! Sende mir ein Geburtsdatum im Format 'TT.MM.JJJJ, HH:MM' (z.B. 09.12.1982, 14:50).")

# Funktion zur Konvertierung des gregorianischen Datums in den chinesischen Kalender
def convert_to_chinese_year(gregorian_date_str):
    try:
        gregorian_date = datetime.strptime(gregorian_date_str, "%d.%m.%Y, %H:%M")
        print(f"Umgewandeltes Datum: {gregorian_date}")  # Debug-Ausgabe
        return gregorian_date.year
    except ValueError:
        print("Ungültiges Datumsformat!")  # Fehlermeldung
        return None

# Funktion zur Berechnung des chinesischen Jahres und der Elemente
def get_chinese_elements(year):
    heavenly_stems = ["Yang Holz", "Yin Holz", "Yang Feuer", "Yin Feuer", "Yang Erde", "Yin Erde", "Yang Metall", "Yin Metall", "Yang Wasser", "Yin Wasser"]
    earthly_branches = ["Ratte", "Ochse", "Tiger", "Hase", "Drache", "Schlange", "Pferd", "Ziege", "Affe", "Hahn", "Hund", "Schwein"]

    # Berechnung des Zyklus, basierend auf dem Jahr 1924
    year_diff = year - 1924
    heavenly_stem = heavenly_stems[(year_diff % 10)]
    earthly_branch = earthly_branches[(year_diff % 12)]

    # Community-Wirkung hinzufügen
    community_impact = {
        ("Yang Holz", "Ratte"): "Holz - Deine Energie ist kreativ, impulsiv und voller Inspiration. Du erinnerst andere daran, dass der Weg zur Selbstverwirklichung mit Mut und der Bereitschaft beginnt, neue Wege zu gehen und sich auf das Unbekannte einzulassen.",
        ("Yin Holz", "Ochse"): "Holz - Du bist geduldig, entwickelst dich langsam, aber stetig und lässt dich nicht entmutigen. Deine Reise zeigt, wie wertvoll es ist, in die eigene Tiefe zu gehen und sich Zeit für den wahren inneren Wandel zu nehmen.",
        ("Yang Feuer", "Tiger"): "Feuer - Du bist leidenschaftlich, abenteuerlustig und sprühst vor Energie. Deine Abenteuerlust ermutigt andere, ihr Herz zu öffnen und sich von der Lebensenergie zu leiten, um das zu finden, was sie wirklich erfüllt.",
        ("Yin Feuer", "Hase"): "Feuer - Du bist sanft, aber auch zielstrebig und weißt genau, wohin du willst. Deine Fähigkeit, mit innerer Ruhe und klarer Intuition zu handeln, zeigt anderen, wie sie ihren eigenen inneren Kompass finden und ihm folgen können.",
        ("Yang Erde", "Drache"): "Erde - Du bist stark, ein natürlicher Führer und gibst anderen Orientierung. Deine Präsenz als Fels in der Brandung ermutigt andere, ihre innere Stärke zu erkennen und Verantwortung für ihr eigenes Leben zu übernehmen.",
        ("Yin Erde", "Schlange"): "Erde - Du bist weise, geheimnisvoll und ein brillanter Planer. Deine Fähigkeit, aus der Stille heraus strategisch zu denken, zeigt anderen, wie wichtig es ist, Geduld zu üben und den richtigen Moment für Entscheidungen zu finden.",
        ("Yang Metall", "Pferd"): "Metall - Du bist entschlossen, direkt und voller Tatendrang. Deine klare Vision und Zielstrebigkeit sind ein kraftvolles Beispiel dafür, wie man die eigenen Ziele nicht nur visualisiert, sondern mit Entschlossenheit verwirklicht.",
        ("Yin Metall", "Ziege"): "Metall - Du bist sorgfältig, achtest auf Details und schätzt Schönheit. Deine Wertschätzung für das Feinste im Leben hilft anderen, mehr auf das zu achten, was wirklich zählt – in sich selbst und in der Welt um sie herum.",
        ("Yang Wasser", "Affe"): "Wasser - Du bist anpassungsfähig, intelligent und meisterst jede Situation. Deine Fähigkeit, auf Veränderungen flexibel zu reagieren, erinnert andere daran, dass wahre Stärke im Loslassen und Anpassen an die Strömungen des Lebens liegt.",
        ("Yin Wasser", "Hahn"): "Wasser - Du bist ruhig, nachdenklich und vertraust auf deine Intuition. Deine Intuition ist wie ein inneres Licht, das dir den Weg weist. Du zeigst anderen, wie sie ihr eigenes inneres Wissen entdecken und ihm vertrauen können.",
        ("Yang Holz", "Hund"): "Holz - Du bist loyal, unterstützend und ein verlässlicher Begleiter. Deine bedingungslose Unterstützung zeigt anderen, wie wichtig es ist, in schwierigen Zeiten zusammenzuhalten und einander zu stärken.",
        ("Yin Holz", "Schwein"): "Holz - Du bist großzügig, mitfühlend und bringst Liebe in die Welt. Deine Fähigkeit, Liebe und Mitgefühl zu teilen, lässt andere erkennen, wie wahre Erfüllung aus dem Geben kommt und wie sie ihr Herz öffnen können.",
        ("Yang Feuer", "Drache"): "Feuer - Du bist charismatisch, energisch und ziehst Menschen mit deiner Präsenz an. Deine Energie und Ausstrahlung erinnern andere daran, dass ihre eigene innere Leuchtkraft das ist, was die Welt braucht.",
        ("Yin Feuer", "Schlange"): "Feuer - Du bist kreativ, strategisch und gehst mit Bedacht vor. Deine Fähigkeit, sowohl kreativ als auch weise zu handeln, zeigt anderen, dass es nicht nur um Visionen geht, sondern auch um die Geduld, diese in die Realität umzusetzen.",
        ("Yang Erde", "Affe"): "Erde - Du bist praktisch, durchsetzungsfähig und hast immer einen klaren Plan. Deine Bodenständigkeit ist ein Anker für andere, die lernen wollen, wie man mit Klarheit und Strategie die Herausforderungen des Lebens meistert.",
        ("Yin Erde", "Hahn"): "Erde - Du bist fleißig, detailorientiert und bringst alles zur Perfektion. Deine Liebe zum Detail inspiriert andere, ihren eigenen Standard zu setzen und ihre Projekte mit Hingabe und Präzision zu vollenden.",
        ("Yang Metall", "Schwein"): "Metall - Du bist stark, entschlossen und gehst deine Ziele konsequent an. Deine Kraft und Zielstrebigkeit sind ein Beispiel dafür, wie man mit Entschlossenheit und innerer Klarheit seine Ziele erreicht.",
        ("Yin Metall", "Tiger"): "Metall - Du bist fokussiert, zielsicher und erreichst alles, was du dir vornimmst. Deine Fähigkeit, mit Konzentration und Präzision zu handeln, zeigt anderen, wie sie ihre eigenen Stärken nutzen können, um ihre Träume zu verwirklichen.",
        ("Yang Wasser", "Ziege"): "Wasser - Du bist intuitiv, anpassungsfähig und lässt dich von deinem inneren Wissen leiten. Deine Fähigkeit, auf dein tiefes inneres Wissen zu hören, zeigt anderen, wie sie Vertrauen in ihre eigene Intuition aufbauen können.",
        ("Yin Wasser", "Pferd"): "Wasser - Du bist ruhig, künstlerisch begabt und lässt deiner Kreativität freien Lauf. Deine Kunst, aus der Ruhe heraus zu erschaffen, erinnert andere daran, dass wahre Kreativität aus der Stille und dem Fluss des Lebens kommt.",
        ("Yang Feuer", "Affe"): "Feuer - Du bist abenteuerlustig, enthusiastisch und voller Energie. Deine Lebensfreude ist ein lebendiges Beispiel dafür, wie man das Leben mit Begeisterung und Mut annehmen kann, während du gleichzeitig andere inspirierst, ihren eigenen Weg zu gehen.",
        # Hinzugefügte Kombination für Yin Wasser, Ochse
        ("Yin Wasser", "Ochse"): "Wasser - Du bist ruhig, nachdenklich und vertraust auf deine Intuition. Deine Intuition ist wie ein inneres Licht, das dir den Weg weist. Du zeigst anderen, wie sie ihr eigenes inneres Wissen entdecken und ihm vertrauen können."
    }

    # Rückgabe der Ergebnisse
    return heavenly_stem, earthly_branch, community_impact.get((heavenly_stem, earthly_branch), "Keine Beschreibung verfügbar.")

async def handle_birthday(update, context):
    birth_date = update.message.text
    print(f"Empfangenes Geburtsdatum: {birth_date}")  # Debug-Ausgabe
    await update.message.reply_text(f"Geburtsdatum erhalten: {birth_date}. Jetzt wird dein Bazi Jahr gelesen...")

    # Berechnung des chinesischen Jahres
    chinese_year = convert_to_chinese_year(birth_date)
    if not chinese_year:
        await update.message.reply_text("Das Datum ist ungültig. Bitte stelle sicher, dass es im Format 'TT.MM.JJJJ, HH:MM' ist.")
        return

    heavenly_stem, earthly_branch, description = get_chinese_elements(chinese_year)
    
    # Ausgabe der chinesischen Jahr-Kombination und der Community-Wirkung
    await update.message.reply_text(f"Das Jahr {chinese_year} im chinesischen Kalender ist: {heavenly_stem} {earthly_branch}. {description}")

# Anwendung erstellen
app = Application.builder().token(TOKEN).build()

# Handler hinzufügen
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_birthday))

# Bot starten
if __name__ == "__main__":
    print("Bot läuft...")  # Debug-Ausgabe
    app.run_polling(poll_interval=2, allowed_updates=["message"])
