from django import template

from ..models import Menu, MenuItem

register = template.Library()

def build_tree_data(root, prev_dict = None):
    if prev_dict is None:
        prev_dict = dict()
    dictionary = dict()
    dictionary['name'] = root.name
    prev_url = prev_dict.get('url', '')
    dictionary['url'] = "/".join([prev_url, root.name])
    root_childs = root.childs.all()
    if root_childs:
        dictionary['childs'] = []
        for child in root_childs:
            dictionary['childs'].append(build_tree_data(child, dictionary))
    # print(dictionary)
    return dictionary

def build_tree_data_2(foreign_keys, curr, prev_dict=None):
    if prev_dict is None:
        prev_dict = dict()
    print(curr)
    dictionary = dict()
    dictionary['name'] = curr['name']
    dictionary['childs'] = []
    prev_url = prev_dict.get('url', '')
    dictionary['url'] = "/".join([prev_url, curr['name']])
    for fk in foreign_keys:
        if curr['id'] == fk['parent_id']:
            dictionary['childs'].append(build_tree_data_2(foreign_keys, fk, dictionary))
    return dictionary

        # dictionary['childs'] = foreign_keys.get()


@register.inclusion_tag('tree_tag.html', takes_context=True)
def tree_menu(context, name):
    url = context['request'].path
    menu = Menu.objects.get(name=name)
    foreign_keys = menu.foreign_keys.strip('[')
    foreign_keys = foreign_keys.strip(']') #TODO: remove this
    foreign_keys = [int(i) for i in foreign_keys.split(',')]
    foreign_keys = MenuItem.objects.filter(id__in=foreign_keys).select_related('parent').values()
    for fk in foreign_keys:
        if fk['parent_id'] is None:
            dictionary = [build_tree_data_2(foreign_keys, foreign_keys[0])]
            break
    paths = url.split('/')
    paths = list(filter(None, paths))
    return {'tree': dictionary, 'paths': paths}