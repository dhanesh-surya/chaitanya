import os
import shutil
import django

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_portal.settings')
django.setup()

from core.models import QuickLinkCard

SRC_DIR = r"C:\temp-csac\chaitanyafiles01.s3.amazonaws.com\homeImages"
DEST_DIR = r"C:\temp-csac\csac_portal\media\cards"

os.makedirs(DEST_DIR, exist_ok=True)

# Define our professional academic design configurations for the 9 cards
card_designs = {
    1: { # Merit List
        "bg_image_name": "Merit_List.png",
        "bg_color": "#ffffff",
        "overlay_color": "#000000",
        "overlay_opacity": 0.55
    },
    2: { # Infrastructure
        "bg_image_name": "College_Building.png",
        "bg_color": "#ffffff",
        "overlay_color": "#B71A34",
        "overlay_opacity": 0.65
    },
    3: { # NEP 2020
        "bg_image_name": None,
        "bg_color": "#B71A34",
        "overlay_color": "#000000",
        "overlay_opacity": 0.0
    },
    4: { # Events
        "bg_image_name": "pic7.jpg",
        "bg_color": "#ffffff",
        "overlay_color": "#000000",
        "overlay_opacity": 0.55
    },
    5: { # Guest Lectures
        "bg_image_name": "dr_kiran_seth.png",
        "bg_color": "#ffffff",
        "overlay_color": "#111827",
        "overlay_opacity": 0.65
    },
    6: { # IIC
        "bg_image_name": "3_Star_Rating_IIC.png",
        "bg_color": "#ffffff",
        "overlay_color": "#000000",
        "overlay_opacity": 0.50
    },
    7: { # Our Products
        "bg_image_name": None,
        "bg_color": "#111827",
        "overlay_color": "#000000",
        "overlay_opacity": 0.0
    },
    8: { # NSS
        "bg_image_name": None,
        "bg_color": "#B71A34",
        "overlay_color": "#000000",
        "overlay_opacity": 0.0
    },
    9: { # Sports
        "bg_image_name": "pic6.jpg",
        "bg_color": "#ffffff",
        "overlay_color": "#B71A34",
        "overlay_opacity": 0.55
    }
}

for card_id, design in card_designs.items():
    try:
        card = QuickLinkCard.objects.get(id=card_id)
        print(f"Updating card {card.id}: {card.title}")
        
        # Copy image if configured
        if design["bg_image_name"]:
            src_path = os.path.join(SRC_DIR, design["bg_image_name"])
            dest_path = os.path.join(DEST_DIR, design["bg_image_name"])
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                card.bg_image = f"cards/{design['bg_image_name']}"
                print(f"  Copied and set background image: cards/{design['bg_image_name']}")
            else:
                print(f"  Warning: Source image {src_path} not found.")
                card.bg_image = None
        else:
            card.bg_image = None
            
        # Set colors and opacity
        card.bg_color = design["bg_color"]
        card.overlay_color = design["overlay_color"]
        card.overlay_opacity = design["overlay_opacity"]
        card.save()
        print(f"  Successfully saved design styling.")
    except QuickLinkCard.DoesNotExist:
        print(f"Card ID {card_id} does not exist in database, skipping.")
    except Exception as e:
        print(f"Error updating card {card_id}: {e}")

print("All card designs updated successfully!")
