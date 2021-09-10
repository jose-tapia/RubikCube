# Rubik's cube


Cubo rubik  
 - Cada color un numero entre 0 y 5
 - Cada cara como un arreglo de 3x3
 - Seis caras

Cubo objetivo:
 - Cada cara, tenga sus 9 numeros iguales 


Como lo lograremos:
 - Generar scramble
   - Variables aleatorias para generar la secuencia que vamos a aplicar

 - Aplicar scramble (El estado inicial que queremos resolver)
   - Como vamos a guardar cada estado del cubo rubik
   - Como vamos a hacer las operaciones

 - Aplicar nuestro algoritmo A* 
   - Pensar en heuristicas

 - Exponer el camino encontrado
   - Libreria vpython (interfaz grafica)
   - Pablo puede armar un robot/electronica (interfaz fisica)


Heuristicas:
- Regresa siempre 0 (no hace nada)
- Distancia manhattan 3D
  - De cada arista a donde debe de ir
  - De cada vertice a donde debe de ir
- Distancia manhattan 2D
  - 
- 