# Описание проекта

## Введение

В качестве третьей проектной работы мы с напарницей выбрали создание web-приложение на Flask. Смысл этого приложения заключается в том, чтобы дать возможность пользователю изучать иностранный язык (испанский) в интерактивной форме. Целью нашего приложения является стимулирование желания и развитие мотивации у потенциальных постоянных учеников нашего курса к изучению иностранного языка. Чтобы использовать все функции нашего приложения, пользователю следует зарегистрироваться на нашем сайте. После регистрации каждый раз при входе в приложение у ученика будут свои личные данные (логин/почта и пароль), которые система будет запрашивать. Так, благодаря нашему приложению, не обязательно будет вести конспекты и печатать огромное количество материалов, поскольку все необходимые материалы (теория и практика) будут находиться на платформе дистанционного обучения.

## Какие модули использовались в создании программы?

В разработке web-приложения используются модули: flask, pygsr, flask_login, flask_wtf, wtforms, csv, random, speech_recognition.

## Как выглядит web-приложение?

Всё очень просто. Сначала открывается главная страница. На данной странице приведено описание нашего проекта, краткая история нашего труда и информация о курсе. В верхей части страницы закреплено меню, из которого есть возможность перехода на страницы "Модули", "Поддержка", "Войти", "Зарегистрироваться" и обратно на главную страницу "Главная страница". На этих страницах в соответствии с приведёнными названиями располагается соответствующее наполнение.

## Алгоритм работы с web-приложением

1. При первом открытии приложения пользователь первым делом заходит на страницу регистрации, заполняет форму – так создаётся личный кабинет. Если же личный кабинет у пользователя уже есть, то он заходит во вкладку "Войти" и заходит в свой профиль.

2. Теперь, когда пользователь авторизирован, он может перейти во вкладку "Модули", где и находится вся информация, касающаяся непосредственного изучения языка.

3. Если что-то непонятно или возникают непредвиденные трудности, пользователь может написать в поддержку, форма для заполнения обращения находится во вкладке "Поддержка". Желаем Вам удачи в использовании программы и успехов в изучении испанского языка!
