import streamlit as st
import sqlite3

from database import(
    initialize_database,
    add_task,
    get_tasks,
    update_task
)

st.set_page_config(page_title="slate", page_icon="🗒️", layout="wide")

try:
    initialize_database()
except sqlite3.Error:
    st.error("Slate could not open the session database.")
    st.stop()

tabs = ["coding", "personal", "test"]

if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

selected_category = st.segmented_control("Slate", tabs)

with st.form("Add Task", key="add_task_form"):
    new_task = st.text_input(
        "Enter new task",
        key="new_task_name"                 
    ).strip()
    submitted = st.form_submit_button("Add")

    if submitted:
        try:
            add_task(new_task, selected_category)
        except ValueError as error:
            st.warning(str(error))
        except sqlite3.Error:
            st.error("Could not save task, please try again.")
        else:
            st.rerun()

try:
    tasks = get_tasks()
except:
    st.error("Could not load tasks. Please refresh to try again.")
else:
    if not tasks:
        st.info("Added tasks will display here.")
    else:
        for task in tasks:
           if selected_category == task["category"]:
                completed = False
                if task["status"] == "complete":
                    completed = True
                else:
                    completed = False
                
                status = st.checkbox(f"{task["title"]}", value=completed, key=task["id"])
                
                if status != completed and status == False:
                    update_task(task["id"], "incomplete")
                elif status != completed and status == True:
                    update_task(task["id"], "complete")