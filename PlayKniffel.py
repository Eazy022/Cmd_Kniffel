import random
import sqlite3
import hashlib

# ---------------- DATABASE & LOGIN ----------------
def init_db():
    conn = sqlite3.connect('kniffel_users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def register(username, password):
    conn = sqlite3.connect('kniffel_users.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login(username, password):
    conn = sqlite3.connect('kniffel_users.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
    result = c.fetchone()
    conn.close()
    return result is not None

def login_screen():
    init_db()
    print("=== KNiffel LOGIN ===")
    while True:
        choice = input("1=Login, 2=Registrieren (q=beenden): ")
        if choice.lower() == 'q': return None
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            if login(username, password):
                print(f"✅ Willkommen {username}!")
                return username
            else:
                print("❌ Falsche Daten!")
        elif choice == '2':
            username = input("Neuer Username: ")
            password = input("Neues Password: ")
            if register(username, password):
                print("✅ Registriert!")
            else:
                print("❌ Username existiert bereits!")

# ---------------- WÜRFEL ----------------
def roll_dice(num_dice=5):
    return [random.randint(1, 6) for _ in range(num_dice)]

# ---------------- SCORING ----------------
def pips_sum(pips, dice):
    return sum(d for d in dice if d == pips)

def group_sizes(dice):
    return [dice.count(p) for p in set(dice)]

def three_of_a_kind(dice):
    if any(g >= 3 for g in group_sizes(dice)): return sum(dice)
    return 0

def four_of_a_kind(dice):
    if any(g >= 4 for g in group_sizes(dice)): return sum(dice)
    return 0

def full_house(dice):
    if sorted(group_sizes(dice)) == [2, 3]: return 25
    return 0

def small_straight(dice):
    s = set(dice)
    if {1,2,3,4}.issubset(s) or {2,3,4,5}.issubset(s) or {3,4,5,6}.issubset(s):
        return 30
    return 0

def large_straight(dice):
    s = set(dice)
    if s == {1,2,3,4,5} or s == {2,3,4,5,6}: return 40
    return 0

def kniffel(dice):
    if len(set(dice)) == 1: return 50
    return 0

def chance(dice):
    return sum(dice)

# ---------------- SPIELSTAND ----------------
CATEGORIES = [
    "Einser", "Zweier", "Dreier", "Vierer", "Fünfer", "Sechser",
    "Dreierpasch", "Viererpasch", "Full House", "Kleine Straße", 
    "Große Straße", "Kniffel", "Chance"
]

def create_empty_scoreboard():
    return {cat: None for cat in CATEGORIES}

def total_score(scoreboard):
    return sum(v for v in scoreboard.values() if v is not None)

# ---------------- TABELLE ANZEIGEN ----------------
def show_player_table(player_name, scores):
    print(f"\n📋 Tabelle von {player_name}:")
    print("🎯 OBERER BLOCK:")
    for cat in CATEGORIES[:6]:
        val = scores[player_name][cat]
        print(f"  {cat:<12}: {val or '---'}")
    
    print("\n🔥 UNTERER BLOCK:")
    for cat in CATEGORIES[6:]:
        val = scores[player_name][cat]
        print(f"  {cat:<12}: {val or '---'}")
    
    print(f"\n📊 Gesamt: {total_score(scores[player_name])} Punkte")

# ---------------- KATEGORIE WÄHLEN ----------------
def choose_category_and_score(player, dice, scores):
    print(f"\n{player} ist dran.")
    print("🎲 Endgültige Würfel:", dice)
    print("📋 Kategorien:")
    
    for cat in CATEGORIES:
        val = scores[player][cat]
        status = "frei" if val is None else f"belegt ({val})"
        print(f"  {cat:<12}: {status}")
    
    while True:
        cat = input("\nWelche Kategorie? (q=Abbruch): ").strip()
        if cat.lower() == 'q': return False
        if cat not in CATEGORIES:
            print("❌ Unbekannte Kategorie!")
            continue
        if scores[player][cat] is not None:
            print("❌ Kategorie bereits belegt!")
            continue
        break
    
    # Punkte berechnen
    if cat == "Einser": points = pips_sum(1, dice)
    elif cat == "Zweier": points = pips_sum(2, dice)
    elif cat == "Dreier": points = pips_sum(3, dice)
    elif cat == "Vierer": points = pips_sum(4, dice)
    elif cat == "Fünfer": points = pips_sum(5, dice)
    elif cat == "Sechser": points = pips_sum(6, dice)
    elif cat == "Dreierpasch": points = three_of_a_kind(dice)
    elif cat == "Viererpasch": points = four_of_a_kind(dice)
    elif cat == "Full House": points = full_house(dice)
    elif cat == "Kleine Straße": points = small_straight(dice)
    elif cat == "Große Straße": points = large_straight(dice)
    elif cat == "Kniffel": points = kniffel(dice)
    elif cat == "Chance": points = chance(dice)
    else: points = 0
    
    scores[player][cat] = points
    print(f"✅ {cat} für {player}: {points} Punkte eingetragen!")
    return True

# ---------------- SICHERHEITSABFRAGE ----------------
def safe_exit(scores, players):
    print("\n⚠️  SICHERHEITSABFRAGE")
    confirm = input("Wirklich beenden? (j/n): ")
    if confirm.lower() == 'j':
        print("\n=== ZWISCHENSTAND ===")
        for p in players:
            print(f"  {p['name']:<12}: {total_score(scores[p['name']])} Punkte")
        return True
    return False

# ---------------- BEGRÜSSUNGSMENÜ ----------------
def welcome_menu():
    print("\n🎲" + "="*50 + "🎲")
    print("     WILLKOMMEN ZU KNiffel!")
    print("🎲" + "="*50 + "🎲")
    
    num_players = int(input("Anzahl Spieler (2-4): "))
    if num_players < 2 or num_players > 4:
        print("❌ Nur 2-4 Spieler möglich!")
        return None
    
    players = []
    for i in range(num_players):
        name = input(f"\nSpieler {i+1} Name: ").strip()
        if not name: name = f"Spieler {i+1}"
        players.append({"name": name})
    
    # Login für jeden Spieler
    logged_players = []
    for player in players:
        print(f"\n🔐 {player['name']} bitte einloggen:")
        username = login_screen()
        if username:
            player['username'] = username
            logged_players.append(player)
        else:
            print("❌ Login fehlgeschlagen!")
            return None
    
    if input("\n🚀 Spiel starten? (j/n): ").lower() == 'j':
        return logged_players
    return None

# ---------------- HAUPTSPIEL ----------------
def play_game_complete(players):
    scores = {p['name']: create_empty_scoreboard() for p in players}
    
    try:
        print("\n🎮 SPIEL GESTARTET! (Strg+C zum Beenden)")
        
        while True:
            # Prüfen ob alle Felder gefüllt
            all_filled = all(
                all(v is not None for v in board.values()) 
                for board in scores.values()
            )
            if all_filled:
                break
            
            for player_data in players:
                player = player_data['name']
                
                print(f"\n{'='*60}")
                print(f"🎯 {player} - NEUE RUNDE")
                print(f"{'='*60}")
                
                # Tabelle anzeigen?
                if input("Tabelle anzeigen? (t): ").lower() == 't':
                    show_player_table(player, scores)
                
                # 🎲 FIX: GENAU 3 WÜRFE
                dice = roll_dice()
                rolls_left = 2  # 1. Wurf gemacht, 2 weitere möglich
                
                while rolls_left > 0:
                    print(f"\n🎲 Würfel {3-rolls_left}/3: {dice}")
                    reroll_input = input("Positionen neu würfeln (1-5) oder Enter: ").strip()
                    
                    if not reroll_input:  # Enter = beenden
                        break
                    if reroll_input.lower() == 'q':
                        if safe_exit(scores, players): 
                            return
                        break
                    
                    # 🎲 FIX: Genau die richtige Anzahl neu würfeln
                    try:
                        indices = [int(x)-1 for x in reroll_input.split() if x.isdigit()]
                        indices = [i for i in indices if 0 <= i < 5]  # Validierung
                        
                        # Nur die ausgewählten Positionen neu würfeln
                        for i in indices:
                            dice[i] = random.randint(1, 6)
                            
                        rolls_left -= 1
                        print(f"🎲 Neuer Wurf: {dice}")
                        
                    except:
                        print("❌ Ungültige Eingabe! (z.B. '1 3' für Position 1+3)")
                
                print(f"\n🎲 Endgültig: {dice}")
                
                # Kategorie wählen
                if not choose_category_and_score(player, dice, scores):
                    if safe_exit(scores, players): 
                        return
        
        # Ranking
        final_scores = [(p['name'], total_score(scores[p['name']])) for p in players]
        final_scores.sort(key=lambda x: x[1], reverse=True)
        
        print("\n🏆 FINALER RANKING 🏆")
        for i, (name, score) in enumerate(final_scores, 1):
            medal = "🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else "🏅"
            print(f"{medal} {i}. {name}: {score} Punkte")
                
    except KeyboardInterrupt:
        safe_exit(scores, players)

    except KeyboardInterrupt:
        print("\n\n⚠️  Spiel unterbrochen!")
        if safe_exit(scores, players):
            return


# ---------------- START ----------------
if __name__ == "__main__":
    print("🎲 KNiffel startet!")
    players = welcome_menu()
    if players:
        play_game_complete(players)
    else:
        print("👋 Spiel abgebrochen!")