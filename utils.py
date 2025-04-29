players_scores = {}
registered_players = []

def get_total_players():
    return len(players_scores)

def get_top_3_scores():
    if not players_scores:
        return ["- kosong -", "- kosong -", "- kosong -"]
    sorted_players = sorted(players_scores.items(), key=lambda item: item[1], reverse=True)
    return [f"{p[0]} - {p[1]} pts" for p in sorted_players[:3]]

def reset_scores():
    global players_scores
    players_scores = {}

def reset_players():
    global registered_players
    registered_players = []

def save_player(player):
    if player not in registered_players:
        registered_players.append(player)
        players_scores[player] = 0  # Score mula kosong
