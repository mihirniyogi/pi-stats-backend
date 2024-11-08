import psutil
import socket
import platform
import distro
import time
import subprocess
from datetime import datetime


### ----- CONSTANTS ----- ##
DECIMAL = 10




## ----- GENERAL STATS ----- ##

def get_gen_stats():
  check_strapi()
  return {
    "hostname": get_hostname(),
    "os_type": get_os_type(),
    "os_name": get_os_name(),
    "os_version": get_os_version(),
    "kernel_version": get_kernel_version(),
    "arch": get_arch()
  } | get_uptime()
  
def get_hostname():
  return socket.gethostname()

def get_os_type():
  return platform.system()

def get_os_name():
  return distro.name(pretty=True)

def get_os_version():
  return platform.release()

def get_kernel_version():
  return platform.version()

def get_arch():
  return platform.machine()

def get_uptime():
  current_time = time.time() # epoch -> now
  boot_time = psutil.boot_time() # epoch -> boot
  
  boot_datetime = datetime.fromtimestamp(boot_time).strftime('%d %B %Y %H:%M:%S')

  seconds_alive = current_time - boot_time

  days_alive = seconds_alive // 86400  # 86400 seconds in a day
  hours_alive = (seconds_alive % 86400) // 3600  # Remaining hours
  minutes_alive = (seconds_alive % 3600) // 60  # Remaining minutes
  seconds_alive = seconds_alive % 60  # Remaining seconds

  time_strings = ["seconds", "minutes", "hours", "days"]
  time_values = [seconds_alive, minutes_alive, hours_alive, days_alive]

  return {
    "last_boot": boot_datetime,
    "uptime": {time_strings[i]: time_values[i] for i in range(len(time_strings))}
  }






## ----- CPU STATS ----- ##

def get_cpu_stats():

  return {
    "cpu_usage": get_cpu_usage(),
    "cpu_temp": get_cpu_temp(),
    "cpu_freq": get_cpu_freq(),
    "cpu_count": get_cpu_count(),
    "cpu_usage_per_core": get_cpu_usage_per_core()
  }

def get_cpu_usage():
  return psutil.cpu_percent(interval=1)

def get_cpu_temp():
  temp = psutil.sensors_temperatures()["cpu_thermal"][0].current
  return temp
  
def get_cpu_freq():
  freq = psutil.cpu_freq()
  if not freq:
    return 0
  return freq.current

def get_cpu_count():
  return psutil.cpu_count(logical=True)

def get_cpu_usage_per_core():
  x = psutil.cpu_percent(interval=1, percpu=True)
  return {f"C{i+1}": x[i] for i in range(len(x))}





## ----- MEMORY STATS ----- ##

def get_mem_stats():
  mem = psutil.virtual_memory()
  return {
    "total": get_total_ram(mem),
    "used": get_used_ram(mem),
    "available": get_available_ram(mem),
    "free": get_free_ram(mem),
    "buffers": get_buffers_ram(mem),
    "cached": get_cached_ram(mem),
    "percent": get_percent_ram(mem)
  }

def get_total_ram(mem):
  return round(mem.total / 10 ** 9, DECIMAL)

def get_used_ram(mem):
  return round(mem.used / 10 ** 9, DECIMAL)

def get_available_ram(mem):
  return round(mem.available / 10 ** 9, DECIMAL)

def get_free_ram(mem):
  return round(mem.free / 10 ** 9, DECIMAL)

def get_buffers_ram(mem):
  return round(mem.buffers / 10 ** 9, DECIMAL)

def get_cached_ram(mem):
  return round(mem.cached / 10 ** 9, DECIMAL)

def get_percent_ram(mem):
  return mem.percent






## ----- DISK STATS ----- ##

def get_disk_stats():
  disk = psutil.disk_usage('/')
  return {
    "total": get_total_disk(disk),
    "used": get_used_disk(disk),
    "free": get_free_disk(disk),
    "percent": get_percent_disk(disk)
  }

def get_total_disk(disk):
  return round(disk.total / 10 ** 9, DECIMAL)

def get_used_disk(disk):
  return round(disk.used / 10 ** 9, DECIMAL)

def get_free_disk(disk):
  return round(disk.free / 10 ** 9, DECIMAL)

def get_percent_disk(disk):
  return disk.percent







## ----- SERVICES STATS ----- ##
def get_svc_stats():
  return {
    "strapi": {
      "status": check_strapi(),
      "process": "pm2",
      "link": "https://strapi.mihirniyogi.com/admin"
    },
    "cloudflared": {
      "status": check_cloudflared(),
      "process": "docker",
      "link": "https://dash.cloudflare.com/"
    },
    "ssh": {
      "status": check_ssh(),
      "process": "systemd",
      "link": "https://ssh.mihirniyogi.com/"  
    }
  }

def check_strapi():
  try:
    output = subprocess.check_output(['pm2', 'show', 'strapi']).decode()
    return 'strapi' in output and 'online' in output
  except subprocess.CalledProcessError:
    return False 

def check_cloudflared():
  try:
    output = subprocess.check_output(['docker', 'ps', '--format', '{{.Names}}']).decode()
    return 'MY_TUNNEL_CONTAINER' in output
  except subprocess.CalledProcessError:
    return False 

def check_ssh():
  try:
    output = subprocess.check_output(['systemctl', 'is-active', 'ssh']).decode().strip()
    return output == 'active'  
  except subprocess.CalledProcessError:
    return False 