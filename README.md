# Tickets. Система учета заявок на обслуживание IT инфраструктуры. 
Академический проект, написанный для изучения JS и Python. 
Фронтенд приложения реализован на JS ES6 без использования фреймворков с целью углубленного понимания работы типичного SPA.  
В бэкенде применен Python, Django REST framework, аутентификация - Token, dj-rest-auth.  
Приложение не предназначено для использования как система хэлп деск (хотя изначально задумывалась таковой), мотивом для написания послужил личный опыт - заявки, поданные пользователями, плохо поддаются фильтрации и классификации (в связи с разнообразными формами самих заявок - в некоторых это текстовая информация, в некоторых - графическая (сканы, фото)), в итоге для подготовки отчета приходится перебирать все вручную.  
Сценарий использования - техники/админы сами регистрируют запросы на обслуживание по категориям дли их последующего анализа и составления отчетности.  
Заявка (Ticket) связана со следующими сущностями:  
- Владелец (Owner). Исполнитель, за которым закреплена заявка;  
- Устройство (Device). Краеугольный камень - нет устройства - нет заявки;  
- Выполненные работы (WorkType). Список, отражает выполненные по заявке работы;  
- Приоритет (Priority). Нужен для ранжирования завок по срочности исполнения;  
- Категория (Category). Может казаться избыточным атрибутом, но по факту категория заявки не всегда соответствует типу устройства (как пример - заявка может быть подана на неисправный принтер, но неполадки вызваны сбоем в драйверах или принт-сервере);  
- Расход (Expenditure). Расход компонентов со склада;
    
![](https://github.com/anon811/tickets/blob/main/readme-img/ticket_form.png)

На странице "Сводка" отображаются последние 10 открытых заявок, гистограммы в верхней частью отображают открытые/закрытые заявки за выбранный период. 
    
![](https://github.com/anon811/tickets/blob/main/readme-img/dashboard.png)

Страница заявок позволяет просматривать и фильтровать заявки. Таблица поддерживает "ленивую загрузку" данных по мере прокрутки окна вниз. 
    
![](https://github.com/anon811/tickets/blob/main/readme-img/ticket-list.png)

Авторизация требуется для редактирования/создания, для просмотра информации авторизация не нужна. Стоит признать, что это тот еще"велосипед", работает с помощью local storage. Изначально проект использовал JWT и Google Firebase auth, был выпилен за ненадобностью - сильно усложнял проект без видимых преимуществ. 

## Инструкции по запуску
Для запуска проекта потребуется Docker.
Находясь в корневой папке репозитория, выполнить команду

    docker-compose up

После развертывания приложения оно станет доступно по адресу

    localhost:9080/
### Внимание!
Сборка не предназначена для развертывания на сервере и не сконфигурирована для "боевого" применения. Используются dev-сервера. 
