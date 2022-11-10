from socket  import *
from constCS import *

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

# Classe representando um cálculo de Índice de Massa Corporal (IMC)
class IMC:
  def __init__(self):
    self.mass = 70
    self.height = 175
  
  def __call__(self):
    return self.mass * 10000 / (self.height * self.height)
  
  def info(self):
    imc = self.__call__()
    if imc < 18.5:
      return 'Magreza'
    elif imc < 25:
      return 'Normal'
    elif imc < 30:
      return 'Sobrepeso'
    elif imc < 40:
      return 'Obesidade'
    else:
      return 'Obesidade Grave'

# Variáveis
imc = IMC()
(conn, addr) = s.accept()

# funções ultilitárias
def set_mass(data):
  try:
    mass = int(data[5:])
    imc.mass = mass
    print('mass = {}'.format(mass))
    conn.send(str.encode('massa = {} kg'.format(imc.mass)))
  except:
    print('Sintax error in mass assignment')
    conn.send(str.encode('Erro na sintaxe de atribuição de massa'))

def set_height(data):
  try:
    height = int(data[6:])
    imc.height = height
    print('height = {}'.format(height))
    conn.send(str.encode('altura = {:.2f} m'.format(imc.height/100)))
  except:
    print('Sintax error in height assignment')
    conn.send(str.encode('Erro na sintaxe de atribuição de altura'))

def show_imc():
  imc_ = imc()
  info = imc.info()
  print('IMC = {:.2f}'.format(imc_))
  conn.send(str.encode('Massa = {} kg, Altura = {:.2f} m, IMC = {:.2f} - {}'.format(imc.mass, imc.height/100, imc_, info)))

def error_msg():
  print('Sintax error')
  conn.send(str.encode('Erro! Atente-se à sintaxe - massa 59 | altura 165 | imc | sair'))

# Mensagens com instruções para o uso
def use_instructions():
  conn.send(str.encode('Uso:\n'
  + 'Para atribuir um valor de altura de 1.80 m, digite:\n'
  + '>>> altura 180\n'
  + 'Para atribuir um valor de massa de 67 kg, digite:\n'
  + '>>> massa 67\n'
  + 'Para obter o imc, digite:\n'
  + '>>> imc\n'
  + 'Para sair, digite:\n'
  + '>>> sair\n'))

use_instructions()

while True:
  data = conn.recv(1024)
  if not data: break

  decodedData = bytes.decode(data)

  # Lógica para acessar as diversas operações
  if decodedData.startswith('massa'):
    set_mass(decodedData)
  elif decodedData.startswith('altura'):
    set_height(decodedData)
  elif decodedData.startswith('imc'):
    show_imc()
  else:
    error_msg()

conn.close()