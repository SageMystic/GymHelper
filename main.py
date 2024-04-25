import sys
from random import shuffle
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QMainWindow, QAction, QButtonGroup
from PyQt5.QtWidgets import QPushButton, QCheckBox, QStackedWidget, QGridLayout, QDialog, QRadioButton
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from math import floor


class BlankField(Exception):
    def __init__(self, message='Обнаружены пустые строки или пункты, заполни их'):
        self.message = message
        super().__init__(self.message)



class GymHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gym Helper")
        self.setGeometry(400, 50, 600, 200)
        self.initUI()
        self.Database = {'Age': None, 'Height': None, 'Weight': None, 'Bulking': False,
                        'Losing': False, 'Healthing': False, 'Sex': False}
        self.ExerciseDatabase = {
            'Bulking': [('Присед со штангой', 2), ('Сгибание/разгибание ног на трнеажёре', 2), ('Тяга верхнего блока', 3), ('Горизонтальная тяга блока', 3), ('Поднятие штанги в наклоне', 3),
                    ('Поднятие штанги на бицепс', 2), ('Молотки с гантелями', 2), ('Поднятие гантели на бицепс со скручиванием', 2),
                    ('Опускание туловища на брусьях', 3), ('Разгибание верхнего блока с канатом', 3), ('Жим лёжа', 3), ('Жим гантелей лёжа', 3), ('Махи гантелей', 2), ('Разведение рук', 2)],
            'Losing': [('Бег на дорожке', 0), ('Велоупражнения', 0), ('Бёрпи', 1), ('Выпрыгивания с упора сидя', 1), ('Альпинист', 1), ('Бег на месте', 1)],
            'Healthing': [('Растяжка', -1), ('Вис на турнике', -1), ('Ходьба по лесу', 0), ('Подъём коленей', 1)]}
        self.DurationDatabase = {-1: ['1-2 минуты', '2-3 минуты', '30 секунд'], 0: ['1 час', '2 часа', 'Полчаса'], 1: ['10-15 раз', '20-25 раз', '5 раз'], 
                                2: ['6-8 раз', '8-10 раз', '4-6 раз'], 3: ['4-6 раз', '6-8 раз', '2-4 раз']}

    def initUI(self):
        CentralWidg = QWidget()
        self.setCentralWidget(CentralWidg)
        self.MainLayout = QVBoxLayout(CentralWidg)

        self.StackedWidg = QStackedWidget(self)
        self.MainLayout.addWidget(self.StackedWidg)

        Page1 = QWidget()
        Page2 = QWidget()

        self.StackedWidg.addWidget(Page1)
        self.StackedWidg.addWidget(Page2)
        self.Page1UI(Page1)
        self.Page2UI(Page2)




    def Page1UI(self, page):
        MainLayout = QVBoxLayout()
        page.setLayout(MainLayout)

        WelcomeLabel1 = QLabel("Привет! Если тебе понадобилась помощь в тренировках, то смело используй эту программу.")
        WelcomeLabel2 = QLabel("Для начала заполни данные ниже:")
        MainLayout.addWidget(WelcomeLabel1)
        MainLayout.addWidget(WelcomeLabel2)

        self.heightinp = QLineEdit()
        self.weightinp = QLineEdit()
        self.ageinp = QLineEdit()

        AgeHeightWeightlayout = QHBoxLayout()
        page.heightl = QLabel("Рост (см):")
        page.weightl = QLabel("Вес (кг):")
        page.agel = QLabel("Возраст:")

        AgeHeightWeightlayout.addWidget(page.heightl)
        AgeHeightWeightlayout.addWidget(self.heightinp)
        AgeHeightWeightlayout.addWidget(page.weightl)
        AgeHeightWeightlayout.addWidget(self.weightinp)
        AgeHeightWeightlayout.addWidget(page.agel)
        AgeHeightWeightlayout.addWidget(self.ageinp)
        MainLayout.addLayout(AgeHeightWeightlayout)

        SexLayout = QHBoxLayout()
        self.SexGroup = QButtonGroup()
        page.SexLabel = QLabel("Введите пол:")
        self.MaleRadio = QRadioButton("Мужской")
        self.MaleRadio.clicked.connect(self.UpdateSex)
        self.body_fat_dialog = None
        self.FemaleRadio = QRadioButton("Женский")
        self.FemaleRadio.clicked.connect(self.UpdateSex)
        self.SexGroup.addButton(self.MaleRadio)
        self.SexGroup.addButton(self.FemaleRadio)
        SexLayout.addWidget(page.SexLabel)
        SexLayout.addWidget(self.MaleRadio)
        SexLayout.addWidget(self.FemaleRadio)
        MainLayout.addLayout(SexLayout)

        Page1Layout = QVBoxLayout()
        page.GoalLabel = QLabel("Выбери цели:")
        self.BulkBox = QRadioButton("Набрать мышечную массу")
        self.SkinnyBox = QRadioButton("Похудеть")
        self.HealthBox = QRadioButton("Укрепить здоровье")
        self.SelectedGoals = QLabel("Выбрана цель:")
        stateChanged = QButtonGroup(self)
        stateChanged.addButton(self.BulkBox)
        stateChanged.addButton(self.SkinnyBox)
        stateChanged.addButton(self.HealthBox)

        self.BulkBox.clicked.connect(self.UpdateGoals)
        self.SkinnyBox.clicked.connect(self.UpdateGoals)
        self.HealthBox.clicked.connect(self.UpdateGoals)

        Page1Layout.addWidget(page.GoalLabel)
        Page1Layout.addWidget(self.BulkBox)
        Page1Layout.addWidget(self.SkinnyBox)
        Page1Layout.addWidget(self.HealthBox)
        Page1Layout.addWidget(self.SelectedGoals)
        MainLayout.addLayout(Page1Layout)

        self.FillInfoButton = QPushButton('Ввести данные')
        MainLayout.addWidget(self.FillInfoButton)
        self.FillInfoButton.clicked.connect(self.FillInfo)
        page.setLayout(Page1Layout)

        self.statusBar().showMessage(f'Перед началом введи данные о себе')

    def UpdateSex(self):
        if self.SexGroup.checkedButton() is not None:
            self.Database['Sex'] = 'Мужской' if self.SexGroup.checkedButton() == self.MaleRadio else 'Женский'

    def UpdateGoals(self):
        Selected = []

        if self.BulkBox.isChecked():
            Selected.append("Набрать мышечную массу")

        if self.SkinnyBox.isChecked():
            Selected.append("Похудеть")

        if self.HealthBox.isChecked():
            Selected.append("Укрепить здоровье")

        self.SelectedGoals.setText("Выбрана цель: " + ', '.join(Selected))

    def FillInfo(self):
        try:
            EmptyBoxChecker = 0
            if self.ageinp.text() == '' or self.heightinp.text() == '' or self.weightinp.text() == '':
                raise BlankField()
            else:
                age = float(self.ageinp.text())
                if age < 16 or age > 60:
                    raise ValueError("Возраст должен быть от 16 до 60 лет")
                self.Database['Age'] = age
                self.Database['Height'] = float(self.heightinp.text())
                self.Database['Weight'] = float(self.weightinp.text())
                if self.BulkBox.isChecked():
                    self.Database['Bulking'] = True
                else:
                    EmptyBoxChecker += 1
                if self.SkinnyBox.isChecked():
                    self.Database['Losing'] = True
                else:
                    EmptyBoxChecker += 1
                if self.HealthBox.isChecked():
                    self.Database['Healthing'] = True
                else:
                    EmptyBoxChecker += 1
                if self.Database['Sex'] is False:
                    raise BlankField
                if EmptyBoxChecker == 3:
                    raise BlankField

                self.StackedWidg.setCurrentIndex(1)
                self.page2()

                self.statusBar().clearMessage()
        except BlankField as B:
            self.statusBar().showMessage(f'Ошибка! {B}')
        except ValueError as ve:
            self.statusBar().showMessage(f'Ошибка! {ve}')

    def UpdateSex(self):
        if self.SexGroup.checkedButton() is not None:
            self.Database['Sex'] = 'Мужской' if self.SexGroup.checkedButton() == self.MaleRadio else 'Женский'

    def UpdateGoals(self):
        Selected = []

        if self.BulkBox.isChecked():
            Selected.append("Набрать мышечную массу")

        if self.SkinnyBox.isChecked():
            Selected.append("Похудеть")

        if self.HealthBox.isChecked():
            Selected.append("Укрепить здоровье")

        self.SelectedGoals.setText("Выбрана цель: " + ', '.join(Selected))

    def ShowLinks(self):
        self.LinkWind = LinksWidget()
        self.LinkWind.show()

    def page2(self):
        StatusMessage = self.statusBar().currentMessage()
        if not StatusMessage:
            self.StackedWidg.setCurrentIndex(1)

    def Page2UI(self, page):
        MainLayout = QGridLayout()
        page.setLayout(MainLayout)
        page.MainInfoButton = QPushButton('Основная информация')
        page.MainInfoButton.clicked.connect(self.Welcome)
        MainLayout.addWidget(page.MainInfoButton, 0, 0, 1, 2)
        DaysLayout = QHBoxLayout()
        page.DaysLabel = QLabel("Выберите дни тренировок:")
        self.DaysCheckboxes = []

        for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
            checkbox = QCheckBox(day)
            self.DaysCheckboxes.append(checkbox)
            DaysLayout.addWidget(checkbox)

        MainLayout.addWidget(page.DaysLabel, 1, 0, 1, 2)
        MainLayout.addLayout(DaysLayout, 2, 0, 1, 2)

        self.StartWorkoutButton = QPushButton('Начать тренировку')
        self.StartWorkoutButton.setEnabled(True)
        self.StartWorkoutButton.clicked.connect(self.StartWorkout)

        MainLayout.addWidget(self.StartWorkoutButton, 4, 0, 1, 2)

        self.MeasureBodyFatButton = QPushButton('Узнать оптимальное КБЖУ', self)
        self.MeasureBodyFatButton.clicked.connect(self.BodyFatMeasure)
        MainLayout.addWidget(self.MeasureBodyFatButton, 5, 0, 1, 2)

    def BodyFatMeasure(self): 
        self.body_fat_dialog = BodyFatDialog(self.Database)
        self.body_fat_dialog.show()

    def ShowWorkoutPlan(self, WorkoutPlan):
        self.WorkoutPlanWidg = WorkoutPlanWidget(WorkoutPlan)
        self.WorkoutPlanWidg.show()

    def StartWorkout(self):
        SelectedDays = [checkbox.text() for checkbox in self.DaysCheckboxes if checkbox.isChecked()]

        if not SelectedDays:
            self.statusBar().showMessage("Выберите хотя бы один день недели")
            return

        WorkoutPlan = {}
        for i in SelectedDays:
            WorkoutPlan[i] = []
        Exercises = []
        for i in self.Database.keys():
            if self.Database[i] == True:
                Exercises.extend(self.ExerciseDatabase[i])
        shuffle(Exercises)
        AgeLimiter = 0
        if 16 <= self.Database['Age'] <= 20:
            AgeLimiter = 0
        elif 21 <= self.Database['Age'] <= 40:
            AgeLimiter = 1
        else:
            AgeLimiter = 2
        Step = 0
        while Exercises != []:
            if Step == len(SelectedDays):
                Step = 0
            WorkoutPlan[SelectedDays[Step]].append((Exercises[0][0], self.DurationDatabase[Exercises[0][1]][AgeLimiter]))
            del Exercises[0]
            Step += 1
        self.ShowWorkoutPlan(WorkoutPlan)

    def Welcome(self):
        self.WelcomeWidg = WelcomeWidg(self.Database)
        self.WelcomeWidg.show()



class BodyFatDialog(QWidget):
    def __init__(self, database):
        super().__init__()
        self.Db = database
        self.setWindowTitle('Оптимальное КБЖУ')
        self.setGeometry(600, 300, 600, 400)

        layout = QVBoxLayout(self)
        
        self.body_fat_label = QLabel('Данные пользователя:')
        self.body_fat_label.setAlignment(Qt.AlignCenter)
        self.body_fat_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.body_fat_label)

        info_label = QLabel(f"Возраст: {int(self.Db['Age'])} лет\nРост: {int(self.Db['Height'])} см\nВес: {int(self.Db['Weight'])} кг")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Arial", 14))
        layout.addWidget(info_label)

        self.calculate_and_display_info()

    def calculate_and_display_info(self):
        gender = self.Db['Sex']
        weight = self.Db['Weight']
        height = self.Db['Height']
        age = self.Db['Age']
        bulking = self.Db['Bulking']
        losing = self.Db['Losing']
        healthing = self.Db['Healthing']

        if bulking or losing or healthing:
            calories = self.calculate_calories(gender, weight, height, age, bulking, losing, healthing)
            rounded_calories = int(calories)
            proteins = int(rounded_calories * 0.35 / 4)
            fats = int(rounded_calories * 0.4 / 9)
            carbs = int(rounded_calories * 0.25 / 4)

            bulking_info_text = f"{'Для набора мышечной массы' if bulking else 'Для похудения' if losing else 'Для укрепления здоровья'}:\n" \
                                f"Калории: {rounded_calories}\n" \
                                f"Белки: {proteins} г\n" \
                                f"Жиры: {fats} г\n" \
                                f"Углеводы: {carbs} г"

            bulking_info_label = QLabel(bulking_info_text)
            bulking_info_label.setAlignment(Qt.AlignCenter)
            bulking_info_label.setFont(QFont("Arial", 14))

            self.layout().addWidget(bulking_info_label)

    def calculate_calories(self, gender, weight, height, age, bulking, losing, healthing):
        if bulking:
            if gender == 'Мужской':
                return round((10 * weight) + (6.25 * height) - (5 * age) + 5)
            elif gender == 'Женский':
                return round((10 * weight) + (6.25 * height) - (5 * age) - 161)
        elif losing:
            if gender == 'Мужской':
                return round((88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)) * 0.8)
            elif gender == 'Женский':
                return round((447.593 + (9.247 * weight) + (3.098 * height) - (4.33 * age)) * 0.8)
        elif healthing:
            if gender == 'Мужской':
                return round(447.593 + (9.247 * weight) + (3.098 * height) - (4.33 * age))
            elif gender == 'Женский':
                return round(88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age))
        else:
            return 0


class WorkoutPlanWidget(QWidget):
    def __init__(self, WorkoutPlan):
        super().__init__()
        self.setWindowTitle("Тренировочный план")
        self.setGeometry(300, 300, 700, 500)

        layout = QVBoxLayout(self)

        font = QFont()
        font.setPointSize(12)  # Увеличиваем размер шрифта на 5 пунктов

        bold_font = QFont()
        bold_font.setBold(True)  # Делаем шрифт жирным
        bold_font.setPointSize(12)  # Устанавливаем размер шрифта для жирных линий

        for day, exercises in WorkoutPlan.items():
            day_label = QLabel(f"<b>{day}</b>")
            day_label.setFont(font)
            exercises_text = ', '.join([f"{name} ({duration})" for name, duration in exercises])
            
            exercises_label = QLabel(exercises_text)
            exercises_label.setFont(font)
            exercises_label.setWordWrap(True)  # Устанавливаем перенос по словам

            layout.addWidget(day_label)
            layout.addWidget(exercises_label)

            # Добавляем разделительную линию
            line = QLabel("<hr>")
            line.setFont(bold_font)  # Устанавливаем жирный шрифт для линии
            layout.addWidget(line)


class WelcomeWidg(QWidget): # Инициализация окна с кратким экскурсом
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle('Краткий экскурс')
        self.setGeometry(500, 300, 700, 500)
        Layout = QVBoxLayout()
        self.setLayout(Layout)
        Message = QLabel()
        Layout.addWidget(Message)
        self.WelcomePhrases = {'Bulking': ['Набор массы - трудный и ресурсозатратный процесс.\nВ первую очередь нужно быть готовым к изнурительным физическим нагрузкам',
                                           ' и ужасно большим приёмам пищи. \nПлюсы - можно есть почти всё, что в холодильнике, и не надо делать кардиотренировки',
                                           '.'],
                               'Losing': ['\nСбрасывать вес трудно психологически. Различные ограничения, диеты - очень давит эмоционально.',
                                          '\nПридётся ограничивать себя почти во всём и заниматься, в первую очередь, кардиотренировками: ',
                                          '\nбег, степ, велотренировки и т.п.'],
                               'Healthing': ['\nЗдоровье всегда трудно поправлять. Это походы ко врачам, понимание своих индивидуальных проблем.\nДалее будут лишь общие советы.']}
        MessageText = []
        Font = QFont()
        Font.setPointSize(16)
        Message.setFont(Font)
        for i in self.WelcomePhrases.keys():
            if self.db[i] == True:
                MessageText.append(''.join(self.WelcomePhrases[i]))
        MessageTextLine = ' А теперь к другим советам. '.join(MessageText)
        Message.setText(MessageTextLine)


class LinksWidget(QWidget): # Инициализация окна со ссылками на источники
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ссылки на источники")
        self.setGeometry(1000, 50, 300, 700)
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)
        self.LinkDatabase = [('https://lasalute.ru/blog/uprazhneniya/kardiotrenirovka/', 'Кардиотренировки'),
                             ('https://www.sports.ru/health/blogs/2820510.html', 'Советы по питанию'), ('https://kurl.ru/BJvaY', 'Влияние сна на мышцы'),
                             ('https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763382/', 'Сравнение различных диет'),
                             ('https://kurl.ru/cwYap', 'Мифы о жиросжигании'), ('https://kurl.ru/rHvRk', 'Спортивные добавки и всё о них'),
                             ('https://kurl.ru/QGhJj', 'Влияние стресса на здоровье'), ('https://pubmed.ncbi.nlm.nih.gov/30003901/', 'Всё о влиянии тренировок на потерю веса')]
        for i in self.LinkDatabase:
            LinkLabel = QLabel(self)
            LinkLabel.setText(f'<a href="{i[0]}">{i[1]}</a>')
            LinkLabel.setAlignment(Qt.AlignCenter)
            LinkLabel.setOpenExternalLinks(True)
            self.Layout.addWidget(LinkLabel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fitness_app = GymHelper()
    fitness_app.show()
    sys.exit(app.exec_())
