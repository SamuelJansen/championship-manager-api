from python_helper import log
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


USER_AGENT = globalsInstance.getSetting('browser.user-agent')
MAX_WAITING_TIME = globalsInstance.getSetting('browser.max-waiting-time')
HIDDEN = globalsInstance.getSetting('browser.hidden')
