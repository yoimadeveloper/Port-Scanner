import socket
from common_ports import ports_and_services

def all_numeric(str):
  return all(i.isnumeric() for i in str.split('.'))

def get_open_ports(target, port_range, verbose):
  open_ports = []
  
  try:
    ip_addr = socket.gethostbyname(target)
  except:
    if all_numeric(target):
      return "Error: Invalid IP address"
    else:
      return "Error: Invalid hostname"
  
  # attempt to get valid hostname if one
  # wasn't passed as target
  if not all_numeric(target):
    hostname = target
  else:
    try:
      hostname = socket.gethostbyaddr(target)[0]
    except:
      # hostname not found
      hostname = False

  # print(target, ip_addr, hostname)

  for i in range(port_range[0], port_range[1] + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(.25)

    if (sock.connect_ex((ip_addr, i)) == 0):
      open_ports.append(i)
      
    sock.close()

  if verbose:
    output = f"Open ports for " 
    output += f"{hostname} ({ip_addr})\n" if hostname else f"{ip_addr}\n"
    output += "PORT     SERVICE\n"
    for port in open_ports:
      spacing = 9 - len(str(port))
      service = ports_and_services[port]

      output += f"{port}{' ' * spacing}{service}"
      if port != open_ports[-1]: 
        output += "\n"
    return output
    
  else:
    return open_ports
