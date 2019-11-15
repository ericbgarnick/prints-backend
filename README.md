# sure-prints

APIs for a photo website allowing display of photos and ordering of prints of photos

## Installation

* Clone the Git repository https://github.com/ericbgarnick/sure-prints.git
* Create virtualenv
* Install requirements from requirements.txt

```bash
pip install -r requirements.txt
```

## Usage

#### Run migrations

```bash
python manage.py migrate
```

#### Run localserver

```bash
python manage.py runserver
```

#### Populate DB with print size metadata and photos data

```bash
python manage.py shell_plus
```

```python
>>> from prints.utils import create_print_size_info
>>> from photos.utils import create_photos
>>> create_print_size_info()
>>> create_photos()
```
#### Running Unit Tests
```bash
python manage.py test
```

## TODOs
There were many cut corners in development of this project that I would fix if producing a usable product.  These include:
* `__str__`/`__repr__` methods for all models
* More thorough unit tests covering more edge cases (some unit tests were not completed for the PrintOrder view class)
* More logic abstraction (there is some unnecessarily duplicated logic left in)
* More error handling
* Data validation for POST request
* Encryption of PII and payment info

## APIs
**Resource:** /geospatial/meta

**Description:** Provide a list of all states in the US and countries in the world.

**Supported Methods:** GET

**Parameters:** None

**Response:**
```json
{
    "states": [
        <str>
    ],
    "countries": [
        <str>
    ]
}
```
---

**Resource:** /prints/meta

**Description:** Provide all available print sizes with purchase price and shipping price for each size.

**Supported Methods:** GET

**Parameters:** None

**Response:**
```json
[
    {
        "size_name": <str>,
        "base_price_cents": <int>,
        "ship_price_cents": <int>
    }
]
```

---

**Resource:** /photos/

**Description:** Provide info for requested photos (or all), including path to location in static data folder

**Supported Methods:** GET

**Parameters:** page=\<int\> (optional)

**Response:**
```json
[
    {
        "image_id": <int>,
        "title": <str>,
        "file_location": <str: path/to/file>,
        "num_prints": <int>,
        "shot_date": <date: YYYY-MM-DD>
    }
]
```
**Paginated Response:**
```json
{
    "count": <int (total number of records available)>,
    "next": <str (url for next page, or null)>,
    "previous": <str (url for previous page, or null)>
    "results": [
        {
            "image_id": <int>,
            "title": <str>,
            "file_location": <str: /relative/path/to/file>,
            "max_prints": <int>,
            "shot_date": <date: YYYY-MM-DD>
        }
    ]
}
```
---
**Resource:** /orders/

**Description:** Accept orders for prints of photos, including photo selection, 
print size, billing and shipping info.  Return an order number and order/billing 
summary data.  Sample request data can be found in sample_data/sample_order.json

**Supported Methods:** POST

**Request:**
```json
{
    "customer": {
        "first_name": <str>,
        "last_name": <str>,
        "email": <str>,
        "phone": <str/null>,
        "address": <address**/null>
    },
    "shipping_address": <address**>,
    "prints": [
        {
            "image_id": <int>,
            "size": <SMALL/MEDIUM/LARGE>
        }
    ],
    "payment": {
        "method": <CREDIT/DEBIT>,
        "credit_network": <VISA/MASTERCARD/DISCOVER/AMEX>,
        "account_number": <str>,
        "card_expiration": <str: MMYYYY>,
        "card_cvv": <str>,
        "billing_first_name": <str>,
        "billing_last_name": <str>,
        "billing_address": <address**>
    }
}
```

**Response:**
```json
{
    "order_num": <int>,
    "billing_summary": {
        "prints": [
            "image_title": <str>,
            "size": <SMALL/MEDIUM/LARGE>,
            "base_price_cents": <int>,
            "ship_price_cents": <int>
        ],
        "payment_method": <CREDIT/DEBIT>,
        "payment_account_end": <int>,  # last 4 digits of account number,
        "billing_first_name": <str>,
        "billing_last_name": <str>,
        "billing_address": <address**>,
        "shipping_address": <address**>
    }
}
```
