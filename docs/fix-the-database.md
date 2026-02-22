# Fix the DataBase

If you need to fix the database. There are two main ways to handle this. The simplest approach during the development stage is **to clear the data**.

## Option A: The Fast Way (if DB data is not important)

If you are still in development and don't mind losing the menu items created in the admin panel:

1. Delete the `db.sqlite3` database file in the project root.

2. Delete the migration files in the `core/migrations/` folder (all of them except `__init__.py`).

3. Re-create and apply the migrations:

```Bash copy
python manage.py makemigrations
```

```Bash copy
python manage.py migrate
```

4. You will need to run `createsuperuser` again.

## Option B: The Proper Way (via Console)

If you cannot delete the database, you need to manually create a `Menu` object so the ForeignKey can find its target.

1. Roll back the migration to state `0003` (if possible):

```Bash copy
python manage.py migrate core 0003
```

2. Enter the Django shell:

```Bash copy
python manage.py shell
```

3. Create the menu manually:

```Python copy
from core.models import Menu
# Specify the required fields of the Menu model
Menu.objects.create(id=1, name="Main Menu")
exit()
```

4. Run the migration again:

```Bash copy
python manage.py migrate
```

### Option B: Make the field optional

If a menu item can exist without the menu itself (temporarily), modify the model in `models.py`:

```Python copy
menu = models.ForeignKey(Menu, on_click=models.CASCADE, null=True, blank=True)
```

After doing this, run `makemigrations` and `migrate` again.

> [!NOTE]
> Which option works best for you? If this is a learning project, **I recommend Option A** — it will save you a lot of time debugging relationships.