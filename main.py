"""Entry point for the reaction game.

The core logic lives in :class:`game.reaction_game.ReactionGame`, keeping
initialisation and the game loop separated from the bootstrap script.
"""
from game.reaction_game import ReactionGame


def main() -> None:
    game = ReactionGame()
    game.run()


if __name__ == "__main__":
    main()
