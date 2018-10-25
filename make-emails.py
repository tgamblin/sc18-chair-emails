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
    m['Subject'] = 'SC18 Session'
    m['To'] = '%s <%s>' % (name, email)

    body = m.set_content(f'''\
Dear {name},

We are writing to remind you that you are scheduled to chair paper
session {id} at SC18.  Here is your session information:

    Title: {event.name}
    Time: {event.begin} - {event.end}
    Location: {event.location}

Full information is in the attached ICS calendar file.

Please arrive at your session location 15 minutes ahead of time to meet
the presenters and to help them connect their laptops.

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
