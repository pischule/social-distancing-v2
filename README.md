# social-distancing-v2

<img width="1148" alt="image" src="https://user-images.githubusercontent.com/41614960/166265315-2370a242-3673-4e7b-a397-dbcb33082c20.png">

<img width="1148" alt="image" src="https://user-images.githubusercontent.com/41614960/166265400-46a11b69-b121-44e6-9946-6e068a5da466.png">

<img width="1148" alt="image" src="https://user-images.githubusercontent.com/41614960/166509212-a45a6698-6a42-4ee7-91d4-8a6ff380b3a8.png">


### [видео](https://www.youtube.com/watch?v=Czs4a9fHq8E)

---

Это приложение предназначено для контроля социальной дистанции. 

Как это работает:

1. Сверточная сеть обнаруживает людей
1. Координаты преобразуются в абсолютные
1. Перебираеются все пары координат и вычисляются расстояния

Использованные технологии:

- [YOLOv3](https://pjreddie.com/darknet/yolo/)
- [OpenCV](https://opencv.org/)
- [Qt 6](https://www.qt.io/product/qt6)
<!-- - [SORT](https://github.com/abewley/sort) -->

В мастере настройки можно указать путь к видеофайлу, 0 для веб-камеры и url любой rtsp камеры.
