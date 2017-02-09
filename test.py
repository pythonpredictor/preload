from applist import applist

a = applist()
a.load_app("google maps")
a.load_app("facebook")
for i in range(0, 10):
    a.load_app("emails")
a.get_result("test.csv", 10)