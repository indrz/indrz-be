import collections
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.utils.translation import ugettext as _

from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from poi_manager.models import PoiCategory, Poi
from poi_manager.forms import PoiCategoryForm, PoiForm
from poi_manager.serializers import PoiSerializer, PoiCategorySerializer

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm
from mptt.templatetags.mptt_tags import cache_tree_children


def poi_category_list(request, format=None):
    return render(request, "poi/poi-category.html",
                  {'nodes': PoiCategory.objects.filter(enabled=True)})


def poi_bootstrap_tree(request, format=None):
    return render(request, "poi/poi-tree.html",
                  {'nodes': PoiCategory.objects.filter(enabled=True)})


@api_view(['GET', ])
def get_poi_by_id(request, poi_id, format=None):
    try:
        poi_qs = Poi.objects.filter(id=poi_id).filter(enabled=True)
        serializer = PoiSerializer(poi_qs, many=True)
        return Response(serializer.data)

    except Exception as e:
        raise APIException(detail=e)


@api_view(['GET', ])
def poi_category_json(request, format=None):
    def recursive_node_to_dict(node):
        result = collections.OrderedDict()
        result['id'] = node.pk
        result['name'] = node.cat_name
        result['icon'] = node.icon_css_name

        children = [recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result['children'] = children
        return result

    root_nodes = cache_tree_children(PoiCategory.objects.filter(enabled=True))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))

    return Response(dicts)

@api_view(['GET', ])
def poi_root_nodes(request, format=None):
    def recursive_node_to_dict(node):
        result = collections.OrderedDict()
        result['id'] = node.pk
        result['name'] = _(node.cat_name)
        result['icon'] = node.icon_css_name

        children = [recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result['nodes'] = children
        return result

    root_nodes = cache_tree_children(PoiCategory.objects.filter(enabled=True).filter(parent__isnull=True))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))

    return Response(dicts)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def poi_json_tree(request, format=None):

    def recursive_node_to_dict(node):
        result = collections.OrderedDict()
        result['id'] = node.pk
        result['name'] = node.cat_name_en
        result['name_en'] = node.cat_name_en
        result['name_de'] = node.cat_name_de
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


@api_view(['GET', ])
def get_poi_by_category(request, category_name, format=None):
    if request.method == 'GET':
        try:
            cats = PoiCategory.objects.filter(enabled=True).get(cat_name__contains=category_name)

            if cats:

                poi_qs = Poi.objects.filter(fk_poi_category=cats.id).filter(enabled=True)
                if poi_qs:
                    serializer = PoiSerializer(poi_qs, many=True)
                    return Response(serializer.data)
        except Exception as e:
            raise APIException(detail=e)


@api_view(['GET', ])
def get_poi_by_cat_id(request, cat_id, format=None):
    """
    Get all poi features for children and grandchildren of incomping parent cateogry id
    :param request:
    :param campus_id: id of campus as integer
    :param cat_id:
    :param format:
    :return:
    """
    if request.method == 'GET':

        poicat_qs = PoiCategory.objects.filter(enabled=True).get(pk=cat_id).get_descendants()
        # cat_children = PoiCategory.objects.add_related_count(poicat_qs,Poi,'fk_poi_category', 'cat_name')

        poi_ids = []
        for x in poicat_qs:
            poi_ids.append(x.id)

        qs_objs = Poi.objects.filter(fk_poi_category_id__in=poi_ids).filter(enabled=True)

        if qs_objs:
            serializer = PoiSerializer(qs_objs, many=True)
            return Response(serializer.data)
        elif len(poi_ids)==0:
            qs = Poi.objects.filter(fk_poi_category_id = cat_id).filter(enabled=True)
            serializer = PoiSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'something booomed with category id : ' + cat_id})


@api_view(['GET', ])
def get_poi_by_cat_name(request, category_name, format=None):
    cats = PoiCategory.objects.filter(cat_name__exact=category_name).filter(enabled=True)
    # list = cats.get_descendants()


    # from itertools import chain
    # result_list = list(chain(page_list, article_list, post_list))

    if cats:
        if len(cats) > 1:
            cat_ids = []
            for cat in cats:

                cat_ids.append(cat.id)

            poi_qs = Poi.objects.filter(fk_poi_category__in=cat_ids).filter(enabled=True)

        else:
            poi_qs = Poi.objects.filter(fk_poi_category=cats[0].id).filter(enabled=True)
    else:
        # return Response({'error': 'No Poi found with the given category name: ' + category_name} )
        return Response({'error': 'no category found with the given category name: ' + category_name})

    if poi_qs:
        serializer = PoiSerializer(poi_qs, many=True)

        return Response(serializer.data)

    else:
        return Response({'error': 'sorry no poi entries found assigned to the category name : ' + category_name})


@api_view(['GET', ])
def get_poicat_by_id(request, cat_id, format=None):
    cats = PoiCategory.objects.filter(enabled=True).get(pk=cat_id)
    serializer = PoiCategorySerializer(cats)
    return Response(serializer.data)


@api_view(['GET', ])
def poi_category_by_name(request, category_name, format=None):
    def recursive_node_to_dict(node):
        result = collections.OrderedDict()
        result['id'] = node.pk
        result['name'] = node.cat_name
        result['icon'] = node.icon_css_name

        children = [recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result['children'] = children
        return result

    root_nodes = cache_tree_children(PoiCategory.objects.filter(cat_name__icontains=category_name).filter(enabled=True))
    dicts = []
    if root_nodes:

        for n in root_nodes:
            dicts.append(recursive_node_to_dict(n))

        return Response(dicts)
    else:
        return Response({'error': 'no category found with the name : ' + category_name})


# @api_view(['GET', ])
# def poi_list(request, format=None):
#     try:
#         poi_qs = Poi.objects.filter(enabled=True).order_by('fk_poi_category__icon_css_name')
#         serializer = PoiSerializer(poi_qs, many=True)
#         return Response(serializer.data)
#
#     except Exception as e:
#         raise APIException(detail=e)


@api_view(['GET', ])
def search_poi_by_name(request, poi_name, format=None, **kwargs):
    poi_qs = Poi.objects.filter(name__icontains=poi_name).filter(enabled=True)
    floor = request.GET.get('floor')

    if floor:
        poi_qs = Poi.objects.filter(name__icontains=poi_name).filter(floor_num=floor).filter(enabled=True)

    if poi_qs:
        att = poi_qs.values()

        poi_entries = []

        for value in att:
            poi_entries.append(value)

        return Response(poi_entries)
    else:
        return Response({'error': 'something went wrong no POI with that name found'})



def add_poi(request, category_name_slug):
    try:
        cat = PoiCategory.objects.get(slug=category_name_slug)
    except PoiCategory.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PoiForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return poi_category_list(request)
        else:
            print(form.errors)
    else:
        form = PoiForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'poi/add-poi.html', context_dict)


def move_category(request, category_pk):
    category = get_object_or_404(PoiCategory, pk=category_pk)
    if request.method == 'POST':
        form = MoveNodeForm(category, request.POST)
        if form.is_valid():
            try:
                category = form.save()
                return HttpResponseRedirect(category.get_absolute_url())
            except InvalidMove:
                pass
    else:
        form = MoveNodeForm(category)

    return render_to_response('poi/poi-form.html', {
        'form': form,
        'category': category,
        'category_tree': PoiCategory.objects.all(),
    })

icon_map = [{"name": "icon-h", "description": "exit"},
{"name": "icon-g", "description": "stairs-up"},
{"name": "icon-i", "description": "ramp-up"},
{"name": "icon-l", "description": "baby"},
{"name": "icon-n", "description": "fountain"},
{"name": "icon-t", "description": "plus"},
{"name": "icon-o", "description": "people"},
{"name": "icon-p", "description": "info-library"},
{"name": "icon-q", "description": "sit-workstation"},
{"name": "icon-r", "description": "stand-workstation"},
{"name": "icon-s", "description": "hanger"},
{"name": "icon-u", "description": "no-mobiles"},
{"name": "icon-v", "description": "phone-booth"},
{"name": "icon-y", "description": "security-camera"},
{"name": "icon-B", "description": "no-dogs"},
{"name": "icon-C", "description": "no-sound"},
{"name": "icon-D", "description": "no-fire"},
{"name": "icon-E", "description": "no-skateboarding"},
{"name": "icon-F", "description": "parking"},
{"name": "icon-G", "description": "parking-payment"},
{"name": "icon-H", "description": "motorcycle"},
{"name": "icon-I", "description": "delivery"},
{"name": "icon-J", "description": "bike-parking"},
{"name": "icon-L", "description": "basketball"},
{"name": "icon-M", "description": "pingpong"},
{"name": "icon-N", "description": "cafe"},
{"name": "icon-O", "description": "food"},
{"name": "icon-Q", "description": "sitting-area"},
{"name": "icon-S", "description": "shopping-cart"},
{"name": "icon-T", "description": "smoking"},
{"name": "icon-U", "description": "printer"},
{"name": "icon-V", "description": "print-station"},
{"name": "icon-W", "description": "scanner"},
{"name": "icon-Y", "description": "self-checkout"},
{"name": "icon-Z", "description": "quiet-area"},
{"name": "icon-zero", "description": "info-point"},
{"name": "icon-one", "description": "triangle"},
{"name": "icon-two", "description": "arrow-up"},
{"name": "icon-R", "description": "shopping-cart-empty"},
{"name": "icon-X", "description": "books"},
{"name": "icon-a", "description": "elevator-a"},
{"name": "icon-b", "description": "elevator-b"},
{"name": "icon-c", "description": "elevator-c"},
{"name": "icon-d", "description": "elevator"},
{"name": "icon-x", "description": "info"},
{"name": "icon-K", "description": "basketball"},
{"name": "icon-w", "description": "women-wc"},
{"name": "icon-m", "description": "men-wc"},
{"name": "icon-j", "description": "wc"},
{"name": "icon-k", "description": "wheelchair"},
{"name": "icon-z", "description": "locker"},
{"name": "icon-P", "description": "family"},
{"name": "icon-f", "description": "stairs-arrow-up"},
{"name": "icon-A", "description": "no-smoking"},
{"name": "icon-e", "description": "stairs-arrow-down"},
{"name": "icon-three", "description": "defi"},
{"name": "icon-four", "description": "info-triangle"},
{"name": "icon-five", "description": "baby-buggy"},
{"name": "icon-Agrave", "description": "p1"},
{"name": "icon-Aacute", "description": "p2"},
{"name": "icon-Acircumflex", "description": "p3"},
{"name": "icon-Atilde", "description": "p4"},
{"name": "icon-six", "description": "meeting-point"},
{"name": "icon-agrave", "description": "elevator-d"},
{"name": "icon-aacute", "description": "elevator-e"},
{"name": "icon-seven", "description": "ramp-down"},
{"name": "icon-eight", "description": "bicycle"},
{"name": "icon-nine", "description": "bike-covered"},
{"name": "icon-colon", "description": "front-office"}]
