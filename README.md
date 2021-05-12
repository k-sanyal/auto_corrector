# Корректор ошибок на Python
Наш проект представляет собой корректор орфографии, разработанный на языке программирования Python.

## Подробное описание
* К концу проекта мы должны получить программу - точный корректор ошибок, совершащий правки, основываясь на частотности и левому и правому окружению
* Программа будет принимать слова или тексты
* Корректор будет достаточно точно исправлять ошибки. Программа будет иметь один режим работы - в результате работы программы пользователю укажут на совершенные ошибки и предложат варианты исправления.
* В программе будут использоваться модули: string, re, collections

## Подробное описание программы
Первым шагом в создании корректора была разработка модели языка. Для этого мы выбрали корпус текстов на русском языке различных жанров и стилей - так называемый словарь, то есть то, что будет определять правильность слова. Принцип исправления орфографии основывается на расстоянии Левенштейна и вероятности появления слова в корпусе: всего есть несколько видов ошибок, при которых правильное с точки зрения орфографии слово будет отличаться от неправильного на 1 или 2 символа. Существует пропуск символа, замена символа на другой, перестановка двух символов местами и вставка какого-то символа вместо другого. Мы написали функцию, которая производит данные операции. В результате функция (dist1) возвращает set-список слов с ошибками, в которых удалили, или заменили, или пропустили, или переставили буквы. Также мы написали функцию, которая проделывает операции дважды (dist2). В итоге мы получаем довольно объемный список наборов букв, в котором лежат как и несуществующие слова, так и реальные, получившиеся в результате всех операции и дублирования. Программа принимает на вход строку, разбивает ее на токены. Если токен есть в словаре, то возвращается сам токен, т. к. правильно написан. Если же токена нет в словаре, то с ним проделываются все вышеперечисленные операции. Программа выбирает из получившегося большого списка слов реальные слова (их зачастую получается несколько, и среди них обязательно есть нужное слово), рассчитывает их вероятности появления в словаре. Помимо этого, для исправления повторяющихся подряд букв мы написали отдельную функцию (correct_repeat), возвращающую слово, в котором 3 и более идущие подряд одинаковые символы заменяются одним таким символом. Далее корректор указывает пользователю на ошибки и предлагает варианты правильных слов в порядке убывания вероятности. Так работает базовый корректор, основанный на частостостях. 

## Критерий завершенного проекта
Корректор достаточно точно исправляет ошибки, учитывая частотности, контексты

# Команда проекта
* Тарасов Александр (БКЛ203)
* Югай Максим (БКЛ203)
* Ким Александр (БКЛ203)
 
# Таймлайн проекта
- [x] Собран корпус текстов - базовая модель языка
- [x] Разработан принцип исправления ошибок на расстоянии от 1 до 2, основанный на частотности
- [x] Базовый корректор (Март-Апрель)
- [ ] Собран корпус биграмм (Апрель-май)
- [ ] Разработан принцип исправления ошибок, основанный на правом и левом контексте (Май)
- [ ] Разработан и интегрирован интерфейс - дополнительно (Май)
- [ ] Продвинутый корректор

# Чего нам не хватает для реализации проекта
* Скрипта, основанного на биграммах, для лучшего распознавания ошибок в контексте, более масштабного корпуса текстов, базы данных, в которой хранится корпус, для более быстрого выполнения программы

# Распределение обязанностей в команде
Написание кода: Югай Максим (БКЛ203) Ким Александр (БКЛ203)

Разработка интерфейса: Тарасов Александр (БКЛ203)
