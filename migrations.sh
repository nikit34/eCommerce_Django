apps=(
  'accounts'
  'billing'
  'analytics'
  'addresses'
  'products'
  'carts'
  'marketing'
  'orders'
  'tags'
  'chats'
)

for app in "${apps[@]}"
do
  python manage.py makemigrations $app
  python manage.py migrate $app
done