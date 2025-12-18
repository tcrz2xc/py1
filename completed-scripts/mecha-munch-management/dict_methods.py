"""Functions to manage a users shopping cart items."""


def add_item(current_cart, items_to_add):
    """Add items to shopping cart.

    :param current_cart: dict - the current shopping cart.
    :param items_to_add: iterable - items to add to the cart.
    :return: dict - the updated user cart dictionary.
    """
    for item in items_to_add:
        if item in current_cart:
            current_cart[item]+=1
        current_cart.setdefault(item,1)
    return current_cart


def read_notes(notes):
    """Create user cart from an iterable notes entry.

    :param notes: iterable of items to add to cart.
    :return: dict - a user shopping cart dictionary.
    """
    new_dict={}
    for item in notes:
        if item in new_dict:
            new_dict[item]+=1
        new_dict.setdefault(item, 1)
    return new_dict



def update_recipes(ideas, recipe_updates):
    """Update the recipe ideas dictionary.

    :param ideas: dict - The "recipe ideas" dict.
    :param recipe_updates: iterable -  with updates for the ideas section.
    :return: dict - updated "recipe ideas" dict.
    """

    ideas.update(recipe_updates)
    return ideas


def sort_entries(cart):
    """Sort a users shopping cart in alphabetically order.

    :param cart: dict - a users shopping cart dictionary.
    :return: dict - users shopping cart sorted in alphabetical order.
    """
    sorted_dict=dict(sorted(cart.items()))
    return sorted_dict


def send_to_store(cart, aisle_mapping):
    """Combine users order to aisle and refrigeration information.

    :param cart: dict - users shopping cart dictionary.
    :param aisle_mapping: dict - aisle and refrigeration information dictionary.
    :return: dict - fulfillment dictionary ready to send to store.
    """
    new_dict=cart.copy()
    for item, value in aisle_mapping.items():
        if item in new_dict:
            if isinstance(new_dict[item], list):
                new_dict[item].extend(value)
            else:
                new_dict[item]=[new_dict[item], value[0], value[1]]

    new_dict1=dict(sorted(new_dict.items(), reverse=True))
        
            
    return new_dict1 
    


def update_store_inventory(fulfillment_cart, store_inventory):
    """Update store inventory levels with user order.

    :param fulfillment cart: dict - fulfillment cart to send to store.
    :param store_inventory: dict - store available inventory
    :return: dict - store_inventory updated.
    """
    inventory=store_inventory.copy()
    for key, value in fulfillment_cart.items():
        if key in inventory:
            inventory[key][0]=inventory[key][0]-value[0]
            if inventory[key][0]<=0:
                inventory[key][0]="Out of Stock"
            
            
    return inventory   
