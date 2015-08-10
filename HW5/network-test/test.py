
import ast

#
# import csv
#
# input = ['abc,"a string, with a comma","another, one"']
# parser = csv.reader(input)
#
# for fields in parser:
#     for i,f in enumerate(fields):
#          print f


msg = ast.literal_eval("['1',2,'haha']")


# print msg
#
#
# for item in msg:
#     print type(item)


a = "my name is,Bob"

print a.split()

b = "GET"
print b.split()

