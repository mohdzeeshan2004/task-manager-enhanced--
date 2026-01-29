import streamlit as st
from datetime import datetime
import pandas as pd
import json
import os

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="Task Manager Pro",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------
# Custom CSS Styling
# ----------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .task-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            border-left: 5px solid #6366f1;
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        .task-card.high-priority {
            border-left-color: #ef4444;
        }
        
        .task-card.medium-priority {
            border-left-color: #f59e0b;
        }
        
        .task-card.low-priority {
            border-left-color: #10b981;
        }
        
        .priority-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 10px;
        }
        
        .priority-1 { background-color: #fee2e2; color: #991b1b; }
        .priority-2 { background-color: #fef3c7; color: #92400e; }
        .priority-3 { background-color: #fef3c7; color: #92400e; }
        .priority-4 { background-color: #dcfce7; color: #166534; }
        .priority-5 { background-color: #dcfce7; color: #166534; }
        
        .status-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .status-pending {
            background-color: #dbeafe;
            color: #0c4a6e;
        }
        
        .status-completed {
            background-color: #dcfce7;
            color: #166534;
        }
        
        .task-name {
            font-size: 18px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 10px;
        }
        
        .task-meta {
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .header-title {
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        .stats-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            border-top: 4px solid #667eea;
        }
        
        .stats-number {
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
        }
        
        .stats-label {
            font-size: 14px;
            color: #6b7280;
            margin-top: 8px;
        }
        
        .input-section {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            border-top: 4px solid #667eea;
        }
        
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 20px;
        }
        
        .storage-info {
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 12px;
            color: #4f46e5;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Storage Configuration
# ----------------------------------------
STORAGE_DIR = os.path.expanduser("~/.streamlit_app_data")
STORAGE_FILE = os.path.join(STORAGE_DIR, "tasks.json")

# Create storage directory if it doesn't exist
os.makedirs(STORAGE_DIR, exist_ok=True)

# ----------------------------------------
# Initialize Session State
# ----------------------------------------
if 'taskName' not in st.session_state:
    st.session_state.taskName = []
    st.session_state.taskPriority = []
    st.session_state.taskStatus = []
    st.session_state.taskCreated = []

# ----------------------------------------
# Storage Functions
# ----------------------------------------
def loadTasksFromStorage():
    """Load tasks from persistent JSON storage"""
    try:
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, 'r') as f:
                data = json.load(f)
                st.session_state.taskName = data.get('taskName', [])
                st.session_state.taskPriority = data.get('taskPriority', [])
                st.session_state.taskStatus = data.get('taskStatus', [])
                st.session_state.taskCreated = data.get('taskCreated', [])
                return True
        return False
    except Exception as e:
        st.error(f"Error loading tasks: {str(e)}")
        return False

def saveTasksToStorage():
    """Save tasks to persistent JSON storage"""
    try:
        data = {
            'taskName': st.session_state.taskName,
            'taskPriority': st.session_state.taskPriority,
            'taskStatus': st.session_state.taskStatus,
            'taskCreated': st.session_state.taskCreated
        }
        with open(STORAGE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving tasks: {str(e)}")
        return False

def clearAllTasks():
    """Clear all tasks from storage and session"""
    st.session_state.taskName = []
    st.session_state.taskPriority = []
    st.session_state.taskStatus = []
    st.session_state.taskCreated = []
    saveTasksToStorage()

# Load tasks when app starts
if not st.session_state.taskName:
    loadTasksFromStorage()

# ----------------------------------------
# Validation Functions
# ----------------------------------------
def validatePriority(priority):
    """Validate priority is between 1 and 5"""
    try:
        priority_int = int(priority)
        if 1 <= priority_int <= 5:
            return priority_int, True
        else:
            return None, False
    except ValueError:
        return None, False

def validateStatus(status):
    """Validate status is either Pending or Completed"""
    if status in ["Pending", "Completed"]:
        return status, True
    return None, False

def addTask(name, priority, status):
    """Add a new task to the lists"""
    if not name.strip():
        return False, "Task name cannot be empty"
    
    priority_valid, is_valid = validatePriority(priority)
    if not is_valid:
        return False, "Priority must be between 1 and 5"
    
    status_valid, is_valid = validateStatus(status)
    if not is_valid:
        return False, "Status must be 'Pending' or 'Completed'"
    
    st.session_state.taskName.append(name)
    st.session_state.taskPriority.append(priority_valid)
    st.session_state.taskStatus.append(status_valid)
    st.session_state.taskCreated.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Save to persistent storage
    if saveTasksToStorage():
        return True, "Task added successfully!"
    else:
        return False, "Task added but could not save to storage"

def deleteTask(index):
    """Delete a task by index"""
    st.session_state.taskName.pop(index)
    st.session_state.taskPriority.pop(index)
    st.session_state.taskStatus.pop(index)
    st.session_state.taskCreated.pop(index)
    saveTasksToStorage()

def updateTaskStatus(index, new_status):
    """Update task status"""
    st.session_state.taskStatus[index] = new_status
    saveTasksToStorage()

def getPriorityColor(priority):
    """Get priority level label"""
    levels = {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Minimal"}
    return levels.get(priority, "Unknown")

def getPriorityClass(priority):
    """Get CSS class for priority"""
    if priority <= 2:
        return "high-priority"
    elif priority == 3:
        return "medium-priority"
    else:
        return "low-priority"

def exportTasksToCSV():
    """Export tasks to CSV format"""
    if not st.session_state.taskName:
        return None
    
    df = pd.DataFrame({
        'Task': st.session_state.taskName,
        'Priority': [getPriorityColor(p) for p in st.session_state.taskPriority],
        'Status': st.session_state.taskStatus,
        'Created': st.session_state.taskCreated
    })
    return df.to_csv(index=False).encode('utf-8')

# ----------------------------------------
# Sidebar Settings
# ----------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    # Storage Info
    st.markdown(f"""
        <div class='storage-info'>
        💾 **Storage:** {STORAGE_FILE}
        </div>
    """, unsafe_allow_html=True)
    
    # Data Management
    st.markdown("#### 📊 Data Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Now", use_container_width=True):
            if saveTasksToStorage():
                st.success("Tasks saved successfully!")
            else:
                st.error("Failed to save tasks")
    
    with col2:
        if st.button("🔄 Reload", use_container_width=True):
            if loadTasksFromStorage():
                st.success("Tasks reloaded!")
                st.rerun()
            else:
                st.info("No saved tasks found")
    
    # Export
    if st.session_state.taskName:
        csv_data = exportTasksToCSV()
        st.download_button(
            label="📥 Export as CSV",
            data=csv_data,
            file_name=f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Danger Zone
    st.markdown("#### ⚠️ Danger Zone")
    if st.button("🗑️ Clear All Tasks", use_container_width=True):
        if st.button("⚠️ Confirm: Delete All?", use_container_width=True, key="confirm_delete"):
            clearAllTasks()
            st.success("All tasks cleared!")
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
        <div style='font-size: 11px; color: #999;'>
        ✅ Data persists between sessions<br>
        💾 Stored locally on your device<br>
        🔐 Private and secure
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------
# Main App Layout
# ----------------------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<div class='header-title'>✓ Task Manager Pro</div>", unsafe_allow_html=True)
    st.markdown("Organize, prioritize, and track your tasks efficiently")

# ----------------------------------------
# Statistics Section
# ----------------------------------------
if st.session_state.taskName:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-number'>{len(st.session_state.taskName)}</div>
                <div class='stats-label'>Total Tasks</div>
            </div>
        """, unsafe_allow_html=True)
    
    completed = sum(1 for s in st.session_state.taskStatus if s == "Completed")
    with col2:
        st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-number'>{completed}</div>
                <div class='stats-label'>Completed</div>
            </div>
        """, unsafe_allow_html=True)
    
    pending = sum(1 for s in st.session_state.taskStatus if s == "Pending")
    with col3:
        st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-number'>{pending}</div>
                <div class='stats-label'>Pending</div>
            </div>
        """, unsafe_allow_html=True)
    
    completion = int((completed / len(st.session_state.taskName)) * 100) if st.session_state.taskName else 0
    with col4:
        st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-number'>{completion}%</div>
                <div class='stats-label'>Progress</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------
# Add Task Section
# ----------------------------------------
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>➕ Add New Task</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    task_name = st.text_input("Task Description", placeholder="Enter your task...")

with col2:
    priority = st.selectbox("Priority Level", [1, 2, 3, 4, 5], format_func=lambda x: f"{x} - {getPriorityColor(x)}")

with col3:
    status = st.selectbox("Status", ["Pending", "Completed"])

col_add, col_space = st.columns([1, 4])
with col_add:
    if st.button("➕ Add Task", use_container_width=True, key="add_task_btn"):
        success, message = addTask(task_name, priority, status)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------
# Display Tasks Section
# ----------------------------------------
if st.session_state.taskName:
    st.markdown("<div class='section-title'>📋 Your Tasks</div>", unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
    with col2:
        sort_by = st.selectbox("Sort by", ["Priority (High to Low)", "Priority (Low to High)", "Newest First", "Oldest First"])
    with col3:
        search_term = st.text_input("Search tasks", placeholder="Search...")
    
    # Filter tasks
    filtered_indices = []
    for i, (name, status) in enumerate(zip(st.session_state.taskName, st.session_state.taskStatus)):
        if filter_status != "All" and status != filter_status:
            continue
        if search_term and search_term.lower() not in name.lower():
            continue
        filtered_indices.append(i)
    
    # Sort tasks
    if sort_by == "Priority (High to Low)":
        filtered_indices.sort(key=lambda i: st.session_state.taskPriority[i])
    elif sort_by == "Priority (Low to High)":
        filtered_indices.sort(key=lambda i: st.session_state.taskPriority[i], reverse=True)
    elif sort_by == "Newest First":
        filtered_indices.sort(key=lambda i: i, reverse=True)
    
    # Display filtered tasks
    if filtered_indices:
        for idx in filtered_indices:
            task_name = st.session_state.taskName[idx]
            task_priority = st.session_state.taskPriority[idx]
            task_status = st.session_state.taskStatus[idx]
            task_time = st.session_state.taskCreated[idx]
            
            priority_class = getPriorityClass(task_priority)
            priority_label = getPriorityColor(task_priority)
            
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 0.5])
            
            with col1:
                st.markdown(f"""
                    <div class='task-card {priority_class}'>
                        <div class='task-name'>{task_name}</div>
                        <div class='task-meta'>
                            <span class='priority-badge priority-{task_priority}'>Priority: {priority_label}</span>
                            <span class='status-badge status-{task_status.lower()}'>● {task_status}</span>
                            <span style='color: #999; font-size: 12px;'>Added: {task_time}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if task_status == "Pending":
                    if st.button("✓ Complete", key=f"complete_{idx}", use_container_width=True):
                        updateTaskStatus(idx, "Completed")
                        st.rerun()
                else:
                    if st.button("↩ Reopen", key=f"reopen_{idx}", use_container_width=True):
                        updateTaskStatus(idx, "Pending")
                        st.rerun()
            
            with col3:
                st.write("")
            
            with col4:
                st.write("")
            
            with col5:
                if st.button("🗑", key=f"delete_{idx}", help="Delete task"):
                    deleteTask(idx)
                    st.rerun()
    else:
        st.info("No tasks match your filters. Try adjusting your search or filters!")

else:
    st.markdown("""
        <div style='text-align: center; padding: 60px 20px;'>
            <div style='font-size: 48px; margin-bottom: 20px;'>📭</div>
            <h2 style='color: #6b7280;'>No Tasks Yet</h2>
            <p style='color: #9ca3af; font-size: 16px;'>Create your first task using the form above to get started!</p>
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------
# Footer
# ----------------------------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #9ca3af; font-size: 12px; padding: 20px;'>
        Task Manager Pro © 2025 | Built with Streamlit | Data Persists Across Sessions
    </div>
""", unsafe_allow_html=True)
