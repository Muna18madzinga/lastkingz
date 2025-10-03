from quick_sale import QuickSaleManager

qs = QuickSaleManager()
items = qs.get_all_items()

print(f'Found {len(items)} quick sale items:')
for i in items:
    print(f"  {i['id']}: {i['icon']} {i['name']} - ${i['price']}")
