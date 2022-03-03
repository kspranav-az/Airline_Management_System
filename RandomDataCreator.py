import mysql.connector
import random
import datetime

time = datetime.time.min
co = tuple()
col = list()


def randomplane():
    str1 = "6E"
    str2 = str(random.randint(100, 999))
    return str1 + str2


def randomflightdate(end_):  # end_ = 2022-04-30
    td = datetime.date  # td = 2021-12-30
    start = "".join(str(td.today()).split("-"))
    start_y = int(start[0:4])
    end = "".join(str(end_).split("-"))
    end_y = int(end[0:4])
    r_y = random.randint(start_y + 1, end_y)
    r_m = random.randint(1, int(end[4:6]))
    r_d = random.randint(1, 30)
    if int(r_m) == 2 and int(r_d) > 28:
        rc = random.choice([1, 2])
        if rc == 1:
            r_d = random.randint(1, 28)
        else:
            r_m = random.randrange(1, int(end[4:6]) + 1, 2)
    if len(str(r_m)) == 1:
        r_m = "0" + str(r_m)
    if len(str(r_d)) == 1:
        r_d = "0" + str(r_d)
    lst = [r_y, r_m, r_d]
    return "".join(list(map(str, lst)))


def randomflighttime():
    global time
    mi = "".join(str(datetime.time.min).split(":"))
    mx = "".join(str(datetime.time.max)[:8].split(":"))
    mi_h, mi_m = mi[0:2], mi[2:4]
    mx_h, mx_m = mx[0:2], mx[2:4]
    hour = random.randint(int(mi_h), int(mx_h))
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    mint = random.randrange(int(mi_m), int(mx_m))
    if len(str(mint)) == 1:
        mint = "0" + str(mint)
    sec = "00"
    time = str(hour) + ":" + str(mint) + ":" + str(sec)
    return "".join(time.split(":"))


def randomnxtflighttime():
    global time
    mi = "".join(str(time).split(":"))
    mx = "".join(str(datetime.time.max)[:8].split(":"))
    mi_h, mi_m = mi[0:2], mi[2:4]
    mx_h, mx_m = mx[0:2], mx[2:4]
    mi_h = int(mi_h) + random.randint(2, 3)
    if int(mi_h) >= 24:
        mi_h = random.randint(1, 3)
    hour = random.randint(int(mi_h), int(mx_h))
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    mint = random.randrange(0, int(mx_m))
    if len(str(mint)) == 1:
        mint = "0" + str(mint)
    sec = "00"
    time = str(hour) + ":" + str(mint) + ":" + str(sec)
    return "".join(time.split(":"))


def randomdestination(c):
    global co
    global col
    col = list(ports)
    col.remove(c)
    co = random.choice(col)
    return str(co[0])


def randomnxtdestination():
    global co
    global col
    col.remove(co)
    co = random.choice(col)
    return str(co[0])


def randomcost():
    cost = random.randrange(random.randrange(2400, 3000, 50),
                            random.randrange(4000, 6000, 50),
                            random.choice([40, 50]))
    return str(cost)


def randomgcost():
    cost = random.randrange(random.randrange(3000, 3600, 50),
                            random.randrange(4000, 7000, 50),
                            random.choice([40, 50, 20]))
    return str(cost)


if __name__ == "__main__":
    # connection
    Igdb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2004"
    )
    print("Connected to server successfully....")

    cr = Igdb.cursor()

    cr.execute("USE airline_schedule_info;")
    cr.execute("SELECT * FROM airports")
    ports = cr.fetchall()

    for port in ports:
        print(port)
        for num in range(60):
            data = \
                tuple([
                    str(port[0]),
                    randomplane(),
                    randomflightdate("2022-04-30"),
                    randomflighttime(),
                    randomnxtflighttime(),
                    randomdestination(port),
                    randomcost()
                ])
            print(data)

            cmnd = ('INSERT INTO ' + port[2] + '(a_id,\
            plane_name,\
            flight_date,\
            departure_time,\
            destination_time,\
            destination,\
            ticket_fare) VALUES(%s,%s,%s,%s,%s,%s,%s)')
            cr.execute(cmnd, data)

        for num in range(24):
            data = \
                tuple([
                    str(port[0]),
                    randomplane(),
                    randomflightdate("2022-04-30"),
                    randomflighttime(),
                    randomnxtflighttime(),
                    randomdestination(port),
                    randomnxtflighttime(),
                    randomnxtdestination(),
                    randomgcost(),
                    "Y"
                ])
            print(data)

            cmnd = ('INSERT INTO ' + port[2] + '(a_id,\
            plane_name,\
            flight_date,\
            departure_time,\
            mid_time,\
            mid_location,\
            destination_time,\
            destination,\
            ticket_fare,\
            multi) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
            cr.execute(cmnd, data)
    Igdb.commit()
