from datetime import date
from tkinter import *
from tkinter import ttk
from BackEnd import *
from tkcalendar import DateEntry

ACCESS = [-1, "Nil", "Nil"]
reserve = []
order = []
cache = []
plane = []
qtys = [1]

root = Tk()
root.title("Indigo Airline Management system")
root.geometry("570x540")
icon = PhotoImage(master=root, file=r'.\icons\iconi.png')
root.wm_iconphoto(True, icon)
root.configure(background="CYAN")


def is_packed(widget):
    try:
        widget.pack_info()
    except TclError:
        return False
    else:
        return True


def sign():
    if is_packed(adm_cli):
        adm_cli.pack_forget()
    elif is_packed(RegisterUserI):
        RegisterUserI.pack_forget()
    elif is_packed(RegisterUser):
        RegisterUser.pack_forget()
    if ACCESS[0] != -1:
        RegisterUserI.pack_forget()
        main_label.pack(expand=True)
        prof_update()
    else:
        SignIn.pack(expand="yes")


def Id_Pass_Ch(username, password):
    if not ("@" in username):
        return False, 0
    elif not (username.strip().split("@"))[1] in ["gmail.com",
                                                  "reddiffmail.com",
                                                  "yahoo.com"]:
        return False, 0
    else:
        return signin(username, password)


def sinin():
    if not Id_Pass_Ch(str1_sin.get(), str2_sin.get())[0]:
        global ACCESS
        if Id_Pass_Ch(str1_sin.get(), str2_sin.get())[1] == 0:
            msglb = messagebox.showerror("error syntax",
                                         "invalid email syntax....")
            str1_sin.set("")
            str2_sin.set("")
            print(msglb)
        else:
            msg_lb = messagebox.askokcancel("user not found !",
                                            "Either your username or "
                                            "password is incorrect \n\n"
                                            "Don't have a account ??  \n"
                                            "register")
            if msg_lb is True:
                str1_sin.set("")
                str2_sin.set("")
                button2_sin.config(bg="green")
            else:
                str2_sin.set("")
            print(msg_lb)
    else:
        ACCESS = user(str1_sin.get(), str2_sin.get())
        up_tab()
        print("USER ACCESS GRANTED.....")
        SignIn.pack_forget()
        main_label.pack(expand=True)
        prof_update()
        # search.pack(expand="yes")


def reg():
    SignIn.pack_forget()
    RegisterUser.pack(expand="yes")


def registeruseri():
    if is_packed(RegisterUser):
        RegisterUser.pack_forget()
    RegisterUserI.pack(expand=True)


def Register():
    global ACCESS
    if not Id_Pass_Ch(str1_reg.get(), str2_reg.get())[0]:
        if Id_Pass_Ch(str1_reg.get(), str2_reg.get())[1] == 0:
            popup = messagebox.showerror("error syntax",
                                         "invalid email syntax....")
            str1_reg.set("")
            str2_reg.set("")
            str3_reg.set("")
            print(popup)
        elif str3_reg.get() != str2_reg.get():
            popup = messagebox.showerror("error password",
                                         " both passwords are not identical !")
            str2_reg.set("")
            str3_reg.set("")
            print(popup)
        else:
            register(str1_reg.get(), str2_reg.get())
            print("User registered !")
            popup = messagebox.showinfo("Welcome to the family",
                                        "YOU ARE SUCCESSFULLY REGISTERED")
            ACCESS = user(str1_reg.get(), str2_reg.get())
            print(popup)
            if popup == "ok":
                registeruseri()
    else:
        messagebox.showwarning("","Given user has Previously Registered")


def usrinfo():
    print(entry1_regf.get(), entry2_regf.get(), entry3_regf.get_date(), gen.get(),
          age(entry3_regf.get_date()))
    if entry1_regf.get() == "" or entry2_regf.get() == "":
        messagebox.showerror("incomplete entry",
                             "Either firstname or " +
                             "lastname is incomplete\n" +
                             "fill and register")
    elif gen.get() == "":
        messagebox.showerror("incomplete entry",
                             "Gender not filled.\n" +
                             "Please enter the gender")
    elif entry3_regf.get_date() == dt1:
        messagebox.showerror("incomplete entry",
                             "Date Of Birth not filled.\n" +
                             "Please enter the DOB")
    else:
        if choi.get() == 1:
            id2 = 1
        else:
            fam = family(int(ACCESS[0]))
            lstid2 = fam[0][1]
            choi.set(int(lstid2) + 1)
            id2 = choi.get()
        inf = (
            int(user(ACCESS[1], ACCESS[2])[0]),
            id2,
            entry1_regf.get(),
            entry2_regf.get(),
            genders[gen.get()],
            "".join(str(entry3_regf.get_date()).split("-")),
            age(entry3_regf.get_date())
        )
        family_register(inf)
        up_tab()
        sign()


def Search():
    if is_packed(main_label):
        main_label.pack_forget()
    entry_srch5.config(text="Select")
    T_search.pack(expand=True)


def age(dt):
    dt2 = date.today()
    Age = dt2.year - dt.year
    return Age


def prof_update():
    try:
        tup = personinfo(ACCESS[0], 1)
        print("User info Fetched ....")
        fn, ln, gdr, dob, ag = tup[2:]
    except IndexError:
        print(ACCESS)
        print("No User info Found....")
        fn, ln, gdr, dob, ag = "Nil", "Nil", "Nil", "Nil", "Nil",
    label8_prf.config(text=fn)
    label9_prf.config(text=ln)
    labelA1_prf.config(text=ACCESS[1])
    labelA2_prf.config(text=gdr)
    labelA3_prf.config(text=ag)
    labelA4_prf.config(text=dob)


def del_user():
    slc_user = tv.focus()
    lst = family(ACCESS[0])
    try:
        per = (lst[int(slc_user)])
    except ValueError:
        return None
    if slc_user:
        if int(per[1]) == 1:
            messagebox.showwarning("Personal Info", "You can't delete your own info")
        else:
            choice = messagebox.askyesno("Caution", "Do you really want to delete \n" +
                                         per[2] + "'s data from your Family record")
            if choice:
                id1, id2 = per[:2]
                try:
                    delete_user(int(id1), int(id2))
                except mysql.connector.errors.IntegrityError:
                    pass
                up_tab()
            else:
                pass

    else:
        messagebox.showerror("Selection Error", "Please select the person to be deleted")


def up_tab():
    global ACCESS
    global tv
    try:
        for i in tv.get_children():
            tv.delete(i)
        n = 0
        inf = family(int(ACCESS[0]))
        lth = len(inf)
        for row in inf:
            print(row)
            lst = list(row)[2:-2]
            lst.append(row[-1])
            tv.insert(parent="", index=0, iid=n, text=lth,
                      values=lst)
            lth -= 1
            n += 1
    except ValueError:
        pass


def addmem():
    if is_packed(main_label):
        main_label.pack_forget()
    RegisterUserI.pack(expand=True)
    entry1_regf.delete(0, END)
    entry2_regf.delete(0, END)
    gen.set(date.today())
    entry4_regf.set("")

    title.set("Add member")
    btn1.set("Add")
    button2_regf.config(state=NORMAL)
    choi.set(0)
    label1_regf.config(text=title.get())
    button1_regf.config(text=btn1.get())


def up_user():
    if is_packed(main_label):
        main_label.pack_forget()
    UpdateUser.pack(expand=True)


def updt_f():
    slc_user = tv.focus()
    lst = family(ACCESS[0])
    if slc_user:
        per = (lst[int(slc_user)])
        print(entry1_updt.get(), entry2_updt.get(), entry3_updt.get_date(),
              gen1.get(), age(entry3_updt.get_date()))
        if entry1_updt.get() == "" or entry2_updt.get() == "":
            messagebox.showerror("incomplete entry",
                                 "Either firstname or " +
                                 "lastname is incomplete\n" +
                                 "fill and register")
        elif gen1.get() == "":
            messagebox.showerror("incomplete entry",
                                 "Gender not filled.\n" +
                                 "Please enter the gender")
        elif entry3_updt.get_date() == dt1:
            messagebox.showerror("incomplete entry",
                                 "Date Of Birth not filled.\n" +
                                 "Please enter the DOB")
        else:
            if per[1] == 1:
                messagebox.showinfo("Error:678", "Use Update Profile")
            else:
                id2 = per[1]
                inf = (
                    int(ACCESS[0]),
                    int(id2),
                    entry1_updt.get(),
                    entry2_updt.get(),
                    genders[gen1.get()],
                    "".join(str(entry3_updt.get_date()).split("-")),
                    age(entry3_updt.get_date())
                )
                print(inf)
                update_personinfo(inf)
                back1()
                entry1_updt.delete(0, END)
                entry2_updt.delete(0, END)
                # entry3_updt.set_date(date.today())
                gen1.set("")
                tv.focus_set()
                up_tab()

    else:
        messagebox.showerror("Selection Error", "Please select the person to be Updated")


def back1():
    if is_packed(RegisterUserI):
        RegisterUserI.pack_forget()
    if is_packed(UpdateUser):
        UpdateUser.pack_forget()
    main_label.pack(expand=True)


def select_f():
    res_lst = []
    global reserve
    global tv3
    global qtys

    def back():
        root2.destroy()

    def remove():

        try:
            tv3.tag_configure(str(tv3.focus()), background="white", foreground="black")
            res_lst.remove(fam[int(tv3.focus())])
        except ValueError:
            pass

    def add():

        tv3.tag_configure(str(tv3.focus()), background="blue", foreground="white")
        if fam[int(tv3.focus())] not in res_lst:
            res_lst.append(fam[int(tv3.focus())])

    def selected():
        global reserve
        global qtys
        reserve = list(res_lst)
        qtys = list(range(1, len(reserve) + 1))
        print(reserve)
        entry_srch5.config(text="Pass :" + str(len(reserve)))
        root2.destroy()

    root2 = Toplevel()
    root2.grab_set()
    fam = family(int(ACCESS[0]))

    T_sel = LabelFrame(root2)

    F1_sel = LabelFrame(T_sel)
    F2_sel = LabelFrame(T_sel)
    F3_sel = LabelFrame(T_sel)

    label1_sel = Label(F1_sel, text="select passengers & extra seats", font=("algerian", 15), padx=15)
    label1_sel.grid(row=1, column=1)

    tv3 = ttk.Treeview(F2_sel, height=8)

    tv3["column"] = ("First Name", "Last Name", "Gender", "Age")

    tv3.column("#0", width=10, minwidth=35, anchor=CENTER)
    tv3.column("First Name", width=120, anchor=CENTER)
    tv3.column("Last Name", width=120, anchor=CENTER)
    tv3.column("Gender", width=75, anchor=CENTER)
    tv3.column("Age", width=65, anchor=CENTER)

    tv3.heading("#0", text="no.")
    tv3.heading("First Name", text="First Name")
    tv3.heading("Last Name", text="Last Name")
    tv3.heading("Gender", text="Gender")
    tv3.heading("Age", text="Age")
    tv3.pack()

    up_tab3()

    button1_sel = Button(F3_sel, text="Back", command=back)
    button2_sel = Button(F3_sel, text="Remove", command=remove)
    button3_sel = Button(F3_sel, text="Add", command=add)
    button4_sel = Button(F3_sel, text="Selected", command=selected)

    button1_sel.grid(row=0, column=0, padx=27, pady=6)
    button2_sel.grid(row=0, column=1, padx=27, pady=6)
    button3_sel.grid(row=0, column=2, padx=27, pady=6)
    button4_sel.grid(row=0, column=3, padx=27, pady=6)

    F1_sel.pack()
    F2_sel.pack()
    F3_sel.pack()

    T_sel.pack(expand=True)
    root2.mainloop()


def up_tab3():
    global ACCESS
    global tv3
    try:
        for i in tv3.get_children():
            tv3.delete(i)
        n = 0
        inf = family(int(ACCESS[0]))
        lth = len(inf)
        for row in inf:
            lst3 = list(row)[2:5]
            lst3.append(row[-1])
            tv3.insert(parent="", index=0, iid=n, text=lth,
                       values=lst3, tag=str(n))
            lth -= 1
            n += 1
    except ValueError:
        pass


def srch():
    global inf
    print(entry_srch1.get(), entry_srch2.get(), entry_srch3.get_date(),
          entry_srch4.get_date(), entry_srch6.get())
    if entry_srch1.get() == "" or entry_srch2.get() == "":
        messagebox.showerror("Select Ports", "\n kindly select the \n\
        Departure & Destination Ports")
    elif entry_srch1.get() == entry_srch2.get():
        messagebox.showerror("Select Ports", "\n kindly select distinct \n\
                Departure & Destination Ports")
        entry_srch1.set("")
        entry_srch2.set("")
    elif len(reserve) == 0:
        messagebox.showerror("Select Passengers", "Kindly Select the \n\
        family members to be boarded")

    elif entry_srch3.get_date() == date.today():
        inf = searchow(entry_srch1.get(), cur_id(entry_srch6.get()),
                       entry_srch2.get())
        print(inf)
        if is_packed(T_search):
            T_search.pack_forget()
        up_tab2()
        F_search.pack(expand=True)
    else:
        inf = searchow(entry_srch1.get(), cur_id(entry_srch6.get()),
                       entry_srch2.get(),
                       "".join(str(entry_srch3.get_date()).split("-")))
        print(inf)
        if is_packed(T_search):
            T_search.pack_forget()
        up_tab2()
        F_search.pack(expand=True)


def back2():
    if is_packed(T_search):
        T_search.pack_forget()
    reserve.clear()
    main_label.pack()


def up_tab2():
    global tv2
    global inf
    try:
        for i in tv2.get_children():
            tv2.delete(i)
        n = 0
        # inf = searchow("Lucknow", 7, "Coimbatore")
        print(inf)
        lth = len(inf)
        for row in inf:
            print(row)
            tv2.insert(parent="", index=0, iid=n, text=lth,
                       values=row[2:] + tuple(str(row[-1])))
            lth -= 1
            n += 1
    except ValueError and TypeError:
        pass


def back3():
    if is_packed(F_search):
        F_search.pack_forget()
    T_search.pack(expand=True)


def book():
    global inf
    global plane
    try:
        x = tv2.focus()
        plane = list(inf[int(x)])
        print(plane)
        inf_update()
        up_tab4()
        if is_packed(F_search):
            F_search.pack_forget()
        P_main.pack(expand=True)
    except IndexError:
        pass


def back4():
    if is_packed(P_main):
        P_main.pack_forget()
    F_search.pack(expand=True)


def up_tab4():
    global tv4
    global reserve
    try:
        for i in tv4.get_children():
            tv4.delete(i)
        n = 0
        inf = reserve
        lth = len(inf)
        for row in inf:
            lst3 = list(row)[2:4]
            lst3.append(row[-1])
            tv4.insert(parent="", index=0, iid=n, text=lth,
                       values=lst3)
            lth -= 1
            n += 1
    except ValueError:
        pass


def up_tab5():
    global tv5
    global order
    try:
        for i in tv5.get_children():
            tv5.delete(i)
        n = 0
        inf = order
        lth = len(inf)
        for row in inf:
            lst3 = row[1], row[3], row[2] * row[3]
            tv5.insert(parent="", index=0, iid=n, text=lth,
                       values=lst3, tag=str(n))
            lth -= 1
            n += 1
    except ValueError:
        pass


def up_tab6():
    global tv6
    try:
        for i in tv6.get_children():
            tv6.delete(i)
        n = 0
        inf = get_items(cur_id(t6.get()))
        lth = len(inf)
        for row in inf:
            lst3 = list(row)[1:3]
            tv6.insert(parent="", index=0, iid=n, text=lth,
                       values=lst3, tag=str(n))
            lth -= 1
            n += 1
    except ValueError:
        pass


def up_tab7():
    global tv7
    global cache
    try:
        for i in tv7.get_children():
            tv7.delete(i)
        n = 0
        inf = cache
        lth = len(inf)
        for row in inf:
            lst3 = row[1], row[3], row[2] * row[3]
            tv7.insert(parent="", index=0, iid=n, text=lth,
                       values=lst3, tag=str(n))
            lth -= 1
            n += 1
    except ValueError:
        pass


def inf_update():
    global plane
    global order
    print(plane)
    try:
        label8_pln.config(text=plane[2])
        label9_pln.config(text=get_city(plane[3]))
        labelA1_pln.config(text=get_city(plane[4]))
        labelA2_pln.config(text=str(plane[5]))
        labelA3_pln.config(text=plane[7])
        labelA4_pln.config(text=plane[9])

        labelA7_pln.config(text=str(plane[6] * len(reserve)))

        val = 0
        for x in order:
            val = val + x[2] * x[3]
        tot = (plane[6] * len(reserve)) + val
        labelA8_pln.config(text=str(val))
        labelB1_pln.config(text=str(tot))
    except IndexError:
        pass


def select_o():
    def select():
        try:
            print(od[int(tv6.focus())])
            label5_selo.config(text=od[int(tv6.focus())][1])
            cacher.append(od[int(tv6.focus())])
        except ValueError:
            pass

    def add():
        try:
            o = cacher[-1] + (qty.get(),)
            print(o)
            for odr in cache:
                if odr[0] == o[0]:
                    cache.remove(odr)
                    cache.append(o)
                    cache.sort(reverse=False)
                    up_tab7()
                    break
            else:
                cache.append(o)
                cache.sort(reverse=False)
                up_tab7()
        except IndexError:
            pass

    def remove():
        try:
            cache.remove(cache[int(tv7.focus())])
            up_tab7()
        except ValueError:
            pass

    def back():
        global cache
        cache = []
        root3.destroy()

    def Order():
        global order
        order = cache
        up_tab5()
        val = 0
        for x in order:
            val = val + x[2] * x[3]
        tot = (plane[6] * len(reserve)) + val
        labelA8_pln.config(text=str(val))
        labelB1_pln.config(text=str(tot))

        root3.destroy()

    global order
    global tv6
    global tv7
    global qtys
    global cache

    cacher = []
    root3 = Toplevel()
    root3.grab_set()
    od = get_items(cur_id(t6.get()))
    qty = IntVar()
    qty.set(1)
    cache = []

    T_selo = LabelFrame(root3)

    F1_selo = LabelFrame(T_selo)
    F2_selo = LabelFrame(T_selo)
    F3_selo = LabelFrame(T_selo, borderwidth=0)
    F4_selo = LabelFrame(T_selo)

    label1_selo = Label(F1_selo, text="Select Order", font=("algerian", 18))
    label1_selo.pack()

    tv6 = ttk.Treeview(F2_selo, height=8)

    tv6["column"] = ("Item", "Cost")

    tv6.column("#0", width=10, minwidth=35, anchor=CENTER)
    tv6.column("Item", width=120, anchor=CENTER)
    tv6.column("Cost", width=85, anchor=CENTER)

    tv6.heading("#0", text="no.")
    tv6.heading("Item", text="Item")
    tv6.heading("Cost", text="Cost")

    tv6.grid(row=1, column=0, padx=2)

    tv7 = ttk.Treeview(F2_selo, height=8)

    tv7["column"] = ("Item", "Qty", "total")

    tv7.column("#0", width=10, minwidth=35, anchor=CENTER)
    tv7.column("Item", width=120, anchor=CENTER)
    tv7.column("Qty", width=45, anchor=CENTER)
    tv7.column("total", width=95, anchor=CENTER)

    tv7.heading("#0", text="no.")
    tv7.heading("Item", text="Item")
    tv7.heading("Qty", text="Qty")
    tv7.heading("total", text="Total")

    tv7.grid(row=1, column=1, padx=2)

    label2_selo = Label(F2_selo, text="Menu", font=("Consolas", 18))
    label3_selo = Label(F2_selo, text="Your Order", font=("Consolas", 18))

    label2_selo.grid(row=0, column=0, padx=2)
    label3_selo.grid(row=0, column=1, padx=2)
    up_tab6()

    label4_selo = Label(F3_selo, text="Item :", font=("consolas", 15))
    label5_selo = Label(F3_selo, text="", width=20, font=("consolas", 15))
    label6_selo = ttk.Combobox(F3_selo, values=qtys, textvariable=qty, width=4, height=4, font=("consolas", 15))

    label4_selo.grid(row=0, column=0)
    label5_selo.grid(row=0, column=1)
    label6_selo.grid(row=0, column=2)

    button1_sel = Button(F4_selo, text="Back", command=back)
    button2_sel = Button(F4_selo, text="select", command=select)
    button3_sel = Button(F4_selo, text="Add", command=add)
    button4_sel = Button(F4_selo, text="Remove", command=remove)
    button5_sel = Button(F4_selo, text="Order", command=Order)

    button1_sel.grid(row=0, column=0, padx=27, pady=6)
    button2_sel.grid(row=0, column=1, padx=27, pady=6)
    button3_sel.grid(row=0, column=2, padx=27, pady=6)
    button4_sel.grid(row=0, column=3, padx=27, pady=6)
    button5_sel.grid(row=0, column=4, padx=27, pady=6)

    F1_selo.pack()
    F2_selo.pack()
    F3_selo.pack()
    F4_selo.pack()

    T_selo.pack(expand=True)
    root3.mainloop()


def c_reserve():
    RESERVE = reserve
    ORDER = order
    PLANE = plane
    CURRENCY = cur_id(t6.get())
    BOOK(PLANE, RESERVE, ORDER, ACCESS, CURRENCY)

    reserve.clear()
    order.clear()
    plane.clear()
    up_tab5()

    if is_packed(P_main):
        P_main.pack_forget()
    main_label.pack(expand=True)


def up_tab8():
    global tv8
    global bkings
    try:
        for i in tv8.get_children():
            tv8.delete(i)
        bkings = all_bookings(ACCESS[0])
        n = 0
        inf = bkings
        lth = len(inf)
        for row in inf:
            lst3 = list(row)[2:7]
            lst3.append(row[-1])
            tv8.insert(parent="", index=0, iid=n, text=lth,
                       values=lst3)
            lth -= 1
            n += 1
    except ValueError:
        pass


def check_res():
    global bkings
    global tv8
    global tv9
    global tvA1

    def up_tab9(pn):
        global tv9
        global tvA1
        print(pn)

        try:
            label8_res.config(text=pn[2])
            label9_res.config(text=get_city(pn[3]))
            labelA1_res.config(text=get_city(pn[4]))
            labelA2_res.config(text=str(pn[5]))
            labelA3_res.config(text=pn[6])
            labelA4_res.config(text=pn[7])

            trans = get_trans(pn[-2])

            labelA7_res.config(text=str(trans[0]))
            labelA8_res.config(text=str(trans[1]))
            labelB1_res.config(text=str(trans[2]) + "  " + trans[-1],
                               font=(None, 14))
            try:
                for i in tv9.get_children():
                    tv9.delete(i)
                n = 0
                inf = get_names(pn[-4])
                lth = len(inf)
                for row in inf:
                    tv9.insert(parent="", index=0, iid=n, text=lth,
                               values=row, tag=str(n))
                    lth -= 1
                    n += 1
                try:
                    for i in tvA1.get_children():
                        tvA1.delete(i)
                    n = 0
                    inf = get_order(pn[-3])
                    print(inf)
                    lth = len(inf)
                    for row in inf:
                        row = row[1:]
                        tvA1.insert(parent="", index=0, iid=n, text=lth,
                                    values=row, tag=str(n))
                        lth -= 1
                        n += 1
                except ValueError:
                    pass
            except ValueError:
                pass
        except IndexError:
            pass

    root4 = Toplevel()

    try:
        root4.grab_set()
        P_main = LabelFrame(root4)
        print(bkings[int(tv8.focus())])
    except ValueError:
        root4.destroy()
        return None

    Frame1_res = LabelFrame(P_main)
    Frame2_res = LabelFrame(P_main)
    Frame2_res_a = LabelFrame(Frame2_res)
    Frame2_res_b = LabelFrame(Frame2_res)
    Frame3_res = LabelFrame(P_main, padx=8, pady=4, borderwidth=0)
    Frame4_res = LabelFrame(P_main, borderwidth=0)
    Frame5_res = LabelFrame(P_main, padx=110, pady=10, borderwidth=0)

    label1_res = Label(Frame1_res, text="Info", width=31, font=("algerian", 18))
    label1_res.grid(row=0, column=0, columnspan=3)

    label2_res = Label(Frame2_res_a, text="Plane Name :")
    label3_res = Label(Frame2_res_a, text="       From     :")
    label4_res = Label(Frame2_res_a, text="        To       :", anchor=W)
    label5_res = Label(Frame2_res_b, text=" Departure       :")
    label6_res = Label(Frame2_res_b, text=" Depart Time  :")
    label7_res = Label(Frame2_res_b, text="Duration        :")

    label2_res.grid(row=0, column=0)
    label3_res.grid(row=1, column=0)
    label4_res.grid(row=2, column=0)
    label5_res.grid(row=0, column=2)
    label6_res.grid(row=1, column=2)
    label7_res.grid(row=2, column=2)

    label8_res = Label(Frame2_res_a, text="")
    label9_res = Label(Frame2_res_a, text="")
    labelA1_res = Label(Frame2_res_a, text="", width=21)
    labelA2_res = Label(Frame2_res_b, text="", width=20)
    labelA3_res = Label(Frame2_res_b, text="")
    labelA4_res = Label(Frame2_res_b, text="")

    label8_res.grid(row=0, column=1)
    label9_res.grid(row=1, column=1)
    labelA1_res.grid(row=2, column=1)
    labelA2_res.grid(row=0, column=3)
    labelA3_res.grid(row=1, column=3)
    labelA4_res.grid(row=2, column=3)

    labelB2_res = Label(Frame3_res, text="Passengers", font=("Consolas", 18))
    labelB3_res = Label(Frame3_res, text="Orders", font=("Consolas", 18))
    labelB2_res.grid(row=0, column=0)
    labelB3_res.grid(row=0, column=1)

    tv9 = ttk.Treeview(Frame3_res, height=8)

    tv9["column"] = ("First Name", "Last Name")

    tv9.column("#0", width=10, minwidth=35, anchor=CENTER)
    tv9.column("First Name", width=120, anchor=CENTER)
    tv9.column("Last Name", width=120, anchor=CENTER)

    tv9.heading("#0", text="no.")
    tv9.heading("First Name", text="First Name")
    tv9.heading("Last Name", text="Last Name")

    tv9.grid(row=1, column=0, padx=2)

    tvA1 = ttk.Treeview(Frame3_res, height=8)

    tvA1["column"] = ("Item", "Qty", "Cost")

    tvA1.column("#0", width=10, minwidth=35, anchor=CENTER)
    tvA1.column("Item", width=120, anchor=CENTER)
    tvA1.column("Qty", width=40, anchor=CENTER)
    tvA1.column("Cost", width=85, anchor=CENTER)

    tvA1.heading("#0", text="no.")
    tvA1.heading("Item", text="Item")
    tvA1.heading("Qty", text="Qty")
    tvA1.heading("Cost", text="Cost")

    tvA1.grid(row=1, column=1, padx=2)

    labelA5_res = Label(Frame4_res, text="Total Flight Fare :",
                        font=("Century Gothic", 14))
    labelA6_res = Label(Frame4_res, text="Total Order Fare  :",
                        font=("Century Gothic", 14))
    labelA9_res = Label(Frame4_res, text="Grand Total :",
                        font=("Century Gothic", 14))
    labelA7_res = Label(Frame4_res, text="", width=7)
    labelA8_res = Label(Frame4_res, text="", width=8)
    labelB1_res = Label(Frame4_res, text="")

    labelA5_res.grid(row=0, column=0)
    labelA6_res.grid(row=0, column=2)
    labelA7_res.grid(row=0, column=1)
    labelA8_res.grid(row=0, column=4)
    labelA9_res.grid(row=1, column=1)
    labelB1_res.grid(row=1, column=2, columnspan=2)

    # inf_update()
    # up_tab4()
    up_tab9(bkings[int(tv8.focus())])

    Frame1_res.pack()
    Frame2_res.pack()
    Frame2_res_a.grid(row=0, column=0)
    Frame2_res_b.grid(row=0, column=1)
    Frame3_res.pack()
    Frame4_res.pack()
    Frame5_res.pack()

    P_main.pack()

    root4.mainloop()


def up_tabA2():
    global tvA2
    try:
        for i in tvA2.get_children():
            tvA2.delete(i)
        n = 0
        inf = get_items(cur_id(get_trans(bkings[int(tv8.focus())][-2])[-1]))
        lth = len(inf)
        for row in inf:
            lst3 = list(row)[1:3]
            tvA2.insert(parent="", index=0, iid=n, text=lth,
                        values=lst3, tag=str(n))
            lth -= 1
            n += 1
    except ValueError:
        pass


def up_tabA3():
    global tvA3
    global cache
    try:
        for i in tvA3.get_children():
            tvA3.delete(i)
        n = 0
        inf = cache
        lth = len(inf)
        for row in inf:
            lst3 = row[1], row[2], row[3]
            tvA3.insert(parent="", index=0, iid=n, text=lth,
                        values=lst3, tag=str(n))
            lth -= 1
            n += 1
    except ValueError:
        pass


def udt_res_or():
    def select():
        try:
            print(od[int(tvA2.focus())])
            label5_reso.config(text=od[int(tvA2.focus())][1])
            cacher.append(od[int(tvA2.focus())])
        except ValueError:
            pass

    def add():
        try:
            print(cacher[-1])
            o = cacher[-1][0:2] + (qty.get(),) + (cacher[-1][2] * qty.get(),)
            print(o)
            for odr in cache:
                if odr[0] == o[0]:
                    cache.remove(odr)
                    cache.append(o)
                    cache.sort(reverse=False)
                    up_tabA3()
                    break
            else:
                cache.append(o)
                cache.sort(reverse=False)
                up_tabA3()
        except IndexError:
            print("error")
            pass

    def remove():
        try:
            cache.remove(cache[int(tvA3.focus())])
            up_tabA3()
        except ValueError:
            pass

    def back():
        global cache
        cache = []
        root5.destroy()

    def Order():
        if messagebox.askyesno("", "do you really want to update ?"):
            oid = bkings[int(tv8.focus())][-3]
            tid = bkings[int(tv8.focus())][-2]
            udt_or(oid, cache, tid)
            cacher.clear()
            cache.clear()
        else:
            pass
        root5.destroy()

    global tvA2
    global tvA3
    global cache

    cacher = []
    root5 = Toplevel()
    root5.grab_set()
    try:
        od = get_items(cur_id(get_trans(bkings[int(tv8.focus())][-2])[-1]))
    except ValueError:
        root5.destroy()
        return None
    qtys = list(range(1, len(get_names(bkings[int(tv8.focus())][-4])) + 1))
    qty = IntVar()
    qty.set(1)
    cache = list(get_order(bkings[int(tv8.focus())][-3]))
    print(cache)

    T_reso = LabelFrame(root5)

    F1_reso = LabelFrame(T_reso)
    F2_reso = LabelFrame(T_reso)
    F3_reso = LabelFrame(T_reso, borderwidth=0)
    F4_reso = LabelFrame(T_reso)

    label1_reso = Label(F1_reso, text="Select Order", font=("algerian", 18))
    label1_reso.pack()

    tvA2 = ttk.Treeview(F2_reso, height=8)

    tvA2["column"] = ("Item", "Cost")

    tvA2.column("#0", width=10, minwidth=35, anchor=CENTER)
    tvA2.column("Item", width=120, anchor=CENTER)
    tvA2.column("Cost", width=85, anchor=CENTER)

    tvA2.heading("#0", text="no.")
    tvA2.heading("Item", text="Item")
    tvA2.heading("Cost", text="Cost")

    tvA2.grid(row=1, column=0, padx=2)

    tvA3 = ttk.Treeview(F2_reso, height=8)

    tvA3["column"] = ("Item", "Qty", "total")

    tvA3.column("#0", width=10, minwidth=35, anchor=CENTER)
    tvA3.column("Item", width=120, anchor=CENTER)
    tvA3.column("Qty", width=45, anchor=CENTER)
    tvA3.column("total", width=95, anchor=CENTER)

    tvA3.heading("#0", text="no.")
    tvA3.heading("Item", text="Item")
    tvA3.heading("Qty", text="Qty")
    tvA3.heading("total", text="Total")

    tvA3.grid(row=1, column=1, padx=2)

    label2_reso = Label(F2_reso, text="Menu", font=("Consolas", 18))
    label3_reso = Label(F2_reso, text="Your Order", font=("Consolas", 18))

    label2_reso.grid(row=0, column=0, padx=2)
    label3_reso.grid(row=0, column=1, padx=2)
    up_tabA2()
    up_tabA3()

    label4_reso = Label(F3_reso, text="Item :", font=("consolas", 15))
    label5_reso = Label(F3_reso, text="", width=20, font=("consolas", 15))
    label6_reso = ttk.Combobox(F3_reso, values=qtys, textvariable=qty, width=4, height=4, font=("consolas", 15))

    label4_reso.grid(row=0, column=0)
    label5_reso.grid(row=0, column=1)
    label6_reso.grid(row=0, column=2)

    button1_reso = Button(F4_reso, text="Back", command=back)
    button2_reso = Button(F4_reso, text="select", command=select)
    button3_reso = Button(F4_reso, text="Add", command=add)
    button4_reso = Button(F4_reso, text="Remove", command=remove)
    button5_reso = Button(F4_reso, text="Update", command=Order)

    button1_reso.grid(row=0, column=0, padx=27, pady=6)
    button2_reso.grid(row=0, column=1, padx=27, pady=6)
    button3_reso.grid(row=0, column=2, padx=27, pady=6)
    button4_reso.grid(row=0, column=3, padx=27, pady=6)
    button5_reso.grid(row=0, column=4, padx=27, pady=6)

    F1_reso.pack()
    F2_reso.pack()
    F3_reso.pack()
    F4_reso.pack()

    T_reso.pack(expand=True)
    root5.mainloop()


def del_res():
    try:
        bkid = bkings[int(tv8.focus())][-4]
        oid = bkings[int(tv8.focus())][-3]
        tid = bkings[int(tv8.focus())][-2]

        if messagebox.askyesno("", "Do You Really Want To \n\
         Cancel Your Reservation"):
            del_book(bkid, oid, tid)
            messagebox.showinfo("", "Reservation Successfully Cancelled")
            up_tab8()
        else:
            pass
    except ValueError:
        pass


def forget_button():
    global bkings
    bkings = all_bookings(ACCESS[0])
    up_tab8()
    if is_packed(button2_res):
        button2_res.pack_forget()
    if is_packed(button3_res):
        button3_res.pack_forget()
    if is_packed(button4_res):
        button4_res.pack_forget()


def chk_b():
    if is_packed(main_label):
        main_label.pack_forget()
    R_main.pack(expand=True)
    forget_button()
    lableB3_res.config(text="Your Reservations")
    button2_res.pack(side="right")


def upod():
    if is_packed(main_label):
        main_label.pack_forget()
    R_main.pack(expand=True)
    forget_button()
    lableB3_res.config(text=" Select and Update")
    button3_res.pack(side="right")


def clbk():
    if is_packed(main_label):
        main_label.pack_forget()
    R_main.pack(expand=True)
    forget_button()
    lableB3_res.config(text="Select and cancel")
    button4_res.pack(side="right")


def back5():
    if is_packed(R_main):
        R_main.pack_forget()
    main_label.pack(expand=True)


# checking for admin or client

adm_cli = LabelFrame(root, width=50, height=50, pady=20, padx=20)
adm_cli.pack(expand="yes")

label1_adm = Label(adm_cli, text="YOU ARE :")
label1_adm.grid(row=0, column=1)

button1_adm = Button(adm_cli, text="Admin")
button2_adm = Button(adm_cli, text="client", command=sign)
button1_adm.grid(row=1, column=0)
button2_adm.grid(row=1, column=2)


# REGISTER USER

RegisterUser = LabelFrame(root, padx=20, pady=5)

str1_reg = StringVar()
str2_reg = StringVar()
str3_reg = StringVar()

label1_reg = Label(RegisterUser, text="Email ID  :", pady=5, justify="right")
label2_reg = Label(RegisterUser, text="Enter Password  :", justify="right")
label3_reg = Label(RegisterUser, text="Enter Password Again :", justify="right", pady=5)
label4_reg = Label(RegisterUser, text="Register", pady=15)
label1_reg.grid(row=1, column=0)
label2_reg.grid(row=2, column=0)
label3_reg.grid(row=3, column=0)
label4_reg.grid(row=0, column=0, columnspan=3)

entry1_reg = Entry(RegisterUser, textvariable=str1_reg, width=32)
entry2_reg = Entry(RegisterUser, textvariable=str2_reg, width=32, show="*")
entry3_reg = Entry(RegisterUser, textvariable=str3_reg, width=32, show="*")

entry1_reg.grid(row=1, column=2)
entry2_reg.grid(row=2, column=2)
entry3_reg.grid(row=3, column=2)

button1_reg = Button(RegisterUser, text="Register", command=Register, pady=5, anchor="center")
button2_reg = Button(RegisterUser, text="Back", command=sign, anchor=W)
button1_reg.grid(row=4, column=2, pady=10)
button2_reg.grid(row=4, column=0)

# USER INFO REGISTER

RegisterUserI = LabelFrame(root)

title = StringVar()
btn1 = StringVar()
choi = IntVar()
title.set("User Info Register")
btn1.set("Register")
choi.set(1)

Info_User1 = LabelFrame(RegisterUserI, borderwidth=0)
Info_User2 = LabelFrame(RegisterUserI, padx=20, pady=20)
Info_User3 = LabelFrame(RegisterUserI, padx=20, pady=5, borderwidth=0)

label1_regf = Label(Info_User1, text=title.get(), font=("algerian", 17))
label2_regf = Label(Info_User2, text="First Name", font=(None, 14))
label3_regf = Label(Info_User2, text="Last Name", font=(None, 14))
label4_regf = Label(Info_User2, text="Date of birth", padx=15, font=(None, 14))
label5_regf = Label(Info_User2, text="Gender", font=(None, 14), padx=15, pady=6)
label6_regf = Label(Info_User3, text="")

label1_regf.grid(row=0, column=0, columnspan=3)
label2_regf.grid(row=2, column=0)
label3_regf.grid(row=2, column=2)
label4_regf.grid(row=4, column=0)
label5_regf.grid(row=4, column=2)

dt1 = date.today()
genders = {"Male": "M", "Female": "F", "Other": None}
gen = StringVar()

entry1_regf = Entry(Info_User2, font=(None, 15), width=20, justify=CENTER)
entry2_regf = Entry(Info_User2, font=(None, 15), width=20, justify=CENTER)
entry3_regf = DateEntry(Info_User2, width=18, selectmode="day", justify="center",
                        font=(None, 15), maxdate=dt1)
entry4_regf = ttk.Combobox(Info_User2, values=list(genders.keys()),
                           width=17, height=96,
                           textvariable=gen, font=(None, 16))

entry1_regf.grid(row=3, column=0)
entry2_regf.grid(row=3, column=2, padx=15)
entry3_regf.grid(row=5, column=0)
entry4_regf.grid(row=5, column=2, padx=15)

button1_regf = Button(Info_User3, text=btn1.get(), font=(None, 13), command=usrinfo)
button2_regf = Button(Info_User3, text="Back", font=(None, 13), command=back1, state=DISABLED)

button2_regf.grid(row=0, column=0, padx=10)
label6_regf.grid(row=0, column=1, padx=170)
button1_regf.grid(row=0, column=2, padx=10)

Info_User1.pack(expand=True)
Info_User2.pack(expand=True)
Info_User3.pack(expand=True, anchor=E, padx=0)


# SIGN IN
SignIn = LabelFrame(root, padx=20, pady=5)

# signin.pack()


str1_sin = StringVar()
str2_sin = StringVar()

label1_sin = Label(SignIn, text="Email ID  :")
label2_sin = Label(SignIn, text="Password  :", pady=5)
label3_sin = Label(SignIn, text="Sign In", pady=15)
label1_sin.grid(row=1, column=0)
label2_sin.grid(row=2, column=0)
label3_sin.grid(row=0, column=0, columnspan=3)

entry1_sin = Entry(SignIn, textvariable=str1_sin, width=32)
entry2_sin = Entry(SignIn, textvariable=str2_sin, width=32, show="*")
entry1_sin.grid(row=1, column=2)
entry2_sin.grid(row=2, column=2)

button1_sin = Button(SignIn, text="Sign In", command=sinin, pady=3, anchor="center")
button2_sin = Button(SignIn, text="Register", command=reg)
button1_sin.grid(row=3, column=2, pady=10)
button2_sin.grid(row=3, column=0)

# PROFILE
main_label = LabelFrame(root)

profile = LabelFrame(main_label, padx=10, pady=10)
# frame 1
frame1 = LabelFrame(profile)

label1_prf = Label(frame1, text="Profile", width=28, font=("algerian", 18))
label1_prf.grid(row=0, column=0, columnspan=3)

frame1.grid(row=0, column=0)

# frame 2
frame2 = LabelFrame(profile, width=45)
frame2a = LabelFrame(frame2)
frame2b = LabelFrame(frame2)

label2_prf = Label(frame2a, text="First name :")
label3_prf = Label(frame2a, text="Last Name :")
label4_prf = Label(frame2a, text="Email ID :", anchor=W)
label5_prf = Label(frame2b, text="Gender :")
label6_prf = Label(frame2b, text="Age :")
label7_prf = Label(frame2b, text="DOB :")

label2_prf.grid(row=0, column=0)
label3_prf.grid(row=1, column=0)
label4_prf.grid(row=2, column=0)
label5_prf.grid(row=0, column=2)
label6_prf.grid(row=1, column=2)
label7_prf.grid(row=2, column=2)

label8_prf = Label(frame2a, text="")
label9_prf = Label(frame2a, text="")
labelA1_prf = Label(frame2a, text="", width=21)
labelA2_prf = Label(frame2b, text="", width=20)
labelA3_prf = Label(frame2b, text="")
labelA4_prf = Label(frame2b, text="")

label8_prf.grid(row=0, column=1)
label9_prf.grid(row=1, column=1)
labelA1_prf.grid(row=2, column=1)
labelA2_prf.grid(row=0, column=3)
labelA3_prf.grid(row=1, column=3)
labelA4_prf.grid(row=2, column=3)

frame2a.grid(row=0, column=0)
frame2b.grid(row=0, column=1)
frame2.grid(row=1, column=0)

# frame 1
frame3 = LabelFrame(profile)

labelA5_prf = Label(frame3, text="Family Info", width=47, font=(None, 12))
labelA6_prf = Label(frame3, text="")
tv = ttk.Treeview(frame3, height=10)

tv["column"] = ("First Name", "Last Name", "Gender", "Age")

tv.column("#0", width=10, minwidth=35, anchor=CENTER)
tv.column("First Name", width=120, anchor=CENTER)
tv.column("Last Name", width=120, anchor=CENTER)
tv.column("Gender", width=75, anchor=CENTER)
tv.column("Age", width=60, anchor=CENTER)

tv.heading("#0", text="no.")
tv.heading("First Name", text="First Name")
tv.heading("Last Name", text="Last Name")
tv.heading("Gender", text="Gender")
tv.heading("Age", text="Age")

up_tab()

labelA5_prf.pack(expand=True)
tv.pack(expand=True)
labelA6_prf.pack()
frame3.grid(row=2, column=0)

# frame 1
frame4 = LabelFrame(profile)
frame4a = LabelFrame(frame4, padx=8, pady=10)
frame4b = LabelFrame(frame4, padx=8, pady=10)

button1_prf = Button(frame4a, text="Update Profile", command=None)
button2_prf = Button(frame4a, text="Update member", command=up_user)
button3_prf = Button(frame4a, text="Delete member", command=del_user)
button4_prf = Button(frame4a, text="  Add member  ", command=addmem)

button5_prf = Button(frame4b, text="  Book Flight  ", command=Search)
button6_prf = Button(frame4b, text="   See Booking   ", command=chk_b)
button7_prf = Button(frame4b, text="Update Order", command=upod)
button8_prf = Button(frame4b, text="Cancel Booking", command=clbk)

button1_prf.grid(row=0, column=0, padx=5)
button2_prf.grid(row=0, column=1)
button3_prf.grid(row=1, column=0, padx=5, pady=5)
button4_prf.grid(row=1, column=1)
button5_prf.grid(row=0, column=0, padx=5)
button6_prf.grid(row=0, column=1)
button7_prf.grid(row=1, column=0, padx=5, pady=5)
button8_prf.grid(row=1, column=1)

frame4a.grid(row=0, column=0)
frame4b.grid(row=0, column=1)
frame4.grid(row=3, column=0)

profile.pack(expand=True)

UpdateUser = LabelFrame(root)

title1 = StringVar()
btn1a = StringVar()
choi1 = IntVar()
title1.set("Update user")
btn1a.set("Update")
choi1.set(1)

Info_User1a = LabelFrame(UpdateUser, borderwidth=0)
Info_User2b = LabelFrame(UpdateUser, padx=20, pady=20)
Info_User3c = LabelFrame(UpdateUser, padx=20, pady=5, borderwidth=0)

label1_updt = Label(Info_User1a, text=title1.get(), font=("algerian", 17))
label2_updt = Label(Info_User2b, text="First Name", font=(None, 14))
label3_updt = Label(Info_User2b, text="Last Name", font=(None, 14))
label4_updt = Label(Info_User2b, text="Date of birth", padx=15, font=(None, 14))
label5_updt = Label(Info_User2b, text="Gender", font=(None, 14), padx=15, pady=6)
label6_updt = Label(Info_User3c, text="")

label1_updt.grid(row=0, column=0, columnspan=3)
label2_updt.grid(row=2, column=0)
label3_updt.grid(row=2, column=2)
label4_updt.grid(row=4, column=0)
label5_updt.grid(row=4, column=2)

dt1 = date.today()
genders = {"Male": "M", "Female": "F", "Other": None}
gen1 = StringVar()

entry1_updt = Entry(Info_User2b, font=(None, 15), width=20, justify=CENTER)
entry2_updt = Entry(Info_User2b, font=(None, 15), width=20, justify=CENTER)
entry3_updt = DateEntry(Info_User2b, width=18, selectmode="day", justify="center",
                        font=(None, 15), maxdate=dt1)
entry4_updt = ttk.Combobox(Info_User2b, values=list(genders.keys()),
                           width=17, height=96,
                           textvariable=gen1, font=(None, 16))

entry1_updt.grid(row=3, column=0)
entry2_updt.grid(row=3, column=2, padx=15)
entry3_updt.grid(row=5, column=0)
entry4_updt.grid(row=5, column=2, padx=15)

button1_updt = Button(Info_User3c, text=btn1a.get(), font=(None, 13), command=updt_f, anchor=E)
button2_updt = Button(Info_User3c, text="Back", font=(None, 13), command=back1)

button2_updt.grid(row=0, column=0, padx=10)
label6_updt.grid(row=0, column=1, padx=170)
button1_updt.grid(row=0, column=2, padx=10)

Info_User1a.pack(expand=True)
Info_User2b.pack(expand=True)
Info_User3c.pack(expand=True, anchor=E, padx=0)

# SEARCH
T_search = LabelFrame(root)
search = LabelFrame(T_search, padx=7, pady=10)
# search.pack()


F1_srch = LabelFrame(search, padx=129)
F2_srch = LabelFrame(search, padx=48)
F3_srch = LabelFrame(search, padx=7, pady=10)
F4_srch = LabelFrame(search)

typ = IntVar()
typ.set("1")

radio1 = Radiobutton(F2_srch, text="One Way", variable=typ, value=1)
radio2 = Radiobutton(F2_srch, text="Round Trip", variable=typ, value=2)
radio3 = Radiobutton(F2_srch, text="Multi City", variable=typ, value=3)
radio1.grid(row=1, column=2)
radio2.grid(row=1, column=3)
radio3.grid(row=1, column=4)

label1_srch = Label(F3_srch, text="From")
label2_srch = Label(F3_srch, text="To")
label3_srch = Label(F3_srch, text="Departure Date")
label4_srch = Label(F3_srch, text="Return date")
label5_srch = Label(F3_srch, text="Passenger(s) & extra seat(s)")
label6_srch = Label(F3_srch, text="Pay in (Currency)")
label7_srch = Label(F1_srch, text="Search", anchor="center", font=("algerian", 15))
label8_srch = Label(F4_srch, text="", padx=56)

label1_srch.grid(row=3, column=2)
label2_srch.grid(row=3, column=4)
label3_srch.grid(row=5, column=2)
label4_srch.grid(row=5, column=4)
label5_srch.grid(row=7, column=2)
label6_srch.grid(row=7, column=4)
label7_srch.grid(row=0, column=2, pady=10, columnspan=3)
label8_srch.grid(row=9, column=2)

print(get_ports("*"))
dct = tuple(map(lambda x: x[1], get_ports("*")))
print(dct)

t6 = StringVar()
fr = StringVar()
ds = StringVar()
t6.set("Indian Rupees")
currency = tuple(map(lambda x: x[1], get_cur()))

dt1 = date.today()

entry_srch1 = ttk.Combobox(F3_srch, values=dct, width=10, height=96,
                           textvariable=fr, font=(None, 16), justify="center")
entry_srch2 = ttk.Combobox(F3_srch, values=dct, width=10, height=96,
                           textvariable=ds, font=(None, 16), justify="center")
entry_srch3 = DateEntry(F3_srch, width=9, selectmode="day", justify="center",
                        font=(None, 17), mindate=dt1)
entry_srch4 = DateEntry(F3_srch, width=9, selectmode="day", justify="center",
                        font=(None, 17), mindate=dt1)
entry_srch5 = Button(F3_srch, text="select", width=12, height=1, bg="white",
                     font=(None, 14), command=select_f)
entry_srch6 = ttk.Combobox(F3_srch, values=currency, width=14, height=15,
                           textvariable=t6, font=(None, 12))

entry_srch1.grid(row=4, column=2, padx=10)
entry_srch2.grid(row=4, column=4, padx=10)
entry_srch3.grid(row=6, column=2)
entry_srch4.grid(row=6, column=4)
entry_srch5.grid(row=8, column=2)
entry_srch6.grid(row=8, column=4)

button1_srch = Button(F4_srch, text="Search Flights",
                      command=srch,
                      width=20, height=2, bg="blue",
                      foreground="white",
                      font=("bold", 8)
                      )

button1_srch.grid(row=9, column=4, padx=10, sticky=E)
button2_srch = Button(F4_srch, text="Back",
                      font=(None, 13),
                      command=back2)

button2_srch.grid(row=9, column=1, padx=10)

# T_search.pack(expand=True)
search.pack(expand=True)

F1_srch.grid(row=1, column=1, columnspan=4)
F2_srch.grid(row=2, column=1, columnspan=4)
F3_srch.grid(row=3, column=1, columnspan=4)
F4_srch.grid(row=4, column=1, columnspan=4)

F_search = LabelFrame(root)

F1_srchf = LabelFrame(F_search, pady=10)
F2_srchf = LabelFrame(F_search, padx=4, pady=10)
F3_srchf = LabelFrame(F_search, padx=10, pady=10)

label1_srchf = Label(F1_srchf, text="Available flights", font=("algerian", 15), padx=185)
label2_srchf = Label(F3_srchf, text="", padx=150)

tv2 = ttk.Treeview(F2_srchf, height=10)
srb = ttk.Scrollbar(F2_srchf, orient="vertical", command=tv2.yview)
tv2.configure(xscrollcommand=srb.set)
srb.pack(side="right", fill="both")

tv2["column"] = ("Flight Name", "From", "To", "Departure", "Fare",
                 "Departure Time", "Destination Time", "Duration")

tv2.column("#0", width=6, minwidth=35, anchor=CENTER)
tv2.column("Flight Name", width=75, anchor=CENTER)
tv2.column("From", width=50, anchor=CENTER)
tv2.column("To", width=50, anchor=CENTER)
tv2.column("Departure", width=70, anchor=CENTER)
tv2.column("Fare", width=47, anchor=CENTER)
tv2.column("Departure Time", width=76, anchor=CENTER)
tv2.column("Destination Time", width=76, anchor=CENTER)
tv2.column("Duration", width=86, anchor=CENTER)

tv2.heading("#0", text="no.")
tv2.heading("Flight Name", text="Flight Name")
tv2.heading("From", text="From")
tv2.heading("To", text="To")
tv2.heading("Departure", text="Departure")
tv2.heading("Fare", text="Fare")
tv2.heading("Departure Time", text="Dep Time")
tv2.heading("Destination Time", text="Des Time")
tv2.heading("Duration", text="Duration")

button1_srchf = Button(F3_srchf, text="Back", font=("bold", 15), command=back3)
button2_srchf = Button(F3_srchf, text=" Book ", font=("bold", 15), command=book)

label1_srchf.pack()
button1_srchf.grid(row=0, column=0, padx=25)
label2_srchf.grid(row=0, column=1)
button2_srchf.grid(row=0, column=2, padx=25)
# up_tab2()
tv2.pack()
F1_srchf.pack()
F2_srchf.pack()
F3_srchf.pack()

P_main = LabelFrame(root)

Frame1_pln = LabelFrame(P_main)
Frame2_pln = LabelFrame(P_main)
Frame2_pln_a = LabelFrame(Frame2_pln)
Frame2_pln_b = LabelFrame(Frame2_pln)
Frame3_pln = LabelFrame(P_main, padx=8, pady=4)
Frame4_pln = LabelFrame(P_main)
Frame5_pln = LabelFrame(P_main, padx=110, pady=10)

label1_pln = Label(Frame1_pln, text="Reservation", width=31, font=("algerian", 18))
label1_pln.grid(row=0, column=0, columnspan=3)

label2_pln = Label(Frame2_pln_a, text="Plane Name :")
label3_pln = Label(Frame2_pln_a, text="       From     :")
label4_pln = Label(Frame2_pln_a, text="        To       :", anchor=W)
label5_pln = Label(Frame2_pln_b, text=" Departure       :")
label6_pln = Label(Frame2_pln_b, text=" Depart Time  :")
label7_pln = Label(Frame2_pln_b, text="Duration        :")

label2_pln.grid(row=0, column=0)
label3_pln.grid(row=1, column=0)
label4_pln.grid(row=2, column=0)
label5_pln.grid(row=0, column=2)
label6_pln.grid(row=1, column=2)
label7_pln.grid(row=2, column=2)

label8_pln = Label(Frame2_pln_a, text="")
label9_pln = Label(Frame2_pln_a, text="")
labelA1_pln = Label(Frame2_pln_a, text="", width=21)
labelA2_pln = Label(Frame2_pln_b, text="", width=20)
labelA3_pln = Label(Frame2_pln_b, text="")
labelA4_pln = Label(Frame2_pln_b, text="")

label8_pln.grid(row=0, column=1)
label9_pln.grid(row=1, column=1)
labelA1_pln.grid(row=2, column=1)
labelA2_pln.grid(row=0, column=3)
labelA3_pln.grid(row=1, column=3)
labelA4_pln.grid(row=2, column=3)

labelB2_pln = Label(Frame3_pln, text="Passengers", font=("Consolas", 18))
labelB3_pln = Label(Frame3_pln, text="Orders", font=("Consolas", 18))
labelB2_pln.grid(row=0, column=0)
labelB3_pln.grid(row=0, column=1)

tv4 = ttk.Treeview(Frame3_pln, height=8)

tv4["column"] = ("First Name", "Last Name")

tv4.column("#0", width=10, minwidth=35, anchor=CENTER)
tv4.column("First Name", width=120, anchor=CENTER)
tv4.column("Last Name", width=120, anchor=CENTER)

tv4.heading("#0", text="no.")
tv4.heading("First Name", text="First Name")
tv4.heading("Last Name", text="Last Name")

tv4.grid(row=1, column=0, padx=2)

tv5 = ttk.Treeview(Frame3_pln, height=8)

tv5["column"] = ("Item", "Qty", "Cost")

tv5.column("#0", width=10, minwidth=35, anchor=CENTER)
tv5.column("Item", width=120, anchor=CENTER)
tv5.column("Qty", width=40, anchor=CENTER)
tv5.column("Cost", width=85, anchor=CENTER)

tv5.heading("#0", text="no.")
tv5.heading("Item", text="Item")
tv5.heading("Qty", text="Qty")
tv5.heading("Cost", text="Cost")

tv5.grid(row=1, column=1, padx=2)

labelA5_pln = Label(Frame4_pln, text="Total Flight Fare :",
                    font=("Century Gothic", 14))
labelA6_pln = Label(Frame4_pln, text="Total Order Fare  :",
                    font=("Century Gothic", 14))
labelA9_pln = Label(Frame4_pln, text="Grand Total :",
                    font=("Century Gothic", 14))
labelA7_pln = Label(Frame4_pln, text="", width=12)
labelA8_pln = Label(Frame4_pln, text="", width=12)
labelB1_pln = Label(Frame4_pln, text="")

labelA5_pln.grid(row=0, column=0)
labelA6_pln.grid(row=0, column=2)
labelA7_pln.grid(row=0, column=1)
labelA8_pln.grid(row=0, column=4)
labelA9_pln.grid(row=1, column=1)
labelB1_pln.grid(row=1, column=2, columnspan=2)

button1_pln = Button(Frame5_pln, text='Back', font=(None, 10), command=back4)
button2_pln = Button(Frame5_pln, text='Order', font=(None, 10), command=select_o)
button3_pln = Button(Frame5_pln, text='Reserve', font=(None, 10), command=c_reserve)

button1_pln.grid(row=0, column=0)
button2_pln.grid(row=0, column=1, padx=85)
button3_pln.grid(row=0, column=2)

inf_update()
up_tab4()

Frame1_pln.pack()
Frame2_pln.pack()
Frame2_pln_a.grid(row=0, column=0)
Frame2_pln_b.grid(row=0, column=1)
Frame3_pln.pack()
Frame4_pln.pack()
Frame5_pln.pack()

R_main = LabelFrame(root, padx=10, pady=10)

F1_res = LabelFrame(R_main)
F2_res = LabelFrame(R_main)
F3_res = LabelFrame(R_main)

lableB3_res = Label(F1_res, text="", font=("algerian", 18))
lableB3_res.pack()

tv8 = ttk.Treeview(F2_res, height=10)
srb8 = ttk.Scrollbar(F2_res, orient="vertical", command=tv8.yview)
tv8.configure(xscrollcommand=srb8.set)
srb8.grid(row=0, column=1)

tv8["column"] = ("Flight Name", "From", "To", "Departure", "Departure Time",
                 "Seats")

tv8.column("#0", width=6, minwidth=35, anchor=CENTER)
tv8.column("Flight Name", width=75, anchor=CENTER)
tv8.column("From", width=50, anchor=CENTER)
tv8.column("To", width=50, anchor=CENTER)
tv8.column("Departure", width=70, anchor=CENTER)
tv8.column("Departure Time", width=90, anchor=CENTER)
tv8.column("Seats", width=80, anchor=CENTER)

tv8.heading("#0", text="no.")
tv8.heading("Flight Name", text="Flight Name")
tv8.heading("From", text="From")
tv8.heading("To", text="To")
tv8.heading("Departure", text="Departure")
tv8.heading("Departure Time", text="Dep Time")
tv8.heading("Seats", text="Seats")

tv8.grid(row=0, column=0)
up_tab8()

button1_res = Button(F3_res, text="Back", height=3,
                     width=10, command=back5)
button2_res = Button(F3_res, text="Check Reservation", height=3,
                     width=50, command=check_res)
button3_res = Button(F3_res, text="Update Order", height=3,
                     width=50, command=udt_res_or)
button4_res = Button(F3_res, text="Cancel Reservation", height=3,
                     width=50, command=del_res)

button1_res.pack(side="left")
F1_res.pack()
F2_res.pack()
F3_res.pack(side="left", pady=5)


root.mainloop()
