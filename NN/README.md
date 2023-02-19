# How to Jupyter notebook

``` bash
> pip3 install --upgrade pip
> pip3 install --upgrade ipython jupyter

> cd {где лежат файлы .ipynb}
> jupyter notebook
# В браузере http://localhost:8888/?token={your_token}
# Найти токен можно командой
> jupyter notebook list
```

# Зависимости

``` bash
> pip3 install pandas numpy pillow pathlib

# pytorch for CPU only:
> pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# pytorch for GPU:
> pip3 install torch torchvision torchaudio

> pip3 install fastai
```

# Контролирование нагрузки на GPU зелёных

``` bash
watch nvidia-smi
```

# lab 1

Затасет собран с этих сабреддитов:

- r/akita

- r/shiba

- r/basset

- r/corgi

- r/husky