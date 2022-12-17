from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import connection
from django.urls import reverse

# Create your views here.
def display_products(request):
    outputProducts = []

    return render(request, 'myApp/index.html', {"products": outputProducts})


# Create Table
def create_table(request):
    with connection.cursor() as cursor:
        create_product_query = "CREATE TABLE Product (maker CHAR(1),model INT PRIMARY KEY,type VARCHAR(20));";
        create_pc_query = "CREATE TABLE PC (model INT PRIMARY KEY,speed NUMERIC(3,2),ram INT,hd INT,price INT);";
        create_laptop_query = "CREATE TABLE Laptop (model INT PRIMARY KEY,speed NUMERIC(3,2),ram INT,hd INT,screen NUMERIC(3,1),price INT);"
        create_printer_query = "CREATE TABLE Printer (model INT PRIMARY KEY,color VARCHAR(20),type VARCHAR(20),price INT);"
        cursor.execute(create_product_query)
        cursor.execute(create_pc_query)
        cursor.execute(create_laptop_query)
        cursor.execute(create_printer_query)
        connection.commit()
        connection.close()

    return HttpResponseRedirect(reverse('display_products'))


# Insert Data
def insert_data(request):
    with connection.cursor() as cursor:
        insert_product_data = "INSERT INTO Product (maker,model,type)" \
                              "VALUES ('A',1001,'pc')," \
                              "('A',1002,'pc')," \
                              "('A',1003,'pc')," \
                              "('A',2004,'laptop')," \
                              "('A',2005,'laptop')," \
                              "('A',2006,'laptop')," \
                              "('B',1004,'pc')," \
                              "('B',1005,'pc')," \
                              "('B',1006,'pc')," \
                              "('B',2007,'laptop')," \
                              "('C',1007,'pc')," \
                              "('D',1008,'pc')," \
                              "('D',1009,'pc')," \
                              "('D',1010,'pc')," \
                              "('D',3004,'printer')," \
                              "('D',3005,'printer')," \
                              "('E',1011,'pc')," \
                              "('E',1012,'pc')," \
                              "('E',1013,'pc')," \
                              "('E',2001,'laptop')," \
                              "('E',2002,'laptop')," \
                              "('E',2003,'laptop')," \
                              "('E',3001,'printer')," \
                              "('E',3002,'printer')," \
                              "('E',3003,'printer')," \
                              "('F',2008,'laptop')," \
                              "('F',2009,'laptop')," \
                              "('G',2010,'laptop')," \
                              "('H',3006,'printer')," \
                              "('H',3007,'printer');"

        insert_pc_data = "INSERT INTO PC (model,speed,ram,hd,price)" \
                              "VALUES (1001,2.66,1024,250,2114)," \
                              "(1002,2.10,512,250,995)," \
                              "(1003,1.42,512,80,478)," \
                              "(1004,2.80,1024,250,649)," \
                              "(1005,3.20,512,250,630)," \
                              "(1006,3.20,1024,320,1049)," \
                              "(1007,2.20,1024,200,510)," \
                              "(1008,2.20,2048,250,770)," \
                              "(1009,2.00,1024,250,650)," \
                              "(1010,2.80,2048,300,770)," \
                              "(1011,1.86,2048,160,959)," \
                              "(1012,2.80,1024,160,649)," \
                              "(1013,3.06,512,80,529);"

        insert_laptop_data = "INSERT INTO Laptop (model,speed,ram,hd,screen,price)" \
                             "VALUES (2001,2.00,2048,240,20.1,3673)," \
                             "(2002,1.73,1024,80,17.0,949)," \
                             "(2003,1.80,512,60,15.4,549)," \
                             "(2004,2.00,2048,80,15.4,1700)," \
                             "(2005,2.16,1024,120,17.0,2500)," \
                             "(2006,2.00,2048,80,15.4,1700)," \
                             "(2007,1.83,1024,120,13.3,1429)," \
                             "(2008,1.60,1024,100,15.4,900)," \
                             "(2009,1.60,512,80,14.1,680)," \
                             "(2010,2.00,2048,160,15.4,2300);"

        insert_printer_data = "INSERT INTO Printer (model,color,type,price)" \
                              "VALUES (3001,'true','ink-jet',99)," \
                              "(3002,'false','laser',239)," \
                              "(3003,'true','laser',899)," \
                              "(3004,'true','ink-jet',120)," \
                              "(3005,'false','laser',120)," \
                              "(3006,'true','ink-jet',100)," \
                              "(3007,'true','laser',200);"

        cursor.execute(insert_product_data)
        cursor.execute(insert_pc_data)
        cursor.execute(insert_laptop_data)
        cursor.execute(insert_printer_data)

        connection.commit()
        connection.close()

    return HttpResponseRedirect(reverse('display_products'))


def first_query(request):
    with connection.cursor() as cursor:
        query = "SELECT AVG(hd) FROM PC"
        cursor.execute(query)
        avg_hd = cursor.fetchall()
        connection.close()
        print(avg_hd)

    return render(request, 'myApp/firstquery.html', {"avg_hd": avg_hd})


def second_query(request):
    with connection.cursor() as cursor:
        query = "SELECT maker,AVG(speed) FROM Product,PC WHERE Product.model = PC.model GROUP BY maker"
        cursor.execute(query)
        avg_speed = cursor.fetchall()
        connection.close()
        print(avg_speed)

    return render(request, 'myApp/index.html', {"avg_speed": avg_speed})


def third_query(request):
    with connection.cursor() as cursor:
        query = """SELECT t1.maker, t1.price
                            FROM
                            (SELECT maker, price FROM Product,Laptop
                            WHERE Product.model = Laptop.model) AS t1,
                            (SELECT maker FROM Product
                            WHERE type = 'laptop' GROUP BY maker HAVING COUNT(maker) = 1) AS t2
                            WHERE t1.maker = t2.maker"""
        cursor.execute(query)
        laptop_price = cursor.fetchall()
        connection.close()
        print(laptop_price)

    return render(request, 'myApp/index.html', {"laptop_price": laptop_price})


def fourth_query(request):
    with connection.cursor() as cursor:
        query = """SELECT p1.maker,p2.model,p1.price
                            FROM
                            (SELECT p1.maker,MAX(p2.price) AS price
                            FROM Printer p2
                            JOIN Product p1 WHERE (p1.model = p2.model)
                            GROUP BY p1.maker) AS p1,Printer p2
                            WHERE p1.price = p2.price"""
        cursor.execute(query)
        printer_info = cursor.fetchall()
        connection.close()
        print(printer_info)

    return render(request, 'myApp/index.html', {"printer_info": printer_info})
