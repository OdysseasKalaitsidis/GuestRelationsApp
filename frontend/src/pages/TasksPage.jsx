import React, { useState, useEffect } from "react";
import { fetchTasks, createTask, createDailyTasks, updateTask, deleteTask, fetchUsers, resetDailyCases, isAuthenticated } from "../services/api";
import UploadModal from "../components/UploadModal";

const TasksPage = ({ user }) => {
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showCreateTask, setShowCreateTask] = useState(false);
  const [showCreateDaily, setShowCreateDaily] = useState(false);
  const [showDailyReset, setShowDailyReset] = useState(false);
  const [editingTask, setEditingTask] = useState(null);


  // Form states
  const [newTask, setNewTask] = useState({
    title: "",
    description: "",
    task_type: "amenity_list",
    assigned_to: "",
    due_date: new Date().toISOString().split('T')[0]
  });
  const [customTitle, setCustomTitle] = useState("");
  const [isCustomTitle, setIsCustomTitle] = useState(false);
  const [dailyTaskDate, setDailyTaskDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    // Only load data if user is authenticated
    if (isAuthenticated()) {
      loadTasks();
      loadUsers();
    }
  }, []);

  const loadTasks = async () => {
    try {
      setIsLoading(true);
      const tasksData = await fetchTasks();
      setTasks(tasksData);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      const usersData = await fetchUsers();
      setUsers(usersData);
    } catch (err) {
      console.error("Failed to load users:", err);
      // Don't set error state for users loading failure as it's not critical
    }
  };



  const handleCreateTask = async (e) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      
      // Determine the final title and task type
      const finalTitle = isCustomTitle ? customTitle : newTask.title;
      const finalTaskType = isCustomTitle ? "custom" : getTaskTypeFromTitle(newTask.title);
      
      const taskData = {
        title: finalTitle,
        description: newTask.description,
        task_type: finalTaskType,
        assigned_to: newTask.assigned_to ? parseInt(newTask.assigned_to) : null,
        due_date: newTask.due_date
      };
      
      await createTask(taskData);
      setNewTask({
        title: "",
        description: "",
        task_type: "amenity_list",
        assigned_to: "",
        due_date: new Date().toISOString().split('T')[0]
      });
      setCustomTitle("");
      setIsCustomTitle(false);
      setShowCreateTask(false);
      loadTasks();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateDailyTasks = async (e) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      await createDailyTasks(dailyTaskDate);
      setShowCreateDaily(false);
      loadTasks();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateTask = async (taskId, updates) => {
    try {
      await updateTask(taskId, updates);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      try {
        await deleteTask(taskId);
        loadTasks();
      } catch (err) {
        setError(err.message);
      }
    }
  };

  const handleDailyReset = async () => {
    if (window.confirm("Are you sure you want to reset all cases, followups, and tasks for a new day? This action cannot be undone.")) {
      try {
        setIsLoading(true);
        const result = await resetDailyCases();
        alert(`Daily reset completed!\nArchived ${result.archived_cases} cases\nCompleted ${result.completed_followups} followups\nCompleted ${result.completed_tasks} tasks`);
        loadTasks();

        setShowDailyReset(false);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const getTaskTypeLabel = (type) => {
    switch (type) {
      case "amenity_list": return "Amenity List";
      case "emails": return "Emails";
      case "courtesy_calls": return "Courtesy Calls";
      case "custom": return "Custom";
      default: return type;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "pending": return "bg-yellow-100 text-yellow-800";
      case "in_progress": return "bg-blue-100 text-blue-800";
      case "completed": return "bg-green-100 text-green-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getUserName = (userId) => {
    const user = users.find(u => u.id === userId);
    return user ? user.name : "Unknown";
  };

  const getTaskTypeFromTitle = (title) => {
    switch (title) {
      case "Amenity List Check":
        return "amenity_list";
      case "Email Management":
        return "emails";
      case "Courtesy Calls":
        return "courtesy_calls";
      default:
        return "custom";
    }
  };

  const handleTitleChange = (value) => {
    if (value === "custom") {
      setIsCustomTitle(true);
      setNewTask({...newTask, title: ""});
    } else {
      setIsCustomTitle(false);
      setCustomTitle("");
      setNewTask({...newTask, title: value});
    }
  };

  // Don't render if user is not authenticated
  if (!isAuthenticated()) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Authentication Required</h1>
          <p className="text-gray-600">Please login to access this page.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold text-gray-900">📋 Tasks Management</h1>
          {user?.is_admin && (
            <div className="flex space-x-3">
              <button
                onClick={() => setShowCreateTask(true)}
                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
              >
                Create Task
              </button>
              <button
                onClick={() => setShowCreateDaily(true)}
                className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
              >
                Create Daily Tasks
              </button>
              <button
                onClick={() => setShowDailyReset(true)}
                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
              >
                Daily Reset
              </button>
    
            </div>
          )}
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}


      </div>

      {/* Tasks Table */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">All Tasks</h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Manage daily tasks and assignments
          </p>
        </div>
        
        {isLoading ? (
          <div className="px-4 py-5 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading tasks...</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Task
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Assigned To
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Due Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tasks.map((task) => (
                  <tr key={task.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{task.title}</div>
                        {task.description && (
                          <div className="text-sm text-gray-500">{task.description}</div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                        {getTaskTypeLabel(task.task_type)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {task.assigned_user_name || "Unassigned"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {task.due_date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <select
                        value={task.status}
                        onChange={(e) => handleUpdateTask(task.id, { status: e.target.value })}
                        className={`text-xs font-medium px-2.5 py-0.5 rounded-full border-0 ${getStatusColor(task.status)}`}
                      >
                        <option value="pending">Pending</option>
                        <option value="in_progress">In Progress</option>
                        <option value="completed">Completed</option>
                      </select>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <select
                          value={task.assigned_to || ""}
                          onChange={(e) => handleUpdateTask(task.id, { assigned_to: e.target.value ? parseInt(e.target.value) : null })}
                          className="text-xs border rounded px-2 py-1"
                        >
                          <option value="">Unassigned</option>
                          {users.map(u => (
                            <option key={u.id} value={u.id}>{u.name}</option>
                          ))}
                        </select>
                        {user?.is_admin && (
                          <button
                            onClick={() => handleDeleteTask(task.id)}
                            className="text-red-600 hover:text-red-900 text-xs"
                          >
                            Delete
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Create Task Modal */}
      {showCreateTask && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Create New Task</h2>
            <form onSubmit={handleCreateTask} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                <select
                  value={isCustomTitle ? "custom" : newTask.title}
                  onChange={(e) => handleTitleChange(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                >
                  <option value="">Select a task type</option>
                  <option value="Amenity List Check">Amenity List Check</option>
                  <option value="Email Management">Email Management</option>
                  <option value="Courtesy Calls">Courtesy Calls</option>
                  <option value="custom">Custom Title</option>
                </select>
              </div>
              {isCustomTitle && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Custom Title</label>
                  <input
                    type="text"
                    value={customTitle}
                    onChange={(e) => setCustomTitle(e.target.value)}
                    className="w-full px-3 py-2 border rounded-md"
                    placeholder="Enter custom task title"
                    required
                  />
                </div>
              )}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={newTask.description}
                  onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                  className="w-full px-3 py-2 border rounded-md"
                  rows={3}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Assign To</label>
                <select
                  value={newTask.assigned_to}
                  onChange={(e) => setNewTask({...newTask, assigned_to: e.target.value})}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="">Unassigned</option>
                  {users.map(u => (
                    <option key={u.id} value={u.id}>{u.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                <input
                  type="date"
                  value={newTask.due_date}
                  onChange={(e) => setNewTask({...newTask, due_date: e.target.value})}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowCreateTask(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300"
                >
                  {isLoading ? "Creating..." : "Create Task"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Daily Tasks Modal */}
      {showCreateDaily && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Create Daily Tasks</h2>
            <p className="text-gray-600 mb-4">
              This will create the three daily tasks: Amenity List, Emails, and Courtesy Calls.
            </p>
            <form onSubmit={handleCreateDailyTasks} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                <input
                  type="date"
                  value={dailyTaskDate}
                  onChange={(e) => setDailyTaskDate(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowCreateDaily(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:bg-gray-300"
                >
                  {isLoading ? "Creating..." : "Create Daily Tasks"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Daily Reset Modal */}
      {showDailyReset && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4 text-red-600">⚠️ Daily Reset</h2>
            <div className="mb-4">
              <p className="text-gray-700 mb-2">
                This will reset all data for a new day:
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                <li>Archive all current cases</li>
                <li>Mark all followups as completed</li>
                <li>Mark all tasks as completed</li>
              </ul>
              <p className="text-red-600 font-semibold mt-3">
                This action cannot be undone!
              </p>
            </div>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowDailyReset(false)}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDailyReset}
                disabled={isLoading}
                className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 disabled:bg-gray-300"
              >
                {isLoading ? "Resetting..." : "Reset Daily"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Upload Modal */}
      <UploadModal
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        onWorkflowComplete={() => {
          setShowUploadModal(false);
          loadTasks(); // Refresh tasks after workflow completion
        }}
      />
    </div>
  );
};

export default TasksPage;
