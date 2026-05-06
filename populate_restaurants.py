import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_buddy.settings')
django.setup()

from delivery.models import Restaurant, Item

restaurants_data = [
    {
        "name": "Pasta Paradise",
        "cuisine": "Italian",
        "rating": 4.8,
        "picture": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&q=80&w=800",
        "items": [
            {"name": "Margherita Pizza", "price": 450, "desc": "Classic delight with 100% real mozzarella cheese", "veg": True},
            {"name": "Penne Alfredo", "price": 350, "desc": "Creamy white sauce pasta", "veg": True},
            {"name": "Chicken Parmesan", "price": 550, "desc": "Breaded chicken breast covered in tomato sauce", "veg": False}
        ]
    },
    {
        "name": "Dragon Wok",
        "cuisine": "Chinese",
        "rating": 4.5,
        "picture": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&q=80&w=800",
        "items": [
            {"name": "Kung Pao Chicken", "price": 380, "desc": "Spicy stir-fried Chinese dish", "veg": False},
            {"name": "Veg Hakka Noodles", "price": 220, "desc": "Classic wok tossed noodles", "veg": True},
            {"name": "Spring Rolls", "price": 180, "desc": "Crispy fried rolls filled with vegetables", "veg": True}
        ]
    },
    {
        "name": "Burger Junction",
        "cuisine": "Fast Food, American",
        "rating": 4.2,
        "picture": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&q=80&w=800",
        "items": [
            {"name": "Classic Cheeseburger", "price": 250, "desc": "Juicy beef patty with cheese", "veg": False},
            {"name": "Crispy Chicken Burger", "price": 280, "desc": "Fried chicken breast with lettuce", "veg": False},
            {"name": "French Fries", "price": 120, "desc": "Golden crinkle cut fries", "veg": True}
        ]
    },
    {
        "name": "Sushi Zen",
        "cuisine": "Japanese",
        "rating": 4.9,
        "picture": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&q=80&w=800",
        "items": [
            {"name": "California Roll", "price": 400, "desc": "Crab, avocado, and cucumber", "veg": False},
            {"name": "Salmon Nigiri", "price": 450, "desc": "Fresh raw salmon over pressed vinegared rice", "veg": False},
            {"name": "Miso Soup", "price": 150, "desc": "Traditional Japanese soup", "veg": True}
        ]
    },
    {
        "name": "Spice Route",
        "cuisine": "Indian",
        "rating": 4.6,
        "picture": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&q=80&w=800",
        "items": [
            {"name": "Butter Chicken", "price": 420, "desc": "Mild curry with creamy tomato sauce", "veg": False},
            {"name": "Palak Paneer", "price": 320, "desc": "Cottage cheese in thick spinach paste", "veg": True},
            {"name": "Garlic Naan", "price": 80, "desc": "Flatbread topped with garlic and cilantro", "veg": True}
        ]
    },
    {
        "name": "Taco Fiesta",
        "cuisine": "Mexican",
        "rating": 4.3,
        "picture": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&q=80&w=800",
        "items": [
            {"name": "Chicken Tacos", "price": 250, "desc": "Soft corn tortillas with grilled chicken", "veg": False},
            {"name": "Beef Burrito", "price": 350, "desc": "Large flour tortilla filled with beef and rice", "veg": False},
            {"name": "Nachos Supreme", "price": 280, "desc": "Tortilla chips topped with cheese and jalapeños", "veg": True}
        ]
    }
]

added_count = 0
for data in restaurants_data:
    if not Restaurant.objects.filter(name=data['name']).exists():
        restaurant = Restaurant.objects.create(
            name=data['name'],
            cuisine=data['cuisine'],
            rating=data['rating'],
            picture=data['picture']
        )
        for item_data in data['items']:
            Item.objects.create(
                restaurant=restaurant,
                name=item_data['name'],
                description=item_data['desc'],
                price=item_data['price'],
                vegeterian=item_data['veg'],
                picture="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&q=80&w=800"
            )
        added_count += 1

print(f"Successfully added {added_count} mock restaurants with items!")
