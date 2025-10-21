import streamlit as st

st.set_page_config(page_title="MiniMart Convenience Store", layout="wide")

st.title("🏪 MiniMart Convenience Store")

# --- Data Setup ---
categories = {
    "Chips": {
        "Lay’s Classic": 2.5,
        "Doritos Nacho Cheese": 2.8,
        "Pringles Original": 3.0,
        "Cheetos Crunchy": 2.6,
        "Ruffles Sour Cream & Onion": 2.7,
        "Lay’s BBQ": 2.5,
        "Takis Fuego": 3.2,
        "Kettle Sea Salt": 2.9,
        "Tostitos Scoops": 3.1,
        "Calbee Hot & Spicy": 3.0
    },
    "Drinks": {
        "Coca-Cola": 1.5,
        "Pepsi": 1.5,
        "Sprite": 1.5,
        "Fanta Orange": 1.6,
        "Mountain Dew": 1.7,
        "Gatorade Lemon-Lime": 2.0,
        "Red Bull": 2.8,
        "Monster Energy": 3.0,
        "Iced Coffee (Can)": 2.2,
        "Bottled Water": 1.0,
        "Minute Maid Apple Juice": 2.0,
        "Milk Tea (Bottle)": 2.5
    },
    "Candies / Chocolate": {
        "Snickers": 1.5,
        "KitKat": 1.5,
        "Twix": 1.6,
        "M&M’s": 1.8,
        "Hershey’s Bar": 1.7,
        "Skittles": 1.5,
        "Reese’s Peanut Butter Cup": 1.9,
        "Mentos": 1.0,
        "Toblerone": 2.0,
        "Ferrero Rocher": 2.5,
        "Sour Patch Kids": 1.8,
        "Chupa Chups Lollipop": 1.0,
        "Kinder Bueno": 2.2,
        "Pocky (Strawberry)": 1.8
    },
    "Instant Noodles": {
        "Nissin Cup Noodles (Chicken)": 2.0,
        "Nissin Spicy Beef": 2.2,
        "Shin Ramyun": 2.5,
        "Samyang Hot Chicken": 3.0,
        "Indomie Mi Goreng": 2.0,
        "Maruchan Seafood Flavor": 2.3,
        "Nongshim Neoguri": 2.5,
        "Mama Shrimp Tom Yum": 2.1
    },
    "Gift Cards": {
        "Steam Gift Card ($10)": 10.0,
        "Google Play Card ($10)": 10.0,
        "Apple Gift Card ($10)": 10.0,
        "Roblox Gift Card ($10)": 10.0,
        "Amazon Gift Card ($10)": 10.0,
        "Netflix Gift Card ($10)": 10.0
    }
}

# --- Initialize Session State ---
if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- Functions ---
def add_to_cart(item, price):
    if item in st.session_state.cart:
        st.session_state.cart[item]["quantity"] += 1
    else:
        st.session_state.cart[item] = {"price": price, "quantity": 1}
    st.toast(f"✅ Added {item} to cart", icon="🛒")

def remove_from_cart(item):
    if item in st.session_state.cart:
        st.session_state.cart[item]["quantity"] -= 1
        if st.session_state.cart[item]["quantity"] <= 0:
            del st.session_state.cart[item]
        st.toast(f"❌ Removed {item}", icon="🗑️")

# --- Sidebar: Cart ---
st.sidebar.header("🛒 Your Cart")

if st.session_state.cart:
    total = 0
    for item, info in st.session_state.cart.items():
        st.sidebar.write(f"{item} x{info['quantity']} - ${info['price'] * info['quantity']:.2f}")
        total += info["price"] * info["quantity"]
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"💰 Total: ${total:.2f}")

    # Use a form for Buy Now to ensure immediate state update
    with st.sidebar.form(key="buy_form"):
        submitted = st.form_submit_button("🛍️ Buy Now")
        if submitted:
            st.sidebar.success("Purchase complete! Example receipt below:")
            st.sidebar.text("Card: ##########1234\nThank you for shopping with us!")
            st.session_state.cart = {}  # Clear cart immediately
else:
    st.sidebar.write("Your cart is empty.")

# --- Category Selection ---
category = st.selectbox("Choose a category:", list(categories.keys()))

st.subheader(f"🧺 {category}")

# --- Display Items with compact dark boxes ---
cols = st.columns(3)
i = 0

for item, price in categories[category].items():
    with cols[i % 3]:
        st.markdown(
            f"""
            <div style="
                border:1px solid #444;
                border-radius:12px;
                padding:15px;
                margin-bottom:15px;
                background-color:#1e1e1e;
                color:white;
                text-align:center;
                box-shadow:2px 2px 6px rgba(0,0,0,0.3);
            ">
                <h4 style="margin-bottom:5px;">{item}</h4>
                <p style="margin-top:0;">💵 ${price:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col1, col2 = st.columns([1,1])
        with col1:
            st.button("➕ Add", key=f"add_{item}", on_click=add_to_cart, args=(item, price))
        with col2:
            st.button("➖ Remove", key=f"remove_{item}", on_click=remove_from_cart, args=(item,))
    i += 1

