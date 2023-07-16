from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import functools

from zones.models import Zone
from zones.models import Distribution
from zones.api.serializers import DistributionSerializer

@api_view(['POST'])
def edit(request):
    """ Get data from request """
    zone_id = request.data.get('id')
    name = request.data.get('name')
    distributions = request.data.get('distributions')
    distributions_to_delete = request.data.get('distributions_delete')

    """ Validation """
    if not name:
        return Response("Name is required", status=status.HTTP_400_BAD_REQUEST)
    
    if len(list(distributions)) < 1:
        return Response("At least 1 distribution is required", status=status.HTTP_400_BAD_REQUEST)

    percentages = list(map(lambda item: item['percentage'], distributions))
    sum_percentages = functools.reduce(lambda a,b: a+b,percentages)
    if sum_percentages != 100:
        return Response("Sum of distributions must be 100", status=status.HTTP_400_BAD_REQUEST)
        
    repeated_zone = Zone.objects.filter(name__iexact = name).exclude(pk=zone_id).first()
    print(repeated_zone)
    if repeated_zone is not None:
        return Response("Zone name must be unique", status=status.HTTP_400_BAD_REQUEST)
    
        
    """ Bulk delete distributions """
    distribution_bulk_delete = Distribution.objects.filter(id__in=distributions_to_delete)
    if distribution_bulk_delete:
        distribution_bulk_delete.delete()

    """ Bulk edit distributions """
    for item in distributions:
        distribution = Distribution.objects.filter(pk=item['id']).first()
        if distribution:
            distribution.percentage = item['percentage']
        else:            
            distribution= Distribution(percentage=item['percentage'], zone_id=zone_id)
        distribution.save()

    """ Edit zone """
    zone = Zone.objects.filter(pk=zone_id).first()
    if not zone:
        return Response('', status=status.HTTP_400_BAD_REQUEST)

    zone.name =  name.strip()
    zone.save()

    """ Return distributions """
    distributions_data = DistributionSerializer(Distribution.objects.filter(zone_id = zone_id), many=True).data
    return Response(distributions_data)