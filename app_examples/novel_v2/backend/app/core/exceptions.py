class NovelException(Exception):
    """Base exception for novel app"""

    pass


class SessionNotFoundError(NovelException):
    """Game session not found"""

    pass


class StoryNotFoundError(NovelException):
    """Story not found"""

    pass


class SceneNotFoundError(NovelException):
    """Scene not found in story"""

    pass


class InvalidChoiceError(NovelException):
    """Invalid choice index"""

    pass
