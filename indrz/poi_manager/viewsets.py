from mptt.templatetags.mptt_tags import cache_tree_children

from indrz.poi_manager.models import PoiCategory


def poi_json_tree(request, campus_id, format=None):

    lang_code = request.LANGUAGE_CODE

    def recursive_node_to_dict(node):
        result = collections.OrderedDict()
        result['id'] = node.pk
        if lang_code == "de":
            name = node.cat_name_de
        elif lang_code == "en":
            name = node.cat_name_en
        result['name'] = name
        result['icon'] = node.icon_css_name
        result['selectedIcon'] = node.icon_css_name + "_active"

        if node.pk in (1,2,3,4,5):
            result['selectable'] = False
        # result['state'] = {"checked": False, "disabled": True, "expanded": False, "selected": False}

        children = [recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result['children'] = children
        return result

    root_nodes = cache_tree_children(PoiCategory.objects.filter(enabled=True))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))

    return Response(dicts)
