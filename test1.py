from moc_data import mock_data


me = {
    "name": "Martin",
    "last": "Avelar",
    "age": 35,
    "hobbies": [],
    "address": {
        "street": "Evergreen",
        "city": "Springfield",
    }
}

print(me["name"]+ " " + me["last"])

# print full name

#print city
print(me["address"]["city"])

#modify existing
me["age"] = 36

# creat new variable
me["new"] = 1
print(me)






# list

names = []

names.append("Guillermo")
names.append("Jake")
names.append("Krystle")

print(names)

#get elements
print(names[0])
print(names[2])

# for loop
for name in names:
    print(name)






    ages = [12,32,456,10,23,678,4356,2,46,789,23,67,13]

# 1- youngest
# Create variables with the first (0 any) number from the list
#travel the list and compare each number with your variable
# if find a younger, update your variable to be that number
#print the variable

youngest = ages[-1]
for age in ages:
    if age < youngest:
        youngest = age

print(youngest)


#print the title for every product
# travel mock_data list
# get and print the little from the porduct (dict)

for item in mock_data:
    print(item["title"])
