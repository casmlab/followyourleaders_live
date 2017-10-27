#https://stackoverflow.com/questions/21768963/group-consecutive-dates-together-with-python
from datetime import datetime, timedelta

x=['Mar 13 2012','Feb 10 2012','Jun 17 2014']
x=map(lambda v : datetime.strptime(v, '%b %d %Y').strftime('%Y%m'), x)
x = sorted(map(int,x))
print x

def findContiMonth(L):
    first = last = L[0]
    for n in L[1:]:
        print n
        if n - 1 == last: # Part of the group, bump the end
            last = n
        else: # Not part of the group, yield current group and start a new
            yield first, last
            first = last = n
    yield first, last # Yield the last group

print list(group(x))
