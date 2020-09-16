import random
import math
import simpy 
SEMILLA = 30
NUM_PELUQUEROS = 0
TIEMPO_CORTE_MIN = 0
TIEMPO_CORTE_MAX = 0
T_LLEGADAS = 0
TOT_CLIENTES =0

te  = 0.0 # tiempo de espera total
dt  = 0.0 # duracion de servicio total
fin = 0.0 # minuto en el que finaliza
def cortar(cliente):
 global dt  #Para poder acceder a la variable dt declarada anteriormente
 R = random.random()  # Obtiene un numero aleatorio y lo guarda en R
 tiempo = TIEMPO_CORTE_MAX - TIEMPO_CORTE_MIN  
 tiempo_corte = TIEMPO_CORTE_MIN + (tiempo*R) # Distribucion uniforme
 yield env.timeout(tiempo_corte) # deja correr el tiempo n minutos
 print(" \o/ Corte listo a %s en %.2f minutos" % (cliente,tiempo_corte))
 dt = dt + tiempo_corte # Acumula los tiempos de uso de la i
    


def cliente (env, name, personal ):
	global te
	global fin
	llega = env.now # Guarda el minuto de llegada del cliente
	print ("\n---> %s llego a peluqueria en minuto %.2f" % (name, llega))
	with personal.request() as request: # Espera su turno
		yield request # Obtiene turno
		pasa = env.now # Guarda el minuto cuado comienza a ser atendido
		espera = pasa - llega # Calcula el tiempo que espero
		te = te + espera # Acumula los tiempos de espera
		print ("\n**** %s pasa con peluquero en minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
		yield env.process(cortar(name)) # Invoca al proceso cortar
		deja = env.now #Guarda el minuto en que termina el proceso cortar 
		print ("\n<--- %s deja peluqueria en minuto %.2f" % (name, deja))
		fin = deja # Conserva globalmente el ultimo minuto de la simulacion
       
	

def principal (env, personal):
	llegada = 0
	i = 0
	for i in range(TOT_CLIENTES): # Para n clientes
		R = random.random()
		llegada = -T_LLEGADAS * math.log(R) # Distribucion exponencial
		yield env.timeout(llegada)  # Deja transcurrir un tiempo entre uno y otro
		i += 1
		env.process(cliente(env, 'Cliente %d' % i, personal))

print ("\n---------------------------------------------------------------------")
print ("\n----------------- Bienvenido Simulacion Peluqueria MERCYS ------------------")
print ("\n---------------------------------------------------------------------")
print ("\n---------------------------------------------------------------------")
NUM_PELUQUEROS = int(input('Ingrese la cantidad de peluqueros:'))
TIEMPO_CORTE_MIN =int(input('Ingrese el tiempo de corte minimo:'))
TIEMPO_CORTE_MAX = int(input('Ingrese tiempo de corte maximo:'))
T_LLEGADAS = int(input('Ingrese el tiempo de llegada del cliente en minutos:'))
TOT_CLIENTES =int(input('Ingrese la cantidad de clientes:'))

random.seed (SEMILLA)  # Cualquier valor
env = simpy.Environment() # Crea el objeto entorno de simulacion
personal = simpy.Resource(env, NUM_PELUQUEROS) #Crea los recursos (peluqueros)
env.process(principal(env, personal)) #Invoca el proceso princial
env.run() #Inicia la simulacion
print ("\n---------------------------------------------------------------------")
print ("\nIndicadores obtenidos: ")

lpc = te / fin
print ("\nLongitud promedio de la cola: %.2f" % lpc)
tep = te / TOT_CLIENTES
print ("Tiempo de espera promedio = %.2f" % tep)
upi = (dt / fin) / NUM_PELUQUEROS
print ("Uso promedio de la instalacion = %.2f" % upi)
print ("\n---------------------------------------------------------------------")
		
