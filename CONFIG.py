# K39 WiFi setup Jan 2024
SSID = "2G"
PASSWORD = "Ming@l@b@r39"
USER = "Eric8266"  #Github User
REPOSITORY = "OTA-SENKO"
BRANCH = "main"
GITHUB_URL = "https://github.com"
GITHUB_RAW_URL = "https://raw.githubusercontent.com"
FILES = "test1.py", "test2.py"  # FILES to update from the Repository
REMOTE_UPDATE = "YES"  # Update FILES remote
REMOTE_ACCESS = "NO"  # Access via WebREPL
UPDATE_TIMER = "YES"  # Allow updates per PERIODIC intervals = UPDATE_PERIODIC * UPDATE_PERIOD_MULT 
UPDATE_PERIODIC = 48000  #(480000 mS = ~8 minutes) Block of 'x' mS
UPDATE_PERIOD_MULT = 1 #Number of times UPDATE_PERIODIC = blocks of 8 minutes