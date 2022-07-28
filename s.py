num = int(input("Enter number of servers: "))
print("Enter names of {num} servers below:".format(num=num))
names = [input() for i in range(num)]
print(names)