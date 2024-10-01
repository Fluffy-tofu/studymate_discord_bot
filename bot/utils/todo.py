import pandas as pd
from bot.db.database import SessionLocal
from bot.db.models import User, Todo
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


def add_todo_to_db(username, user_id, title, description, due_date):
    try:
        now = datetime.now()
        with SessionLocal() as db_session:
            # Query the User by discord_id
            user = db_session.query(User).filter_by(discord_id=str(user_id)).first()

            # Create the user in the database if they don't exist
            if not user:
                user = User(discord_id=str(user_id), username=username,
                            email='placeholder@test.com', password_hash='placeholder')
                db_session.add(user)
                db_session.flush()

            else:
                new_session = Todo(discord_user_id=user.discord_id,
                                   title=title,
                                   description=description,
                                   due_date=due_date,
                                   status="pending",
                                   created_at=now)
                db_session.add(new_session)
                db_session.commit()
    except Exception as e:
        print(e)


"""
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
"""


def delete_todo_from_db(todo_item_index, user_id):
    try:
        with SessionLocal() as db_session:
            # Query the User by discord_id
            user = db_session.query(User).filter_by(discord_id=str(user_id)).first()

            if not user:
                return False

            # Get all todos for the user, ordered by creation time
            todos = db_session.query(Todo).filter_by(discord_user_id=user.discord_id).order_by(Todo.created_at.asc()).all()

            # Check if the index is valid
            if 0 <= todo_item_index - 1 < len(todos):
                todo_to_delete = todos[todo_item_index - 1]
                db_session.delete(todo_to_delete)
                db_session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return False


def update_todo_in_db(todo_id: int, **kwargs):
    try:
        with SessionLocal() as db_session:
            todo = db_session.query(Todo).filter(Todo.id == todo_id).first()
            print(todo.title)

            if not todo:
                return None, "Todo item not found"

            # Update the fields provided in kwargs
            for key, value in kwargs.items():
                if hasattr(todo, key):
                    setattr(todo, key, value)

            # If due_date is provided, ensure it's a datetime object
            if 'due_date' in kwargs:
                todo.due_date = datetime.strptime(kwargs['due_date'], "%Y-%m-%d")

            # Commit the changes to the database
            db_session.commit()
            print('test')

            return todo, "Todo updated successfully"
    except SQLAlchemyError as e:
        db_session.rollback()
        return None, f"An error occurred: {str(e)}"
