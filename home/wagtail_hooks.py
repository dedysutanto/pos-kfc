# home/wagtail_hooks.py
from wagtail.core import hooks

# https://docs.wagtail.io/en/latest/reference/hooks.html#construct-main-menu
@hooks.register('construct_main_menu')
def hide_page_explorer_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'explorer']
    menu_items[:] = [item for item in menu_items if item.name != 'documents']
    menu_items[:] = [item for item in menu_items if item.name != 'reports']
    menu_items[:] = [item for item in menu_items if item.name != 'images']
