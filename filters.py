from datetime import datetime


def timeago(dt):
    seconds = int((datetime.now() - dt).total_seconds())
    if seconds < 1:
        return "Just now"
    elif seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours}h"
    elif seconds < 2592000:
        days = seconds // 86400
        return f"{days}d"
    else:
        return dt.strftime('%b %d, %Y')
