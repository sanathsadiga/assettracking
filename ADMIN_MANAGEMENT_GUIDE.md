# Admin Management Features - User Guide

## 📋 Overview

The Asset Tracking System now includes **Admin-only management dashboards** for managing:
- **Locations** (offices, facilities)
- **Departments** (HR, IT, Finance, etc.)
- **Users** (team members, staff)

Only **Admin users** can access these management pages.

---

## 🔐 Admin Access Control

### Who Can Access?
- **Admin Users** (is_staff = True): Full access to all management features
- **Regular Users**: Cannot access management pages (redirected to dashboard)
- **Superusers**: Can access everything (including Django Admin)

### Access URLs
All management pages are protected by login + admin status check:
- Unauthorized access → Redirected to Dashboard
- Non-logged-in users → Redirected to Login page

---

## 📍 Managing Locations

### Access
```
Dashboard → Locations (Admin only)
URL: /tracker/manage/locations/
```

### Features

#### View All Locations
- Table showing all locations
- Shows location name, description, asset count, creation date
- Shows total assets assigned to each location

#### Add Location
1. Click **"+ Add Location"** button
2. Fill in:
   - **Location Name** (required): e.g., "Bangalore Office", "Reception"
   - **Description** (optional): e.g., "Ground floor reception area"
3. Click **"Add Location"**
4. ✅ Location created and appears in the list

#### Edit Location
1. Click **"Edit"** button on any location
2. Modal opens with current details
3. Update information
4. Click **"Update Location"**
5. ✅ Changes saved

#### Delete Location
1. Click **"Delete"** button on any location
2. Confirm deletion
3. ✅ Location removed from system
4. **Note**: Assets assigned to deleted location won't be affected (location_id becomes NULL)

### Using Locations in Assets
Once locations are added:
- They appear in **Add Asset** form location dropdown
- They appear in **Asset Update Modal** location dropdown
- Users can assign/change asset locations

---

## 🏢 Managing Departments

### Access
```
Dashboard → Departments (Admin only)
URL: /tracker/manage/departments/
```

### Features

#### View All Departments
- Table showing all departments
- Shows department name, description, asset count, creation date
- Helpful for team categorization

#### Add Department
1. Click **"+ Add Department"** button
2. Fill in:
   - **Department Name** (required): e.g., "Human Resources", "IT"
   - **Description** (optional): e.g., "Information Technology Division"
3. Click **"Add Department"**
4. ✅ Department created and available in dropdowns

#### Edit Department
1. Click **"Edit"** button on any department
2. Modal opens with current details
3. Update department name/description
4. Click **"Update Department"**
5. ✅ Changes saved

#### Delete Department
1. Click **"Delete"** button on any department
2. Confirm deletion
3. ✅ Department removed from system

### Using Departments in Assets
Once departments are added:
- They appear in **Asset Detail View** (new Financial Information section)
- They appear in **Asset Update Modal** for assigning/changing
- Users can organize assets by department

---

## 👥 Managing Users

### Access
```
Dashboard → Users (Admin only)
URL: /tracker/manage/users/
```

### Features

#### View All Users
- Table showing all system users
- Shows username, full name, email, role, assets assigned, status, last login
- Can identify active/inactive users

#### User Roles
- **Admin** (Staff): Can manage assets, users, locations, and departments
- **User** (Regular): Can view assets assigned to them and available assets
- **Superuser**: Django admin level (protected, cannot be deleted)

#### Add User
1. Click **"+ Add User"** button
2. Fill in required fields:
   - **Username** (required): Unique login name
   - **Email** (required): User email address
   - **Password** (required): Initial password
   - **Confirm Password** (required): Must match
3. Optional fields:
   - **First Name**: User's first name
   - **Last Name**: User's last name
   - **Admin User** (checkbox): Check to make admin
4. Click **"Add User"**
5. ✅ User account created, can login immediately

#### Edit User
1. Click **"Edit"** button on any user
2. Modal opens with current details
3. Update:
   - First/Last Name
   - Email
   - Password (optional - leave blank to keep current)
   - Admin status (checkbox)
   - Active status (checkbox)
4. Click **"Update User"**
5. ✅ Changes saved

#### Delete User
1. Click **"Delete"** button on any non-admin user
2. Confirm deletion
3. ✅ User account removed
4. **Note**: Assets assigned to deleted user won't be deleted (assigned_to becomes NULL)

### User Status
- **Active** (checkbox checked): User can login and use the system
- **Inactive** (checkbox unchecked): User cannot login
- Useful for deactivating users without deleting them

---

## 📊 Integrated Workflow

### Complete Asset Management Flow

```
1. CREATE LOCATION
   Admin → Manage Locations → Add "Bangalore Office"

2. CREATE DEPARTMENT
   Admin → Manage Departments → Add "IT"

3. CREATE USER
   Admin → Manage Users → Add "john_doe" (can be admin or regular user)

4. CREATE ASSET
   Admin → Add Asset
   - Select created location: "Bangalore Office"
   - Asset created and available in dropdowns

5. UPDATE ASSET
   Admin/User → Asset Detail → Edit
   - Assign to created user: "john_doe"
   - Assign to department: "IT"
   - Update location if needed

6. VIEW ASSET
   Everyone → Asset List
   - See assets with current values
   - Current Value calculated based on depreciation
```

---

## 🎯 Common Admin Tasks

### Daily Admin Checklist

```
□ Check for new users (Manage Users)
□ Update locations if needed (Manage Locations)
□ Review department assignments (Manage Departments)
□ Monitor asset inventory (Assets List)
□ Check depreciation values (Run update_depreciation command)
```

### Setting Up the System (First Time)

```
1. Create Admin Account
   - Already done during initial setup
   - Username: admin, Password: (your choice)

2. Create Locations
   - Dashboard → Locations
   - Add all office locations
   - Examples: "HQ Office", "Bangalore Branch", "Delhi Office"

3. Create Departments
   - Dashboard → Departments
   - Add all company departments
   - Examples: "HR", "IT", "Finance", "Operations"

4. Create User Accounts
   - Dashboard → Users
   - Add team members
   - Assign admin role to senior staff
   - Assign regular user role to others

5. Create Assets
   - Dashboard → Add Asset
   - Select previously created locations/departments
   - Assign to users
   - Set financial info (purchase date, cost, depreciation)

6. Start Tracking
   - Users can now scan/view assets
   - Depreciation auto-calculated daily
```

---

## 🔍 Admin Responsibilities

### Access Control
- Only admins can manage locations, departments, and users
- Regular users are automatically redirected if they try to access
- Superuser accounts are protected and cannot be deleted

### Data Integrity
- **Deleted items**: Assets/Users/Locations not deleted (only unassigned)
- **Active/Inactive**: Can deactivate users instead of deleting
- **Admin roles**: Carefully assign admin privileges

### Best Practices
1. **Create locations first** - then add assets to them
2. **Create departments** - for organizing teams
3. **Add users** - then assign assets to them
4. **Assign proper roles** - only trusted staff as admins
5. **Regular backups** - backup database regularly
6. **Update depreciation** - run command daily or weekly

---

## ⚠️ Important Notes

### What Happens When You Delete?

| Item | When Deleted | Effect |
|------|-------------|--------|
| Location | Removed | Assets lose location (NULL) |
| Department | Removed | Assets lose department (NULL) |
| User | Removed | Assets lose assignment (NULL) |
| Admin Status | Toggled Off | Becomes regular user |
| User Active Status | Toggled Off | User cannot login |

### Protected Items
- **Superuser Accounts**: Cannot be deleted by admin
- **Asset Records**: Remain even if location/department/user deleted
- **Activity Logs**: Preserved for audit trail

---

## 🛠️ Troubleshooting

### Issue: Cannot See Management Links
**Cause**: Not logged in as admin
**Solution**: 
1. Check admin status: Dashboard → Edit Profile (if available)
2. Ask superuser to grant admin privileges
3. Or login as superuser

### Issue: Cannot Add User
**Possible Causes**:
- Username already exists (try different username)
- Passwords don't match
- Email field is empty
**Solution**: Check error message and verify all required fields

### Issue: Location/Department Still Shows After Delete
**Cause**: Page not refreshed
**Solution**: Refresh page (F5 or Cmd+R)

### Issue: Assets Lost When Location Deleted
**This is Expected**: Assets become unassigned when location deleted
**Prevention**: Reassign assets to different location before deleting
**Recovery**: Edit asset and assign new location

---

## 🚀 Advanced Admin Features

### Using Django Admin
Superusers can access more detailed admin panel:
- URL: `/admin/`
- Access models directly
- Bulk operations
- Advanced filtering

### Bulk Operations
Coming soon:
- Bulk import users from CSV
- Bulk assign assets to locations
- Bulk depreciation updates

### Reporting
See `DEPRECIATION_GUIDE.md` for:
- Financial value reports
- Depreciation tracking
- Asset portfolio analysis

---

## 📞 Admin Support

### Quick Reference

**Management Pages:**
- Locations: `/tracker/manage/locations/`
- Departments: `/tracker/manage/departments/`
- Users: `/tracker/manage/users/`

**Related Commands:**
```bash
# Update all asset depreciation
python manage.py update_depreciation --verbose

# Check system
python manage.py check

# Create backup
mysqldump asset_tracking > backup.sql
```

**Admin Checklist:**
- ✅ Add locations first
- ✅ Create departments
- ✅ Add users
- ✅ Assign roles carefully
- ✅ Regular backups
- ✅ Update depreciation weekly

---

## 🎓 User Training

When training regular users:

1. **Show them**:
   - How to view assets
   - How to scan barcodes
   - How to check asset details
   - How to see their assignments

2. **Tell them**:
   - They cannot manage locations/departments/users
   - For admin features, contact the admin
   - Activity logs track all changes

3. **Have them practice**:
   - Scanning an asset
   - Viewing asset details
   - Viewing their assigned assets

---

**Happy Admin Managing! 🎯**

*Last Updated: 23 March 2026*
