from fastapi import APIRouter, Depends

from routers.utils import get_collection, handle_error
from routers.auth import validate_api_key

router = APIRouter()


class FilterFields:
    POSITION = 'position'
    CITY = 'city'


def get_offers_collection():
    OFFERS_COLLECTION_NAME = 'offers'
    return get_collection(OFFERS_COLLECTION_NAME)


def filter_offers(items, filter_field):
    filtered_items = set()
    for item in items:
        data = item.to_dict()
        field_item = data.get(filter_field)
        if field_item:
            filtered_items.add(field_item)
    return {"filters": list(filtered_items)}


@router.get("/positionFilters")
def filter_by_position():
    try:
        collection = get_offers_collection()
        offers = collection.stream()
        return filter_offers(offers, FilterFields.POSITION)
    except Exception as e:
        handle_error(e)


@router.get("/cityFilters")
def filter_by_city():
    try:
        collection = get_offers_collection()
        offers = collection.stream()
        return filter_offers(offers, FilterFields.CITY)
    except Exception as e:
        handle_error(e)
