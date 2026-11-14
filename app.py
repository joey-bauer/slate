import streamlit as st
import sqlite3

from database import(
    initialize_database,
    add_task,
    get_tasks
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

with st.form("Add Task"):
    new_task = st.text_input("Enter new task")
    add_new_task = st.form_submit_button("Add")
    if add_new_task:
        add_task(new_task, selected_category)

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
               st.write(f"{task["title"]}")