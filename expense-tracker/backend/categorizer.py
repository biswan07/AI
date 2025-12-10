import re

# Category keywords mapping
CATEGORY_KEYWORDS = {
    'grocery': [
        'walmart', 'target', 'costco', 'safeway', 'kroger', 'whole foods',
        'trader joe', 'grocery', 'supermarket', 'food lion', 'publix',
        'aldi', 'market', 'fresh', 'produce'
    ],
    'dining': [
        'restaurant', 'cafe', 'coffee', 'starbucks', 'mcdonald', 'burger',
        'pizza', 'chipotle', 'subway', 'domino', 'taco bell', 'kfc',
        'wendy', 'dunkin', 'dining', 'food delivery', 'uber eats', 'doordash',
        'grubhub', 'postmates', 'bar', 'pub', 'grill'
    ],
    'transport': [
        'uber', 'lyft', 'taxi', 'gas', 'fuel', 'shell', 'chevron', 'bp',
        'exxon', 'parking', 'metro', 'transit', 'train', 'bus', 'airline',
        'flight', 'car rental', 'hertz', 'enterprise', 'toll'
    ],
    'utility/bill payment': [
        'electric', 'electricity', 'water', 'gas bill', 'internet', 'phone',
        'mobile', 'at&t', 'verizon', 't-mobile', 'comcast', 'spectrum',
        'utility', 'bill payment', 'payment'
    ],
    'entertainment': [
        'netflix', 'spotify', 'hulu', 'disney', 'amazon prime', 'youtube',
        'movie', 'theater', 'cinema', 'concert', 'ticket', 'gaming',
        'steam', 'playstation', 'xbox', 'entertainment'
    ],
    'retail': [
        'amazon', 'ebay', 'best buy', 'apple store', 'mall', 'clothing',
        'fashion', 'shoes', 'sports', 'electronics', 'home depot', 'lowe',
        'ikea', 'retail', 'store', 'shop'
    ],
    'insurance': [
        'insurance', 'geico', 'state farm', 'allstate', 'progressive',
        'health insurance', 'car insurance', 'life insurance'
    ],
    'education': [
        'school', 'university', 'college', 'tuition', 'books', 'course',
        'education', 'learning', 'udemy', 'coursera', 'training'
    ],
    'healthcare': [
        'hospital', 'clinic', 'doctor', 'pharmacy', 'cvs', 'walgreens',
        'medical', 'health', 'dental', 'vision'
    ],
    'gift': [
        'gift', 'present', 'donation', 'charity', 'contribution'
    ],
    'travel': [
        'hotel', 'airbnb', 'booking', 'expedia', 'travel', 'vacation',
        'resort', 'lodge'
    ],
    'convenience store': [
        'convenience', '7-eleven', 'circle k', 'speedway', 'wawa', 'sheetz'
    ],
    'miscellaneous': []
}

def categorize_expense(description):
    """
    Automatically categorize an expense based on its description.

    Args:
        description (str): The expense description

    Returns:
        str: The categorized expense type
    """
    description_lower = description.lower()

    # Check each category for keyword matches
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category

    # Default to miscellaneous if no match found
    return 'miscellaneous'

def extract_provider(description):
    """
    Extract the provider/merchant name from the description.

    Args:
        description (str): The expense description

    Returns:
        str: The provider name (simplified)
    """
    description_lower = description.lower()

    # Common card providers
    card_providers = {
        'amex': 'AMEX',
        'american express': 'AMEX',
        'bankwest': 'Bankwest',
        'chase': 'Chase',
        'visa': 'Visa',
        'mastercard': 'Mastercard',
        'discover': 'Discover'
    }

    for keyword, provider in card_providers.items():
        if keyword in description_lower:
            return provider

    # If no card provider found, return first word as provider
    words = description.split()
    if words:
        return words[0].title()

    return 'Unknown'

def determine_person(filename):
    """
    Determine who made the expense based on the filename.

    Args:
        filename (str): The uploaded filename

    Returns:
        str: Person name (Soo or Biswa)
    """
    filename_lower = filename.lower()

    if 'soo' in filename_lower:
        return 'Soo'
    elif 'biswa' in filename_lower:
        return 'Biswa'
    else:
        # Default to unknown, can be updated later
        return 'Unknown'
