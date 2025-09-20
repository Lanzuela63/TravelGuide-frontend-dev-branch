# apps/dashboards/views/cards_utils.py
def get_dashboard_cards(role, stats):
    """
    Generate dashboard cards for different user roles.
    Each card includes a title, value, and optional styling.
    """

    cards = []

    if role == "Admin":
        cards = [
            {"title": "Total Tourist Spots", "value": stats.get("total_spots", 0)},
            {"title": "Approved Spots", "value": stats.get("approved_spots", 0)},
            {"title": "Pending Spots", "value": stats.get("pending_spots", 0)},
            {"title": "Total Events", "value": stats.get("total_events", 0)},
            {"title": "Upcoming Events", "value": stats.get("upcoming_events", 0)},
            {"title": "Past Events", "value": stats.get("past_events", 0)},
            {"title": "Total Businesses", "value": stats.get("total_businesses", 0)},
            {"title": "Active Businesses", "value": stats.get("active_businesses", 0)},
            {"title": "Inactive Businesses", "value": stats.get("inactive_businesses", 0)},
            {"title": "Total Ratings", "value": stats.get("total_ratings", 0)},
            {"title": "Average Rating", "value": round(stats.get("average_rating", 0), 2)},
            {"title": "Total Users", "value": stats.get("total_users", 0)},
            {"title": "Active Users", "value": stats.get("active_users", 0)},
        ]

    elif role == "Business":
        cards = [
            {"title": "Total Businesses", "value": stats.get("total_businesses", 0)},
            {"title": "Active Businesses", "value": stats.get("active_businesses", 0)},
            {"title": "Inactive Businesses", "value": stats.get("inactive_businesses", 0)},
        ]

    elif role == "Event":
        cards = [
            {"title": "Total Events", "value": stats.get("total_events", 0)},
            {"title": "Upcoming Events", "value": stats.get("upcoming_events", 0)},
            {"title": "Past Events", "value": stats.get("past_events", 0)},
        ]

    elif role == "Tourism":
        cards = [
            {"title": "Total Tourist Spots", "value": stats.get("total_spots", 0)},
            {"title": "Approved Spots", "value": stats.get("approved_spots", 0)},
            {"title": "Pending Spots", "value": stats.get("pending_spots", 0)},
        ]

    elif role == "Tourist":
        cards = [
            {"title": "Total Ratings", "value": stats.get("total_ratings", 0)},
            {"title": "Average Rating", "value": round(stats.get("average_rating", 0), 2)},
            {"title": "Rated Tourist Spots", "value": stats.get("rated_spots", 0)},
        ]

    return cards
