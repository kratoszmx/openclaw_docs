import json
from pathlib import Path
p = Path.home()/'.openclaw'/'openclaw.json'
obj = json.loads(p.read_text())

channels = obj.setdefault('channels', {})

telegram = channels.setdefault('telegram', {})
telegram['dmPolicy'] = 'allowlist'
telegram['allowFrom'] = ['5674620028']
telegram['groupPolicy'] = 'disabled'

whatsapp = channels.setdefault('whatsapp', {})
whatsapp['groupPolicy'] = 'disabled'
whatsapp['selfChatMode'] = False

imessage = channels.setdefault('imessage', {})
imessage['cliPath'] = '/opt/homebrew/bin/imsg'
imessage['dbPath'] = str(Path.home()/'Library'/'Messages'/'chat.db')

update = obj.setdefault('update', {})
update['checkOnStart'] = True
auto = update.setdefault('auto', {})
auto['enabled'] = True
update.setdefault('channel', 'stable')
auto.setdefault('stableDelayHours', 6)
auto.setdefault('stableJitterHours', 12)
auto.setdefault('betaCheckIntervalHours', 1)

p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
print(f'UPDATED {p}')
