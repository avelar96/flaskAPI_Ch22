

# 1
print("Martin Avelar")


# 2 a for loop
for i in range(30, 71):
    print(i)


# Working with files
#
file_read = open("notes.txt", "r")
all_lines = file_read.readlines()
print(f"There are {len(all_lines)} lines in the file")
file_read.close()

# create a new file
test = open("demo.txt", "w")  # mode w = write
test.write("Hello from python\n")
test.write("This should be a second line\n")
test.write("\n")
test.close()

# write a line in the bottom of notes.txt
notes = open("notes.txt", "a")
notes.write("\n***This text was added with Python code")
notes.close()

