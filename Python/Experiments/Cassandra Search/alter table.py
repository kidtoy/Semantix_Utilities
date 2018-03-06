list = ["semantix","bradesco","pernambucanas","claro"]

for l in list:
    print "alter table "+l+".campaign drop sense_time_end;"
    print "alter table "+l+".campaign drop sense_time_start;"
    print "alter table "+l+".campaign add sense_time_end smallint;"
    print "alter table "+l+".campaign add sense_time_start smallint;"
