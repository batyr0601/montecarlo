import math
import time

e=math.e

def taylorSeries(iterations):

  startTimer = time.perf_counter() # Begin trial timer
  value=0

  for i in range(0,iterations): # Sum the first i terms of the series
    value=value+(1**i)/math.factorial(i)

  endTimer = time.perf_counter() - startTimer # Finish trial timer 
  print(f'Iteration {iterations}')
  print(f'{value:.10f}: {(endTimer*1000):8.4f}ms') # Output info about the trial ? Change significant figures
  print ((abs(value-e)/e*100),"%")

for i in range(1,16):
  print("")
  taylorSeries(i)
  print("")
  print("-----------------------")

