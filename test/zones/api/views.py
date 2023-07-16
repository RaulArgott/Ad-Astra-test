from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from zones.models import Zone
from zones.models import Distribution

@api_view(['POST'])
def edit(request):
    zone_id = request.data.get('id')
    name = request.data.get('name')
    distributions = request.data.get('distributions')
    for item in distributions:
        print(item)
        distribution = Distribution.objects.filter(pk=item['id']).first()
        if distribution:
            distribution.percentage = item['percentage']
        else:            
            distribution= Distribution(percentage=item['percentage'], zone_id=zone_id)
        distribution.save()

    zone = Zone.objects.filter(pk=zone_id).first()
    if not zone:
        return Response('', status=status.HTTP_400_BAD_REQUEST)

    zone.name = name
    zone.save()

    return Response()