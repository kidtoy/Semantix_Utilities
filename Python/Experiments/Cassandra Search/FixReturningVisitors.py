list = (
           ("Loja Modelo","2017","8","23","returningVisitors","static","13"),
           ("Loja Modelo","2017","8","22","returningVisitors","static","4"),
           ("Loja Modelo","2017","8","21","returningVisitors","static","6"),
           ("Loja Modelo","2017","8","20","returningVisitors","static","19"),
           ("Loja Modelo","2017","8","19","returningVisitors","static","10"),
           ("Loja Modelo","2017","8","18","returningVisitors","static","9"),
           ("Loja Modelo","2017","8","17","returningVisitors","static","0"),
           ("Loja Modelo","2017","8","16","returningVisitors","static","5"),
           ("Loja Modelo","2017","8","15","returningVisitors","static","5"),
           ("Loja Modelo","2017","8","14","returningVisitors","percent","0")

)
company = "pernambucanas"

for i in list:
    print "INSERT INTO "+company+".analytics_day ( id_sensor , year , month , day , category , key , value) values('"+i.__getitem__(0)+"',"+i.__getitem__(1)+","+i.__getitem__(2)+","+i.__getitem__(3)+",'"+i.__getitem__(4)+"','"+i.__getitem__(5)+"',"+i.__getitem__(6)+");"

for i in list:
    print "DELETE from "+company+".analytics_day where id_sensor = '"+i.__getitem__(0)+"' and year = "+i.__getitem__(1)+" and month = "+i.__getitem__(2)+" and day = "+i.__getitem__(3)+" and category = '"+i.__getitem__(4)+"';"