from models import MAX_JERSEY, TOTAL_MATCHDAYS, MAX_PER_MATCHDAY



def validate_not_empty(text, field_name):
    text = text.strip()
    if text == "":
        raise ValueError(f"{field_name} cannot be empty")
    return text


def validate_name(text):
    name = validate_not_empty(text, "Name")
    if len(name) > 30:
        raise ValueError("Name cannot be longer than 30 characters")
    has_letter = False
    for ch in name:
        if ch.isalpha():
            has_letter = True
        elif ch not in (" ", ".", "'", "-"):
            raise ValueError("Name can only contain letters")
    if not has_letter:
        raise ValueError("Name must contain at least one letter")
    return name



def validate_jersey(text):
    text = str(text).strip()
    try:
        number = int(text)
    except ValueError:
        raise ValueError("Jersey must be a whole number")
    if number < 1 or number > MAX_JERSEY:
        raise ValueError(f"Jersey must be between 1 and {MAX_JERSEY}")
    return number



def validate_choice(text, options, field_name):
    text = text.strip()
    if text not in options:
        raise ValueError(f"Please choose a {field_name}")
    return text


def validate_no_duplicate(player_id, name, team, existing_ids, existing_keys):
    if player_id in existing_ids:
        raise ValueError(f"That jersey number is already used in this team (ID {player_id})")
    if (name.lower(), team) in existing_keys:
        raise ValueError("This player already exists in this team")


def validate_existing_player_id(player_id, existing_ids):
    player_id = player_id.strip()
    if player_id not in existing_ids:
        raise ValueError("Player not found")
    return player_id


def validate_appearance_limit(appearances):
    if appearances >= TOTAL_MATCHDAYS:
        raise ValueError(f"This player already has {TOTAL_MATCHDAYS} appearances")


def validate_stat(text, field_name):
    text = str(text).strip()
    try:
        number = int(text)
    except ValueError:
        raise ValueError(f"{field_name} must be a whole number")
    if number < 0:
        raise ValueError(f"{field_name} cannot be negative")
    limit = MAX_PER_MATCHDAY[field_name]
    if number > limit:
        raise ValueError(f"{field_name} cannot be more than {limit} in one match day")
    return number


