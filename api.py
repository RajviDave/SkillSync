dict={"name":"rajvi","number":4,"surname":"dave","city":"rajkot"}
dic1={}

for dic in dict:
    
    if dic in dic1:
        print("noting")
    else:
        dic1[dic]=dict[dic]

print(dict)
print(dic1)

