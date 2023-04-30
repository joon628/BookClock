import sutime
import datetime
print(sutime.__file__)
# create an instance of the SUTime class
sutime = sutime.SUTime(mark_time_ranges=True, include_range=True)

# extract all time expressions from the book
with open('D:\\BookClockData\\the_barrier&beach_rex_18771949.txt', 'r') as f:
    book_text = f.read()

time_expressions = sutime.parse(book_text)
print(time_expressions)
# create datetime objects for each time expression
datetimes = []
for te in time_expressions:
    date_str = f"{te['value']} {te['text']}"
    try:
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        datetimes.append(dt)
    except ValueError:
        pass

# sort the datetime objects in ascending order
datetimes.sort()

