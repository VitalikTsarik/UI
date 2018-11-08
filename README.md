﻿# UI

## Team members
* Fiodor Suslionkov 
* Sychik Ekaterina
* Виталик Царик

## Граф визуальный прекрасный I

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
Каждую линию образует 2 точки (points).

## Запуск приложения
* установите python3 на ваш пк
* в командной строке пропишите pip3 install pyqt5
* в командной строке пропишите python Application.py

