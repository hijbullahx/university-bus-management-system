"""
UBus Tracking System - Streamlit Analytics Dashboard
A comprehensive analytics dashboard for authority users.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import os

# Configuration
st.set_page_config(
    page_title="UBus Analytics Dashboard",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0d6efd;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0d6efd;
    }
</style>
""", unsafe_allow_html=True)


def get_mock_data():
    """Generate mock data for demo purposes when API is not available."""
    # Routes data
    routes = pd.DataFrame({
        'route_name': ['Campus Loop', 'Downtown Express', 'North Campus', 'South Station', 'Library Shuttle'],
        'total_trips': [450, 380, 290, 320, 210],
        'total_passengers': [8500, 7200, 5100, 6000, 3800],
        'on_time_rate': [92.5, 88.3, 95.1, 87.6, 96.2]
    })
    
    # Daily performance data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    daily = pd.DataFrame({
        'date': dates,
        'total_trips': [45 + (i % 10) for i in range(30)],
        'on_time': [40 + (i % 8) for i in range(30)],
        'passengers': [800 + (i * 20) % 400 for i in range(30)]
    })
    
    # Issue data
    issues = pd.DataFrame({
        'type': ['Mechanical', 'Traffic', 'Weather', 'Emergency', 'Accident', 'Other'],
        'count': [25, 45, 12, 8, 5, 15]
    })
    
    # Feedback data
    feedback = pd.DataFrame({
        'category': ['Service Quality', 'Timing', 'Cleanliness', 'Driver Behavior', 'App/System'],
        'count': [120, 85, 65, 45, 90],
        'avg_rating': [4.2, 3.8, 4.5, 4.1, 3.9]
    })
    
    return routes, daily, issues, feedback


def fetch_api_data(endpoint):
    """Fetch data from Django API."""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return None


def main():
    # Header
    st.markdown('<p class="main-header">🚌 UBus Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown("Real-time analytics and insights for the bus tracking system.")
    
    # Sidebar
    st.sidebar.image("https://via.placeholder.com/150x50?text=UBus", width=150)
    st.sidebar.title("Navigation")
    
    page = st.sidebar.radio(
        "Select Dashboard",
        ["Overview", "Live Tracking", "Route Analytics", "Performance Metrics", "Issue Analysis", "User Feedback"]
    )
    
    st.sidebar.markdown("---")
    
    # Date range selector
    st.sidebar.subheader("Date Range")
    date_range = st.sidebar.selectbox(
        "Select Period",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"]
    )
    
    if date_range == "Custom":
        start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
        end_date = st.sidebar.date_input("End Date", datetime.now())
    else:
        days = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90}[date_range]
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
    
    # Load data
    routes, daily, issues, feedback = get_mock_data()
    
    # Display selected page
    if page == "Overview":
        show_overview(routes, daily, issues, feedback)
    elif page == "Live Tracking":
        show_live_tracking()
    elif page == "Route Analytics":
        show_route_analytics(routes, daily)
    elif page == "Performance Metrics":
        show_performance_metrics(daily, routes)
    elif page == "Issue Analysis":
        show_issue_analysis(issues)
    elif page == "User Feedback":
        show_feedback_analysis(feedback)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("UBus Analytics v1.0\n\nConnected to: Demo Mode")


def show_live_tracking():
    """Display live tracking map with buses and drivers."""
    st.header("🗺️ Live Tracking Map")
    
    # Refresh button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
    with col2:
        auto_refresh = st.checkbox("Auto-refresh (10s)", value=False)
    
    if auto_refresh:
        import time
        time.sleep(10)
        st.rerun()
    
    # Fetch data from API
    buses_data = fetch_api_data("buses/locations/")
    drivers_data = fetch_api_data("location/active/")
    
    # Use mock data if API unavailable
    if buses_data is None:
        buses_data = [
            {"id": 1, "bus_number": "BUS-001", "latitude": 40.7128, "longitude": -74.0060, "route_name": "Campus Loop"},
            {"id": 2, "bus_number": "BUS-002", "latitude": 40.7148, "longitude": -74.0080, "route_name": "Downtown Express"},
            {"id": 3, "bus_number": "BUS-003", "latitude": 40.7108, "longitude": -74.0040, "route_name": "North Campus"},
        ]
    
    if drivers_data is None:
        drivers_data = [
            {"driver_id": 1, "driver_name": "John Driver", "latitude": 40.7138, "longitude": -74.0070, "route_name": "Campus Loop", "last_updated": datetime.now().isoformat()},
            {"driver_id": 2, "driver_name": "Jane Driver", "latitude": 40.7158, "longitude": -74.0090, "route_name": "Downtown Express", "last_updated": datetime.now().isoformat()},
        ]
    
    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🚌 Active Buses", len(buses_data))
    with col2:
        st.metric("👤 Active Drivers", len(drivers_data))
    
    # Create map data
    map_data = []
    
    # Add buses
    for bus in buses_data:
        map_data.append({
            "lat": float(bus.get("latitude", 0)),
            "lon": float(bus.get("longitude", 0)),
            "type": "Bus",
            "name": bus.get("bus_number", "Unknown"),
            "route": bus.get("route_name", "N/A"),
            "color": "#007bff"
        })
    
    # Add drivers
    for driver in drivers_data:
        map_data.append({
            "lat": float(driver.get("latitude", 0)),
            "lon": float(driver.get("longitude", 0)),
            "type": "Driver",
            "name": driver.get("driver_name", driver.get("driver_username", "Unknown")),
            "route": driver.get("route_name", "N/A"),
            "color": "#198754"
        })
    
    if map_data:
        df = pd.DataFrame(map_data)
        
        # Display map using plotly
        fig = px.scatter_mapbox(
            df,
            lat="lat",
            lon="lon",
            color="type",
            hover_name="name",
            hover_data={"route": True, "lat": False, "lon": False, "type": False},
            color_discrete_map={"Bus": "#007bff", "Driver": "#198754"},
            zoom=13,
            height=500
        )
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Data tables
        st.subheader("📋 Details")
        
        tab1, tab2 = st.tabs(["🚌 Buses", "👤 Drivers"])
        
        with tab1:
            if buses_data:
                bus_df = pd.DataFrame(buses_data)
                st.dataframe(bus_df[['bus_number', 'route_name', 'latitude', 'longitude']] if 'bus_number' in bus_df.columns else bus_df, use_container_width=True, hide_index=True)
            else:
                st.info("No active buses")
        
        with tab2:
            if drivers_data:
                driver_df = pd.DataFrame(drivers_data)
                cols = ['driver_name', 'route_name', 'latitude', 'longitude', 'last_updated']
                display_cols = [c for c in cols if c in driver_df.columns]
                st.dataframe(driver_df[display_cols] if display_cols else driver_df, use_container_width=True, hide_index=True)
            else:
                st.info("No active drivers sharing location")
    else:
        st.warning("No buses or drivers currently active")


def show_overview(routes, daily, issues, feedback):
    """Display overview dashboard."""
    st.header("📊 System Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Trips (30 days)",
            value=f"{routes['total_trips'].sum():,}",
            delta="↑ 8%"
        )
    
    with col2:
        st.metric(
            label="Total Passengers",
            value=f"{routes['total_passengers'].sum():,}",
            delta="↑ 12%"
        )
    
    with col3:
        avg_on_time = routes['on_time_rate'].mean()
        st.metric(
            label="Avg On-Time Rate",
            value=f"{avg_on_time:.1f}%",
            delta="↑ 2.3%"
        )
    
    with col4:
        avg_rating = feedback['avg_rating'].mean()
        st.metric(
            label="Avg User Rating",
            value=f"{avg_rating:.1f}/5",
            delta="↑ 0.2"
        )
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Trips Trend")
        fig = px.area(
            daily, x='date', y='total_trips',
            color_discrete_sequence=['#0d6efd']
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Trips",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Route Popularity")
        fig = px.pie(
            routes, values='total_passengers', names='route_name',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Issue Distribution")
        fig = px.bar(
            issues, x='type', y='count',
            color='count', color_continuous_scale='Oranges'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Feedback by Category")
        fig = px.bar(
            feedback, x='category', y='count',
            color='avg_rating', color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def show_route_analytics(routes, daily):
    """Display route-specific analytics."""
    st.header("🛣️ Route Analytics")
    
    # Route selector
    selected_route = st.selectbox("Select Route", routes['route_name'].tolist())
    route_data = routes[routes['route_name'] == selected_route].iloc[0]
    
    # Route metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trips", f"{route_data['total_trips']:,}")
    with col2:
        st.metric("Total Passengers", f"{route_data['total_passengers']:,}")
    with col3:
        st.metric("On-Time Rate", f"{route_data['on_time_rate']:.1f}%")
    with col4:
        avg_per_trip = route_data['total_passengers'] / route_data['total_trips']
        st.metric("Avg Passengers/Trip", f"{avg_per_trip:.1f}")
    
    st.markdown("---")
    
    # Route comparison
    st.subheader("Route Comparison")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Total Trips',
        x=routes['route_name'],
        y=routes['total_trips'],
        marker_color='#0d6efd'
    ))
    fig.add_trace(go.Scatter(
        name='On-Time Rate (%)',
        x=routes['route_name'],
        y=routes['on_time_rate'],
        mode='lines+markers',
        yaxis='y2',
        marker_color='#198754'
    ))
    
    fig.update_layout(
        yaxis=dict(title='Total Trips'),
        yaxis2=dict(title='On-Time Rate (%)', overlaying='y', side='right', range=[0, 100]),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Passenger distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Passengers by Route")
        fig = px.bar(
            routes.sort_values('total_passengers', ascending=True),
            x='total_passengers', y='route_name',
            orientation='h', color='total_passengers',
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Efficiency Score")
        routes_copy = routes.copy()
        routes_copy['efficiency'] = (routes_copy['on_time_rate'] * routes_copy['total_passengers']) / 1000
        fig = px.treemap(
            routes_copy, path=['route_name'], values='efficiency',
            color='on_time_rate', color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)


def show_performance_metrics(daily, routes):
    """Display performance metrics."""
    st.header("📈 Performance Metrics")
    
    # Performance trend
    st.subheader("Daily Performance Trend")
    
    daily['on_time_rate'] = (daily['on_time'] / daily['total_trips'] * 100).round(1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily['date'], y=daily['total_trips'],
        name='Total Trips', mode='lines',
        line=dict(color='#0d6efd', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=daily['date'], y=daily['on_time'],
        name='On-Time Trips', mode='lines',
        line=dict(color='#198754', width=2)
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Trips",
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("On-Time Rate Distribution")
        fig = px.histogram(
            routes, x='on_time_rate', nbins=10,
            color_discrete_sequence=['#0d6efd']
        )
        fig.add_vline(x=90, line_dash="dash", line_color="green", 
                      annotation_text="Target: 90%")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Passenger Volume Trend")
        fig = px.line(
            daily, x='date', y='passengers',
            color_discrete_sequence=['#6f42c1']
        )
        fig.update_layout(yaxis_title="Passengers")
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance table
    st.subheader("Route Performance Summary")
    
    performance_df = routes.copy()
    performance_df['status'] = performance_df['on_time_rate'].apply(
        lambda x: '🟢 Excellent' if x >= 95 else ('🟡 Good' if x >= 90 else '🔴 Needs Improvement')
    )
    
    st.dataframe(
        performance_df[['route_name', 'total_trips', 'on_time_rate', 'status']],
        use_container_width=True,
        hide_index=True
    )


def show_issue_analysis(issues):
    """Display issue analysis."""
    st.header("⚠️ Issue Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Issue distribution
        st.subheader("Issues by Type")
        fig = px.bar(
            issues.sort_values('count', ascending=False),
            x='type', y='count',
            color='type', color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Issue summary
        st.subheader("Quick Stats")
        total_issues = issues['count'].sum()
        st.metric("Total Issues", total_issues)
        st.metric("Most Common", issues.iloc[issues['count'].idxmax()]['type'])
        st.metric("Avg per Type", f"{total_issues / len(issues):.1f}")
    
    # Issue trends (mock data)
    st.subheader("Issue Trends Over Time")
    
    issue_trends = pd.DataFrame({
        'week': [f"Week {i}" for i in range(1, 9)],
        'Mechanical': [12, 15, 10, 8, 14, 11, 9, 13],
        'Traffic': [25, 30, 28, 22, 35, 32, 28, 30],
        'Weather': [5, 8, 3, 2, 10, 6, 4, 7]
    })
    
    fig = px.line(
        issue_trends.melt(id_vars=['week'], var_name='Issue Type', value_name='Count'),
        x='week', y='Count', color='Issue Type',
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Resolution status
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resolution Status")
        status_data = pd.DataFrame({
            'Status': ['Resolved', 'In Progress', 'Pending'],
            'Count': [75, 20, 15]
        })
        fig = px.pie(
            status_data, values='Count', names='Status',
            color='Status',
            color_discrete_map={'Resolved': '#198754', 'In Progress': '#ffc107', 'Pending': '#dc3545'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Priority Distribution")
        priority_data = pd.DataFrame({
            'Priority': ['High', 'Medium', 'Low'],
            'Count': [25, 55, 30]
        })
        fig = px.bar(
            priority_data, x='Priority', y='Count',
            color='Priority',
            color_discrete_map={'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#0dcaf0'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def show_feedback_analysis(feedback):
    """Display user feedback analysis."""
    st.header("💬 User Feedback Analysis")
    
    # Overall rating
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        avg_rating = feedback['avg_rating'].mean()
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h1 style="font-size: 4rem; margin: 0;">{avg_rating:.1f}</h1>
            <p style="font-size: 1.5rem; margin: 0;">Average Rating</p>
            <p style="margin-top: 1rem;">{"⭐" * int(avg_rating)} ({feedback['count'].sum()} reviews)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Feedback by Category")
        fig = px.bar(
            feedback.sort_values('count', ascending=True),
            x='count', y='category', orientation='h',
            color='avg_rating', color_continuous_scale='Blues',
            labels={'count': 'Number of Reviews', 'avg_rating': 'Avg Rating'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Rating Distribution by Category")
        fig = px.scatter(
            feedback, x='category', y='avg_rating',
            size='count', color='category',
            size_max=60
        )
        fig.add_hline(y=4, line_dash="dash", line_color="green",
                      annotation_text="Target: 4.0")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Rating trend (mock)
    st.subheader("Rating Trend Over Time")
    
    rating_trend = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'rating': [3.8, 3.9, 4.0, 4.1, 4.0, 4.2],
        'reviews': [85, 92, 105, 98, 110, 120]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=rating_trend['month'], y=rating_trend['reviews'],
        name='Reviews', marker_color='#0d6efd', opacity=0.6
    ))
    fig.add_trace(go.Scatter(
        x=rating_trend['month'], y=rating_trend['rating'],
        name='Avg Rating', mode='lines+markers',
        yaxis='y2', line=dict(color='#ffc107', width=3)
    ))
    
    fig.update_layout(
        yaxis=dict(title='Number of Reviews'),
        yaxis2=dict(title='Avg Rating', overlaying='y', side='right', range=[0, 5]),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Feedback table
    st.subheader("Category Performance")
    
    feedback_display = feedback.copy()
    feedback_display['status'] = feedback_display['avg_rating'].apply(
        lambda x: '⭐⭐⭐⭐⭐' if x >= 4.5 else ('⭐⭐⭐⭐' if x >= 4.0 else ('⭐⭐⭐' if x >= 3.5 else '⭐⭐'))
    )
    
    st.dataframe(
        feedback_display[['category', 'count', 'avg_rating', 'status']].rename(columns={
            'category': 'Category',
            'count': 'Reviews',
            'avg_rating': 'Avg Rating',
            'status': 'Rating Stars'
        }),
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()
