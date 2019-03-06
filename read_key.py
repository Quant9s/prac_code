file = open('key.key', 'rb')

key = file.read()
file.close()

print(key)