
# Run to check tensorflow devices

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())
