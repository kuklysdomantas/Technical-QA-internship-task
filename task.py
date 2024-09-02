from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import random


def fill_shipping_form(driver, shipping_form, email_address, first_name_text, last_name_text,
                       address_text, city_text, country_text, state_text, postal_code_text,
                       phone_number_text):

    # Fill in email
    email = shipping_form.find_element(By.NAME, "username")
    email.send_keys(email_address)

    # Fill in first name
    first_name = shipping_form.find_element(By.NAME, "firstname")
    first_name.send_keys(first_name_text)

    # Fill in last name
    last_name = shipping_form.find_element(By.NAME, "lastname")
    last_name.send_keys(last_name_text)

    # Fill in address
    address = shipping_form.find_element(By.NAME, "street[0]")
    address.send_keys(address_text)

    # Fill in city
    city = shipping_form.find_element(By.NAME, "city")
    city.send_keys(city_text)

    # Select country
    country = shipping_form.find_element(By.NAME, "country_id")
    country.send_keys(country_text)

    # Select province
    state = shipping_form.find_element(By.NAME, "region_id")
    state.send_keys(state_text)

    # Fill in postal code
    postal_code = shipping_form.find_element(By.NAME, "postcode")
    postal_code.send_keys(postal_code_text)

    # Fill in phone number
    phone_number = shipping_form.find_element(By.NAME, "telephone")
    phone_number.send_keys(phone_number_text)

    # Select paid shipping
    paid_shipping = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='flatrate_flatrate']"))
    )
    paid_shipping.click()


def complete_checkout(driver):
    # Proceed to the next step in checkout
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-role='opc-continue']"))
    )
    next_button.click()

    # Ensure billing and shipping addresses are the same
    billing_shipping_same_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "billing-address-same-as-shipping-checkmo"))
    )
    if not billing_shipping_same_button.is_selected():
        billing_shipping_same_button.click()

    # Place the order
    place_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.action.primary.checkout[data-bind*='placeOrder']"))
    )

    # Wait for any loading masks to disappear
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "loading-mask"))
    )
    place_order_button.click()

    # Wait for the checkout success page to load
    checkout_success = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.checkout-success"))
    )

    # Verify that the "Thank you" message is correct
    thank_you_message = driver.find_element(By.CSS_SELECTOR, "h1.page-title span.base[data-ui-id='page-title-wrapper']")
    assert thank_you_message.text == "Thank you for your purchase!", "Thank you message not correct"

# Disable select engine start screen
chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")
chrome_options.add_experimental_option("detach", True)

# We are using chrome
driver = webdriver.Chrome(options = chrome_options)
driver.get("https://magento.softwaretestingboard.com/")

# For hovering functionality
actions = ActionChains(driver)

# Although some elements themselves can be found individually
# We are simulating try to create a real user flow
# This means clicking and hovering on all the elements that
# The user would actually interact with

# TASK 1

# POINT 1
# Locate navbar (with waiting for the page to load)
navbar_list = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ui-id-2"))
)

# Locate mens link and hover over it
nav_men = navbar_list.find_element(By.ID, "ui-id-5")
actions.move_to_element(nav_men).perform()

assert nav_men.text == "Men", "Nav element is not \"Men\""

# Locate mens tops and hover on it
nav_mens_top = navbar_list.find_element(By.ID, "ui-id-17")
actions.move_to_element(nav_mens_top).perform()

assert nav_mens_top.text == "Tops", "Nav element is not \"Tops\""

# Locate mens hoodies and hover click on it
mens_top_hoodies = navbar_list.find_element(By.ID, "ui-id-20")
assert mens_top_hoodies.text == "Hoodies & Sweatshirts", "Nav element is not \"Hoodies & Sweatshirts\""

mens_top_hoodies.click()

# POINT 2
# Testing only for the first option because the larger ones do not have enough elements

# Wait until the per page picker is loaded until doing anything
per_page_picker = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "limiter"))
)

# Select the 12 value
per_page_selector = Select(per_page_picker)
selected_per_page = per_page_selector.first_selected_option
selected_value = selected_per_page.get_attribute('value')

# Get items and see the length of it
items = driver.find_elements(By.CLASS_NAME, "product-item")
assert selected_value == str(len(items)), "Number of elements in page does not match selected per page amount"

# POINT 3

# Click on Frankie Sweatshirt
frankie_found = False

for item in items:
    item_link = item.find_element(By.CLASS_NAME, "product-item-link")
    item_name = item_link.text.strip()

    # If frankie sweatshirt,
    if item_name == "Frankie Sweatshirt":
        frankie_found = True
        item_link.click()
        break

assert frankie_found == True, "Frankie Sweatshirt not found in page"

# POINT 4

# Get the form for choices
product_form = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "product_addtocart_form"))
)

# Select a random size
size_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute.size .swatch-option")
random_size = random.choice(size_options)
random_size.click()

random_size_text = random_size.text

# Select a random color
color_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute.color .swatch-option")
random_color = random.choice(color_options)
random_color.click()

random_color_text = random_color.get_attribute("option-label")

# Select a random quantity
random_qty = random.randint(1, 10)
qty_field = driver.find_element(By.ID, "qty")
qty_field.clear()
qty_field.send_keys(str(random_qty))

# Assert the right size and color are displayed
show_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute-selected-option")
assert random_size_text == show_options[0].text, "Size does not match selected size"
assert random_color_text == show_options[1].text, "Color does not match selected color"

# POINT 5
# Get initial cart quantity
initial_qty = driver.find_element(By.CLASS_NAME, "counter-number").text

# Add selected items to cart
add_to_cart_button = product_form.find_element(By.ID, "product-addtocart-button")
add_to_cart_button.click()

# Wait for cart to be added to
WebDriverWait(driver, 10).until(
    lambda driver: driver.find_element(By.CLASS_NAME, "counter-number").text != initial_qty
)

# See if cart quantity matches selected quantity
cart_qty = driver.find_element(By.CLASS_NAME, "counter-number").text
assert cart_qty == str(random_qty), "Cart quantity does not match selected quantity"

# POINT 6
# Get cart link and go to it
cart_link = driver.find_element(By.CLASS_NAME, "action.showcart")
driver.get(cart_link.get_attribute("href"))

# Wait for cart to load
item_name_tag = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "product-item-name"))
)
# This is needed because to fix the weird formatting of the text
item_name = " ".join(item_name_tag.get_attribute("textContent").split())

# Get the selected options of item in cart
item_options_list = driver.find_element(By.CLASS_NAME, "page-title-wrapper")
item_options_list = driver.find_element(By.CLASS_NAME, "item-options")
item_options = item_options_list.find_elements(By.TAG_NAME, "dd")

assert item_name == "Frankie Sweatshirt", "Cart sweatshirt name does not match Frankie Sweatshirt"
assert item_options[0].text == random_size_text, "Cart size does not match selected size"
assert item_options[1].text == random_color_text, "Cart color does not match selected color"

# POINT 7
# Go to checkout
checkout_button = driver.find_element(By.CSS_SELECTOR, "button.action.primary.checkout[data-role='proceed-to-checkout']")
checkout_button.click()

# POINT 8
# Wait until checkout is loaded
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "co-shipping-form"))
)

# Get shipping form
shipping_form = driver.find_element(By.ID, "checkout-step-shipping")

# Filling in the shipping form
fill_shipping_form(
    driver=driver,
    shipping_form=shipping_form,
    email_address="kuklys.domantas2001@gmail.com",
    first_name_text="Domantas",
    last_name_text="Kuklys",
    address_text="Sauletekio al. 41",
    city_text="Vilnius",
    country_text="Lithuania",
    state_text="Vilniaus Apskritis",
    postal_code_text="12345",
    phone_number_text="+370655444444"
)

# Completing the checkout
complete_checkout(driver)

driver.quit()

# TASK 2

# POINT 1

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://magento.softwaretestingboard.com/")

actions_women = ActionChains(driver)

# Locate navbar (with waiting for the page to load)
navbar_list_women = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ui-id-2"))
)

# Locate womens link and hover over it
nav_women = navbar_list_women.find_element(By.ID, "ui-id-4")
actions_women.move_to_element(nav_women).perform()

assert nav_women.text == "Women", "Nav element is not \"Women\""

# Locate womens bottoms and hover on it
nav_womens_bottom = navbar_list_women.find_element(By.ID, "ui-id-10")
actions_women.move_to_element(nav_womens_bottom).perform()

assert nav_womens_bottom.text == "Bottoms", "Nav element is not \"Bottoms\""

# Locate womens pants and click on it
womens_bottom_pants = navbar_list_women.find_element(By.ID, "ui-id-15")
assert womens_bottom_pants.text == "Pants", "Nav element is not \"Pants\""

womens_bottom_pants.click()

# POINT 2

# Waiting for the page to load sorter
per_page_picker = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "sorter"))
)

# Selecting the sorter and sorting it by the price
select_sorter = Select(per_page_picker)
select_sorter.select_by_value('price')

# Checking if the sorting is correct
descending_or_ascending_price = driver.find_element(By.XPATH, "//a[@data-role='direction-switcher']")

# Check if the element is currently set to descending
if 'desc' in descending_or_ascending_price.get_attribute('data-value'):
    print("Sorting is correct (Descending). No action needed.")
else:
    print("Sorting is incorrect. Clicking to correct...")
    # Click the element to correct the sorting
    descending_or_ascending_price.click()

WebDriverWait(driver, 10)

# POINT 3

# Locate the first item in the list
first_item = driver.find_element(By.CSS_SELECTOR, 'ol.products li.product-item:first-child')

first_item.click()

# Get the form for choices
product_form = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "product_addtocart_form"))
)

# Select a random size
size_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute.size .swatch-option")
random_size = random.choice(size_options)
random_size.click()

random_size_text = random_size.text

# Select a random color
color_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute.color .swatch-option")
random_color = random.choice(color_options)
random_color.click()

random_color_text = random_color.get_attribute("option-label")

# Select a quantity
qty_field = driver.find_element(By.ID, "qty")
qty_field.clear()
qty_field.send_keys('1')

# Assert the right size and color are displayed
show_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute-selected-option")
assert random_size_text == show_options[0].text, "Size does not match selected size"
assert random_color_text == show_options[1].text, "Color does not match selected color"

# Adding item to cart
driver.find_element(By.ID, 'product-addtocart-button').click()

# POINT 4

# Wait for elements to be loaded
WebDriverWait(driver, 10).until(
    lambda driver: driver.find_element(By.CLASS_NAME, "counter-number").text != ''
)

# Saving the carts number
initial_qty = driver.find_element(By.CLASS_NAME, "counter-number").text

# Adding two more randomly picked pants
for added_to_cart in range(2):

    # Navigating to the previous page
    driver.back()
    product_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "maincontent"))
    )

    # Select random pants
    pants_options = driver.find_elements(By.CSS_SELECTOR, 'ol.products li.product-item')
    random_pants = random.choice(pants_options)
    random_pants.click()

    # Get the form for choices
    product_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "product_addtocart_form"))
    )

    # Select a random size
    size_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute.size .swatch-option")
    random_size = random.choice(size_options)
    random_size.click()

    random_size_text = random_size.text

    # Select a random color
    color_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute.color .swatch-option")
    random_color = random.choice(color_options)
    random_color.click()

    random_color_text = random_color.get_attribute("option-label")

    # Select a quantity
    qty_field = driver.find_element(By.ID, "qty")
    qty_field.clear()
    qty_field.send_keys('1')

    # Assert the right size and color are displayed
    show_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute-selected-option")

    assert random_size_text == show_options[0].text, "Size does not match selected size"
    assert random_color_text == show_options[1].text, "Color does not match selected color"

    # Adding item to cart
    driver.find_element(By.ID, 'product-addtocart-button').click()

    # Wait for elements to be loaded
    WebDriverWait(driver, 10).until(
        lambda driver: driver.find_element(By.CLASS_NAME, "counter-number").text != initial_qty
    )

    # Checking if cart icon is updated with each product.
    cart_qty = driver.find_element(By.CLASS_NAME, "counter-number").text
    assert cart_qty == str(int(initial_qty)+1), "The cart icon is not updated with each product"

# POINT 5

# Wait for elements to be loaded
WebDriverWait(driver, 10).until(
    lambda driver: driver.find_element(By.CLASS_NAME, "counter-number").text != initial_qty
)

# Wait for elements to be loaded
WebDriverWait(driver, 10).until(
    lambda driver: driver.find_element(By.CLASS_NAME, "counter-number").text != '3'
)

# Opening mini cart
driver.find_element(By.CLASS_NAME, 'minicart-wrapper').click()

# Waiting for the mini cart to open
per_page_picker = WebDriverWait(driver, 10).until(
   EC.presence_of_element_located((By.ID, 'mini-cart'))
)

# Removing random pants
pants_options_minicart = driver.find_elements(By.CSS_SELECTOR, 'ol.minicart-items li.product-item')
random_choice = random.choice(pants_options_minicart)
random_choice.find_element(By.XPATH, '//a[@title="Remove item"]').click()

# Waiting for the popup to open
per_page_picker = WebDriverWait(driver, 10).until(
   EC.presence_of_element_located((By.XPATH, '//*[@data-role="modal"]'))
)

# Pressing OK for removing the item
ok_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.action-primary.action-accept'))
)
ok_button.click()

# POINT 6

# Pressing the "Proceed to checkout" button
driver.find_element(By.ID, 'top-cart-btn-checkout').click()

# Wait until checkout is loaded
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "co-shipping-form"))
)

# POINT 7

# As I can see suggested products are not shown in the checkout page,
# so I need to go back to the previous page and add it

# Going to the previous page
driver.back()
WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".block-content"))
    )

# Select random suggested pants
suggested_pants_options = driver.find_elements(By.CSS_SELECTOR, 'ol.products li.product-item')
random_suggested_pants = random.choice(suggested_pants_options)
random_suggested_pants.click()

# Get the form for choices
product_form = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "product_addtocart_form"))
)

# Select a random size
size_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute.size .swatch-option")
random_size = random.choice(size_options)
random_size.click()

random_size_text = random_size.text

# Select a random color
color_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute.color .swatch-option")
random_color = random.choice(color_options)
random_color.click()

random_color_text = random_color.get_attribute("option-label")

# Select a quantity
qty_field = driver.find_element(By.ID, "qty")
qty_field.clear()
qty_field.send_keys('1')

# Assert the right size and color are displayed
show_options = driver.find_elements(By.CSS_SELECTOR, ".swatch-attribute-selected-option")
assert random_size_text == show_options[0].text, "Size does not match selected size"
assert random_color_text == show_options[1].text, "Color does not match selected color"

# Saving the carts number
initial_qty = driver.find_element(By.CLASS_NAME, "counter-number").text

# Adding item to cart
driver.find_element(By.ID, 'product-addtocart-button').click()

# Wait for elements to be loaded
WebDriverWait(driver, 10).until(
    lambda driver: driver.find_element(By.CLASS_NAME, "counter-number").text != initial_qty
)

# Checking if cart icon is updated with each product.
cart_qty = driver.find_element(By.CLASS_NAME, "counter-number").text
assert cart_qty == str(int(initial_qty) + 1), "The cart icon is not updated with each product"

# Opening mini cart
driver.find_element(By.CLASS_NAME, 'minicart-wrapper').click()

# Waiting for the mini cart to open
per_page_picker = WebDriverWait(driver, 10).until(
   EC.presence_of_element_located((By.ID, 'mini-cart'))
)

# Pressing the "Proceed to checkout" button
driver.find_element(By.ID, 'top-cart-btn-checkout').click()

# Wait until checkout is loaded
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "co-shipping-form"))
)

# POINT 8

# Get shipping form
shipping_form = driver.find_element(By.ID, "checkout-step-shipping")

# Filling in the shipping form
fill_shipping_form(
    driver=driver,
    shipping_form=shipping_form,
    email_address="kuklys.domantas2001@gmail.com",
    first_name_text="Domantas",
    last_name_text="Kuklys",
    address_text="Sauletekio al. 41",
    city_text="Vilnius",
    country_text="Lithuania",
    state_text="Vilniaus Apskritis",
    postal_code_text="12345",
    phone_number_text="+370655444444"
)

# Completing the checkout
complete_checkout(driver)

driver.quit()
