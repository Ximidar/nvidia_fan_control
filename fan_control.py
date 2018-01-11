import os
import subprocess
import json
import time

class Fan_Control(object):
  def __init__(self):
    super(Fan_PID, self).__init__()
    self.initialize_gpu_fan_control()
    self.monitor_gpus()

  def get_fan_speed(self):
    return self.get_gpu_output("nvidia-smi --query-gpu=fan.speed --format=csv,noheader,nounits")

  def get_temps(self):
    return self.get_gpu_output("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits")

  def set_fan_speed(self, gpu, speed):
    p = self.get_gpu_output("nvidia-settings -a [fan:" + str(gpu) +"]/GPUTargetFanSpeed=" + str(speed))
    return

  def initialize_gpu_fan_control(self):
    temps = self.get_temps()
    num_gpus = len(temps)
    for x in range(num_gpus):
      output = self.get_gpu_output("nvidia-settings -a [gpu:" + str(x) + "]/GPUFanControlState=1")
      print(output)

  def monitor_gpus(self):
    while True:
      temps = self.get_temps()

      for gpu in temps:
        temp = int(temps[gpu])
        gpu_num = int(gpu)
        if temp < 50:
          self.set_fan_speed(gpu_num, 55)
        elif temp in range(50, 64):
          self.set_fan_speed(gpu_num, 65)
        elif temp in range(65, 74):
          self.set_fan_speed(gpu_num, 70)
        elif temp > 75:
          self.set_fan_speed(gpu_num, 100)

      time.sleep(1)
      speeds = self.get_fan_speed()
      output = ""
      num_of_gpus = len(speeds)
      for gpu in range(num_of_gpus):
        output += "GPU" + str(gpu) + " fan:" + str(speeds[str(gpu)]) + " temp " + str(temps[str(gpu)]) + "\t"
      print(output)
      time.sleep(10)

  def get_gpu_output(self, command):
    temp_p = subprocess.Popen(command,
    stdout=subprocess.PIPE,
    shell=True
    )
    output, error = temp_p.communicate()
    p_status = temp_p.wait()

    gpu_num = 0
    gpu_output = {}
    temp_arr = output.splitlines()
    for temp in temp_arr:
      gpu_output[str(gpu_num)] = temp
      gpu_num += 1
    return gpu_output

  def print_dict(self, obj):
    print(json.dumps(obj, indent=4))

Fan_Control()
