import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.set_page_config(page_title="🍓 Smoothie App", page_icon=":cup_with_straw:")
st.title("🍓 Melanie's Smoothies App")
st.subheader(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Conexión a Snowflake
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# Cargar frutas desde tabla
df_snowflake = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in df_snowflake.collect()]

# Inputs del usuario
name_on_order = st.text_input("🧑‍🍳 Name on Smoothie:")
ingredients_list = st.multiselect(
    "🥝 Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# 💡 Muestra el botón después de que se capturan los inputs
submit = st.button("✅ Submit Order")

# Procesar solo cuando se presiona el botón
if submit:
    if not name_on_order.strip():
        st.warning("Please enter your name.")
    elif not ingredients_list:
        st.warning("Please select at least one ingredient.")
    else:
        ingredients_string = ", ".join(ingredients_list)
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        try:
            session.sql(insert_stmt).collect()
            st.success("Your Smoothie is ordered! ✅")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json)
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=true)
