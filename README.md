========================================
        GitHub User Finder
========================================

Author: [Ваше Имя Фамилия]

----------------------------------------
Description
----------------------------------------
GitHub User Finder is a GUI application written in Python that allows you to search for GitHub users via the GitHub API, view their details, and save selected users to a local favorites list stored in JSON format.

----------------------------------------
How to Use the API
----------------------------------------
The application uses the public GitHub Search API endpoint:
  https://api.github.com/search/users

To perform a search, the application sends a GET request with a query parameter 'q' containing the username or keywords. The API returns a JSON response with a list of matching users, including their login name, profile URL, avatar URL, type, and score.

Example API request:
  GET https://api.github.com/search/users?q=octocat&per_page=10

Response includes:
  - login        : GitHub username
  - html_url     : Link to the user's GitHub profile
  - avatar_url   : Link to the user's avatar image
  - type         : Account type (User or Organization)
  - score        : Search relevance score

No API key is required for basic search, but GitHub rate limits apply (10 requests per minute for unauthenticated requests).

----------------------------------------
How to Run the Application
----------------------------------------
1. Make sure you have Python 3 installed.
2. Install the required dependency:
     pip install requests
3. Run the application:
     python gwaqh.py
4. Enter a username or keyword in the search field and click "Search".
5. Select a user from the results to view details.
6. Click "Add to Favorites" to save a user.
7. Switch to the "Favorites" tab to see saved users.

----------------------------------------
Usage Examples / Tests
----------------------------------------
Example 1: Search for "octocat"
  - Enter "octocat" in the search field.
  - Click "Search".
  - The list will show "octocat" and related users.
  - Select "octocat" and click "Add to Favorites".

Example 2: Validation test
  - Leave the search field empty.
  - Click "Search".
  - A warning dialog will appear: "Search field must not be empty!"

Example 3: View favorites after restart
  - Add some users to favorites.
  - Close the application.
  - Re-run python gwaqh.py.
  - Go to the "Favorites" tab — your users are still there.

Example 4: Remove from favorites
  - Go to the "Favorites" tab.
  - Select a saved user.
  - Click "Remove from Favorites".
  - The user is removed from the list and from favorites.json.

----------------------------------------
Files
----------------------------------------
  gwaqh.py        - Main application source code
  favorites.json  - Local storage for favorite users
  .gitignore      - Git ignore rules
  README.txt      - This documentation file

========================================

