import codecs
import sys
from datetime import datetime

def main():
    path = sys.argv[1]
    title = sys.argv[2]
    with codecs.open(path, encoding='utf-8') as f:
        lines = iter(f)
        section = find_section(title, lines)
    print section
    entries = parse_section(section)
    print entries
    entries.sort(key=lambda entry: entry.start)
    for entry in entries:
        d0 = entry.start.date()
        d1 = entry.end.date()
        if d0 == d1:
            print d0
        else:
            print d0, '--', d1
        h, m = divmod(entry.minutes, 60)
        print '    %d:%02d' % (h, m)

def find_section(title, lines):
    """Return the section with the given title, as a list of field-lists.

    ** Title
       Description of several words or lines
       CLOCK: [2013-07-19 Fri 15:30]--[2013-07-19 Fri 18:40] =>  3:10
       CLOCK: [2013-07-19 Fri 12:55]--[2013-07-19 Fri 13:19] =>  0:24
       Another description; each description refers to the clock entries
       that follow it.
       CLOCK: [2013-07-19 Fri 02:44]--[2013-07-19 Fri 04:47] =>  2:03
       CLOCK: [2013-07-18 Thu 20:10]--[2013-07-18 Thu 20:47] =>  0:37

    The above entry would be returned as a list of length 7, each of
    whose entries is itself a list of what were originally whitespace
    separated fields.

    """
    tlist = title.split()

    for line in lines:
        fields = line.split()
        if not fields:
            continue
        if fields[0].count('*') != len(fields[0]):
            continue
        if fields[1:] == tlist:
            break
    else:
        return []

    section = []

    for line in lines:
        fields = line.split()
        if not fields:
            continue
        if fields[0].count('*') == len(fields[0]):
            break
        section.append(fields)

    return section

def parse_section(section):
    alternating = [[]]  # becomes: [[description, ...], [clock, ...], ...]
    for fields in section:
        clockish = (fields[0] == 'CLOCK:')
        if len(alternating) % 2 == clockish:
            alternating.append([])
        alternating[-1].append(fields)
    return [ Entry(alternating[i], alternating[i + 1])
             for i in range(0, len(alternating) - 1, 2) ]

class Entry(object):
    def __init__(self, description_data, clock_data):
        self.description = u' '.join( field for fieldlist in description_data
                                      for field in fieldlist )
        self.minutes = sum( clocked_minutes(fields) for fields in clock_data)
        self.start = times(clock_data[-1])[0]
        self.end = times(clock_data[0])[1]

    def __repr__(self):
        return '<%d minutes %r...>' % (self.minutes, self.description[:10])

def times(fields):
    """Return a starting and ending datetime, given `fields` like:

    [u'CLOCK:', u'[2013-03-08', u'Fri', u'14:24]--[2013-03-08', u'Fri',
     u'15:41]', u'=>', u'1:17']

    """
    return (datetime.strptime(fields[1] + fields[3][:5], u'[%Y-%m-%d%H:%M'),
            datetime.strptime(fields[3][9:] + fields[5], u'%Y-%m-%d%H:%M]'))

def clocked_minutes(fields):
    """Return an integer number of minutes, given `fields` like:

    [u'CLOCK:', u'[2013-03-08', u'Fri', u'14:24]--[2013-03-08', u'Fri',
     u'15:41]', u'=>', u'1:17']

    """
    d0, d1 = times(fields)
    return (d1 - d0).total_seconds() // 60

main()
