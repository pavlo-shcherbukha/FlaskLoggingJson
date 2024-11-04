# FlaskLoggingJson Логування сервісу Python Flask в JSON


## Запуск локально


 - склонувати репозиторій

```bash
 git clone https://github.com/pavlo-shcherbukha/FlaskLoggingJson

```

В терміналі Visual Studio Code створити python virtual environment

```bash
py -m venv env
```


В терміналі Visual Studio Code активувати python virtual environment


```bash
.\env\Scripts\activate.ps1
```


Встановити птрібні пакети python, що перелічені в  файлі requirements.txt


```bash
python.exe -m pip install --upgrade pip
py -m pip install -r requirements.txt
```
Запускати додаток, вибравши  в режимі debug  когфігурацію **sh_app: Win Flask**




## Корисні ресурси

- [Python JSON Logging](https://aminalaee.dev/posts/2022/python-json-logging/)
По суті це базовий ресурс, з якого взято більшість підходів.

- [logging — Logging facility for Python](https://docs.python.org/3/library/logging.html#logrecord-attributes)

Лінк на базову документацію по пакету [logging](https://pypi.org/project/logging/).
А ось і документація україгською [logging — Можливість журналювання для Python](https://docs.python.org/uk/3.9/library/logging.html).

- [Structured log files in Python using python-json-logger](http://web.archive.org/web/20201130054012/https://wtanaka.com/node/8201)
Тут трошки про структуру логування в  Python.
- [Injecting Request Information](https://flask.palletsprojects.com/en/2.3.x/logging/#injecting-request-information)
про те, як достукатися до інформації з запиту flask

корисне, що можна взяти з пакету json-logging
https://github.com/bobbui/json-logging-python/blob/master/json_logging/framework/flask/__init__.py

