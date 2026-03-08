"""Functions to keep track and alter inventory."""


def create_inventory(items):
    """Create a dict that tracks the amount (count) of each element on the `items` list.

    :param items: list - list of items to create an inventory from.
    :return: dict - the inventory dictionary.
    """
    values=[]
    for item in items:
        values.append((item, items.count(item)))
    inventory= dict(values)
    return inventory
    


def add_items(inventory, items):
    """Add or increment items in inventory using elements from the items `list`.

    :param inventory: dict - dictionary of existing inventory.
    :param items: list - list of items to update the inventory with.
    :return: dict - the inventory updated with the new items.
    """
    inv = create_inventory(items)
    new_inv = {key: inventory.get(key,0)+ inv.get(key,0) for key in set(inventory) | set(inv)}
    return new_inv
    


def decrement_items(inventory, items):
    """Decrement items in inventory using elements from the `items` list.

    :param inventory: dict - inventory dictionary.
    :param items: list - list of items to decrement from the inventory.
    :return: dict - updated inventory with items decremented.
    """
    for key in inventory:
        for item in items:
            if key == item:
                inventory[key]=inventory[key]-1
                if inventory[key]==0:
                    break
    return inventory
    


def remove_item(inventory, item):
    """Remove item from inventory if it matches `item` string.

    :param inventory: dict - inventory dictionary.
    :param item: str - item to remove from the inventory.
    :return: dict - updated inventory with item removed. Current inventory if item does not match.
    """
    hold=[]
    hold.append(item)
    return {k:v for k, v in inventory.items() if k not in hold}
    


def list_inventory(inventory):
    """Create a list containing only available (item_name, item_count > 0) pairs in inventory.

    :param inventory: dict - an inventory dictionary.
    :return: list of tuples - list of key, value pairs from the inventory dictionary.
    """
    list=[]
    for key, value in inventory.items():
        if value>0:
            list.append((key, value))
    return list
    

