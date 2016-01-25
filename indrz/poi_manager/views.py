from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from poi_manager.models import PoiCategory, Poi
from poi_manager.forms import PoiCategoryForm, PoiForm

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm


def poi_category_list(request):
    return render_to_response("poi/poi-category.html",
                              {'nodes': PoiCategory.objects.all()},
                              context_instance=RequestContext(request))


def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = PoiCategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return poi_category_list(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = PoiCategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'poi/add-poi-category.html', {'form': form})


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
