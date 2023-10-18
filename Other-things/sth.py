#Start
s1 = set()
s2 = set()
s3 = set()
state = True
#Prompt user to enter the name of animals in park 1 and enter 0 to move to park 2
while state:
    name = input("Enter an animal name and enter q to move to names of park 2:  ")
    if name == 'q':
        break
    else:
        s1.add(str(name))
while state:
    name = input("Enter names of animals in park2 and q to exit:  ")
    if name == 'q':
        break
    else:
        s2.add(str(name))



#Count the number of animals in park 1 and then in park 2
print(f"The number of animals in park 1 is: {len(s1)}")
print(f"The number of animals in park 2 is {len(s2)}")
#Questions
#Name of animals in both parks(union)
s3 = s1.union(s2)
print("The animals in both parks are: ")
for i in s3:
    print(i)
#Animals found in 2nd park only Difference(2-1)
print("The animals found in second park only are: ")
s3 = s2.difference(s1)
for i in s3:
    print(i)
#Animals found in 1 and 2 but not both (symmetric-difference)
print("The animals found in park 1 and 2 but not both are: ")
s3 = s1.symmetric_difference(s2)
for i in s3:
    print(i)