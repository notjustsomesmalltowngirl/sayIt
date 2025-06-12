from sqlalchemy.sql import func


def get_game_to_type_mapping(game_type):
    """Returns the internal attribute name for a given game type string.

    This function maps a human-readable game type (e.g., "Would You Rather")
    to its corresponding attribute name used in the Playground model
    (e.g., "would_you_rather_questions").

    Parameters:
        game_type (str): The display name of the game type.

    Returns:
        str: The internal attribute name corresponding to the game type."""
    mapping = {
        'did you know': 'did_you_knows',
        'hypotheticals': 'hypotheticals',
        'hot takes': 'hot_takes',
        'never have i ever': 'never_have_i_evers',
        'would you rather': 'would_you_rather_questions',
        'story builder': 'story_builders',
        'riddles': 'riddles',
        'two truths and a lie': 'two_truths_and_a_lie'
    }
    key = game_type.lower()
    return mapping[key]


def return_error_for_wrong_params(game_type):
    """    Returns an appropriate error response for invalid or missing game type.

    This function checks whether the provided game_type is missing or not among the
    supported types. If invalid, it returns a dictionary describing the error along
    with the appropriate HTTP status code.

    Parameters:
        game_type (str | None): The value of the 'game_type' query parameter.

    Returns:
        tuple[dict, int] | None: A tuple containing the error message dictionary and status code (400 or 422),
                                 or None if the game_type is valid."""
    if not game_type:
        return {
            'error': {
                'Bad Request': "Missing 'game_type' in query parameters."
            }
        }, 400
    valid_types = ['did you know', 'hypotheticals', 'hot takes', 'never have i ever', 'would you rather',
                   'story builder', 'riddles', 'two truths and a lie']
    if game_type.lower() not in valid_types:
        return {
            'error': {
                'Unprocessable Entity': f"{game_type} is not a valid game type . Valid options are: "
                                        f"{', '.join([t.title() for t in valid_types])}"

            }
        }, 422


def get_game_by_type(game, game_type, model_class, category=None, limit=None):
    """Fetches game entries of a specified type, optionally filtered by category or limited in number.

    This helper function dynamically accesses a relationship on the game object using game_type.
    It applies optional filtering by category and random ordering with a result limit.
    The results are returned as a dictionary and a success status code.

    Parameters:
        game (Playground): The Playground model instance containing the relationships.
        game_type (str): The name of the relationship attribute (e.g., 'did_you_knows').
        model_class (db.Model): The SQLAlchemy model class corresponding to the game type.
        category (str, optional): Category to filter results by.
        limit (int, optional): Maximum number of results to return.

    Returns:
        tuple[dict, int]: A tuple containing the queried game data and HTTP status code 200."""
    query = getattr(game, game_type)
    if not category and not limit:
        result = query.all()
    elif category:
        result = query.filter(model_class.category == category).all() if not limit \
            else (query.filter(model_class.category == category).
                  order_by(func.random()).limit(limit).all())
    else:
        result = query.order_by(func.random()).limit(limit).all()
    return {
        game_type: [
            q.to_dict() for q in result
        ]
    }, 200
