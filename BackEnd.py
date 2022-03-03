import mysql.connector
from tkinter import messagebox


# BackEnd Functions (CLIENT)


def check(user_name, password):
    """ IS USED TO CHECK IF THE GIVEN USER NAME
     EXIST IN DATABASE OR NOT """
    cr.execute("USE client_info;")
    cr.execute("SELECT * \
             FROM SignedAccounts\
             WHERE accounts ='" + user_name + "'")
    tbl1 = cr.fetchall()
    cr.execute("SELECT * \
                 FROM SignedAccounts\
                 WHERE password ='" + password + "' AND accounts ='" + user_name + "' ")
    tbl2 = cr.fetchall()
    if not tbl1:
        return False, False
    else:
        if not tbl2:
            return True, False

        return True, True


def user(user_name, password):
    cr.execute("USE Client_info;")
    cr.execute("SELECT * \
                     FROM SignedAccounts\
                     WHERE password ='" + password + "' AND accounts ='" + user_name + "' ")
    tbl2 = cr.fetchall()
    return tbl2[0]


def family(iid):
    cr.execute("USE Client_info;")
    cr.execute("SELECT * \
                     FROM user_family_info\
                     WHERE id1 ='" + str(iid) + "'\
                     ORDER BY id2 DESC")
    tbl2 = cr.fetchall()
    return tbl2


def signin(user_name, password):
    """ USED TO GIVE ACCESS TO THE USER"""

    if check(user_name, password)[0]:
        if check(user_name, password)[1]:
            print("ID PASS EXISTENCE CONFIRMED !")
            return True, 1
        else:
            return False, 1
    else:
        return False, 1


def register(user_name, password):
    """ USED TO INSERT A GIVEN USER ID AND PASSWORD\
    IN DATABASE"""

    if not check(user_name, password)[1]:
        cmnd = "INSERT INTO SignedAccounts (accounts,password)\
         VALUES (%s,%s)"
        idn = (user_name, password)
        cr.execute(cmnd, idn)
        Igdb.commit()
        print("id pass inserted ....")
        return True
    else:
        return False


def familys_register(lst, last_id=1):
    """ USED TO INSERT FAMILY INFO INTO DATABASE """

    cmnd = "INSERT INTO User_Family_Info (id1,id2,first_name,\
    last_name,gender,date_of_birth,age)\
    VALUES (%s,%s,%s,%s,%s,%s,%s)"
    idn = lst
    cr.executemany(cmnd, idn)
    Igdb.commit()
    print("family info inserted ....")


def family_register(lst, last_id=1):
    """ USED TO INSERT FAMILY INFO INTO DATABASE """

    cr.execute("use client_info;")
    cmnd = "INSERT INTO User_Family_Info (id1,id2,first_name,\
    last_name,gender,date_of_birth,age)\
    VALUES (%s,%s,%s,%s,%s,%s,%s)"
    idn = lst
    cr.execute(cmnd, idn)
    Igdb.commit()
    print("family info inserted ....")


def personinfo(id1, id2):
    cmnd = "SELECT * FROM client_info.user_family_info\n\
    WHERE id1 = " + str(id1) + " AND id2 = " + str(id2) + ""
    cr.execute(cmnd)
    return cr.fetchall()[0]


def update_personinfo(tpl):
    id1, id2, fname, lname, gender, dob, age = tpl
    cr.execute("use client_info;")
    cr.execute(
        "update ignore user_family_info\n\
            set \n\
	            first_name ='" + str(fname) + "',\n\
                last_name ='" + str(lname) + "',\n\
                gender ='" + str(gender) + "',\n\
                date_of_birth ='" + str(dob) + "',\n\
                age = " + str(age) + "\n\
            where id1 = " + str(id1) + " and id2 = " + str(id2) + ";"
    )
    Igdb.commit()


def delete_user(id1, id2):
    cr.execute("use client_info")
    cr.execute(
        "DELETE \n\
        FROM user_family_info\n\
        WHERE id1 =" + str(id1) + " AND id2 =" + str(id2)
    )
    Igdb.commit()
    messagebox.showinfo("Deleted", " Person Successfully deleted from Family Records")


def searchow(_from, val, _to=None, _on=None):
    global cond
    val = cur_val(val)
    if _to or _on:
        if _to and _on:
            cond = "destination = " + str(port_aid(_to)) + " and flight_date <= '" + _on + "'"
        elif _to:
            cond = " destination =" + str(port_aid(_to))
        elif _on:
            cond = " flight_date <= '" + _on + "'"
    else:
        cond = port_iata(_from) + ".a_id = " + str(port_aid(_from))
    cr.execute("use airline_schedule_info;")
    cr.execute("SELECT air.a_id,take_off_id,plane_name,air.iata,a.iata,flight_date,ticket_fare* " + str(val) + "\n\
    ,concat(time_format(departure_time,'%H:%i'),' hr'),concat(time_format(destination_time,'%H:%i'),' hr'),\n\
    concat(time_format(abs(timediff(destination_time,departure_time)),'%H:%i'),' hr')\n\
    FROM " + port_iata(_from) + " \n\
    join airports air using (a_id)\n\
    join airports a on destination = a.a_id\n\
    where " + cond + " \n\
    order by flight_date asc,ticket_fare desc;")

    return cr.fetchall()


def get_ports(str1):
    cr.execute("USE airline_schedule_info;")
    cr.execute("SELECT " + str1 + " FROM airports")
    a_ports = cr.fetchall()
    return a_ports


def port_iata(str1):
    cr.execute("USE airline_schedule_info;")
    cr.execute("SELECT iata FROM airports \n\
               WHERE city = '" + str1 + "';")
    return cr.fetchone()[0]


def port_iata2(str1):
    cr.execute("USE airline_schedule_info;")
    cr.execute("SELECT iata FROM airports \n\
               WHERE a_id = " + str(str1) + ";")
    return cr.fetchone()[0]


def get_city(str1):
    cr.execute("USE airline_schedule_info;")
    cr.execute("SELECT city FROM airports \n\
                   WHERE iata = '" + str1 + "';")
    return cr.fetchone()[0]


def port_aid(str1):
    cr.execute("USE airline_schedule_info;")
    cr.execute("SELECT a_id FROM airports \n\
                   WHERE city = '" + str1 + "';")
    # try:
    return cr.fetchone()[0]
    # except TypeError:
    #    return ''


def get_cur():
    cr.execute("use airline_reservations; ")
    cr.execute("SELECT * FROM airline_reservations.currencies;")
    return cr.fetchall()


def cur_val(cid):
    cr.execute("use airline_reservations; ")
    cid = str(cid)
    cr.execute("SELECT cr_value FROM airline_reservations.currencies \n\
    WHERE cr_id =" + cid + ";")
    return cr.fetchone()[0]


def cur_id(cnm):
    cr.execute("use airline_reservations; ")
    cnm = str(cnm)
    cr.execute("SELECT cr_id FROM airline_reservations.currencies \n\
        WHERE cr_name ='" + cnm + "';")
    return int(cr.fetchone()[0])


def get_resid(tid):
    cr.execute("select reservation_id\n\
    from airline_reservations.reservation\n\
    where transaction_id = " + str(tid) + ";")
    return int(cr.fetchone()[0])


def get_items(cr_id=1):
    cr.execute("use airline_reservations; ")
    cr.execute("SELECT pro_id,pro_name,pro_cost\
     * " + str(cur_val(cr_id)) + " FROM items")

    return cr.fetchall()


def last_oid():
    cr.execute("use airline_reservations; ")
    cr.execute("SELECT order_no FROM airline_reservations.orders \
               ORDER BY order_no DESC")
    return cr.fetchone()[0]


def last_bid():
    cr.execute("use airline_reservations; ")
    cr.execute("SELECT booking_id FROM airline_reservations.booking \
                   ORDER BY booking_id DESC")
    return cr.fetchone()[0]


def BOOK(p, r, o, a, ci):
    bi = last_bid() + 1
    oi = last_oid() + 1
    booking = []
    order = []
    cri = ci
    cmnd = ("insert into airline_reservations.booking\n\
     (booking_id,a_id,take_off_id,id1,id2) \n\
     values (%s,%s,%s,%s,%s)")
    for per in r:
        booking.append([bi, p[0], p[1], per[0], per[1]])

    cr.executemany(cmnd, booking)
    Igdb.commit()
    print("booking done.....")

    cmnd = "insert into airline_reservations.orders\n\
     (order_no,pro_id,qty,cost)values (%s,%s,%s,%s)"

    if o:
        for od in o:
            order.append([oi, od[0], od[3], od[2] * od[3]])

        cr.executemany(cmnd, order)
        Igdb.commit()
        print("Order Placed.....")
    else:
        oi = None

    val = 0
    for x in o:
        val = val + x[2] * x[3]
    tot = (p[6] * len(r)) + val

    if val == 0:
        val = None

    cmnd = "insert into airline_reservations.transactions\
    (id,booking_id,order_no,booking_cost,order_cost,\
    total_cost,cr_id) values (%s,%s,%s,%s,%s,%s,%s) "

    trans = \
        [
            a[0],
            bi,
            oi,
            p[6] * len(r),
            val,
            tot,
            cri
        ]

    cr.execute(cmnd, trans)
    Igdb.commit()
    print("Transaction done......")

    tid = cr.getlastrowid()

    cmnd = "insert into airline_reservations.reservation\
     (id,booking_id,order_no,transaction_id) \
     values(%s,%s,%s,%s)"

    res = \
        [
            a[0],
            bi,
            oi,
            tid
        ]

    cr.execute(cmnd, res)
    Igdb.commit()
    print("Reservation Successfully Done.....")

    messagebox.showinfo("           CONGRATULATIONS", "YOU SUCCESSFULLY RESERVED\n\
    " + str(len(r)) + "   SEATS in PLANE :  " + str(p[2]) + " \n\
    Order ID:" + str(oi) + "   Reservation ID :" + str(cr.getlastrowid()) + " \n   \
     Transaction ID :" + str(tid) + "")


def get_flight(iata, tkf):
    cr.execute(
        "select plane_name , a.iata,air.iata,flight_date,\n\
        concat(time_format(departure_time,'%H:%i'),' hr'),\n\
        concat(time_format(abs(timediff(destination_time,departure_time)),'%H:%i'),' hr')\n\
    from airline_schedule_info." + port_iata2(iata) + " l\n\
    join airline_schedule_info.airports a using(a_id)\n\
    join airline_schedule_info.airports air\n\
    on air.a_id = l.destination\n\
    where take_off_id = " + str(tkf) + ";"
    )
    return cr.fetchone()


def all_bookings(id1):
    cr.execute("use airline_reservations; ")
    cr.execute("\
    select a_id,take_off_id,bk.booking_id,order_no,transaction_id,count(bk.booking_id)\n\
    from reservation res\n\
    join booking bk on res.booking_id = bk.booking_id and  id = id1\n\
    where id = " + str(id1) + " \n\
    group by booking_id;\n\
    ")
    print("Reservation data fetched")
    flyf = []
    for i in cr.fetchall():
        fly = [i[0], i[1]]
        for j in get_flight(i[0], i[1]):
            fly.append(j)
        fly.append(i[2])
        fly.append(i[3])
        fly.append(i[4])
        fly.append(i[5])
        flyf.append(fly)
    return flyf


def get_trans(tid):
    cr.execute("select booking_cost , order_cost , total_cost,cr_name\n\
    from airline_reservations.transactions\n\
    join airline_reservations.currencies using(cr_id)\n\
    where transaction_id = " + str(tid) + ";")

    return cr.fetchone()


def get_names(bid):
    cr.execute("select first_name , last_name\n\
    from airline_reservations.booking\n\
    join client_info.user_family_info using(id1,id2)\n\
    where booking_id = " + str(bid) + "\n\
    order by id2 desc;")

    return cr.fetchall()


def get_order(oid):
    cr.execute("select o.pro_id,pro_name,qty,cost\n\
    from airline_reservations.orders o\n\
    join airline_reservations.items using(pro_id)\n\
    where order_no = " + str(oid) + "\n\
    order by pro_id desc;")

    return cr.fetchall()


def udt_or(oid, nor, tid):
    cr.execute("delete\n\
    from orders\n\
    where order_no = " + str(oid) + ";")
    Igdb.commit()
    cmnd = "insert into airline_reservations.orders\n\
         (order_no,pro_id,qty,cost)values (%s,%s,%s,%s)"
    order = []
    if oid is None:
        oid = last_oid() + 1
    if nor:
        for od in nor:
            order.append([oid, od[0], od[2], od[3]])

        cr.executemany(cmnd, order)
        Igdb.commit()
        print("Order Updated.....")
        val = 0
        for x in order:
            val = val + float(x[3])
        bk_c = get_trans(int(tid))[0]
        ttl_c = bk_c + val

        cr.execute("update airline_reservations.transactions\n\
        set\n\
            order_no = " + str(oid) + ",\n\
	        booking_cost = " + str(bk_c) + ",\n\
            order_cost = " + str(val) + ",\n\
            total_cost = " + str(ttl_c) + "\n\
        where transaction_id = " + str(tid) + ";")
        Igdb.commit()
        print("transaction updated......")
    else:
        bk_c = get_trans(int(tid))[0]
        ttl_c = bk_c
        cr.execute("update airline_reservations.transactions\n\
                set\n\
                    order_no = null,\n\
        	        booking_cost = " + str(bk_c) + ",\n\
                    order_cost = null,\n\
                    total_cost = " + str(ttl_c) + "\n\
                where transaction_id = " + str(tid) + ";")
        Igdb.commit()
        print("Order removed")


def del_book(bkid, oid, tid):

    cr.execute("delete\n\
    from airline_reservations.reservation\n\
    where reservation_id = " + str(get_resid(tid)) + ";")

    cr.execute("delete\n\
    from airline_reservations.transactions\n\
    where transaction_id = " + str(tid) + ";")

    cr.execute("delete\n\
    from airline_reservations.orders\n\
    where order_no = " + str(oid) + ";")

    cr.execute("delete\n\
    from airline_reservations.booking\n\
    where booking_id = " + str(bkid) + ";")
    Igdb.commit()
    print("Successfully Cancelled Your Reservation.......")


# BackEnd Functions (ADMIN)

# connection
Igdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2004",
)
print("Connected to server successfully....")

cr = Igdb.cursor(buffered=True)

if __name__ == "__main__":

    cr.execute("SHOW DATABASES")
    for x in cr:
        print(x)

    cr.execute("CREATE DATABASE Client_Info;")
    cr.execute("USE Client_info;")
    cr.execute("CREATE TABLE SignedAccounts (id INT AUTO_INCREMENT PRIMARY KEY);")
    cr.execute("alter table SignedAccounts add column accounts varchar(320),\
    add column password varchar(22);")
    cr.execute("show databases")

    for x in cr:
        print(x)
    
    cr.execute("CREATE TABLE User_Family_Info (\n\
    id1 INT NOT NULL,\n\
    id2 INT NOT NULL,\n\
    first_name VARCHAR(50) NOT NULL,\n\
    last_name VARCHAR(50) NOT NULL,\n\
    gender VARCHAR(5),\n\
    date_of_birth DATE,\n\
    age INT,\n\
    PRIMARY KEY (id1,id2)\n\
        )")
    

    cr.execute('CREATE DATABASE airline_schedule_info;')
    cr.execute('USE airline_schedule_info;')
    cr.execute('CREATE TABLE airports\n\
	(\n\
    a_id int AUTO_INCREMENT PRIMARY KEY,\n\
    city VARCHAR(50),\n\
    iata VARCHAR(4)\n\
    );\n\
    '
               )
    cmnd = "INSERT INTO airline_schedule_info.airports (city,iata) VALUES (%s,%s)"
    ports = \
        [
            ("Lucknow", "LKW"),
            ("NewDelhi", "DEL"),
            ("Mumbai", "BOM"),
            ("Coimbatore", "CJB"),
            ("Cochin", "COK"),
            ("Hyderabad", "HYD"),
            ("Goa", "GOI")
        ]
    cr.executemany(cmnd, ports)
    Igdb.commit()

    ports = get_ports("city,iata")
    print(ports)
    for c in ports:
        city = c[1]
        CMND = 'CREATE TABLE ' + city + '\n\
        	(\n\
            a_id INT NOT NULL ,\n\
            take_off_id INT AUTO_INCREMENT PRIMARY KEY,\n\
            plane_name VARCHAR(10) NOT NULL,\n\
            flight_date DATE NOT NULL,\n\
            departure_time TIME NOT NULL,\n\
            mid_time TIME,\n\
            mid_location INT,\n\
            destination_time TIME NOT NULL,\n\
            destination INT NOT NULL,\n\
            ticket_fare INT NOT NULL,\n\
            multi VARCHAR(2), \n\
            FOREIGN KEY (a_id) REFERENCES airline_schedule_info.airports(a_id) \n\
            )'
        print(city)
        cr.execute(CMND)
    Igdb.commit()

    cr.execute("create database airline_reservations;")
    Igdb.commit()
    cr.execute("use airline_reservations; ")

    cr.execute("create table airline_reservations.currencies\n\
    	(\n\
    	cr_id int primary key not null auto_increment,\n\
    	cr_name varchar(50) not null,\n\
    	cr_value float\n\
    	);")
    cr.execute("create table airline_reservations.items\n\
    	(\n\
    	pro_id int primary key auto_increment,\n\
    	pro_name varchar(50),\n\
    	pro_cost float\n\
    	);")
    Igdb.commit()
    cr.execute("create table airline_reservations.orders\n\
    	(\n\
    	order_no int ,\n\
    	pro_id int,\n\
    	qty int,\n\
    	cost float,\n\
    	foreign key(pro_id) references airline_reservations.items(pro_id)\n\
    	);")

    Igdb.commit()

    cr.execute("create table airline_reservations.booking\n\
    	(\n\
    	booking_id int ,\n\
    	a_id int ,\n\
    	take_off_id int,\n\
    	id1 int,\n\
    	id2 int,\n\
    	foreign key(id1,id2) references client_info.user_family_info(id1,id2)\n\
    	);")
    Igdb.commit()

    curren = [("Indian Rupees", 1),
              ("US Dollar", 0.013),
              ("Thailand Bhat", 0.43),
              ("UAE Dirham", 0.049),
              ("Nepalese Rupee", 1.60),
              ("Riyal Omani", 0.0051),
              ("Singapore Dollar", 0.018),
              ("Euro", 0.012)]
    cmnd = "INSERT INTO airline_reservations.currencies(cr_name,cr_value)\
     VALUES(%s,%s)"
    cr.executemany(cmnd, curren)
    Igdb.commit()
    for i in get_cur():
        print(i)
    cr.execute("create table airline_reservations.transactions\n\
        	(\n\
        	transaction_id int primary key auto_increment,\n\
            id int,\n\
        	booking_id int ,\n\
        	order_no int ,\n\
        	booking_cost float,\n\
        	order_cost float,\n\
        	total_cost float,\n\
        	cr_id int,\n\
        	transaction_datetime timestamp default current_timestamp(),\n\
            foreign key(id) references client_info.signedaccounts(id),\n\
        	foreign key(cr_id) references airline_reservations.currencies(cr_id)\n\
        	);")
    Igdb.commit()

    cr.execute("create table airline_reservations.reservation\n\
        	(\n\
        	reservation_id int primary key auto_increment,\n\
            id int,\n\
        	booking_id int,\n\
        	order_no int,\n\
        	transaction_id int,\n\
        	foreign key(id) references client_info.signedaccounts(id),\n\
        	foreign key(transaction_id) references airline_reservations.transactions(transaction_id)\n\
        	)")
    print("done")

    items = \
        [
            ("Veg Sandwich", 60),
            ("Chicken Sandwich", 80),
            ("Bakery Biscuit", 20),
            ("Cup Noodle", 30),
            ("Veg Biryani", 100),
            ("Doughnuts", 40),
            ("Chicken Wings", 120),
            ("Soft Drink", 40)
        ]
    cmnd = "INSERT INTO airline_reservations.items(pro_name,pro_cost)\
           VALUES(%s,%s)"
    cr.executemany(cmnd, items)
    Igdb.commit()
    
    for i in get_items(5):
        print(i)
    cr.execute("insert into airline_reservations.orders (order_no,pro_id,qty,cost)values (1,1,1,60);")

    cr.execute("insert into airline_reservations.booking (booking_id,a_id,take_off_id,id1,id2)\n\
     values (2,1,1,1,1)")
    c = cr.getlastrowid()
    Igdb.commit()
    print(type(c), c)

