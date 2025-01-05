print("for:- (in):")
def overlapping(list1, list2):
    for i in list1:
        for j in list2:
            if i == j:
                return 1  # Return 1 if there is any match
    return 0  # Return 0 if no match is found

def main():
    list1 = [1, 2, 3, 4, 5]
    list2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    if overlapping(list1, list2):
        print("overlapping")
    else:
        print("not overlapping")

if __name__ == "__main__":
    main()

print("For:- (not in):")

def main():
    x = 14
    my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    if x not in my_list:
        print("not overlapping")
    else:
        print("overlapping")

if __name__ == "__main__":
    main()
