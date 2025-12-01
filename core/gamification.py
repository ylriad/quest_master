# core/gamification.py

class GamificationEngine:
    LEVELS = [
        ("Ученик", 0),
        ("Мастер пергаментов", 50),
        ("Архимаг документов", 100)
    ]

    def __init__(self):
        self.total_xp = 0

    def add_xp(self, amount: int):
        self.total_xp += amount

    def get_current_level(self):
        for i, (name, threshold) in enumerate(self.LEVELS):
            if self.total_xp < threshold:
                return self.LEVELS[i - 1] if i > 0 else self.LEVELS[0]
        return self.LEVELS[-1]  # Max level

    def get_xp(self):
        return self.total_xp

    def get_progress_to_next(self):
        current_name, current_threshold = self.get_current_level()
        next_index = None
        for i, (_, thresh) in enumerate(self.LEVELS):
            if thresh == current_threshold:
                next_index = i + 1
                break
        if next_index and next_index < len(self.LEVELS):
            next_threshold = self.LEVELS[next_index][1]
            return (self.total_xp - current_threshold) / (next_threshold - current_threshold)
        return 1.0  # Maxed out

    def get_status(self):
        level_name, _ = self.get_current_level()
        return {
            "level_name": level_name,
            "xp": self.total_xp,
            "progress": self.get_progress_to_next()
        }