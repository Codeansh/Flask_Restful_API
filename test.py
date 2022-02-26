import requests

base="http://127.0.0.1:5000/"

response=requests.put(base+"video/1",{"name":"cat", "views":29, "likes":1000})
data = response.json()
print(response,data)

input()

response=requests.put(base+"video/2",{"name":"dog", "views":879, "likes":167000})
data = response.json()
print(response,data)

input()

response=requests.put(base+"video/3",{"name":"rat", "views":264, "likes":100044})

data = response.json()

print(response,data)

input()

response=requests.get(base+"video/1")
data = response.json()
print(response,data)

response=requests.get(base+"video/2")
data = response.json()
print(response,data)


response=requests.patch(base+"video/3",{'likes':1})
data = response.json()

print(response,data)


# response=requests.delete(base+"video/3")
# data = response
# print(data)

# response=requests.delete(base+"video/3")
# data = response



#print(data)





