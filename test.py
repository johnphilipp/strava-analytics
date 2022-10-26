from datetime import datetime


epoch = round((datetime.now() - datetime(1970, 1, 1)).total_seconds())
print(epoch)
print("boom")
