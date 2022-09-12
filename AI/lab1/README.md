# lab1

Методы неинформированного (слепого) поиска: в глубину, в ширину - на примере игры "пятнашки". Нужно сделать так:

``` txt
5 8 3          1 2 3
4 0 2    ->    4 5 6
7 6 1          7 8 0
```

# Настройка

В файле `lab1.py` поменяйте значения, как вам нужно, в `Variable section`.

# Зависимости

Модуль `pydot` для визуализации графов, если в `Variable section` выбрано `GRAPH_VISIALISATION`.

``` bash
> pip install --upgrade pip
> pip install pydot
```

# Запуск

После настройки `Variable section` выполните:

``` bash
> python3 lab1.py
```