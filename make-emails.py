#!/usr/bin/env python3
import re
import json

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.policy import SMTP

from glob import glob
from ics import Calendar

session_files = glob('sess*.ics')

# session id -> chair name/email mapping
chairs = {}
with open('chairs.json') as f:
    records = json.load(f)
    for r in records:
        id = r['id']
        chairs[id] = (r['chair'], r['email'])

# grab session info from calendar invite files and make emails with
# attachments.
for file_name in session_files:
    # get id from session file name
    id = int(re.match(r'sess(\d\d\d).ics', file_name).group(1))

    # chair name and email from session id
    name, email = chairs[id]

    # open the calendar file and read it in
    with open(file_name) as f:
        ics_file = f.read()
        f.seek(0)
        event = Calendar(f.read()).events[0]

    m = EmailMessage()
    m['From'] = 'Todd Gamblin <tgamblin@llnl.gov>'
    m['To'] = '%s <%s>' % (name, email)
    m['Cc'] = 'Torsten Hoefler <htor@inf.ethz.ch>'
    m['Subject'] = f'Session Chair for {event.name} at SC18'

    body = m.set_content(f'''\
Dear {name},

Thanks for agreeing to be a session chair at SC18! Session chairs help to
ensure that SC technical talks run smoothly, and they help to provide
lively and engaging technical discussion after presentations.

You are scheduled to chair paper session {id} at SC18:

    Title: {event.name}
    Time: {event.begin.format('ddd, MMM DD')}, {event.begin.format('h:mmA')}  - {event.end.format('h:mmA')}
    Location: {event.location}

There is also a calendar invitation attached.

We've put together some guidance for your session below.  Please read it
carefully to make sure you're in sync with the instructions we've sent to
your presenters:

1. Please arrive at your session 15 minutes ahead of time to meet the
   presenters.  We've instructed them to arrive 15 minutes early as well.
   Help the presenters make sure that their laptops can connect to the
   projector, and if there are any issues, alert the AV staff.  If no AV
   staff are present in the presentation room, there will be staff
   available in Lower Level C, Room 151/152.

2. Presenters have been instructed to seek you out and to provide a 2-3
   sentence introduction to you before the session.  You can use this
   when introducing each speaker before their presentation.

3. Keep the sessions running on time.  Presenters are expected to target
   25 minutes for their talks, with 3 minutes for questions and 2 minutes
   for changeover.  Let your presenters know that you'll be timing them
   and let them know with hand signals when there are, e.g., 10, 5, and 1
   minutes left.  You can allow them to go slightly over time, be sure
   they at least stop before the next session starts, and ideally be sure
   they leave time for questions.

4. Each talk should start at the beginning of its scheduled time slot.
   If a talk ends early, do not simply go on to the next talk -- wait
   until its scheduled start time, to accommodate attendees who walk
   between rooms to hear talks in different sessions.

5. To ensure that the question time does not go unused, we ask that
   session chairs pay close attention to presentations and have a
   question of their own ready for cases when the audience does not ask
   any questions.  Try to encourage the audience to ask questions before
   you ask your own.

That's all!  We look forward to seeing you at SC18!

If you are unable to chair this session for ANY reason, please let us
know as soon as possible so that we can find a substitute chair.

Thanks again!

Todd and Torsten
SC18 Tech Papers Co-chairs
''')

    m.make_mixed()  # set to multipart and add attachment
    attachment_part = MIMEText(ics_file)
    del attachment_part['Content-Type']
    attachment_part.add_header(
        'Content-Type', 'text/calendar', name='invite.ics')
    attachment_part.add_header(
        'Content-Disposition', 'attachment', filename='invite.ics')
    m.attach(attachment_part)

    email_name = re.sub('.ics$', '.eml', file_name)
    with open(email_name, 'wb') as f:
        f.write(m.as_bytes(policy=SMTP))
