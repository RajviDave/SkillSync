# Troubleshooting Guide - Login/Signup Fixes

## Issues Fixed

### 1. **Table Name Mismatch** ✅
- **Problem**: Code was using `users` (plural) but database has `user` (singular)
- **Fix**: Changed all PHP files to use `user` table
- **Files Updated**: 
  - `backend/login.php`
  - `backend/signup.php`
  - `backend/google_login.php`

### 2. **CORS Headers** ✅
- **Problem**: Network errors when accessing from different origins
- **Fix**: Added CORS headers to all PHP files
- **Files Updated**: All backend PHP files

### 3. **Error Handling** ✅
- **Problem**: Poor error messages and no logging
- **Fix**: Added comprehensive error handling and logging
- **Files Updated**: All backend PHP files

### 4. **Path Issues** ✅
- **Problem**: Paths not working when accessing via different methods
- **Fix**: Added dynamic path detection in auth.html
- **Files Updated**: `templates/auth.html`

## Testing Steps

### Step 1: Test Database Connection
1. Open your browser and go to: `http://localhost/SkillSync/backend/test_db.php`
2. This will show you:
   - If database connection works
   - If the `user` table exists
   - Table structure
   - Number of users

### Step 2: Create Table (if needed)
If the table doesn't exist:
1. Open phpMyAdmin
2. Select `businessdb` database
3. Go to SQL tab
4. Copy and paste the SQL from `backend/create_user_table.sql`
5. Click "Go"

### Step 3: Test Login/Signup
1. **Via Flask (Recommended)**:
   - Run: `python app.py`
   - Go to: `http://127.0.0.1:5000/auth`
   - Try signing up with a new account
   - Try logging in

2. **Via XAMPP**:
   - Make sure XAMPP Apache is running
   - Go to: `http://localhost/SkillSync/templates/auth.html`
   - Try signing up and logging in

## Common Issues & Solutions

### Issue: "Network error" still appears
**Solutions**:
1. Check if XAMPP Apache is running
2. Check browser console (F12) for detailed error
3. Check PHP error logs in XAMPP
4. Verify database connection using `test_db.php`

### Issue: "Table 'user' doesn't exist"
**Solution**: Run the SQL script in `backend/create_user_table.sql`

### Issue: "Database connection failed"
**Solutions**:
1. Check if MySQL is running in XAMPP
2. Verify database name is `businessdb`
3. Check username is `root` and password is empty (default XAMPP)
4. Update `backend/db.php` if your credentials are different

### Issue: "Invalid credentials" but password is correct
**Solutions**:
1. Check if password was hashed correctly during signup
2. Try creating a new account
3. Check database to see if user exists

### Issue: Session not persisting
**Solutions**:
1. Make sure cookies are enabled in browser
2. Check if PHP sessions are working
3. Verify session files directory is writable

## File Structure
```
SkillSync/
├── backend/
│   ├── db.php (Database connection)
│   ├── login.php (Email login)
│   ├── signup.php (Email signup)
│   ├── google_login.php (Google OAuth)
│   ├── check_session.php (Session check)
│   ├── logout.php (Logout)
│   ├── test_db.php (Database test - NEW)
│   └── create_user_table.sql (SQL script - NEW)
├── templates/
│   └── auth.html (Login/Signup page - UPDATED)
└── app.py (Flask app)
```

## Next Steps
1. Test the database connection using `test_db.php`
2. Ensure the `user` table exists with correct structure
3. Try signing up with a new account
4. Try logging in with the created account
5. Check browser console (F12) for any JavaScript errors
6. Check PHP error logs if issues persist

## Debugging Tips
- Open browser Developer Tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab to see API requests/responses
- Check PHP error logs: `C:\xampp\php\logs\php_error_log`
- Use `test_db.php` to verify database setup
