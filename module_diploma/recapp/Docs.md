# Проект - Рекомендательная система для интернет-магазина.
Клиент компании заинтересован в повышении прибыли от допродаж в интернет-магазине на 20 %.<br>
Для решения задачи - реализовать рекомендательную систему на главной странице сайта интернет-магазина.<br>
Целевая техническая метрика - Precision@3.

### Набор данных от заказчика
events — датасет с событиями:
* timestamp — время события
* visitorid — идентификатор пользователя
* event — тип события
* itemid — идентификатор объекта
* transactionid — идентификатор транзакции, если она проходила

category_tree — файл с деревом категорий (можно восстановить дерево):
* category_id — идентификатор категорий
* parent_id — идентификатор родительской категории

item_properties — файл с свойствами товаров:
* timestamp — момент записи значения свойства
* item_id — идентификатор объекта
* property — свойство, кажется, они все, кроме категории, захешированы
* value — значение свойства

## Формат входных данных для обучения (формат, факторы)

### Генерация дополнительных признаков
* prop - конкатенация текстовых значений item_id, property, value для работы с текстовыми движками;
* freq - частота посещения пользователем интернет-магазина;
* day_of_week, Year, Month, Day, Hour, minute - признаки, сгенерированные на основе исходного признака event_datetime;
* Day Period - категориальный признак, производная от Hour (утро, день, вечер, ночь);
* top3 - список из трех наиболее часто встречающихся в логах товаров у всех пользователей list(train.itemid.value_counts()[:3].index);

## Получение датасета для обучения (трансформации исходного датасета)
Для обучения итоговой модели используется датасет events от заказчика. <br>
Преобразования:
1. events.sort_values(by=['timestamp'], ignore_index=True, inplace=True) - в соответствии с рекомендациями заказчика будем использовать time-based разделение на тренировочную и тестовую выборки для валидации.
2. events.drop(['timestamp', 'event', 'transactionid'], axis=1, inplace=True) - для реализации модели Most Frequent Items In User's GroupBy требуются два признака - itemid, visitorid.
Последующие преобразования осуществлять отдельно для тренировочной и тестовой выборок:
3. train['first'] = train.groupby('visitorid')['itemid'].transform(lambda s: s.value_counts().index[0])
4. train['second'] = train.groupby('visitorid')['itemid'].transform(lambda s: s.value_counts().index[1] if len(s.value_counts())>1 else np.nan)
5. train['third'] = train.groupby('visitorid')['itemid'].transform(lambda s: s.value_counts().index[2] if len(s.value_counts())>2 else np.nan)
Для ускорения работы сервиса рекомендаций recapp.py по результатам обучения выкатываем в прод базу пользователей (словарь), сформированный запросами (items_list содержит три наиболее часто связанных с пользователем товаров либо None, если такие товары для пользователя отсутствуют; cold_start_count - счётчик, позволяющий оценить необходимость рекомендации пользователю товаров из ранее связанных с ним либо из списка наиболее популярных среди всех пользователей):
* visitors = train.groupby('visitorid').agg({'first': 'first', 'second': 'first', 'third': 'first'}).reset_index()
* visitors['items_list'] = visitors[['first', 'second', 'third']].values.tolist()
* visitors['cold_start_count'] = visitors.apply(lambda row: sum(row.isnull()), axis=1)
* visitors.to_csv('visitors.csv', index=False)

## Построение валидации
Для построения тренировочной и тестовой выборки используется sklearn.model_selection.train_test_split. Для обучения используем 80% выборки, для тестирования - 20%. Не используем перемешивание, чтобы сохранить хронологически верный порядок событий в тренировочном и тестовом датасете. <br>
train_test_split(events, test_size=0.2, shuffle=False)


## Проведенные эксперименты: модели, гиперпараметры, метрики

### Colaborative Filtering
- 

### Cosine Similarity
Run out of memory <br>
source: rai-harshit/music-recommendation-engine

### Most Frequent Items In User's GroupBy
Как и в тренировочном датасете, в тестовом есть два признака - itemid, visitorid. На этапе валидации:
1. test = pd.merge(test, visitors, on='visitorid', how='left') сопоставляем пользователей с пользователей из ранее созданной базы пользователей visitors;
2. test['cold_start_count'] = test.apply(lambda row: sum(row[['first', 'second', 'third']].isnull()), axis=1) определяем, к какой группе пользователей относится текущий - можно ли ему рекомендовать что-то из ранее связанных с ним товаров либо следует обратиться к списку наиболее популярных товаров среди всех пользователей;
3. Заполняем отсутствующие значения в соответствии с ранее полученным значением cold_start_count:<br>
test.loc[test['cold_start_count'] == 1, 'third'] = top3[0]<br>
test.loc[test['cold_start_count'] == 2, 'second'] = top3[0]<br>
test.loc[test['cold_start_count'] == 2, 'third'] = top3[1]<br>
test.loc[test['cold_start_count'] == 3, 'first'] = top3[0]<br>
test.loc[test['cold_start_count'] == 3, 'second'] = top3[1]<br>
test.loc[test['cold_start_count'] == 3, 'third'] = top3[2]<br>
4. Делаем predict в форме публикации списка трех товаров для каждого пользователя:<br>
test['pred'] = test[['first', 'second', 'third']].values.tolist()
5. Расчет метрики качества рекомендации:<br>
test['is_true'] = test.apply(lambda row: row['itemid'] in row['pred'], axis=1)<br>
results = test.is_true.value_counts()<br>
metric = results[1] / (results[0] + results[1])<br>
Значение метрики на тестовом датасете - 2.26%.

## Запуск сервиса и его структура
In Terminal:<br>
svn export https://github.com/Segodnya/data-science-studies/trunk/module_diploma/recapp ~/Downloads/diploma_project<br>
Go to diploma_project folder (not recapp one)<br>
docker build -t recapp:latest recapp/<br>
docker run -d -p 4455:4455 recapp:latest --network="host"<br>
Web-app runs at localhost:4455 - open it in your browser<br>
To stop the web-app:<br>
docker ps -a<br>
docker stop <docker_id>

В структуре проекта:
* Dockerfile - контейнер, устанавливающий необходимые библиотеки (flask, pandas, numpy) и запускающий веб-сервис с порта 4455;
* requirements.txt - список необходимых для запуска сервиса библиотек, используется при первом запуске контейнера;
* recapp.py - исполняемый файл сервиса, содержит маршрутизацию и рекомендательную модель;
* visitors.zip - архив, содержит visitors.csv - базу пользователей, полученную на обучающей выборке и необходимую для представления рекомендаций пользователям, которые ранее уже пользовались магазином;
* templates - папка с шаблонами страниц, содержит файлы-разметки base.html (корневой) и index.html (разметка главной страницы).

## Описание API сервиса
Сервис запускается по адресу 0.0.0.0:4455.<br>
В input-форме text сервис принимает от пользователя visitorid методом POST-запроса.<br>
По нажатию submit-кнопки Predict, visitorid передается функции predict().<br>
Функция predict() возвращает по маршруту /repidct три-кортеж из itemid.