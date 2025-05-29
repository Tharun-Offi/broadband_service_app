document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchQuery = document.getElementById('search-query');
    const planFilter = document.getElementById('plan-filter');
    const userTableContainer = document.getElementById('user-table-container');

    const fetchUsers = () => {
        const query = searchQuery.value;
        const plan = planFilter.value;

        fetch(`${searchForm.action}?query=${query}&plan_filter=${plan}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(response => response.json())
            .then(data => {
                let tableContent = '';
                if (data.length > 0) {
                    tableContent += `
                        <table class="user_table">
                            <thead>
                                <tr>
                                    <th>Username</th>
                                    <th>Phone</th>
                                    <th>Email</th>
                                    <th>Address</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    data.forEach(user => {
                        tableContent += `
                            <tr>
                                <td>${user.username}</td>
                                <td>${user.phone_number}</td>
                                <td>${user.email}</td>
                                <td>${user.address}</td>
                                <td>
                                    <a href="/admin/edit_user/${user.id}">Edit</a>
                                    <form method="POST" action="/admin/delete_user/${user.id}" style="display:inline;">
                                        <button type="submit">Delete</button>
                                    </form>
                                </td>
                            </tr>
                        `;
                    });
                    tableContent += '</tbody></table>';
                } else {
                    tableContent = '<p class="no-users">No users found.</p>';
                }
                userTableContainer.innerHTML = tableContent;
            });
    };

    searchQuery.addEventListener('input', fetchUsers);
    planFilter.addEventListener('change', fetchUsers);
});
