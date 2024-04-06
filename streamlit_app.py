import streamlit as st
import snowflake.connector

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in customize Smoothie!
    
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be', name_on_order)

# Connect to Snowflake
conn = snowflake.connector.connect(
    user='sahaja',
    password='Snowflake2024',
    account='BOHRATX-XP49780',
    warehouse='COMPUTE_WH',
    database='SMOOTHIES',
    schema='PUBLIC'
)

cursor = conn.cursor()

cursor.execute("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")
fruit_options = [row[0] for row in cursor.fetchall()]

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ', '.join(ingredients_list)

    my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('{ingredients_string}', '{name_on_order}')"

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        cursor.execute(my_insert_stmt)
        conn.commit()
        st.success('Your Smoothie is ordered!', icon="✅")

cursor.close()
conn.close()
