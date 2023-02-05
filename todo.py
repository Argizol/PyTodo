from cProfile import label
import json
from datetime import date, datetime


#консольное прилозение заметок
__file = "todo.json"

def delete_todo(_id:int):
    try:
        get_all_todo = read_todo_all() if read_todo_all() is not None else []
        if 'нет' in get_all_todo:
            return get_all_todo
        get_all_ids = [__id["id"] for __id in get_all_todo]
        if _id not in get_all_ids:
            return 'Запись с таким id остсутствует\n'
        new_all_todo = [todo for todo in get_all_todo if todo['id'] != _id]
        with open(__file, "w") as f:
            f.write(json.dumps(new_all_todo, ensure_ascii=False))
        return f'Заметка успешно удалена\n'
    except FileNotFoundError:
        return "Заметки отсутствуют\n"

def update_todo(_id:int, title, body):
    try:
        get_all_todo = read_todo_all() if read_todo_all() is not None else []
        if 'нет' in get_all_todo:
            return get_all_todo
        get_all_ids = [__id["id"] for __id in get_all_todo]
        if _id not in get_all_ids:
            return 'Запись с таким id остсутствует\n'
        new_todo = [todo for todo in get_all_todo if todo['id'] != _id]
        todo = {}
        for i in get_all_todo:
            if _id == i['id']:
                todo.update(
                        {
                            "id": i['id'], 
                            "title": title, 
                            "body": body, 
                            "created_at": i['created_at'], 
                            "date_update": datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
                        }               
                    )
                break
        new_todo.append(todo)
        with open(__file, 'w') as f:
            f.write(json.dumps(new_todo, ensure_ascii=False))
        return f"Заметка успешно обновлена\n"
    except FileNotFoundError:
        return "Заметки отсутствуют\n"

def read_todo(_id:int):
    try:
        get_all_todo = read_todo_all() if read_todo_all() is not None else []
        if 'нет' in get_all_todo:
            return get_all_todo
        get_all_ids = [__id["id"] for __id in get_all_todo]
        if _id not in get_all_ids:
            return 'Запись с таким id остсутствует\n'
        with open(__file,'r') as f:
            todo = json.loads(f.read())
            for _ in todo:
                if _id == _['id']:
                    return _
    except FileNotFoundError:
        return "Записей нет\n"

def read_todo_all():
    try:
        with open(__file,'r') as f:
            return sorted(
                json.loads(f.read()),
                key=lambda x: (x["created_at"] == "null", x["created_at"] == "", x["created_at"]), 
                reverse=True
            )
    except json.JSONDecodeError:
        return None
    except FileNotFoundError:
        return "Записей нет\n"
               
def __get_last_id():
    try:
        with open(__file,'r') as f:
            last_id = [_id['id'] for _id in json.loads(f.read())]
            return max(last_id) if len(last_id) != 0 else 0
    except json.JSONDecodeError:
        return None
    except FileNotFoundError:
        with open(__file,'a') as f:
            return None


def add_todo(title, body):
    __date = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    last_id = __get_last_id() if __get_last_id() is not None else 0
    new_todo = {
        "id": last_id + 1 , 
        "title": title, 
        "body": body, 
        "created_at": __date, 
        "date_update": __date
    }
    get_all_todo = read_todo_all() if read_todo_all() is not None else []
    all_todo = list(get_all_todo)
    all_todo.append(new_todo)
    with open(__file, "w") as f:
        f.write(json.dumps(all_todo, ensure_ascii=False))
    return f"Заметка успешно сохранена\n"


def beautiful_conclusion(data):
    if type(data) is str:
        print(data)
    if type(data) is dict:
        print(f"\nID - {data['id']}\nЗаголовок - {data['title']}\nТело - {data['body']}\nДата-создания - {data['created_at']}\nДата-обновления заметки - {data['date_update']}\n")
    if type(data) is list:
        for i in data:
            print(f"\nID - {i['id']}\nЗаголовок - {i['title']}\nТело - {i['body']}\nДата-создания - {i['created_at']}\nДата-обновления заметки - {i['date_update']}\n")

if __name__ == "__main__":
    print("Что бы узнать мой список комманд введите help\n")    
    while True:
        _command = str(input("Введите команду: ")).replace(" ", "")
        match _command:
            case "add": 
                _title = str(input("Введите заголовок заметки: "))
                _body = str(input("Введите тело заметки: "))
                beautiful_conclusion(add_todo(_title, _body))
            case "read": 
                _id = int(input("Введите ID записи которую хотите прочитать: "))
                beautiful_conclusion(read_todo(_id))
            case "read_all": 
                beautiful_conclusion(read_todo_all())
            case "delete": 
                _id = int(input("Введите ID записи которую хотите удалить: "))
                beautiful_conclusion(delete_todo(_id))
            case "update": 
                _id = int(input("Введите ID записи которую хотите изменить: "))
                _title = str(input("Введите новый заголовок заметки: "))
                _body = str(input("Введите новое тело заметки: "))
                beautiful_conclusion(update_todo(_id, _title, _body))
            case "help":
                print("\nadd -> Добавить запись\nread -> Показать определенную заметку ID\nread_all -> Показать все заметки\ndelete -> Удалить заметку по ID\nupdate -> Обновить заметку\nexit -> Выход из программы\n")
            case "exit":
                print("Пока!")
                break
    