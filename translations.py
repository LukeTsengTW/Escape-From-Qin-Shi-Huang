import locale
from config import load_config
from constants import FIRST_OPEN_GAME

config = load_config()

# === Language Setting ===

lang, encoding = locale.getdefaultlocale()

current_language = ""

if not FIRST_OPEN_GAME:
    if lang == 'zh_TW':
        current_language = "zh_tw"
    elif lang == 'zh_CN':
        current_language = "zh_cn"
    elif lang.startswith('en'):
        current_language = "en"
    else:
        current_language = "zh_tw"
else:
    current_language = config["current_language"]

translations = {
    "zh_tw": {
        "title": "逃離秦始皇",
        "play": "開始遊戲",
        "setting": "設定",
        "how_to_play" : "如何遊玩",
        "htp_line1" : "1. 你將扮演北極熊，在迷宮中逃離秦始皇的魔掌",
        "htp_line2" : "2. 透過 ↑ ↓ ← → 四個方向鍵移動",
        "htp_line3" : "3. 路途上有道具，用於干擾秦始皇",
        "htp_line4" : "4. 按住 Shift 可以奔跑，但會消耗體力",
        "exit" : "離開遊戲",
        "language": "語言",
        "sound": "音效",
        "resolution": "解析度",
        "resolution_setting": "解析度設定",
        "current_resolution": "目前解析度:",
        "resolution_restart_note": "更改解析度後需要重新啟動遊戲",
        "fullscreen": "全螢幕模式",
        "switch_to_windowed": "切換至視窗模式",
        "switch_to_fullscreen": "切換至全螢幕模式",
        "back": "返回",
        "select_language": "選擇語言",
        "select_language_note" : "更換語言後請重啟遊戲",
        "traditional_chinese": "繁體中文",
        "simplified_chinese": "简体中文",
        "english": "English",
        "invisible_time" : "秦始皇出現時間:",
        "is_key_obtained" : "已獲得鑰匙",
        "game_paused" : "遊戲暫停",
        "resume" : "繼續遊戲",
        "back_menu" : "回到主選單",
        "invincible_time" : "無敵時間：",
        "red_time" : "反傷持續：",
        "blue_time" : "冰凍持續：",
        "difficulty" : "難度",
        "difficulty_setting" : "難度設定",
        "now_difficulty" : "現在難度:",
        "easy" : "簡單",
        "normal" : "普通",
        "difficult" : "困難",
        "gameover" : "遊戲結束，你被秦始皇抓到了",
        "pass" : "恭喜通關！逃離秦始皇的魔掌！",
        "master_volume" : "主音量",
        "bgm" : "背景音量",
        "se" : "音效音量",
        "stamina": "體力",
    },
    "zh_cn": {
        "title": "逃离秦始皇",
        "play": "开始游戏",
        "setting": "设置",
        "how_to_play" : "如何游玩",
        "htp_line1" : "1. 你将扮演北极熊，在迷宫中逃离秦始皇的魔掌",
        "htp_line2" : "2. 透过 ↑ ↓ ← → 四个方向键移动",
        "htp_line3" : "3. 路途上有道具，用于干扰秦始皇",
        "htp_line4" : "4. 按住 Shift 可以奔跑，但会消耗体力",
        "exit" : "离开游戏",
        "language": "语言",
        "sound": "音效",
        "resolution": "分辨率",
        "resolution_setting": "分辨率设置",
        "current_resolution": "当前分辨率:",
        "resolution_restart_note": "更改分辨率后需要重新启动游戏",
        "fullscreen": "全屏模式",
        "switch_to_windowed": "切换至窗口模式",
        "switch_to_fullscreen": "切换至全屏模式",
        "back": "返回",
        "select_language": "选择语言",
        "select_language_note" : "更换语言后请重启游戏",
        "traditional_chinese": "繁体中文",
        "simplified_chinese": "简体中文",
        "english": "English",
        "invisible_time" : "秦始皇出现时间:",
        "is_key_obtained" : "已获得钥匙",
        "game_paused" : "游戏暂停",
        "resume" : "继续游戏",
        "back_menu" : "回到主菜单",
        "invincible_time" : "无敌时间：",
        "red_time" : "反伤持续：",
        "blue_time" : "冰凍持续：",
        "difficulty" : "难度",
        "difficulty_setting" : "难度设置",
        "now_difficulty" : "现在难度:",
        "easy" : "简单",
        "normal" : "普通",
        "difficult" : "困难",
        "gameover" : "游戏结束，你被秦始皇抓到了",
        "pass" : "恭喜通关！逃离秦始皇的魔掌！",
        "master_volume" : "主音量",
        "bgm" : "背景音量",
        "se" : "音效音量",
        "stamina": "体力",
    },
    "en": {
        "title": "Escape from Qin Shi Huang",
        "play": "Play",
        "setting": "Setting",
        "how_to_play" : "How To Play",
        "htp_line1" : "1. You play as a polar bear and escape from the clutches of Qin Shi Huang in the maze",
        "htp_line2" : "2. Use the ↑ ↓ ← → arrow keys to move",
        "htp_line3" : "3. There are items on the road to interfere with Qin Shi Huang",
        "htp_line4" : "4. Hold Shift to sprint, but it consumes stamina",
        "exit" : "Exit",
        "language": "Language",
        "sound": "Sound",
        "resolution": "Resolution",
        "resolution_setting": "Resolution Setting",
        "current_resolution": "Current Resolution:",
        "fullscreen": "Fullscreen Mode",
        "switch_to_windowed": "Switch to Windowed",
        "switch_to_fullscreen": "Switch to Fullscreen",
        "back": "Back",
        "select_language": "Select Language",
        "select_language_note" : "Please restart game when you change the language",
        "traditional_chinese": "Traditional Chinese",
        "simplified_chinese": "Simplified Chinese",
        "english": "English",
        "invisible_time" : "Time of Qin Shi Huang's appearance:",
        "is_key_obtained" : "Key Obtained",
        "game_paused" : "Pause",
        "resume" : "Resume",
        "back_menu" : "Back to menu",
        "invincible_time" : "Invincible time:",
        "red_time" : "Thorn Sword Time:",
        "blue_time" : "Frozen Time:",
        "difficulty" : "Difficulty",
        "difficulty_setting" : "Difficulty Setting",
        "now_difficulty" : "Current Difficulty:",
        "easy" : "Easy",
        "normal" : "Normal",
        "difficult" : "Difficult",
        "gameover" : "Game Over, You Failed",
        "pass" : "Complete the game!",
        "master_volume" : "Main Volume",
        "bgm" : "BGM Volume",
        "se" : "Sound Effect Volume",
        "stamina": "Stamina",
    }
}

