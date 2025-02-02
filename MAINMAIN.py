import sys
from random import shuffle
import customtkinter as ctk
from tkinter import messagebox
import json
import matplotlib.pyplot as plt
from datetime import datetime
'''В общем, этот файл пока самая последняя версия. дальше нужно реализовать советы про ментальное здоровье и осанку. про менталку нужно задавать вопросы
    как засыпаете, как просыпаетесь, что делаете перед сном и отталкиваясь от ответов приводить советы.'''

class BlankField(Exception):
    """Исключение для пустых полей ввода."""
    def __init__(self, message='Обнаружены пустые строки или пункты, заполни их'):
        super().__init__(message)

class GymHelper(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gym Helper")
        self.geometry("700x500")
        # Инициализация интерфейса
        self.init_ui()
        # Базы данных
        self.database = {
            'Age': None, 'Height': None, 'Weight': None,
            'Bulking': False, 'Losing': False, 'Healthing': False, 'Sex': None
        }
        self.exercise_database = {
            'Bulking': [
                ('Присед со штангой', 2), ('Сгибание/разгибание ног на тренажёре', 2),
                ('Тяга верхнего блока', 3), ('Горизонтальная тяга блока', 3),
                ('Поднятие штанги в наклоне', 3), ('Поднятие штанги на бицепс', 2),
                ('Молотки с гантелями', 2), ('Поднятие гантели на бицепс со скручиванием', 2),
                ('Опускание туловища на брусьях', 3), ('Разгибание верхнего блока с канатом', 3),
                ('Жим лёжа', 3), ('Жим гантелей лёжа', 3), ('Махи гантелей', 2), ('Разведение рук', 2)
            ],
            'Losing': [
                ('Бег на дорожке', 0), ('Велоупражнения', 0), ('Бёрпи', 1),
                ('Выпрыгивания с упора сидя', 1), ('Альпинист', 1), ('Бег на месте', 1)
            ],
            'Healthing': [
                ('Растяжка', -1), ('Вис на турнике', -1), ('Ходьба по лесу', 0), ('Подъём коленей', 1)
            ]
        }
        self.duration_database = {
            1: ['1-2 минуты', '2-3 минуты', '30 секунд'],
            0: ['1 час', '2 часа', 'Полчаса'],
            1: ['10-15 раз', '20-25 раз', '5 раз'],
            2: ['6-8 раз', '8-10 раз', '4-6 раз'],
            3: ['4-6 раз', '6-8 раз', '2-4 раз']
        }
        # Прогресс пользователя
        self.progress_data = {}
        self.load_progress()

    def init_ui(self):
        # Главный фрейм
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)
        # Стек виджетов
        self.stacked_widget = ctk.CTkFrame(main_frame)
        self.stacked_widget.pack(fill="both", expand=True)
        # Создание страниц
        page0 = ctk.CTkFrame(self.stacked_widget)  # Новая страница
        page1 = ctk.CTkFrame(self.stacked_widget)  # Страница ввода данных
        page2 = ctk.CTkFrame(self.stacked_widget)  # Страница тренировок
        page0.pack(fill="both", expand=True)
        page1.pack(fill="both", expand=True)
        page2.pack(fill="both", expand=True)
        # Настройка UI для страниц
        self.page0_ui(page0)  # Новая страница
        self.page1_ui(page1)  # Страница ввода данных
        self.page2_ui(page2)  # Страница тренировок
        # Показываем первую страницу
        page1.pack_forget()
        page2.pack_forget()

    def page0_ui(self, page):
        layout = ctk.CTkFrame(page, fg_color="#333333")  # окантовка
        layout.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(layout, text="Выберите цель:", font=("Arial", 24))
        title_label.pack(pady=20)

        # Кнопка "Улучшить осанку"
        posture_button = ctk.CTkButton(
            layout, text="Улучшить осанку", command=self.improve_posture
        )
        posture_button.pack(pady=10)

        # Кнопка "Улучшить сон"
        sleep_button = ctk.CTkButton(
            layout, text="Улучшить сон", command=self.improve_sleep
        )
        sleep_button.pack(pady=10)

        # Кнопка "Улучшить тело"
        body_button = ctk.CTkButton(
            layout, text="Улучшить тело", command=self.go_to_main_program
        )
        body_button.pack(pady=10)

    def improve_posture(self):
        messagebox.showinfo("Информация", "Здесь будет информация о улучшении осанки.")

    def improve_sleep(self):
        messagebox.showinfo("Информация", "Здесь будет информация о улучшении сна.")

    def go_to_main_program(self):
        # Переход на страницу 1 (основная программа)
        self.stacked_widget.winfo_children()[1].pack(fill="both", expand=True)
        self.stacked_widget.winfo_children()[0].pack_forget()

    def page1_ui(self, page):
        layout = ctk.CTkFrame(page, fg_color="#333333")  # окантовка
        layout.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Приветственная информация
        welcome_label1 = ctk.CTkLabel(layout, text="Привет! Если тебе нужна помощь в тренировках, то смело используй эту программу.")
        welcome_label1.pack(pady=10)
        welcome_label2 = ctk.CTkLabel(layout, text="Для начала заполни данные ниже:")
        welcome_label2.pack(pady=5)
        
        # Ввод данных пользователя
        input_frame = ctk.CTkFrame(layout)
        input_frame.pack(pady=10)
        
        self.age_input = ctk.CTkEntry(input_frame, placeholder_text="Возраст")
        self.height_input = ctk.CTkEntry(input_frame, placeholder_text="Рост (см)")
        self.weight_input = ctk.CTkEntry(input_frame, placeholder_text="Вес (кг)")
        
        self.age_input.grid(row=0, column=0, padx=10, pady=5)
        self.height_input.grid(row=0, column=1, padx=10, pady=5)
        self.weight_input.grid(row=0, column=2, padx=10, pady=5)
        
        # Выбор пола
        sex_frame = ctk.CTkFrame(layout)
        sex_frame.pack(pady=10)
        
        self.sex_var = ctk.StringVar(value="")
        male_radio = ctk.CTkRadioButton(sex_frame, text="Мужской", variable=self.sex_var, value="Мужской")
        female_radio = ctk.CTkRadioButton(sex_frame, text="Женский", variable=self.sex_var, value="Женский")
        
        male_radio.grid(row=0, column=0, padx=10)
        female_radio.grid(row=0, column=1, padx=10)
        
        # Выбор целей
        goal_frame = ctk.CTkFrame(layout)
        goal_frame.pack(pady=10)
        
        self.goal_var = ctk.StringVar(value="")
        bulk_radio = ctk.CTkRadioButton(goal_frame, text="Набрать мышечную массу", variable=self.goal_var, value="Bulking")
        skinny_radio = ctk.CTkRadioButton(goal_frame, text="Похудеть", variable=self.goal_var, value="Losing")
        health_radio = ctk.CTkRadioButton(goal_frame, text="Укрепить здоровье", variable=self.goal_var, value="Healthing")
        
        bulk_radio.pack(anchor="w", pady=5)
        skinny_radio.pack(anchor="w", pady=5)
        health_radio.pack(anchor="w", pady=5)
        
        # Кнопка для отправки данных
        self.fill_info_button = ctk.CTkButton(layout, text="Ввести данные", command=self.fill_info)
        self.fill_info_button.pack(pady=10)

    def page2_ui(self, page):
        layout = ctk.CTkFrame(page, fg_color="#333333")  # окантовка
        layout.pack(fill="both", expand=True, padx=20, pady=20)
        # Кнопка для просмотра основной информации (остается вверху)
        main_info_button = ctk.CTkButton(layout, text="Основная информация", command=self.welcome)
        main_info_button.pack(pady=10)
        # Разделение на левую и правую части
        left_frame_outer = ctk.CTkFrame(layout, fg_color="transparent")
        left_frame_outer.pack(side="left", fill="both", expand=True, padx=10)
        right_frame_outer = ctk.CTkFrame(layout, fg_color="transparent")
        right_frame_outer.pack(side="right", fill="both", expand=True, padx=10)
        # Левая часть
        left_frame = ctk.CTkFrame(left_frame_outer, fg_color="#2b2b2b")  # Прозрачный фон
        left_frame.pack(fill="both", expand=True, padx=10, pady=10)
        days_frame = ctk.CTkFrame(left_frame, fg_color="transparent")  # Прозрачный фон
        days_frame.pack(pady=10)
        days_label = ctk.CTkLabel(days_frame, text="Выберите дни тренировок:")
        days_label.pack(pady=5)
        self.days_checkboxes = []
        for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
            checkbox = ctk.CTkCheckBox(days_frame, text=day)
            checkbox.pack(anchor="w", padx=10, pady=2)
            self.days_checkboxes.append(checkbox)
        start_workout_button = ctk.CTkButton(left_frame, text="Начать тренировку", command=self.start_workout)
        start_workout_button.pack(pady=10)
        measure_body_fat_button = ctk.CTkButton(left_frame, text="Узнать оптимальное КБЖУ", command=self.body_fat_measure)
        measure_body_fat_button.pack(pady=10)
        # Правая часть
        right_frame = ctk.CTkFrame(right_frame_outer, fg_color="#2b2b2b")  # Прозрачный фон
        right_frame.pack(fill="both", expand=True, padx=10, pady=10)
        progress_button = ctk.CTkButton(right_frame, text="Просмотреть прогресс", command=self.show_progress_graph)
        progress_button.pack(pady=10)
        update_progress_button = ctk.CTkButton(right_frame, text="Обновить прогресс", command=self.update_progress)
        update_progress_button.pack(pady=10)
        save_progress_button = ctk.CTkButton(right_frame, text="Сохранить прогресс", command=self.save_progress)
        save_progress_button.pack(pady=10)
        reset_progress_button = ctk.CTkButton(right_frame, text="Сбросить прогресс", command=self.reset_progress)
        reset_progress_button.pack(pady=10)

    def load_progress(self):
        """Загрузка прогресса из файла."""
        try:
            with open('progress_data.json', 'r') as file:
                self.progress_data = json.load(file)
        except FileNotFoundError:
            self.progress_data = {}

    def save_progress(self):
        """Сохранение прогресса в файл."""
        try:
            with open('progress_data.json', 'w') as file:
                json.dump(self.progress_data, file, indent=4)
            messagebox.showinfo("Успех", "Прогресс успешно сохранён!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить прогресс: {str(e)}")

    def update_progress(self):
        """Обновляет данные о прогрессе пользователя."""
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_weight = float(self.weight_input.get().replace(',', '.'))
            self.progress_data[current_date] = current_weight
            self.save_progress()
            messagebox.showinfo("Успех", "Прогресс обновлён!")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность введенных данных. Важно, чтобы вы вводили только числа.")

    def show_progress_graph(self):
        """Отображение графика прогресса."""
        if not self.progress_data:
            messagebox.showinfo("Информация", "Нет данных о прогрессе.")
            return
        sorted_dates = sorted(self.progress_data.keys())
        weights = [self.progress_data[date] for date in sorted_dates]
        plt.figure(figsize=(8, 5))
        plt.plot(sorted_dates, weights, marker='o', linestyle='-', color='b')
        plt.title("Прогресс по весу")
        plt.xlabel("Даты")
        plt.ylabel("Вес (кг)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def reset_progress(self):
        """Сброс прогресса."""
        self.progress_data = {}
        self.save_progress()
        messagebox.showinfo("Успех", "Прогресс успешно сброшен!")

    def fill_info(self):
        try:
            # Проверка на пустые поля
            if not all([self.age_input.get(), self.height_input.get(), self.weight_input.get()]):
                raise BlankField()
            
            # Проверка на выбор пола
            if not self.sex_var.get():
                raise ValueError("Выберите пол")
            
            # Преобразование значений в числа
            age = float(self.age_input.get().replace(',', '.'))
            height = float(self.height_input.get().replace(',', '.'))
            weight = float(self.weight_input.get().replace(',', '.'))
            
            # Проверка на возраст
            if age < 16 or age > 60:
                raise ValueError("Возраст должен быть от 16 до 60 лет")
            
            # Заполнение базы данных
            self.database['Age'] = age
            self.database['Height'] = height
            self.database['Weight'] = weight
            self.database['Sex'] = self.sex_var.get()
            
            goal = self.goal_var.get()
            if goal == "Bulking":
                self.database['Bulking'] = True
            elif goal == "Losing":
                self.database['Losing'] = True
            elif goal == "Healthing":
                self.database['Healthing'] = True
            
            if not any([self.database['Bulking'], self.database['Losing'], self.database['Healthing']]):
                raise BlankField()
            
            # Переход на вторую страницу
            self.stacked_widget.winfo_children()[2].pack(fill="both", expand=True)
            self.stacked_widget.winfo_children()[1].pack_forget()
        
        except BlankField as e:
            messagebox.showerror("Ошибка", str(e))
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def body_fat_measure(self):
        dialog = BodyFatDialog(self.database)
        dialog.mainloop()

    def start_workout(self):
        selected_days = [cb.cget("text") for cb in self.days_checkboxes if cb.get()]
        if not selected_days:
            messagebox.showwarning("Предупреждение", "Выберите хотя бы один день недели")
            return
        workout_plan = {}
        for day in selected_days:
            workout_plan[day] = []
            exercises = []
            for key in self.database.keys():
                if self.database[key] and key in self.exercise_database:
                    exercises.extend(self.exercise_database[key])
            shuffle(exercises)
            age_limiter = 0
            if 16 <= self.database['Age'] <= 20:
                age_limiter = 0
            elif 21 <= self.database['Age'] <= 40:
                age_limiter = 1
            else:
                age_limiter = 2
            step = 0
            while exercises:
                if step == len(selected_days):
                    step = 0
                workout_plan[selected_days[step]].append(
                    (exercises[0][0], self.duration_database[exercises[0][1]][age_limiter])
                )
                del exercises[0]
                step += 1
        self.show_workout_plan(workout_plan)

    def show_workout_plan(self, workout_plan):
        plan_window = ctk.CTkToplevel(self)
        plan_window.title("Тренировочный план")
        plan_window.geometry("700x500")
        for day, exercises in workout_plan.items():
            day_label = ctk.CTkLabel(plan_window, text=day, font=("Arial", 16, "bold"))
            day_label.pack(pady=5)
            exercises_text = ', '.join([f"{name} ({duration})" for name, duration in exercises])
            exercises_label = ctk.CTkLabel(plan_window, text=exercises_text, font=("Arial", 14), wraplength=600)
            exercises_label.pack(pady=5)

    def welcome(self):
        welcome_window = ctk.CTkToplevel(self)
        welcome_window.title("Краткий экскурс")
        welcome_window.geometry("700x500")
        welcome_phrases = {
            'Bulking': [
                "Набор массы - трудный и ресурсозатратный процесс.",
                " и ужасно большим приёмам пищи. ",
                "Плюсы - можно есть почти всё, что в холодильнике, и не надо делать кардиотренировки."
            ],
            'Losing': [
                "\nСбрасывать вес трудно психологически. Различные ограничения, диеты - очень давит эмоционально.",
                "\nПридётся ограничивать себя почти во всём и заниматься, в первую очередь, кардиотренировками: ",
                "\nбег, степ, велотренировки и т.п."
            ],
            'Healthing': [
                "\nЗдоровье всегда трудно поправлять. Это походы ко врачам, понимание своих индивидуальных проблем.",
                "\nДалее будут лишь общие советы."
            ]
        }
        message_text = []
        for key in welcome_phrases.keys():
            if self.database[key]:
                message_text.append(''.join(welcome_phrases[key]))
        message_label = ctk.CTkLabel(welcome_window, text=' А теперь к другим советам. '.join(message_text), wraplength=600, font=("Arial", 16))
        message_label.pack(padx=20, pady=20)

class BodyFatDialog(ctk.CTkToplevel):
    def __init__(self, database):
        super().__init__()
        self.title("Оптимальное КБЖУ")
        self.geometry("600x400")
        self.db = database
        layout = ctk.CTkFrame(self)
        layout.pack(fill="both", expand=True, padx=20, pady=20)
        info_label = ctk.CTkLabel(layout, text=f"Возраст: {int(self.db['Age'])} лет\n"
                                               f"Рост: {int(self.db['Height'])} см\n"
                                               f"Вес: {int(self.db['Weight'])} кг",
                                  font=("Arial", 20))
        info_label.pack(pady=10)
        self.calculate_and_display_info()

    def calculate_and_display_info(self):
        gender = self.db['Sex']
        weight = self.db['Weight']
        height = self.db['Height']
        age = self.db['Age']
        bulking = self.db['Bulking']
        losing = self.db['Losing']
        healthing = self.db['Healthing']
        calories = self.calculate_calories(gender, weight, height, age, bulking, losing, healthing)
        rounded_calories = int(calories)
        proteins = int(calories * 0.3 / 4)
        fats = int(calories * 0.3 / 9)
        carbs = int(calories * 0.4 / 4)
        info_text = f"{'Для набора мышечной массы' if bulking else 'Для похудения' if losing else 'Для укрепления здоровья'}:\n" \
                    f"Калории: {rounded_calories}\n" \
                    f"Белки: {proteins} г\n" \
                    f"Жиры: {fats} г\n" \
                    f"Углеводы: {carbs} г"
        info_label = ctk.CTkLabel(self, text=info_text, font=("Arial", 20))
        info_label.pack(pady=10)

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

if __name__ == "__main__":
    app = GymHelper()
    app.mainloop()