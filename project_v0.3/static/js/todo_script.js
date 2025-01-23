// Get references to the input field, button, and todo list
const todoInput = document.getElementById('todoInput');
const addTodoButton = document.getElementById('addTodoButton');
const todoList = document.getElementById('todoList');


// Function to load todos from the `/todos` endpoint
async function loadTodos() {
    try {
        const response = await fetch('/todos');
        if (!response.ok) {
            throw new Error(`Failed to fetch todos: ${response.statusText}`);
        }
        const data = await response.json();

        // Clear the existing todo list
        todoList.innerHTML = '';

        // Add todos to the list
        if (data.todos && Array.isArray(data.todos)) {
            data.todos.forEach(todo => {
                const listItem = document.createElement('li');
                listItem.textContent = todo;
                todoList.appendChild(listItem);
            });
        }
    } catch (error) {
        console.error('Error loading todos:', error);
    }
}

// Enable the button only if there is text input
todoInput.addEventListener('input', () => {
    if (todoInput.value.trim().length > 0) {
        addTodoButton.disabled = false; // Enable button
    } else {
        addTodoButton.disabled = true; // Disable button
    }
});

addTodoButton.addEventListener('click', async () => {
    const newTodo = todoInput.value.trim();

    if (newTodo.length > 0 && newTodo.length <= 140) {
        // Send the new todo to the backend via POST
        const response = await fetch('/add_todo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ todo: newTodo }),
        });

        // If response is OK, refresh the list
        const data = await response.json();
        if (data.todos) {
            // Clear and re-render the list with updated todos
            todoList.innerHTML = ''; // Clear existing list
            data.todos.forEach(todo => {
                const listItem = document.createElement('li');
                listItem.textContent = todo;
                todoList.appendChild(listItem);
            });

            // Reset input field
            todoInput.value = '';
            addTodoButton.disabled = true;
        }
    }
});

// Load todos automatically when the page loads
window.onload = loadTodos;
