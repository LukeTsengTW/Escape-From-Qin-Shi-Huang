import constants

class DifficultyConfig:
    """Difficulty configuration class for better organization"""
    
    # Define difficulty settings as class constants
    DIFFICULTY_SETTINGS = {
        "easy": {
            "boost_speed": 2,
            "enemy_speed_base": 2,
            "boost_duration": 3000,
            "freeze_duration": 3000,
            "invisible_duration": 6000,
            "red_duration": 7000,
            "blue_duration": 7000,
            "spawn_items_times": 6,
            "description": "Easy mode - More forgiving gameplay"
        },
        "normal": {
            "boost_speed": 2,
            "enemy_speed_base": 3,
            "boost_duration": 2500,
            "freeze_duration": 3000,
            "invisible_duration": 3000,
            "red_duration": 5000,
            "blue_duration": 5000,
            "spawn_items_times": 5,
            "description": "Normal mode - Balanced difficulty"
        },
        "difficult": {
            "boost_speed": 3,
            "enemy_speed_base": 4,
            "boost_duration": 2000,
            "freeze_duration": 3000,
            "invisible_duration": 6000,
            "red_duration": 3000,
            "blue_duration": 3000,
            "spawn_items_times": 4,
            "description": "Difficult mode - Challenging gameplay"
        }
    }
    
    @classmethod
    def get_settings(cls, level):
        """Get settings for a specific difficulty level"""
        if level not in cls.DIFFICULTY_SETTINGS:
            print(f"Warning: Unknown difficulty '{level}', using 'normal' as default")
            level = "normal"
        return cls.DIFFICULTY_SETTINGS[level]
    
    @classmethod
    def get_available_levels(cls):
        """Get list of available difficulty levels"""
        return list(cls.DIFFICULTY_SETTINGS.keys())
    
    @classmethod
    def get_level_description(cls, level):
        """Get description for a difficulty level"""
        settings = cls.get_settings(level)
        return settings.get("description", "No description available")
    
def difficulty_parameter_setting(level):
    """Set game parameters based on difficulty level"""
    
    # Get difficulty settings
    settings = DifficultyConfig.get_settings(level)
    
    # Apply settings to constants module variables
    constants.BOOST_SPEED = settings["boost_speed"]
    constants.ENEMY_SPEED = settings["enemy_speed_base"] + constants.HATE_VALUE
    constants.BOOST_DURATION = settings["boost_duration"]
    constants.FREEZE_DURATION = settings["freeze_duration"]
    constants.INVISIBLE_DURATION = settings["invisible_duration"]
    constants.RED_DURATION = settings["red_duration"]
    constants.BLUE_DURATION = settings["blue_duration"]
    constants.SPAWN_ITEMS_TIMES = settings["spawn_items_times"]

    print(f"Difficulty set to: {level.title()} - {settings['description']}")