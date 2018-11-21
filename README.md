# UI

Программа, которая визуализирует граф представленный в формате JSON
```json
{
    "idx": 1,
    "lines": [
        {
            "idx": 192,
            "length": 1,
            "points": [
                112,
                107
            ]
        },
        {
            "idx": 193,
            "length": 2,
            "points": [
                101,
                102
            ]
        },
        ...
    ],
    "name": "map01",
    "points": [
        {
            "idx": 101,
            "post_idx": 13
        },
        {
            "idx": 102,
            "post_idx": null
        },
        ...
    ]
}
```
* points - вершины графа;
* lines - рёбра графа;
* length - длинна ребра;
* idx - уникальный индекс для линии, вершины, графа;
* name - имя графа
* Каждую линию образует 2 точки (points).

## Team members
* [Fiodor Suslinkov](https://github.com/FiodorSuslionkov) - Fiodor Suslionkov 
* [Katia Sychik](https://github.com/KatiaSychik) - Сычык Кацярына
* [Vitalik Tsarik](https://github.com/VitalikTsarik) - Виталик Царик

## Запуск приложения
* установите python3 на ваш пк
* в командной строке пропишите pip3 install pyqt5
* в командной строке пропишите python app.py

## Задания
### Граф визуальный прекрасный I
[Задание 1](tasks/task_1.md)

### Клиент игровой великолепный II
[Задание 2](tasks/task_2.md)
