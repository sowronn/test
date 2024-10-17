from PySide6.QtCore import QObject, Slot
from Python.CRUD.Task.Create import insert_task

class TaskHandler(QObject):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.task_name = ""
        self.task_priority = 0
        self.tags = []
        self.users = []
        self.start_date = None
        self.end_date = None
        self.checked = 0

    @Slot(str)
    def add_task_name(self, taskname):
        if taskname.strip():
            self.task_name = taskname
        else:
            print("Erreur : Le nom de la tâche ne peut pas être vide.")

    @Slot(int)
    def add_task_priority(self, priority):
        if priority in [0, 1, 2]:
            self.task_priority = priority
        else:
            print("Erreur : Priorité invalide.")

    @Slot(str)
    def add_tag(self, tag):
        if tag.strip():
            self.tags.append(tag)
            self._update_tags_in_qml()
        else:
            print("Erreur : Tag invalide.")

    @Slot()
    def remove_last_tag(self):
        if self.tags:
            self.tags.pop()
            self._update_tags_in_qml()

    @Slot(str)
    def add_user(self, user):
        if user.strip():
            self.users.append(user)
            self._update_users_in_qml()
        else:
            print("Erreur : Utilisateur invalide.")

    @Slot()
    def remove_last_user(self):
        if self.users:
            self.users.pop()
            self._update_users_in_qml()

    def _update_tags_in_qml(self):
        root_object = self.engine.rootObjects()[0]
        root_object.setProperty("tagsListModel", self.tags)

    def _update_users_in_qml(self):
        root_object = self.engine.rootObjects()[0]
        root_object.setProperty("usersListModel", self.users)

    @Slot(str)
    def add_start_date(self, startdate):
        try:
            self.start_date = self._validate_date_format(startdate)
        except ValueError as e:
            print(f"Erreur : {e}")

    @Slot(str)
    def add_end_date(self, enddate):
        try:
            self.end_date = self._validate_date_format(enddate)
        except ValueError as e:
            print(f"Erreur : {e}")

    def _validate_date_format(self, date_str):
        from format_date import validate_date_format
        return validate_date_format(date_str)

    def _check_dates_consistency(self):
        if self.start_date and self.end_date:
            from format_date import check_dates_consistency
            check_dates_consistency(self.start_date, self.end_date)

    @Slot(int)
    def task_completed(self, status):
        self.checked = status

    @Slot()
    def validate_info(self):
        try:
            if not self.task_name:
                raise ValueError("Le nom de la tâche ne peut pas être vide.")
            if not self.start_date or not self.end_date:
                raise ValueError("Les dates de début et de fin doivent être renseignées.")
            self._check_dates_consistency()
            formatted_tags = ", ".join(self.tags)

            insert_task("Task", {
                "name": self.task_name,
                "end_date": self.end_date,
                "checked": self.checked,
                "priority": self.task_priority,
                "tag": formatted_tags,
            })

            print("----- Informations sur la tâche -----")
            priority_labels = ["Priorité basse", "Priorité moyenne", "URGENT"]
            print(f"Nom de la tâche : {self.task_name}")
            print(f"Priorité : {priority_labels[self.task_priority]}")
            print(f"Tags : {self.tags}")
            print(f"Utilisateurs : {self.users}")
            print(f"Date de début : {self.start_date}")
            print(f"Date de fin : {self.end_date}")
            print(f"Checked : {self.checked}")

        except ValueError as e:
            print(f"Erreur de validation : {e}")
