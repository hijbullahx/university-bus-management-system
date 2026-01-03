# IUBAT Bus Tracker - User Guide

## 🚌 Welcome to IUBAT Real-Time Bus Tracking System

This guide will help you track your bus in real-time and get accurate arrival predictions.

---

## 🗺️ Getting Started

### Access the Tracker
1. Open your browser
2. Navigate to: `http://your-domain.com/buses/user/`
3. The map will load automatically showing all active buses

---

## 📍 Main Features

### 1. View Real-Time Bus Locations

**What you see**:
- 🚌 **Green bus icons** = Live GPS tracking
- 🚌 **Orange bus icons** = Simulation mode
- Icons move automatically as buses move

**How to use**:
- Zoom in/out using `+` and `-` buttons or mouse wheel
- Pan the map by clicking and dragging
- The map centers on IUBAT University by default

---

### 2. Get Bus Information

**To see bus details**:
1. Click on any bus icon on the map
2. A popup appears showing:
   - 🚌 **Bus Number** (e.g., "Bus-01")
   - 📍 **Route Name** (where it's going)
   - 🆔 **Bus ID** (unique identifier)
   - 🚏 **Next Stop** (where it's heading)
   - ⏰ **ETA** (minutes until arrival at next stop)
   - 🏃 **Speed** (current speed in km/h)
   - 📏 **Distance** (km to next stop)
   - 🕐 **Last Update** (when data was last refreshed)

**Tip**: The popup stays open even as the bus moves!

---

### 3. Follow a Specific Bus

**Why follow?**
- Keep your bus centered on the screen
- Never lose track of your bus
- Perfect for monitoring your ride

**How to follow**:
1. Click on your bus icon
2. In the popup, click **"Follow This Bus"** button
3. The map will automatically center on your bus every 3 seconds
4. The button turns red and says **"Stop Following"**

**To stop following**:
- Click **"Stop Following"** button in the popup
- The map returns to normal mode

**Note**: You can only follow one bus at a time.

---

### 4. Filter by Route

**See only specific buses**:
1. Look at the top-right of the screen
2. Click the **Route Selection Dropdown**
3. Choose a route (e.g., "Bus-01 - Mirpur - IUBAT")
4. Map shows only buses on that route
5. Select **"All Routes"** to see everything again

**Quick Access**:
- Open the sidebar (click ☰ button if hidden)
- Click any route in the "Quick Access" section
- Automatically filters and focuses on that route

---

### 5. Use the Sidebar

**Toggle Sidebar**:
- Click the **☰ button** on the left side
- Sidebar slides in/out
- Gives you more map space when hidden

**Sidebar Contents**:
- 📢 **Notifications**: Important announcements
- 🚌 **Quick Access**: One-click route filtering

---

### 6. Check System Status

**Bottom of screen shows**:
- 🚌 **Active Buses**: How many buses are running
- 🗺️ **Routes**: Total number of routes
- ⚡ **Status**: System is Online/Offline

**Status Indicators** (top-right):
- 🟢 **Live Tracking** = Real GPS data
- 🔵 **Simulation Mode** = Demo data
- ⚪ **No Active Buses** = No buses running

---

## 💡 Pro Tips

### Get the Best Experience

1. **Use on Mobile**
   - Works great on phones and tablets
   - Touch-friendly interface
   - Tap to interact, pinch to zoom

2. **Bookmark Your Route**
   - Filter by your usual route
   - Bookmark the page
   - Quick access next time

3. **Check ETA**
   - Look at the popup's ETA badge
   - Plan your arrival at the stop
   - Factor in walking time

4. **Follow Your Bus**
   - Use follow mode when walking to stop
   - See exactly where your bus is
   - Know when to hurry or wait

5. **Check Notifications**
   - Important updates appear in sidebar
   - Service changes, delays, etc.
   - Check before your trip

---

## 📱 Mobile Usage

### Best Practices
- **Portrait mode** for better sidebar view
- **Landscape mode** for more map space
- **Pull down to refresh** browser (if needed)
- **Add to home screen** for app-like experience

### Touch Gestures
- **Tap** bus icon → Show info
- **Tap and hold** → No special action
- **Pinch** → Zoom in/out
- **Swipe** → Pan the map
- **Double tap** → Zoom in

---

## 🔄 Auto-Refresh

The system updates automatically:
- **Bus locations**: Every 10 seconds
- **No need to refresh** the page
- **Seamless updates** without flickering
- **Your view preserved** (zoom, pan, follow)

---

## ❓ Common Questions

### "Why is my bus orange?"
- Orange = Simulation mode (demo data)
- Green = Live GPS tracking
- Check the status badge at top-right

### "The ETA changed, why?"
- Based on current speed and distance
- Adjusts as bus speeds up/slows down
- More accurate than fixed schedules

### "Bus disappeared from map?"
- Not active in last 5 minutes
- May have finished route
- Check schedule for next departure

### "Can I see where the bus has been?"
- Currently shows only current position
- Historical tracking coming soon

### "Why can't I follow multiple buses?"
- System limits to one bus for clarity
- Stop following first, then follow another

### "Map is laggy on my phone?"
- Close other apps for more memory
- Reduce browser tabs
- Older phones may experience lag

---

## 🆘 Troubleshooting

### Map Not Loading
1. Check internet connection
2. Refresh the page (pull down or F5)
3. Clear browser cache
4. Try different browser

### Bus Icons Not Appearing
1. Wait 10 seconds for update
2. Check if any buses are running
3. Look at status indicator
4. Refresh the page

### Follow Button Not Working
1. Stop following current bus first
2. Click bus icon again
3. Try the follow button again
4. Refresh if issue persists

### Route Filter Not Working
1. Select "All Routes" first
2. Then select your desired route
3. Refresh page if needed

---

## 📞 Need Help?

### Contact Support
- **Email**: support@iubat.edu
- **Phone**: [Your number]
- **Office**: IUBAT Transport Office

### Report Issues
- Bus not showing correctly
- Wrong ETA information
- Map not loading
- Other technical problems

---

## 🎯 Quick Reference Card

| Action | How To |
|--------|--------|
| View all buses | Open map at /buses/user/ |
| See bus info | Click bus icon |
| Follow a bus | Click "Follow This Bus" button |
| Stop following | Click "Stop Following" button |
| Filter by route | Use dropdown at top-right |
| Show/hide sidebar | Click ☰ button |
| Zoom in/out | Use +/- buttons or scroll |
| Pan map | Click and drag |

---

## 🌟 Feature Highlights

✅ Real-time GPS tracking  
✅ Accurate ETA calculation  
✅ One-click bus following  
✅ Route filtering  
✅ Mobile-friendly design  
✅ Auto-refresh (10 seconds)  
✅ Professional interface  
✅ No login required  

---

## 📚 Additional Resources

- [Full System Documentation](README.md)
- [Technical Implementation](FEATURES_IMPLEMENTATION.md)
- [API Documentation](../../api_docs.md)

---

**Version**: 1.0  
**Last Updated**: January 3, 2026  
**System**: IUBAT Bus Management System  
**Platform**: Web-based (works on all devices)
