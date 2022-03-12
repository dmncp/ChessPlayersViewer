# Chess Player Info Viewer



Z aplikacji można skorzystać używając linku poniżej:

https://restapiservice.damiancyper.repl.co/



## O aplikacji

Prosta aplikacja webowa stworzona w celu przećwiczenia korzystania z REST API. 

Na stronie głównej można zobaczyć prosty formularz, który umożliwia podanie nazwy użytkownika gracza z serwisu szachowego lichess lub chesscom, a także podanie tempa gry - wtedy użytkownik aplikacji zobaczy więcej danych. 

Po wypełnieniu formularza serwer aplikacji odpytuje zewnętrzne api serwisów lichess oraz chesscom o odpowiednie dane na temat gracza o nazwie podanej przez użytkownika. Dane te są następnie odpowiednio przygotowywane do wyświetlenia.



## Technologie

* Python 3.9
* Flask 2.0.3
* requests
* bootstrap



## Jak uruchomić?

Żeby uruchomić aplikację lokalnie wystarczy zainstalować potrzebne biblioteki korzystając z polecenia:

```bash
$ pip install -r requirements.txt
```

Następnie należy uruchomić serwer aplikacji korzystając z polecenia:

```bash
$ python ./app.py
```

Aplikacja zostanie uruchomiona na porcie 5000:

http://127.0.0.1:5000/

Innym sposobem skorzystania z aplikacji jest skorzystanie z linku:

https://restapiservice.damiancyper.repl.co/
