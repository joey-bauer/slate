import streamlit as st

tabs = ["coding", "personal", "test"]

if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

selected_category = st.segmented_control("Slate", tabs)

with st.form("Add Task"):
    new_task = st.text_input("Enter new task")
    add_new_task = st.form_submit_button("Add")
    if add_new_task:
        st.session_state["tasks"].append({
            "task name": new_task,
            "tab": selected_category
        })

for task in st.session_state["tasks"]:
    if task["tab"] == selected_category:
        st.write(task["task name"])