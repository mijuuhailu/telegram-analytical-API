TOP_PRODUCTS = """
SELECT "object" AS object_name, COUNT(*) as frequency
FROM raw.yolo_detections
GROUP BY "object"
ORDER BY frequency DESC
LIMIT :limit
"""

CHANNEL_ACTIVITY = """
SELECT channel_name, COUNT(*) as total_posts
FROM raw.telegram_messages
WHERE channel_name = :channel_name
GROUP BY channel_name
ORDER BY total_posts DESC
"""

SEARCH_MESSAGES = """
SELECT message_id, message_text, view_count, channel_name
FROM public_staging.stg_telegram_messages
WHERE message_text ILIKE '%' || :query || '%'
LIMIT :limit
"""

VISUAL_STATS = """
SELECT image_category, COUNT(*) as total
FROM fct_image_detections
GROUP BY image_category
"""