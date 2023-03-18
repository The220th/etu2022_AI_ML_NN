# How to Jupyter notebook

``` bash
> pip3 install --upgrade pip
> pip3 install --upgrade ipython jupyter

> cd {где лежат файлы .ipynb}
> jupyter notebook --no-browser
# В браузере http://localhost:8888/?token={your_token}
# Найти токен можно командой
> jupyter notebook list
```

# Зависимости

``` bash
> pip3 install pandas numpy pillow pathlib scikit-learn scipy matplotlib

# pytorch for CPU only:
> pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# pytorch for GPU:
> pip3 install torch torchvision torchaudio torchtext pytorch-nlp torchsummary

> pip3 install fastai
```

# Контролирование нагрузки на GPU зелёных

``` bash
watch -n 0.5 nvidia-smi
```

# lab 1

Датасет собран с этих сабреддитов:

- r/akita

- r/shiba

- r/basset

- r/corgi

- r/husky

Задание:

- Собрать свой датасет (хотя бы 3 класса)

- Использовать только `pytorch`.

- Реализовать свою архитектуру с регуляризацией, дропаутом, ~~блэкджэком и ...~~.

- Изменение гиперпараметров:

- - learning rate

- - коэффициенты регуляризации

- - batch size

- - дропаут

- - параметры архитектуры (например, кол-во нейронов на N-ом слое, но не их веса)

- Трансферное обучение

# lab 2

Рекурентные нейронные сети. Датасет: Toxic Comment Classification.

