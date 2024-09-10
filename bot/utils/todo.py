import pandas as pd



def add_todo_to_csv(todo_item, user_id):
    csv_file = "to_do.csv"
    user_id = str(user_id)

    try:
        df = pd.read_csv(csv_file)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame()

    if user_id not in df.columns:
        df[user_id] = None

    new_row_dict = {col: None for col in df.columns}
    new_row_dict[user_id] = str(todo_item)

    df = pd.concat([df, pd.DataFrame([new_row_dict])], ignore_index=True)

    df.dropna()
    df.to_csv(csv_file, index=False)


def list_todos_from_csv(user_id):
    csv_file = "to_do.csv"
    try:
        df = pd.read_csv(csv_file)
        df.dropna()
        if str(user_id) not in df.columns:
            return []
        return df[str(user_id)].tolist()

    except (FileNotFoundError, pd.errors.EmptyDataError):
        print("why")
        return []


def delete_from_todos_csv(todo_item_index, user_id):
    try:
        user_id = str(user_id)
        df = pd.read_csv("to_do.csv")
        print(df[user_id].count())
        if 0 <= todo_item_index - 1 < df[user_id].count():
            df = df[user_id].drop(todo_item_index - 1).reset_index(drop=True)
            df.to_csv("to_do.csv", index=False)
            return True
        return False
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return False