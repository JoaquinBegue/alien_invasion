from io import open

class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start game in inactive state.
        self.game_active = False
        self.first_game = True

        # High score should never be reset.
        self.high_score = 0
        self.load_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        try:     
            with open("high_scores.txt", "r", encoding="utf8") as file:
                file_content = file.read()
                if len(file_content) > 0:
                    self.high_score = int(file_content)
                else:
                    raise Exception
        except:
            print("High score loading error: Corrupt or empty file.\n")
            file = open("high_scores.txt", "w")
        finally:
            file.close()