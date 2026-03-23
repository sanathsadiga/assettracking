# Dashboard Management Features - Complete Guide

## 📋 Overview

The Asset Tracking System now includes **complete admin dashboard management** for all core entities:

- ✅ **Categories** - Asset types (Laptop, Desktop, Printer, etc.)
- ✅ **Locations** - Physical locations (Bangalore, Mumbai, etc.)
- ✅ **Departments** - Team groups (HR, IT, Finance, etc.)
- ✅ **Users** - System users and admin accounts

**All accessible from the sidebar!** Only admins can manage these items.

---

## 🎯 Access & Permissions

### Who Can Access?

- **Admin Users Only** ✓
- Regular users see read-only view
- Non-admin users cannot access management pages

### How to Access

1. **Log in as Admin**
2. Look at the **left sidebar**
3. Under "Admin Tools" section, click:
   - **Categories** - Manage asset categories
   - **Locations** - Manage physical locations
   - **Departments** - Manage team departments
   - **Users** - Manage system users

---

## 🏷️ Categories Management

### What is a Category?

A **category** classifies assets by type:
- Laptop
- Desktop Computer
- Monitor
- Printer
- Mobile Phone
- Tablet
- Network Equipment
- etc.

### View All Categories

```
Dashboard → Categories (in sidebar)
```

Shows a table with:
- Category name
- Description
- Number of assets in category
- Created date
- Edit/Delete buttons

### Add New Category

**Steps:**

1. Click **"Add Category"** button
2. Fill in:
   - **Category Name** (required): e.g., "Projector"
   - **Description** (optional): e.g., "LCD Projectors for meetings"
3. Click **"Add Category"**

**Result:** Category appears in the list and is available in:
- Asset creation form
- Asset filtering
- Asset list view

### Edit Category

**Steps:**

1. Click **"Edit"** button next to category
2. Update:
   - Category name
   - Description
3. Click **"Update Category"**

**Result:** All assets with this category show updated name/description

### Delete Category

**Steps:**

1. Click **"Delete"** button
2. Confirm deletion

**Restrictions:**
- ❌ Cannot delete category if it has assets
- ✓ Can only delete empty categories
- Delete button is disabled if category has assets

**Example:**
```
Category: Laptop
Assets: 5
Delete button: ❌ Disabled (says "Category has assets")
```

---

## 📍 Locations Management

### What is a Location?

A **location** represents a physical place where assets are stored:
- Bangalore Office
- Mumbai Branch
- Delhi HQ
- Hyderabad Center
- Home Office
- Warehouse
- etc.

### View All Locations

```
Dashboard → Locations (in sidebar)
```

Shows a table with:
- Location name
- Description
- Number of assets in location
- Created date
- Edit/Delete buttons

### Add New Location

**Steps:**

1. Click **"Add Location"** button
2. Fill in:
   - **Location Name** (required): e.g., "Bangalore - Building A"
   - **Description** (optional): e.g., "3rd Floor, West Wing"
3. Click **"Add Location"**

**Result:** Location appears in:
- Asset creation dropdown
- Asset edit dropdown
- Asset list filtering

### Edit Location

**Steps:**

1. Click **"Edit"** button
2. Update name and description
3. Click **"Update Location"**

### Delete Location

**Steps:**

1. Click **"Delete"** button
2. Confirm deletion

**Restrictions:**
- ❌ Cannot delete location with assets
- Delete button disabled if location has assets

---

## 🏢 Departments Management

### What is a Department?

A **department** groups users by their team/role:
- Human Resources (HR)
- Information Technology (IT)
- Finance
- Operations
- Sales
- Marketing
- Management
- etc.

### View All Departments

```
Dashboard → Departments (in sidebar)
```

Shows a table with:
- Department name
- Description
- Number of assets assigned to department
- Created date
- Edit/Delete buttons

### Add New Department

**Steps:**

1. Click **"Add Department"** button
2. Fill in:
   - **Department Name** (required): e.g., "Human Resources"
   - **Description** (optional): e.g., "HR team managing recruitment"
3. Click **"Add Department"**

**Result:** Department appears in:
- Asset creation form
- Asset edit form
- Asset detail page

### Edit Department

**Steps:**

1. Click **"Edit"** button
2. Update name and description
3. Click **"Update Department"**

### Delete Department

**Steps:**

1. Click **"Delete"** button
2. Confirm

**Restrictions:**
- ❌ Cannot delete department with assets
- Delete button disabled if department has assets

---

## 👥 Users Management

### What is a User?

A **user** is a person who can log in to the system:
- Can be admin or regular user
- Each has a username, email, and full name
- Can be active or inactive

### View All Users

```
Dashboard → Users (in sidebar)
```

Shows a table with:
- Username
- Email
- Full name (First Last)
- Admin status
- Active status
- Actions (Edit, Delete)

### Add New User

**Steps:**

1. Click **"Add User"** button
2. Fill in:
   - **Username** (required): e.g., "john_doe"
   - **Email** (required): e.g., "john@company.com"
   - **Password** (required): Set initial password
   - **Confirm Password**: Must match
   - **First Name** (optional): e.g., "John"
   - **Last Name** (optional): e.g., "Doe"
   - **Make Admin**: Checkbox to give admin privileges
3. Click **"Add User"**

**Result:** User can now log in with username and password

### Edit User

**Steps:**

1. Click **"Edit"** button
2. Update:
   - Email
   - First name
   - Last name
   - Admin status (checkbox)
   - Active status (checkbox)
   - Password (leave blank to keep current)
3. Click **"Update User"**

**Changes:**
- Email: Used for future notifications
- Name: Displays in asset assignment
- Admin: Grants management permissions
- Active: Disabled users cannot log in

### Delete User

**Steps:**

1. Click **"Delete"** button
2. Confirm

**Restrictions:**
- ❌ Cannot delete superuser/main admin
- Other users can be deleted
- Assets assigned to deleted user remain in system

---

## 🔄 Relationship Between Entities

### How They Connect

```
Asset
├── Category (Which type: Laptop, Printer, etc.)
├── Location (Where: Bangalore, Mumbai, etc.)
├── Department (Whose team: HR, IT, etc.)
└── Assigned To (Which user)
```

### Example Asset Structure

```
Asset: ASSET0001
├── Name: HP Laptop
├── Category: Laptop (managed via Categories)
├── Location: Bangalore - Building A (managed via Locations)
├── Department: IT (managed via Departments)
└── Assigned To: John Doe (managed via Users)
```

---

## 🎓 Common Workflows

### Workflow 1: Adding a New Department

```
1. Admin clicks "Departments" in sidebar
2. Clicks "Add Department"
3. Enters "Sales" as name, "Sales team" as description
4. Clicks "Add Department"
5. New department is now available in asset forms
```

### Workflow 2: Moving Office Locations

```
1. Admin adds new location: "Delhi - New Office"
2. Admin edits existing location: "Bangalore - Old Office" → "Bangalore - Archive"
3. Admin reassigns assets from old to new location
4. Uses asset detail page to change location for each asset
```

### Workflow 3: Adding New Team Member

```
1. Admin clicks "Users" in sidebar
2. Clicks "Add User"
3. Enters username, email, password
4. Checks "Make Admin" if need management privileges
5. Clicks "Add User"
6. User receives login credentials
7. User can now log in and view assigned assets
```

### Workflow 4: Organizing New Category

```
1. Admin clicks "Categories"
2. Clicks "Add Category" (e.g., "External Drives")
3. Enters description: "USB and external storage devices"
4. Clicks "Add Category"
5. When creating assets, can now select "External Drives" as category
```

---

## ⚙️ Advanced Operations

### Bulk Operations via Django Admin

For advanced bulk operations, admins can also use Django Admin:

```
URL: http://localhost:8000/admin/
Login: Use your admin account
```

Features:
- Bulk delete categories/locations/departments
- Search and filter
- Direct database editing
- Export to CSV

---

## 🛡️ Safety Features

### Deletion Protection

- **Cannot delete if has assets**: Categories, Locations, Departments with assets cannot be deleted
- **Cannot delete superuser**: Main admin account cannot be deleted
- **Confirmation required**: All deletions require confirmation

### Data Integrity

- **Unique names**: Categories, Locations, Departments must have unique names
- **Email validation**: User emails validated for format
- **Username validation**: Usernames must be unique
- **Password hashing**: Passwords securely hashed, never stored in plain text

---

## 📊 Examples

### Example 1: Complete Setup

```
Categories:
✓ Laptop
✓ Desktop
✓ Monitor
✓ Printer

Locations:
✓ Bangalore - Building A
✓ Bangalore - Building B
✓ Mumbai - Office
✓ Delhi - HQ

Departments:
✓ IT
✓ HR
✓ Finance
✓ Operations

Users:
✓ admin (Admin)
✓ john_it (Regular)
✓ sarah_hr (Admin)
✓ mike_ops (Regular)
```

### Example 2: Asset Using All Entities

```
Asset: ASSET0015
- Name: Dell Laptop
- Category: Laptop (via Categories)
- Location: Bangalore - Building A (via Locations)
- Department: IT (via Departments)
- Assigned To: john_it (via Users)
- Status: In Use
- Cost: ₹80,000
- Depreciation: 10% per year
```

---

## 🐛 Troubleshooting

### Issue: Can't See Management Links

**Cause**: You're not logged in as admin

**Solution**:
1. Log in with admin account
2. Management links appear in sidebar

### Issue: Can't Delete Category

**Cause**: Category has assets

**Solution**:
1. Click category to see assets
2. Reassign those assets to different category
3. Then delete category

### Issue: User Can't Log In

**Cause**: Account is inactive or wrong credentials

**Solution**:
1. Check if user is "Active" (checkbox in user edit)
2. Reset password: Click Edit, enter new password, save
3. User can now log in

### Issue: Duplicate Category Names Not Allowed

**Cause**: System prevents duplicate names

**Solution**:
1. Choose a unique name
2. Add suffix like "- v2" if needed
3. Example: "Laptop" and "Laptop - Old"

---

## 📝 Best Practices

### Categories

✓ Use clear, specific names (e.g., "Laptop" not "Equipment")
✓ Add descriptions for clarity
✓ Keep list organized (10-15 categories is good)
✗ Don't use similar names (confusing)
✗ Don't delete categories with assets

### Locations

✓ Use full location name (e.g., "Bangalore - Building A, 3rd Floor")
✓ Be specific to avoid confusion
✓ Add description with directions if helpful
✗ Don't use vague names ("Office", "Place")
✗ Don't archive location without moving assets

### Departments

✓ Use standard team names (HR, IT, Finance, etc.)
✓ Match your company structure
✓ Add descriptions for clarity
✗ Don't mix departments with locations
✗ Don't use person names (use team names)

### Users

✓ Use consistent username format (firstname_lastname)
✓ Require strong passwords
✓ Give admin only to trusted people
✓ Deactivate instead of delete when user leaves
✗ Don't share passwords
✗ Don't create duplicate accounts
✗ Don't give admin to everyone

---

## 🔐 Access Control

### Admin-Only Operations

| Operation | Admin Only | Notes |
|-----------|-----------|-------|
| View Management Pages | ✓ | Regular users can't access |
| Add Items | ✓ | Only admins can create |
| Edit Items | ✓ | Only admins can modify |
| Delete Items | ✓ | Only admins can remove |
| Add Users | ✓ | Only admins create accounts |
| Reset Passwords | ✓ | Only admins can reset |

### Regular User Operations

| Operation | Allowed | Notes |
|-----------|---------|-------|
| View Assets | ✓ | See assigned assets |
| View Categories | ✓ | Read-only |
| View Locations | ✓ | Read-only |
| View Departments | ✓ | Read-only |
| View Users | ✓ | See team members |
| Add/Edit Categories | ✗ | Admin only |

---

## 📚 Related Features

These management features integrate with:

- **Asset Creation**: Uses Categories, Locations, Departments, Users
- **Asset Filtering**: Filter by Category, Location, Department
- **Asset Details**: Shows which Category/Location/Department
- **Depreciation**: Works with purchased assets
- **Activity Logs**: Tracks all changes

---

## 🚀 Tips & Tricks

### Tip 1: Pre-Setup Categories

Create all your asset categories **before** creating assets:
```
Categories to setup:
- Laptop
- Desktop
- Monitor
- Printer
- Keyboard
- Mouse
- Network Equipment
- Furniture
- Office Supplies
- Mobile Devices
```

### Tip 2: Organize Locations Hierarchically

Use naming to show hierarchy:
```
Bangalore - Building A - Floor 1
Bangalore - Building A - Floor 2
Bangalore - Building A - Floor 3
Bangalore - Building B - Floor 1
```

### Tip 3: Department Names

Match your company's structure:
```
If company has: Sales, Marketing, Engineering, Operations
Then departments: Sales, Marketing, Engineering, Operations
```

### Tip 4: User Management

Create users with clear structure:
```
Username format: firstname.lastname or firstname_department
Examples:
- john.doe (Generic)
- sarah.it (Shows department)
- mike_operations (Alternative format)
```

---

## 📞 Support

For issues:

1. Check if you're logged in as admin
2. Try refreshing the page
3. Check browser console for errors
4. Review Django admin logs

---

**Happy Managing! 🎉**

*Asset Tracking System - Management Guide*
*Last Updated: 23 March 2026*
