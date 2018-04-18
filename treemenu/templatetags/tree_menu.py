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
    if root.childs.all().exists():
        dictionary['childs'] = []
        for child in root.childs.all():
            dictionary['childs'].append(build_tree_data(child, dictionary))
    # print(dictionary)
    return dictionary

@register.inclusion_tag('tree_tag.html', takes_context=True)
def tree_menu(context, name):
    url = context['request'].path
    menu = Menu.objects.get(name=name)
    root = menu.root_item
    dictionary = [build_tree_data(root)]
    print(dictionary)
    paths = url.split('/')
    paths = list(filter(None, paths))
    print(paths)
    return {'tree': dictionary, 'paths': paths}