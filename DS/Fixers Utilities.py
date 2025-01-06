print('\n#3A part 1\n')
import datetime

print('#1 Removing leading or lagging spaces from a data entry');
baddata = "      Data     Science with too many spaces is bad!!! "
print('>',baddata,'<')
cleandata=baddata.strip()
print('>',cleandata,'<')

print('\n#3A Part 2\n')
import datetime

import string
print('#2 Removing nonprintable characters from a data entry')
printable = set(string.printable)
baddata = "Data\x00  Science with\x10 funny characters is \x10bad!!!"
cleandata=''.join(filter(lambda x: x in string.printable,baddata))
print('Bad Data : ',baddata);
print('Clean Data : ',cleandata)

print('\n#3A part 3\n')
import datetime
print('# 3 Reformatting data entry to match specific formatting criteria.')
baddate = datetime.date(2019, 10 , 30) 
baddata=format(baddate,'%Y-%m-%d') 
gooddate = datetime.datetime.strptime(baddata,'%Y-%m-%d') 
gooddata=format(gooddate,'%d %B %Y') 
print('Bad Data : ',baddata) 
print('Good Data : ',gooddata)
