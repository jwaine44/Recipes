SELECT * FROM recipes;
SELECT * FROM users;

INSERT INTO recipes(name, description, under_30_minutes, instructions, date_made)
VALUES('Garlic Bread', 'Yummy buttery garlic bread!', 'Yes',
'-Load tons of butter and garlic on sliced baguette
-Bake in oven at 400F for 15 minutes or until golden brown
-Consume in a ravenous fashion
-Share with no one!!',
'June 19, 2022');

INSERT into recipes(name, description, under_30_minutes, instructions, date_made) VALUES('Chicken Patties', 'Fried chicken patties', 'Yes', 'Unpack patties and throw in oven for 20 minutes at 400F', 'June 20, 2022');
INSERT into recipes_users(recipe_id, user_id) VALUES('1', '1');

SELECT * FROM users LEFT JOIN recipes_users ON recipes_users.user_id = users.id LEFT JOIN recipes ON recipes_users.recipe_id = recipes.id WHERE users.id = 1;
SELECT * FROM recipes LEFT JOIN recipes_users ON recipes_users.recipe_id = recipes.id LEFT JOIN users ON recipes_users.user_id = users.id WHERE recipes.id = 1;

UPDATE recipes SET name = 'Spaghetti', description = 'Yummy noodles and sauce', under_30_minutes = 'No', instructions = 'Boil the water and add noodles - Toss the noodles with the sauce' WHERE id = 1;