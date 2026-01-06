# defmodule Ej do
#   def hola() do
#     IO.puts("Hola")
#   end
# end

# defmodule Math do
#   def suma(a, b) do
#     a + b
#   end
# end

# #funcion anonima
# suma = fn(a,b)-> a+b end #guardamos en suma. la funcion a+b.
# IO.puts(suma.(3,4))

# #Mapa ->    %{}    mapa en Elixir es una colección de pares clave-valor.
# #Se usa para guardar datos relacionados, como
# persona = %{nombre: "Nico", edad: 30}#ejemplo de mapa
# IO.puts(persona.nombre)  # Imprime "Nico"

# #Pattern matching
# defmodule Factorial do
#   def calcular(0), do: 1
#   def calcular(n),do: n* calcular(n-1)
# end

# #condicional IF y ELSE
# defmodule CondicionalIF do
#   def esuno(n) do
#   if n==1 do
#     IO.puts(Ej.hola())
# else
#   IO.puts("No es uno")
# end
# end
# end

# #Condicion unless
# defmodule CondicionalUnless do
#   def noesuno(n) do
#     unless n==1 do
#       IO.puts("pone un uno gil")
#     end
#   end
# end

# #CondicionalCase
# defmodule CondicionalCase do
#   def de_min_a_may(n) do
#     case n do
#       "a" -> "A"
#       "b" -> "B"
#       "c" -> "C"
#       _ -> "debe ingresar un dato"
#     end
#   end
# end

# #CondicionalCon
# defmodule CondicionalCon do
#   def condicionalAnidado(n, k) do
#     cond do
#     n==2 -> k*2
#     n==3 -> k/2
#     n==4 -> k+2
#     true -> "valor incorrecto"
#     end
#   end
# end

# lista1=[1,2,3,4,5]
# lista2=[6,7,8,9]
# lista3=[2,3]

# #listas y sus funciones
# defmodule Concatenar do
#   def concatenar(l1, l2) do
#     l1 ++ l2
#   end
# end

# defmodule Restar do
#   def restar(lista1, lista3) do
#     lista1 -- lista3
#   end
# end

# defmodule PatterMaching do
#   def patter(l1) do
#     [head|tail]=l1
#      IO.puts(head)
#      if head<4 do
#         patter(tail)
#        end
#   end
# end

# #agregar un nuevo elemento a la lista
# defmodule AgregarElemento do
#   def agregar(a, l1) do
#     nueva_lista = [a | l1]
#   end
# end


# #Ej.hola()
# #IO.puts(Math.suma(2, 2))
# #IO.puts(Factorial.calcular(0))
# #CondicionalIF.esuno(33)
# #CondicionalUnless.noesuno(1)
# #CondicionalCase.de_min_a_may("a")
# #IO.puts(CondicionalCon.condicionalAnidado(2,6))
# #IO.inspect(Concatenar.concatenar(lista1, lista2))
# #IO.inspect(Restar.restar(lista1, lista3))
# #IO.inspect(PatterMaching.patter(lista1))
# #IO.inspect(AgregarElemento.agregar(22,lista1))


#---------------------------------------------#
#Ejercicios del TP
#1)defina una funcion que calcule la enesima potencia de un numero
# defmodule PotEnesima do
#   def potenciaEnesima(_, 0), do: 1
#   def potenciaEnesima(k, n) do
#     k * potenciaEnesima(k,n-1)
#   end
# end
# IO.puts(PotEnesima.potenciaEnesima(2,4))
#version usando COND
# defmodule PotEnesima do
#   def potenciaEnesima(a, b) do
#     cond do
#       b == 0 -> 1
#       b > 0 -> a * potenciaEnesima(a, b - 1)
#     end
#   end
# end
# IO.inspect(PotEnesima.potenciaEnesima(2, 4),label: "Resultado")

#2) Defina una funcion que determine el valor absoluto de un numero.
# defmodule ValorAbsoluto do
#   def valor_absoluto(0), do: 0
#   def valor_absoluto(n) do
#     if n<0 do
#       n*(-1)
#     else
#       n
#     end
#   end

# end
# IO.puts(ValorAbsoluto.valor_absoluto(0))

#3) Escriba una funcion que calcule el i-esimo numero perfecto (los numeros perfectos son aquellos que son iguales a la suma de sus divisores)
##############################
# EJEMPLO 1: Usando Enum y Stream
##############################

defmodule NumeroPerfectoEnum do
  # Calcula los divisores propios de un número (sin incluir al mismo número)
  def divisores(n) do
    1..(n-1)                                # rango de 1 hasta n-1
    |> Enum.filter(fn x -> rem(n, x) == 0 end) # nos quedamos con los que dividen a n
  end

  # Verifica si un número es perfecto
  def perfecto?(n) do
    Enum.sum(divisores(n)) == n
  end

  # Genera un flujo infinito de números perfectos
  def lista_perfectos do
    Stream.iterate(2, &(&1 + 1))   # empieza en 2 y va aumentando
    |> Stream.filter(&perfecto?/1) # se queda solo con los perfectos
  end

  # Obtiene el i-ésimo número perfecto (i empieza en 1)
  def iesimo_perfecto(i) do
    lista_perfectos()
    |> Enum.at(i - 1)   # Enum.at es 0-based, por eso usamos i-1
  end
end

##############################
# EJEMPLO 2: Versión recursiva pura
##############################

defmodule NumeroPerfectoRec do
  # Función recursiva que obtiene los divisores propios de n
  def divisores(n), do: divisores(n, n - 1, [])

  # Caso base: cuando llegamos a 0, devolvemos la lista acumulada
  defp divisores(_n, 0, acc), do: acc

  # Caso recursivo: si i divide a n, lo agregamos a la lista
  defp divisores(n, i, acc) do
    if rem(n, i) == 0 do
      divisores(n, i - 1, [i | acc])
    else
      divisores(n, i - 1, acc)
    end
  end

  # Suma recursiva de los elementos de una lista
  def suma([]), do: 0
  def suma([h | t]), do: h + suma(t)

  # Verifica si un número es perfecto
  def perfecto?(n) do
    suma(divisores(n)) == n
  end

  # Encuentra el i-ésimo número perfecto usando búsqueda recursiva
  def iesimo_perfecto(i), do: buscar(2, i, 0)

  # Función auxiliar que va probando números hasta encontrar el i-ésimo perfecto
  defp buscar(n, i, encontrados) do
    if perfecto?(n) do
      if encontrados + 1 == i do
        n
      else
        buscar(n + 1, i, encontrados + 1)
      end
    else
      buscar(n + 1, i, encontrados)
    end
  end
end

##############################
# EJEMPLOS DE USO
##############################

IO.puts("=== Usando Enum/Stream ===")
IO.puts NumeroPerfectoEnum.iesimo_perfecto(1)  # 6
IO.puts NumeroPerfectoEnum.iesimo_perfecto(2)  # 28
IO.puts NumeroPerfectoEnum.iesimo_perfecto(3)  # 496

IO.puts("=== Usando Recursión pura ===")
IO.puts NumeroPerfectoRec.iesimo_perfecto(1)   # 6
IO.puts NumeroPerfectoRec.iesimo_perfecto(2)   # 28
IO.puts NumeroPerfectoRec.iesimo_perfecto(3)   # 496
