# User Panel Migration Guide

## What Changed?

The user panel functionality has been reorganized into a dedicated subfolder within the buses app for better code organization.

### Before (Old Structure)
```
buses/
├── views_user_map.py
├── views_home.py
├── views.py (contained bus_schedule_list)
├── templates/
│   ├── buses/
│   │   ├── user_map.html
│   │   └── home.html
│   └── bus_schedule_list.html
└── urls.py (all routes mixed together)
```

### After (New Structure)
```
buses/
├── user_panel/
│   ├── __init__.py
│   ├── views.py           # All user-facing views
│   ├── urls.py            # User panel URLs
│   ├── README.md          # Documentation
│   └── templates/
│       └── user_panel/
│           ├── user_map.html
│           ├── home.html
│           └── bus_schedule_list.html
├── views.py (other views)
└── urls.py (includes user_panel URLs)
```

## URL Changes

### New Primary URLs
All user panel routes are now under `/buses/user/`:

| Old URL | New URL | Status |
|---------|---------|--------|
| `/buses/map/` | `/buses/user/map/` | ✅ Preferred |
| `/buses/schedules/` | `/buses/user/schedules/` | ✅ Preferred |
| `/buses/home/` | `/buses/user/home/` | ✅ Preferred |
| `/buses/` | `/buses/user/` | ✅ New default |

### Legacy URL Support
Old URLs are maintained for backward compatibility:
- `/buses/map/` still works (points to old view)
- `/buses/schedules/` still works (points to old view)
- `/buses/home/` still works (points to old view)

## Template Changes

### Template Paths
Templates have been moved to the user_panel subdirectory:
- `buses/user_map.html` → `user_panel/user_map.html`
- `buses/home.html` → `user_panel/home.html`
- `bus_schedule_list.html` → `user_panel/bus_schedule_list.html`

### URL References in Templates
If you're referencing URLs in templates, use the new namespace:

**Old:**
```django
{% url 'buses:user_map' %}
{% url 'buses:bus_schedule_list' %}
```

**New (Recommended):**
```django
{% url 'buses:user_panel:map' %}
{% url 'buses:user_panel:schedules' %}
```

**Note:** Old URL names still work for backward compatibility.

## View Import Changes

### In Python Code

**Old:**
```python
from buses import views_user_map, views_home
from buses.views import bus_schedule_list
```

**New:**
```python
from buses.user_panel import views as user_views
# Or import specific views:
from buses.user_panel.views import user_map_view, home_view, bus_schedule_list
```

## Migration Checklist

For developers updating their code:

- [ ] Update URL references to use new namespace
- [ ] Update template paths if loading templates programmatically
- [ ] Update any imports from old view files
- [ ] Test all user-facing pages
- [ ] Update documentation and links
- [ ] Clear browser cache if styles look broken
- [ ] Update bookmarks and saved links

## Testing the Migration

1. **Test User Map:**
   ```bash
   # Navigate to new URL
   http://localhost:8000/buses/user/map/
   
   # Or legacy URL
   http://localhost:8000/buses/map/
   ```

2. **Test Schedules:**
   ```bash
   # Navigate to new URL
   http://localhost:8000/buses/user/schedules/
   
   # Or legacy URL
   http://localhost:8000/buses/schedules/
   ```

3. **Test Home Page:**
   ```bash
   # Navigate to new URL (requires login)
   http://localhost:8000/buses/user/home/
   
   # Or legacy URL
   http://localhost:8000/buses/home/
   ```

4. **Test API Integration:**
   - Verify map loads bus locations
   - Check that markers update every 10 seconds
   - Verify notifications display correctly
   - Test schedule filtering

## Benefits of This Organization

1. **Better Code Organization**: User-facing features are now in a dedicated module
2. **Easier Maintenance**: All related files are in one place
3. **Clear Separation**: User panel is separate from admin and driver panels
4. **Scalability**: Easier to add new user features
5. **Documentation**: Dedicated README for user panel features

## Rollback Procedure

If you need to rollback to the old structure:

1. The old view files are still in the main buses directory
2. Old URLs are still defined for backward compatibility
3. Simply update main urls.py to point to old views
4. No data migration required (models unchanged)

## Common Issues

### Issue: Templates not found
**Solution:** Ensure `TEMPLATES` setting in settings.py includes app directories:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # This must be True
        ...
    }
]
```

### Issue: 404 on new URLs
**Solution:** Verify urls.py includes the user_panel:
```python
path('user/', include('buses.user_panel.urls', namespace='user_panel')),
```

### Issue: Static files not loading
**Solution:** Run collectstatic if in production:
```bash
python manage.py collectstatic
```

## Support

If you encounter issues:
1. Check the user_panel/README.md for detailed documentation
2. Verify all migrations are applied: `python manage.py migrate`
3. Check server logs for errors
4. Clear browser cache and try again

## Future Plans

The user panel will be further enhanced with:
- Progressive Web App (PWA) features
- Push notifications
- User accounts and favorites
- Route planning
- ETA calculations
- Offline support

This migration is the first step toward these enhancements.
