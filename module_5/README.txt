Проект - Credit Scoring - Компьютер говорит "Нет"

Версия 2 - Исправление ошибок, работа с обратной связью
Обратная связь от ментора - https://docs.google.com/document/d/1pgKC9KFJGabYB3Ulx8TyTbM8J8xuEFWbPHjc3cNzW90/edit?usp=sharing

Исправления:

1. Обработаны выбросы
2. Названия функций отражают действия; при определении соблюден принцип инкапсуляции
3. Исключено преобразование в строку возраста клиентов
4. Добавлены названия графиков и подписи осей
5. Проведен корреляционный анализ после генерации новых признаков, исключены из модели коррелирующиеся признаки
6. Даны комментарии настройкам параметров моделей
7. Добавлена наивную модель (до настройки, до генерации новых признаков)
8. Проведены эксперименты с разным набором признаков
9. Добавлены сравнение и выводы по разным моделям

→ основные цели и задачи проекта

Цель проекта -
Разработка предсказательной модели для оценки риска невозврата кредита клиентом банка при наличии набора его признаков.

Задачи проекта -
Провести предварительный осмотр и предобработку набора данных.
Провести EDA датасета.
Выбрать предсказательную модель и подобрать набор гиперпараметров для оптимизации метрик, в т.ч. ROC AUC.
Принять участие в соревновании на Kaggle, преддложив свой вариант решения (предобработка данных, создание новых признаков и выбор модели).

→ краткая информация о данных

В наборе данных - информация о 110148 клиентах банка с 18 признаками (характеристиками) и целевой переменной default, характеризующей ситуацию, когда клиент не возвращает кредит.

→ этапы работы над проектом

1. Провести первичный осмотр данных, определить наличие пропусков, подготовить датасет к работе, подготовить отчет pandas-profiling.
2. Анализ количественных признаков - строим графики распределения, логарифмируем/стандартизируем признаки, устраняем выбросы.
3. Анализируем номинативные (бинарные и категориальные) признаки - находим уникальные значения, выявляем значимые переменные, проводим LabelEncoding и One-Hot Encoding.
4. Проводим Feature Engineering - добавляем в набор данных новые признаки на основе имеющихся данных.
5. Предлагаем набор признаков для построения модели.
6. Выбираем базовую модель (в нашем случае - LogisticRegression). Оцениваем метрики базовой модели.
7. Подбираем гиперпараметры для нашей модели. Применяем XGBClassifier, RandomizedSearchCV.
8. Предсказываем вероятность default для тестового набора данных при помощи модели с подобранными гиперпараметрами.
7. Отправляем результаты на Kaggle-соревнование.

→ ответы на вопросы саморефлексии

1. Какова была ваша роль в команде?

Это был индивидуальный проект - все этапы работы выполнены самостоятельно при поддержке экспертов и других студентов в Slack. Также использовались открытые источники с информацией о банковской отрасли и статистические сведения, а также советы по написанию конкретных частей кода со StackOverflow и CodeRoad. Большое спасибо ментору проекта за проведенный вводный созвон - полученная информация помогла структурировать работу над проектов на первых этапах его реализации.

2. Какой частью своей работы вы остались особенно довольны?

Мне нравится видеть, как улучшается модель в части предсказания целевого признака после добавления новых признаков, попыток скомбинировать их различным образом, применения методов оптимизации для подбора гиперпараметров. Было интересно сравнивать свои выводы по EDA с выводами других участников соревнования, искать интересные решения по оформлению кода, таблиц и графиков вывода информации.

3. Что не получилось сделать так, как хотелось? Над чем ещё стоит поработать?

Мне необходимо дополнительно поизучать возможности библиотек по оценке качества модели после подбора и применения наиболее удачных гиперпараметров - кажется, что в этой части моя работа могла бы стать еще лучше, если бы я разобрался как это делать.

4. Что интересного и полезного вы узнали в этом модуле?

Подбор гиперпараметров - операция медленная. Очень медленная. В предыдущих проектах: написал код - получил результат. До этого никогда не приходилось ждать по несколько минут чтоб получить результат. Здесь начинаешь понимать как важно писать быстрый и оптимизированный код, чтобы "бутылочное горлышко" скорости работы программы было не с твоей стороны.

5. Что является вашим главным результатом при прохождении этого проекта?

Теперь умею делать не только .fit().predict(), но и использовать методы оптимизации, чтоб получать более точные и качественные  предсказательные модели, а также понимаю зачем и когда это нужно делать.

6. Какие навыки вы уже можете применить в текущей деятельности?

Параллельно с выполнением этого проекта я принял участие в хакатоне SkillFactory, где мы решали задачу анализа эффективности рекламных интеграций на YouTube. Также, во второй половине июля, планирую участвовать в онлайн-стажировке McKenzie & Co, где предлагается решить ряд аналитических задач. Полученные знания при изучении модуля о введении в машинное обучение оказались очень кстати и, надеюсь, пригодятся и на онлайн-стажировке.

7. Планируете ли вы дополнительно изучать материалы по теме проекта?

Планирую более основательно изучить оценку метрик качества моделей, к которым методами оптимизации подобраны гиперпараметры.