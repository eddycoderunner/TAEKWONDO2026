import math

def get_flag(nationality):
    flags = {
        'afghanistan': '🇦🇫', 'albania': '🇦🇱', 'algeria': '🇩🇿',
        'angola': '🇦🇴', 'argentina': '🇦🇷', 'australia': '🇦🇺',
        'austria': '🇦🇹', 'azerbaijan': '🇦🇿', 'bahrain': '🇧🇭',
        'bangladesh': '🇧🇩', 'belarus': '🇧🇾', 'belgium': '🇧🇪',
        'benin': '🇧🇯', 'bolivia': '🇧🇴', 'bosnia': '🇧🇦',
        'botswana': '🇧🇼', 'brazil': '🇧🇷', 'bulgaria': '🇧🇬',
        'burkina faso': '🇧🇫', 'burundi': '🇧🇮', 'cambodia': '🇰🇭',
        'cameroon': '🇨🇲', 'canada': '🇨🇦', 'chad': '🇹🇩',
        'chile': '🇨🇱', 'china': '🇨🇳', 'colombia': '🇨🇴',
        'congo': '🇨🇬', 'croatia': '🇭🇷', 'cuba': '🇨🇺',
        'czech republic': '🇨🇿', 'denmark': '🇩🇰', 'djibouti': '🇩🇯',
        'dominican republic': '🇩🇴', 'dr congo': '🇨🇩', 'ecuador': '🇪🇨',
        'egypt': '🇪🇬', 'eritrea': '🇪🇷', 'estonia': '🇪🇪',
        'ethiopia': '🇪🇹', 'finland': '🇫🇮', 'france': '🇫🇷',
        'gabon': '🇬🇦', 'gambia': '🇬🇲', 'georgia': '🇬🇪',
        'germany': '🇩🇪', 'ghana': '🇬🇭', 'greece': '🇬🇷',
        'guatemala': '🇬🇹', 'guinea': '🇬🇳', 'haiti': '🇭🇹',
        'honduras': '🇭🇳', 'hungary': '🇭🇺', 'india': '🇮🇳',
        'indonesia': '🇮🇩', 'iran': '🇮🇷', 'iraq': '🇮🇶',
        'ireland': '🇮🇪', 'israel': '🇮🇱', 'italy': '🇮🇹',
        'ivory coast': '🇨🇮', 'jamaica': '🇯🇲', 'japan': '🇯🇵',
        'jordan': '🇯🇴', 'kazakhstan': '🇰🇿', 'kenya': '🇰🇪',
        'korea': '🇰🇷', 'south korea': '🇰🇷', 'north korea': '🇰🇵',
        'kuwait': '🇰🇼', 'kyrgyzstan': '🇰🇬', 'laos': '🇱🇦',
        'latvia': '🇱🇻', 'lebanon': '🇱🇧', 'lesotho': '🇱🇸',
        'liberia': '🇱🇷', 'libya': '🇱🇾', 'lithuania': '🇱🇹',
        'madagascar': '🇲🇬', 'malawi': '🇲🇼', 'malaysia': '🇲🇾',
        'mali': '🇲🇱', 'mauritania': '🇲🇷', 'mauritius': '🇲🇺',
        'mexico': '🇲🇽', 'moldova': '🇲🇩', 'mongolia': '🇲🇳',
        'morocco': '🇲🇦', 'mozambique': '🇲🇿', 'myanmar': '🇲🇲',
        'namibia': '🇳🇦', 'nepal': '🇳🇵', 'netherlands': '🇳🇱',
        'new zealand': '🇳🇿', 'nicaragua': '🇳🇮', 'niger': '🇳🇪',
        'nigeria': '🇳🇬', 'norway': '🇳🇴', 'oman': '🇴🇲',
        'pakistan': '🇵🇰', 'palestine': '🇵🇸', 'panama': '🇵🇦',
        'paraguay': '🇵🇾', 'peru': '🇵🇪', 'philippines': '🇵🇭',
        'poland': '🇵🇱', 'portugal': '🇵🇹', 'qatar': '🇶🇦',
        'romania': '🇷🇴', 'russia': '🇷🇺', 'rwanda': '🇷🇼',
        'saudi arabia': '🇸🇦', 'senegal': '🇸🇳', 'serbia': '🇷🇸',
        'sierra leone': '🇸🇱', 'singapore': '🇸🇬', 'slovakia': '🇸🇰',
        'somalia': '🇸🇴', 'south africa': '🇿🇦', 'spain': '🇪🇸',
        'sri lanka': '🇱🇰', 'sudan': '🇸🇩', 'sweden': '🇸🇪',
        'switzerland': '🇨🇭', 'syria': '🇸🇾', 'taiwan': '🇹🇼',
        'tajikistan': '🇹🇯', 'tanzania': '🇹🇿', 'thailand': '🇹🇭',
        'togo': '🇹🇬', 'tunisia': '🇹🇳', 'turkey': '🇹🇷',
        'turkmenistan': '🇹🇲', 'uganda': '🇺🇬', 'ukraine': '🇺🇦',
        'united arab emirates': '🇦🇪', 'uae': '🇦🇪',
        'united kingdom': '🇬🇧', 'uk': '🇬🇧', 'great britain': '🇬🇧',
        'united states': '🇺🇸', 'usa': '🇺🇸', 'america': '🇺🇸',
        'uruguay': '🇺🇾', 'uzbekistan': '🇺🇿', 'venezuela': '🇻🇪',
        'vietnam': '🇻🇳', 'yemen': '🇾🇪', 'zambia': '🇿🇲',
        'zimbabwe': '🇿🇼',
    }
    return flags.get(nationality.lower().strip(), '🏳️')


def build_bracket(players, byes):
    """Build a full bracket tree from players and byes"""
    import math

    all_players = list(players)
    bye_names = [b['full_name'] for b in byes]

  
    total = len(all_players) + len(byes)


    if total <= 1:
        return []

    bracket_size = 2 ** math.ceil(math.log2(total)) if total > 1 else 2


    rounds = []
    first_round = []


    paired = []
    player_list = list(all_players)

    for i in range(0, len(player_list), 2):
        if i + 1 < len(player_list):
            paired.append({
                'player1': player_list[i],
                'player2': player_list[i + 1],
                'winner': None
            })


    for bye in byes:
        paired.append({
            'player1': bye,
            'player2': None,  # BYE
            'winner': bye['full_name']  # auto advance
        })

    rounds.append(paired)


    current_round = paired
    while len(current_round) > 1:
        next_round = []
        for i in range(0, len(current_round), 2):
            match = {
                'player1': None,
                'player2': None,
                'winner': None,
                'from_match1': i,
                'from_match2': i + 1 if i + 1 < len(current_round) else None
            }
            next_round.append(match)
        rounds.append(next_round)
        current_round = next_round

    return rounds