import factory

from buildings.models import Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: 'superorg_%d' % n)

    @factory.post_generation
    def managers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for manager in extracted:
                self.managers.add(manager)
