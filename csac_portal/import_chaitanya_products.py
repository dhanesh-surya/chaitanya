import os
import sys
import shutil
import django

# Configure Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_portal.settings")
django.setup()

from core.models import Product, ProductCategory

def main():
    source_dir = r"C:\Chaitanya Products"
    
    # Define local folder db in workspace and django portal
    db_workspace = r"C:\temp-csac\chaitanyacg.ac.in\db"
    db_portal = r"C:\temp-csac\csac_portal\db"
    media_products_dir = r"C:\temp-csac\csac_portal\media\products"

    # Create directories if they do not exist
    os.makedirs(db_workspace, exist_ok=True)
    os.makedirs(db_portal, exist_ok=True)
    os.makedirs(media_products_dir, exist_ok=True)

    print("Copying files to local folder db and media folder...")
    
    # List of files in source directory
    if not os.path.exists(source_dir):
        print(f"Error: Source directory {source_dir} does not exist.")
        return

    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    for filename in files:
        src_path = os.path.join(source_dir, filename)
        
        # Copy to workspace db
        shutil.copy2(src_path, os.path.join(db_workspace, filename))
        # Copy to portal db
        shutil.copy2(src_path, os.path.join(db_portal, filename))
        
        # If it's a product image, copy to media products folder
        if filename != "20240529_113818am_ByGPSMapCamera.jpg":
            shutil.copy2(src_path, os.path.join(media_products_dir, filename))
            
    print("Files successfully copied.")

    # Create / get Categories
    cat_panchgavya, _ = ProductCategory.objects.get_or_create(
        name="Panchgavya Products",
        defaults={"order": 4}
    )
    cat_herbal, _ = ProductCategory.objects.get_or_create(
        name="Herbal & Cosmetics",
        defaults={"order": 5}
    )

    # 1. Update existing product: Chaitanya College Warli Arts (ID: 1)
    try:
        product_warli = Product.objects.get(id=1)
        product_warli.image = "products/20240529_113613am_ByGPSMapCamera.jpg"
        product_warli.image_url = "" # Clear external url so local image is preferred
        product_warli.save()
        print("Updated Chaitanya College Warli Arts with local image.")
    except Product.DoesNotExist:
        print("Warning: Product Chaitanya College Warli Arts (ID 1) not found.")

    # 2. Add Gonyle Floor Cleaner
    gonyle, created = Product.objects.update_or_create(
        name="Chaitanya Premium Gonyle",
        defaults={
            "category": cat_panchgavya,
            "description": "Premium floor cleaner made from indigenous cow's urine. Safe, eco-friendly, and natural disinfectant.",
            "price": 65.00,
            "image": "products/20240529_113601am_ByGPSMapCamera.jpg",
            "image_url": "",
            "in_stock": True,
            "is_active": True,
            "order": 4
        }
    )
    print(f"{'Created' if created else 'Updated'} Chaitanya Premium Gonyle.")

    # 3. Add Panchgavya Lobhan Dhoop Cones
    dhoop, created = Product.objects.update_or_create(
        name="Panchgavya Lobhan Dhoop Cones",
        defaults={
            "category": cat_panchgavya,
            "description": "Handmade organic dhoop cones prepared using indigenous cow dung and lobhan. Fosters a pure, aromatic, and positive environment.",
            "price": 45.00,
            "image": "products/20240529_113645am_ByGPSMapCamera.jpg",
            "image_url": "",
            "in_stock": True,
            "is_active": True,
            "order": 5
        }
    )
    print(f"{'Created' if created else 'Updated'} Panchgavya Lobhan Dhoop Cones.")

    # 4. Add Chaitanya Aloe Vera Gel
    aloe, created = Product.objects.update_or_create(
        name="Chaitanya Aloe Vera Gel",
        defaults={
            "category": cat_herbal,
            "description": "Pure and soothing Aloe Vera Gel prepared by students in the laboratory. Excellent for skin care, hydration, and soothing burns.",
            "price": 35.00,
            "image": "products/20240529_113655am_ByGPSMapCamera.jpg",
            "image_url": "",
            "in_stock": True,
            "is_active": True,
            "order": 6
        }
    )
    print(f"{'Created' if created else 'Updated'} Chaitanya Aloe Vera Gel.")

    # 5. Add Chaitanya Herbal Gulal
    gulal, created = Product.objects.update_or_create(
        name="Chaitanya Herbal Gulal",
        defaults={
            "category": cat_herbal,
            "description": "Natural and skin-friendly Herbal Gulal prepared by college students in the laboratory. Made using organic ingredients and natural colors.",
            "price": 20.00,
            "image": "products/20240529_113707am_ByGPSMapCamera.jpg",
            "image_url": "",
            "in_stock": True,
            "is_active": True,
            "order": 7
        }
    )
    print(f"{'Created' if created else 'Updated'} Chaitanya Herbal Gulal.")

if __name__ == "__main__":
    main()
