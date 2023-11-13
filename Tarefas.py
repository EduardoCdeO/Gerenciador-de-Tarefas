import flet
from flet import (Checkbox, Column, FloatingActionButton, IconButton, OutlinedButton, Page, Row, Tab, Tabs, Text, 
                  TextField, UserControl, colors, icons)

# Classe de tarefas
class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )

        self.edit_name =TextField(expand=1) # Edição de tarefas
    
        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Editar tarefa", # Texto de orientação
                            on_click=self.edit_clicked,
                            icon_color=colors.GREEN,
                        ),
                        IconButton(
                            icon=icons.DELETE_OUTLINED,
                            tooltip="Remover tarefa", # Texto de orientação
                            on_click=self.delete_clicked,
                            icon_color=colors.RED,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Atualizar tarefa",
                    on_click=self.save_clicked,
                )
            ]
        )
        return Column(controls=[self.display_view, self.edit_view])
    
    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)



# Classe da aplicação
class ToDoApp(UserControl):
    def build(self):
        self.new_task = TextField(
            hint_text= "Digite a tarefa que deseja adicionar...",
            expand=True,
            on_submit=self.add_clicked
        )
        self.tasks = Column()

        self.filter = Tabs(
            selected_index = 0,
            on_change = self.tabs_changed,
            tabs=[Tab(text="Todas tarefas"), Tab(text="Tarefas ativas"), Tab(text="Tarefas concluídas")]
        )

        self.items_left = Text("0 tarefas pendentes")

        return Column(
            width=600,
            controls=[
                # Titulo da aplicação
                Row([Text(value="Tarefas", 
                          style="headlineMedium")], alignment="center"),
                # Input das tarefas
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked)
                    ],
                ),
                Column(
                    spacing=20,
                    controls=[
                        self.filter,
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text="Limpar as tarefas concluídas".upper(),
                                    on_click=self.clear_clicked,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "Todas tarefas"
                or (status == "Tarefas ativas" and task.completed == False)
                or (status == "Tarefas concluídas" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} tarefas pendentes"
        super().update()


# Função Principal
def main(page: Page):
    page.title = "Tarefas"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.update()

    # Instanciado a classe principal
    app = ToDoApp()

    # Adicionando a aplicação na página
    page.add(app)


flet.app(target=main)