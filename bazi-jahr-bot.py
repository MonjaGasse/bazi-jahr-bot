from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from datetime import datetime
import sys
import traceback
import os
import asyncio
from telegram.constants import ParseMode

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def log_exception(exc_type, exc_value, exc_tb):
    print(f"Fehler aufgetreten: {exc_type}, {exc_value}")
    traceback.print_tb(exc_tb)

sys.excepthook = log_exception

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Start-Befehl empfangen!")
    await update.message.reply_text(
        "🌕✨ <i>Herzlich Willkommen.</i>\n\n" "<b>Sende mir dein Geburtsdatum</b> im Format <code>TT.MM.JJJJ, HH:MM</code>\n"  "(z.B. <code>09.12.1982, 14:50</code>)\n\n""🔮 <i>Ich werde für dich in die Bazi-Welt blicken...</i>",
        parse_mode=ParseMode.HTML
    )

def convert_to_chinese_year(gregorian_date_str):
    try:
        gregorian_date = datetime.strptime(gregorian_date_str, "%d.%m.%Y, %H:%M")
        print(f"Umgewandeltes Datum: {gregorian_date}")
        return gregorian_date.year
    except ValueError:
        print("Ungültiges Datumsformat!")
        return None

def get_chinese_elements(year):
    heavenly_stems = ["Yang Holz", "Yin Holz", "Yang Feuer", "Yin Feuer", "Yang Erde", "Yin Erde", "Yang Metall", "Yin Metall", "Yang Wasser", "Yin Wasser"]
    earthly_branches = ["Ratte", "Ochse", "Tiger", "Hase", "Drache", "Schlange", "Pferd", "Ziege", "Affe", "Hahn", "Hund", "Schwein"]

    year_diff = year - 1924
    heavenly_stem = heavenly_stems[year_diff % 10]
    earthly_branch = earthly_branches[year_diff % 12]

    community_impact = {
("Yang Metall", "Tiger"): "Metall - Der Metall-Tiger ist selbstbewusst, wettbewerbsorientiert und unabhängig. Er ist ehrgeizig, aber neigt zu Ungeduld, wenn seine Erwartungen nicht erfüllt werden. Mit viel Energie verfolgt er seine Ziele, zeigt jedoch wenig Flexibilität und akzeptiert selten andere Standpunkte. Er fokussiert sich stark auf seine eigenen Interessen.",
("Yang Wasser", "Tiger"): "Wasser - Der Wasser-Tiger ist intelligent, einfühlsam und ein ausgezeichneter Kommunikator. Er ist in allem, was mit Menschen zu tun hat, erfolgreich und kann andere leicht für sich gewinnen. Beharrlich in seinen Zielen, sollte er jedoch vorsichtig bei Entscheidungen sein und stets auf Intelligenz und Beobachtung setzen.",
("Yang Holz", "Tiger"): "Holz - Der Holz-Tiger ist praktisch, besonnen und ein guter Vermittler. Er ist kreativ, sozial und bringt positive Veränderungen in seiner Umgebung. Als loyaler Freund hilft er Schwächeren und sucht das Beste in den Menschen. Er muss jedoch an seiner Disziplin arbeiten, um Projekte erfolgreich abzuschließen.",
("Yang Feuer", "Tiger"): "Feuer - Der Feuer-Tiger ist energiegeladen, unabhängig und entschlossen. Er stellt sich jeder Herausforderung und lässt sich nie entmutigen. Mit starken Prinzipien und einer schnellen Reaktion erreicht er seine Ziele und kämpft für Gerechtigkeit.",
("Yang Erde", "Tiger"): "Erde - Der Erd-Tiger ist selbstbewusst, intelligent und diszipliniert. Er trifft Entscheidungen basierend auf realistischer Analyse und hat die Fähigkeit, viel Wissen aufzunehmen. Er ist ein konventioneller Kämpfer, der den Underdog verteidigt und altruistisch ist, mit dem Wunsch, anderen zu helfen.",

("Yin Metall", "Hase"): "Metall - Der Metall-Hase ist intelligent, analytisch und hat einen ausgeprägten Sinn für Kunst und Musik. Er kann stur wirken und bevorzugt es, im Hintergrund zu bleiben, anstatt im Rampenlicht zu stehen. Trotz seiner Ruhe ist er schnell gelangweilt und lässt nicht leicht zu, was in ihm vorgeht.",
("Yin Wasser", "Hase"): "Wasser - Der Wasser-Hase ist friedliebend, sensibel und bevorzugt Einsamkeit, um seine Gedanken zu sammeln. Er ist sehr empathisch und freundlich, mit großen geistigen Fähigkeiten und Innovationskraft. Er vermeidet Disharmonie und hat eine starke innere Stärke.",
("Yin Holz", "Hase"): "Holz - Der Holz-Hase ist sanft, großzügig und intuitiv, vermeidet jedoch Konflikte. Er arbeitet gut im Team und ist zuverlässig. Er liebt es, neues Wissen zu sammeln und meistert viele Aufgaben gleichzeitig, ohne seine Stabilität zu verlieren.",
("Yin Feuer", "Hase"): "Feuer - Der Feuer-Hase ist kreativ, humorvoll und einnehmend. Er hat Führungsqualitäten, erkennt Stärken in anderen und ist ein guter Diplomat. Allerdings kann er aufgrund seiner hohen Ansprüche und Stimmungsschwankungen zu Perfektionismus neigen.",
("Yin Erde", "Hase"): "Erde - Der Erd-Hase ist der logischste und diplomatischste der Hasen. Er trifft Entscheidungen nach gründlicher Überlegung und ist stets zuverlässig. Obwohl er introvertiert ist, liebt er Abenteuer. Er neigt zu Materialismus und muss seine Finanzen im Blick behalten.",
("Yang Metall", "Drache"): "Metall - Der Metall-Drache ist willensstark, entschlossen und selbstbewusst. Er strebt nach großen Erfolgen, ist mutig und zieht Anhänger an. Er toleriert keine Faulheit und ist wenig diplomatisch, was dazu führt, dass er Widerspruch leicht ignoriert.",
    
    ("Yang Wasser", "Drache"): "Wasser - Der Wasser-Drache ist ruhig, gelassen und diplomatisch. Er kontrolliert seine Emotionen und verfolgt Ziele mit Geduld und Zusammenarbeit. Er ist fortschrittlich und glaubt, dass Niederlagen ihn stärker machen. Sein gemäßigtes Wesen lässt ihn das gesellschaftliche Leben genießen.",
    
    ("Yang Holz", "Drache"): "Holz - Der Holz-Drache ist furchtlos und neugierig, zieht Ruhm und Reichtum an und kümmert sich wenig um die Meinungen anderer. Er ist innovativ, aber kann überanalysieren. Mit einem großen Ego geht er stets auf sich selbst bedacht vor.",
    
    ("Yang Feuer", "Drache"): "Feuer - Der Feuer-Drache ist ehrgeizig, wettbewerbsfähig und intensiv. Er ist ein Perfektionist, ein großartiger Anführer, aber muss seine Energie und Temperament zügeln. Er sorgt sich um das Wohlergehen anderer und hilft oft in wohltätigen Bereichen.",
    
    ("Yang Erde", "Drache"): "Erde - Der Erde-Drache ist besonnen, fleißig und gesellig. Er schätzt langfristige Verpflichtungen und Selbstverbesserung. Mit gesundem Menschenverstand und Kreativität verfolgt er geduldig seine Ziele und kann leicht Reichtum und Vorteile für das Gemeinwohl schaffen.",

("Yin Metall", "Schlange"): "Metall - Die Metall-Schlange ist unabhängig und geheimnisvoll. Sie ist konkurrenzfähig, besitzergreifend und arbeitet lieber allein. Sie hat Schwierigkeiten, anderen zu vertrauen, zeigt aber Großzügigkeit gegenüber Auserwählten. Mit einer klaren Entschlossenheit strebt sie nach Erfolg und liebt schöne Dinge.",
    
    ("Yin Wasser", "Schlange"): "Wasser - Die Wasser-Schlange ist wissensdurstig und intelligent. Sie ist ruhig, flexibel und sehr erfolgreich, besonders in finanziellen Angelegenheiten. Ihre Geduld und Intuition ermöglichen es ihr, gut mit Menschen und Situationen umzugehen.",
    
    ("Yin Holz", "Schlange"): "Holz - Die Holz-Schlange ist freundlich, kreativ und eine begnadete Kommunikatorin. Sie liebt es, Wissen zu erlangen und zu teilen, und hat einen außergewöhnlichen Geschmack. Sie ist gesellig und hat viele Freunde.",
    
    ("Yin Feuer", "Schlange"): "Feuer - Die Feuer-Schlange ist intensiv, ehrgeizig und leidenschaftlich. Sie ist selbstbewusst, kontaktfreudig und äußerst charismatisch. Ihre Energie und Intuition machen sie zu einer natürlichen Führungspersönlichkeit, aber sie muss aufpassen, nicht zu dominant zu sein.",
    
    ("Yin Erde", "Schlange"): "Erde - Die Erde-Schlange ist vernünftig, bodenständig und besonnen. Sie trifft Entscheidungen basierend auf genauen Beobachtungen und ist disziplinierter als andere Schlangen. Ihre charmante und aufrichtige Art macht sie bei vielen beliebt.",

("Yang Metall", "Pferd"): "Metall - Das Metall-Pferd ist hochaktiv, fähig und geschickt. Es blüht bei Herausforderungen auf und zeigt eine starke Unabhängigkeit. Jedoch ist es unnachgiebig und hat Schwierigkeiten, sich langfristigen Zielen oder Beziehungen zu verpflichten. Es reagiert negativ auf Einschränkungen oder Eingriffe in seine Freiheit.",
    
    ("Yang Wasser", "Pferd"): "Wasser - Das Wasser-Pferd ist freundlich, vielseitig und sehr anpassungsfähig. Es ist bei allen beliebt und hat große zwischenmenschliche Fähigkeiten. Obwohl es leicht ablenkbar ist und seine Meinung oft ändert, kann es sich schnell an neue Situationen anpassen.",
    
    ("Yang Holz", "Pferd"): "Holz - Das Holz-Pferd ist großzügig, fleißig und kontaktfreudig. Es ist das bodenständigste der Pferde und der beste Multitasker. Diszipliniert und fortschrittlich, ist es bereit, neue Ideen zu übernehmen und Kompromisse einzugehen, aber bevorzugt, die Führung zu übernehmen.",
    
    ("Yang Feuer", "Pferd"): "Feuer - Das Feuer-Pferd ist mutig, wettbewerbsorientiert und ein Draufgänger. Es reagiert schnell und geschickt auf Situationen, doch seine Unberechenbarkeit und Unkonzentriertheit können Probleme verursachen. Es muss sein explosives Temperament kontrollieren, um nicht zu schaden.",
    
    ("Yang Erde", "Pferd"): "Erde - Das Erde-Pferd ist das glücklichste und beliebteste Pferd. Es ist beständig und wägt Situationen gut ab, was es jedoch manchmal unentschlossen macht. Es hält sich an einen starken Moralkodex, hört auf Ratschläge und bringt positive Energie in seine Aufgaben.",

("Yin Metall", "Ziege"): "Metall - Die Metall-Ziege ist selbstbewusst, moralisch und verantwortungsbewusst. Sie ist jedoch sehr sensibel und kann durch negatives Feedback entmutigt oder depressiv werden. Sie liebt Schönheit und sucht nach Trost im Vertrauten, meidet Veränderungen und Überraschungen.",
    
    ("Yin Wasser", "Ziege"): "Wasser - Die Wasser-Ziege ist kreativ und beliebt, besonders in Musik und Kunst. Sie ist ruhig, loyal und bevorzugt ein stabiles Umfeld, um nicht von Herausforderungen überwältigt zu werden. Sie kann jedoch leicht von anderen beeinflusst werden und hat Schwierigkeiten, ihre Komfortzone zu verlassen.",
    
    ("Yin Holz", "Ziege"): "Holz - Die Holz-Ziege ist die fürsorglichste und stabilste der Ziegen, mit einem natürlichen Drang, das Leben der anderen zu verbessern. Sie ist sensibel und sucht Anerkennung, hat jedoch Schwierigkeiten, sich durchzusetzen und lässt sich von anderen ausnutzen.",
    
    ("Yin Feuer", "Ziege"): "Feuer - Die Feuer-Ziege ist selbstbewusst, aber egozentrisch und kann die Gefühle anderer ignorieren. Sie ist intuitiv, aber manchmal unvernünftig und dramatisch. Ihre Liebe zu schönen Dingen und Komfort kann ihre kreative Energie anregen oder sie kindisch wirken lassen.",
    
    ("Yin Erde", "Ziege"): "Erde - Erd-Ziegen sind ehrlich, loyal und bereit, jedes Opfer für ihre Familie und Freunde zu bringen. Sie arbeiten gut unter Druck und sind unabhängig sowie vorsichtig, besonders bei Finanzen. Sie sind die konservativsten Ziegen, die Verantwortung übernehmen und weniger von anderen beeinflusst werden.",

("Yang Metall", "Affe"): "Metall - Der Metall-Affe ist scharfsinnig, selbstbewusst und unternehmerisch. Mit großem Ehrgeiz und hoher Kreativität erreicht er Erfolg. Er ist unabhängig und entschlossen, aber auch überdramatisch und kann leicht frustriert werden. Er ist überzeugend und hat große Ambitionen.",
    
    ("Yang Wasser", "Affe"): "Wasser - Der Wasser-Affe liebt es, im Rampenlicht zu stehen, und ist ein genialer Kommunikator. Er ist tolerant, originell und kommt gut mit Menschen aus. Fröhlich und lebenslustig, hat er ein hohes Bedürfnis nach Abwechslung und eine geheimnisvolle Natur. Er kann leicht verletzt werden und leidet manchmal unter Orientierungslosigkeit.",
    
    ("Yang Holz", "Affe"): "Holz - Der Holz-Affe ist mitfühlend, verantwortungsbewusst und arbeitet hart. Er ist ein Pionier und liebt es, sich neuen Herausforderungen zu stellen. Begeistert und gesellig, hat er oft Schwierigkeiten, langsamer zu werden und sich zu mäßigen.",
    
    ("Yang Feuer", "Affe"): "Feuer - Der Feuer-Affe ist abenteuerlustig, optimistisch und ein geborener Anführer. Er ist kreativ, wettbewerbsfähig und entschlossen. Seine vielen Interessen und Energie machen ihn zu einem außergewöhnlichen Problemlöser. Allerdings ist er auch reizbar und kann misstrauisch und eifersüchtig sein.",
    
    ("Yang Erde", "Affe"): "Erde - Der Erde-Affe ist optimistisch, furchtlos und vernünftig. Er ist der realistischste und pflichtbewussteste Affe, neigt jedoch dazu, isolierter zu sein. Er ist intellektuell, fleißig und hat ein gutes Gespür für Finanzen. Ruhiger und gelassener als andere, ist er zuverlässig und wohltätig.",

("Yin Metall", "Hahn"): "Metall - Der Metall-Hahn ist sehr fleißig und entschlossen, seine Ziele zu erreichen. Mit Leidenschaft, Tatendrang und hohen Idealen setzt er sich für sinnvolle Veränderungen ein. Charismatisch und fokussiert, zieht er Menschen an und ist ein Vorkämpfer für sozialen Wandel.",
    
    ("Yin Wasser", "Hahn"): "Wasser - Der Wasser-Hahn ist ein guter Kommunikator und kann sich leicht an Veränderungen anpassen. Besonnen und einfallsreich, ist er in Bereichen, die Kommunikation erfordern, sehr erfolgreich. Mit einem guten Auge für Details und Akribie kann er sich in systematischen Aufgaben auszeichnen.",
    
    ("Yin Holz", "Hahn"): "Holz - Der Holz-Hahn ist ein guter Teamplayer, kooperativ und gesellig. Er setzt hohe Standards und erwartet viel von anderen. Er ist bodenständig und arbeitet hart an sozialer Gerechtigkeit und Gleichheit. Ehrlich und direkt, hat er ein gutes Gespür für das Wohlergehen anderer.",
    
    ("Yin Feuer", "Hahn"): "Feuer - Der Feuer-Hahn ist dynamisch und ein geborener Anführer mit großem Charisma. Unabhängig und organisiert, kann er sich in Details verlieren und überkritisch sein. Er ist der effektivste und effizienteste der Hähne, erledigt alles mit Flair und Erfolg.",
    
    ("Yin Erde", "Hahn"): "Erde - Der Erde-Hahn ist der praktischste und ordentlichste der Hähne. Er trägt viel Verantwortung und setzt hohe Maßstäbe. Fleißig und detailliert, trifft er die vernünftigsten Entscheidungen und bewältigt mehrere Aufgaben gleichzeitig.",

 ("Yang Metall", "Hund"): "Metall - Der Metall-Hund ist loyal, direkt und ethisch. Er gibt alles für seine Freunde und verfolgt hartnäckig seine Ziele. Altruistisch und konservativ, neigt er dazu, selbstgerecht zu sein, und bleibt jemandem feindlich gesinnt, wenn er sich verraten fühlt.",
    
    ("Yang Wasser", "Hund"): "Wasser - Der Wasser-Hund ist offen, freundlich und anpassungsfähig. Er baut gute Beziehungen auf und ist sensibel für die Gefühle anderer. Seine Hilfsbereitschaft bringt ihm viele Freunde, aber er sollte vorsichtig sein, dass seine Güte nicht ausgenutzt wird.",
    
    ("Yang Holz", "Hund"): "Holz - Der Holz-Hund ist altruistisch, zuverlässig und stabil. Mit einer großen Arbeitskapazität und klaren Gedanken trifft er immer die richtigen Entscheidungen. Er ist moralisch stark und immer bereit, andere zu verteidigen – der Held, auf den man sich verlassen kann.",
    
    ("Yang Feuer", "Hund"): "Feuer - Der Feuer-Hund liebt Abenteuer und Herausforderungen. Er ist leidenschaftlich, willensstark und unabhängig. Sein Charme und seine Freundlichkeit bringen ihm viele Bewunderer, aber er setzt seine Ideale auch entschlossen durch.",
    
    ("Yang Erde", "Hund"): "Erde - Der Erde-Hund ist vorsichtig, praktisch und fleißig. Er ist direkt und ehrlich, manchmal überkritisch, aber immer zuverlässig. Ein Realist, der emotionslos plant und seine Entscheidungen weise trifft, dabei die Talente anderer optimal nutzt.",


("Yin Metall", "Schwein"): "Metall - Das Metall-Schwein ist leidenschaftlich, ehrlich und direkt. Es ist äußerst gesellig, fleißig und großzügig. Es kämpft für seine Überzeugungen und erledigt Aufgaben mit Ausdauer. Es neigt dazu, emotional statt logisch zu handeln und wird ein erbitterter Gegner, wenn es provoziert wird.",
    
    ("Yin Wasser", "Schwein"): "Wasser - Das Wasser-Schwein ist gesellig, diplomatisch und ausdrucksstark. Es beeinflusst andere positiv, kann jedoch leicht ausgenutzt werden. Es glaubt an das Gute in den Menschen und ist stets offen und ehrlich. Es muss jedoch seine Ausgaben im Griff haben, um nicht in finanzielle Schwierigkeiten zu geraten.",
    
    ("Yin Holz", "Schwein"): "Holz - Das Holz-Schwein hat ein großes Herz und ist äußerst mitfühlend. Es ist praktisch, fleißig und ehrgeizig. Es schafft Vertrauen und bittet um Hilfe durch seine leidenschaftliche Persönlichkeit. Es ist immer bereit, anderen zu dienen und schafft Wohlwollen, wo auch immer es geht.",
    
    ("Yin Feuer", "Schwein"): "Feuer - Das Feuer-Schwein ist aktiv, kontaktfreudig und leidenschaftlich. Es ist mutig, selbstbewusst und bereit, Risiken einzugehen. Es arbeitet hart für seine Familie und hilft großzügig anderen. Es kann jedoch emotional werden und hat Schwierigkeiten mit Enttäuschungen oder Misserfolgen.",
    
    ("Yin Erde", "Schwein"): "Erde - Das Erde-Schwein ist organisiert, pragmatisch und friedliebend. Es hat ein starkes Durchhaltevermögen und erreicht seine Ziele mit Entschlossenheit. Es ist motiviert, Verantwortung zu übernehmen und sorgt für Harmonie, wo immer es geht.",

("Yin Metall", "Ochse"): "Metall - Der Metall-Ochse ist unnachgiebig und äußerst fleißig. Er ist entschlossen, seine Ziele zu erreichen, jedoch wenig flexibel und manchmal starr in seinen Überzeugungen. Seine unermüdliche Energie hilft ihm, Großes zu erreichen, doch seine Sturheit kann ihm Probleme mit anderen Menschen bringen.",
    
    ("Yin Wasser", "Ochse"): "Wasser - Der Wasser-Ochse ist der unkomplizierteste und geduldigste der Ochsen. Er ist systematisch und logisch, zeigt jedoch eine größere Offenheit für neue Ideen, wenn sie gut erklärt werden. Seine Geduld hilft ihm, Hindernisse zu überwinden und wird ihn bei der Akzeptanz verschiedener Standpunkte unterstützen.",
    
    ("Yin Holz", "Ochse"): "Holz - Der Holz-Ochse ist aufgeschlossen gegenüber Veränderungen und neuen Ideen. Er respektiert die Meinungen anderer und ist sozial kompetent. Trotz seiner konservativen Haltung ist er flexibler und kooperativer als die anderen Ochsen. Er muss jedoch aufpassen, dass er nicht zu unverblümt ist.",
    
    ("Yin Feuer", "Ochse"): "Feuer - Der Feuer-Ochse ist aggressiv, stolz und loyal. Er ist kompromisslos und hat viel Integrität, kann aber auch herrschsüchtig und gefühllos erscheinen, wenn er auf seine Ziele fokussiert ist. Er muss darauf achten, dass seine Sturheit nicht in Arroganz umschlägt und er seine Grenzen überschätzt.",
    
    ("Yin Erde", "Ochse"): "Erde - Der Erde-Ochse ist der zuverlässigste und beständigste der Ochsen. Er ist praktisch, loyal und fleißig und verpflichtet sich nur zu dem, was er auch erfüllen kann. Er ist gut darin, Sicherheit zu schaffen und arbeitet unermüdlich, um seine Ziele zu erreichen, was ihm viele Freunde einbringt.",

 ("Yang Metall", "Ratte"): "Metall - Die Metall-Ratte liebt das Rampenlicht, kann aber hinter ihrer sorglosen Fassade von Emotionen wie Besitzgier und Eifersucht geplagt sein. Sie ist entschlossen, ihre Ziele zu erreichen, kann aber jähzornig und reizbar werden, wenn sie ihren Willen nicht bekommt.",
    
    ("Yang Wasser", "Ratte"): "Wasser - Die Wasser-Ratte ist vielseitig, anpassungsfähig und ein talentierter Kommunikator. Sie nutzt ihre Intuition und Empathie, um Probleme zu lösen und ihre Ziele zu erreichen. Sie ist sensibel und eher introvertiert, aber geschickt darin, andere zu beeinflussen und die Stärken anderer zu nutzen.",
    
    ("Yang Holz", "Ratte"): "Holz - Die Holz-Ratte ist neugierig, beliebt und sehr wissbegierig. Obwohl sie selbstbewusst erscheint, ist sie unsicher und besonders fleißig. Ihre Unsicherheiten können sie zu manipulativen Verhaltensweisen verleiten, um aus schwierigen Situationen herauszukommen.",
    
    ("Yang Feuer", "Ratte"): "Feuer - Die Feuer-Ratte ist ein Freigeist, der ständig nach neuen Abenteuern sucht. Sie ist unabhängig, widerstandsfähig gegenüber Vorschriften und neigt dazu, Verantwortung zu vermeiden. Sie ist wohltätig, großzügig und kann sich leicht in brenzlige Situationen bringen.",
    
    ("Yang Erde", "Ratte"): "Erde - Die Erde-Ratte ist bodenständig, pragmatisch und trifft vernünftige Entscheidungen. Sie ist risikoavers und bevorzugt sichere Wege, was ihr hilft, in Karrieren und Beziehungen erfolgreich zu sein. Sie ist charmant, beliebt und möchte respektiert werden.",



}
    

 

    description = community_impact.get((heavenly_stem, earthly_branch), "Keine Beschreibung verfügbar.")
    return heavenly_stem, earthly_branch, description

async def handle_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birth_date = update.message.text
    
    try:
        # Versuchen, das Geburtsdatum im Format DD.MM.JJJJ zu parsen
        parsed_date = datetime.datetime.strptime(birth_date, "%d.%m.%Y")
        print(f"Empfangenes Geburtsdatum: {parsed_date.strftime('%d.%m.%Y')}")
        
        # Kreative, lebendige Antwort mit Emojis
        await update.message.reply_text(
            f"🎉✨ **Geburtsdatum erhalten:** {parsed_date.strftime('%d.%m.%Y')}! ✨🎉\n\n"
            "🌟 Dein Bazi-Abenteuer beginnt jetzt! 🌟\n"
            "🔮 Lass uns deine **Jahressäule** entschlüsseln und die **magischen Geheimnisse** deines Lebens ergründen...\n"
            "🧘‍♀️ Schließe kurz deine Augen, atme tief ein und spüre, wie sich die Weisheit des Universums entfaltet! 🌌"
        )
    except ValueError:
        # Fehlerbehandlung mit einer freundlichen Nachricht
        await update.message.reply_text(
            "❌ Oh-oh! Das Geburtsdatum scheint nicht korrekt formatiert zu sein. 🙈\n"
            "Bitte gib dein Geburtsdatum im Format **DD.MM.JJJJ** ein, damit wir die Reise starten können. 🌱"
        )
        return

    heavenly_stem, earthly_branch, description = get_chinese_elements(chinese_year)
    print(f"Himmelsstamm: {heavenly_stem}, Erdzweig: {earthly_branch}, Beschreibung: {description}") # Debugging
    await update.message.reply_text(f"Das Jahr {chinese_year} im chinesischen Kalender ist: {heavenly_stem} {earthly_branch}. {description}")

# Bot-Setup
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_birthday))

# Bot starten
if __name__ == "__main__":
    print("Bot läuft...")  # Debug-Ausgabe
    app.run_polling(poll_interval=2, allowed_updates=["message"])