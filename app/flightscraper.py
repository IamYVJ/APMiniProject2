from bs4 import BeautifulSoup

soup = BeautifulSoup(aa, 'html5lib')

flights = []

for row1 in soup.findAll('div', attrs = {'class':'schedule v-aligm-t pr'}):

    flight = []

    t1 = row1.findAll('div', attrs = {'class':'i-b pr'})
    for row in t1:
        dt = str(row)
        dt = dt[20:25]

        ar = str(row.p)
        ar = ar[71:]
        ar = ar[:ar.find('<')]

        fn = row.span.text


    t2 = row1.findAll('p', attrs = {'class':'fs-10 font-lightgrey no-wrap city ellipsis'})
    for row in t2:
        flight.append(row.text)

    t3 = row1.findAll('p', attrs = {'autom':'arrivalTimeLabel'})
    for row in t3:
        at = row.text

    t4 = row1.findAll('p', attrs = {'autom':'durationLabel'})
    for row in t4:
        dr = row.text

    t5 = row1.findAll('span', attrs = {'class':'cursor-default'})
    for row in t5:
        st = row.text

    flight.append(ar)
    flight.append(fn)
    flight.append(dt)
    flight.append(at)
    flight.append(dr)
    flight.append(st)

    flights.append(flight)

print(flights)
