import sqlite3

conn = sqlite3.connect("meal.db")
cur = conn.cursor()
cur.execute("PRAGMA table_info(students)")
print(cur.fetchall())

# Remove old student data
cur.execute("DELETE FROM students")


students = [

# Class 1 : 7 Girls + 2 Boys
("S001","A. Abinaya","1","9000000001","Button Phone","Girl"),
("S002","K. Harini","1","9000000002","Button Phone","Girl"),
("S003","R. Nivetha","1","9000000003","Smartphone","Girl"),
("S004","M. Keerthana","1","9000000004","Smartphone","Girl"),
("S005","P. Kavya","1","9000000005","Smartphone","Girl"),
("S006","S. Divya","1","9000000006","Smartphone","Girl"),
("S007","T. Ananya","1","9000000007","Smartphone","Girl"),
("S008","V. Arun","1","9000000008","Smartphone","Boy"),
("S009","R. Kavin","1","9000000009","Smartphone","Boy"),


# Class 2 : 8 Boys + 2 Girls
("S010","A. Akash","2","9000000010","Smartphone","Boy"),
("S011","K. Ajay","2","9000000011","Smartphone","Boy"),
("S012","M. Bharath","2","9000000012","Smartphone","Boy"),
("S013","P. Dinesh","2","9000000013","Smartphone","Boy"),
("S014","R. Gokul","2","9000000014","Smartphone","Boy"),
("S015","S. Hari","2","9000000015","Smartphone","Boy"),
("S016","T. Karthik","2","9000000016","Smartphone","Boy"),
("S017","V. Praveen","2","9000000017","Smartphone","Boy"),
("S018","R. Priya","2","9000000018","Smartphone","Girl"),
("S019","K. Swetha","2","9000000019","Smartphone","Girl"),


# Class 3 : 1 Boy + 2 Girls
("S020","R. Rahul","3","9000000020","Smartphone","Boy"),
("S021","M. Pavithra","3","9000000021","Smartphone","Girl"),
("S022","P. Aarthi","3","9000000022","Smartphone","Girl"),


# Class 4 : 2 Boys + 2 Girls
("S023","S. Sanjay","4","9000000023","Smartphone","Boy"),
("S024","K. Naveen","4","9000000024","Smartphone","Boy"),
("S025","A. Deepika","4","9000000025","Smartphone","Girl"),
("S026","V. Janani","4","9000000026","Smartphone","Girl"),


# Class 5 : 6 Boys + 4 Girls
("S027","R. Vishal","5","9000000027","Smartphone","Boy"),
("S028","S. Gokul","5","9000000028","Smartphone","Boy"),
("S029","P. Manoj","5","9000000029","Smartphone","Boy"),
("S030","K. Karthik","5","9000000030","Smartphone","Boy"),
("S031","M. Bharath","5","9000000031","Smartphone","Boy"),
("S032","A. Rohit","5","9000000032","Smartphone","Boy"),
("S033","A. Kavya","5","9000000033","Smartphone","Girl"),
("S034","T. Meena","5","9000000034","Smartphone","Girl"),
("S035","N. Riya","5","9000000035","Smartphone","Girl"),
("S036","P. Harini","5","9000000036","Smartphone","Girl"),


# Class 6 : 6 Boys + 8 Girls
("S037","V. Ashwin","6","9000000037","Smartphone","Boy"),
("S038","N. Kishore","6","9000000038","Smartphone","Boy"),
("S039","R. Naveen","6","9000000039","Smartphone","Boy"),
("S040","M. Vinoth","6","9000000040","Smartphone","Boy"),
("S041","K. Sathish","6","9000000041","Smartphone","Boy"),
("S042","P. Saravanan","6","9000000042","Smartphone","Boy"),
("S043","A. Abinaya","6","9000000043","Smartphone","Girl"),
("S044","K. Dharshini","6","9000000044","Smartphone","Girl"),
("S045","S. Monisha","6","9000000045","Smartphone","Girl"),
("S046","R. Lakshmi","6","9000000046","Smartphone","Girl"),
("S047","M. Ramya","6","9000000047","Smartphone","Girl"),
("S048","G. Shalini","6","9000000048","Smartphone","Girl"),
("S049","T. Varshini","6","9000000049","Smartphone","Girl"),
("S050","D. Nandhini","6","9000000050","Smartphone","Girl"),
# Class 7 : 10 Boys + 4 Girls

("S051","R. Aravind","7","9000000051","Smartphone","Boy"),
("S052","M. Prakash","7","9000000052","Smartphone","Boy"),
("S053","V. Ramesh","7","9000000053","Smartphone","Boy"),
("S054","T. Senthil","7","9000000054","Smartphone","Boy"),
("S055","N. Yuvan","7","9000000055","Smartphone","Boy"),
("S056","S. Mithun","7","9000000056","Smartphone","Boy"),
("S057","K. Jeeva","7","9000000057","Smartphone","Boy"),
("S058","M. Madhan","7","9000000058","Smartphone","Boy"),
("S059","P. Vimal","7","9000000059","Smartphone","Boy"),
("S060","A. Kiran","7","9000000060","Smartphone","Boy"),

("S061","R. Ananya","7","9000000061","Smartphone","Girl"),
("S062","S. Akshaya","7","9000000062","Smartphone","Girl"),
("S063","K. Reshma","7","9000000063","Smartphone","Girl"),
("S064","M. Vaishnavi","7","9000000064","Smartphone","Girl"),


# Class 8 : 12 Boys + 8 Girls

("S065","P. Vijay","8","9000000065","Smartphone","Boy"),
("S066","S. Karthik","8","9000000066","Smartphone","Boy"),
("S067","R. Naveen","8","9000000067","Smartphone","Boy"),
("S068","M. Rahul","8","9000000068","Smartphone","Boy"),
("S069","A. Vignesh","8","9000000069","Smartphone","Boy"),
("S070","K. Surya","8","9000000070","Smartphone","Boy"),
("S071","T. Hari","8","9000000071","Smartphone","Boy"),
("S072","V. Ajay","8","9000000072","Smartphone","Boy"),
("S073","N. Lokesh","8","9000000073","Smartphone","Boy"),
("S074","P. Gokul","8","9000000074","Smartphone","Boy"),
("S075","M. Dinesh","8","9000000075","Smartphone","Boy"),
("S076","R. Vinoth","8","9000000076","Smartphone","Boy"),

("S077","A. Nivetha","8","9000000077","Smartphone","Girl"),
("S078","V. Sneha","8","9000000078","Smartphone","Girl"),
("S079","G. Krithika","8","9000000079","Smartphone","Girl"),
("S080","T. Ishwarya","8","9000000080","Smartphone","Girl"),
("S081","D. Preethi","8","9000000081","Smartphone","Girl"),
("S082","N. Sindhu","8","9000000082","Smartphone","Girl"),
("S083","K. Kowsalya","8","9000000083","Smartphone","Girl"),
("S084","R. Sangeetha","8","9000000084","Smartphone","Girl"),

]

cur.executemany("""
INSERT INTO students
(student_id,name,class,phone,phone_type,gender)
VALUES(?,?,?,?,?,?)
""", students)


conn.commit()
conn.close()

print("84 Students Added Successfully")