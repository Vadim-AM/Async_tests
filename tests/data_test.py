from app.config import ADMIN_KEY, PINCODE_LENGTH


class MainPage:
    URL = ['http://localhost:8081/api/v1',
           'http://localhost:8081/']
    CODE = [404, 200]
    RESPONSES = [
        {'detail': 'Not Found'},
        {"Name service": "My Service"}
    ]
    DATA_LIST = list(zip(URL, CODE, RESPONSES))


class SignUp:
    DATA = [
        {
            'pincode': '111222333',  # correct
            'admin_key': f'{ADMIN_KEY}'
        },
        {
            'pincode': '111222333',  # pin-code exists
            'admin_key': f'{ADMIN_KEY}'
        },
        {
            'pincode': '111222333',  # wrong key
            'admin_key': 'wrong_admin_key'
        },
        {
            'pincode': '111',  # short pin
            'admin_key': f'{ADMIN_KEY}'
        }
    ]
    RESPONSE_CODES = [200, 400, 401, 400]
    RESPONSES = [
        {'Detail': 'Terminal created'},
        {'detail': 'Pin-code is registered'},
        {'detail': 'Access is denied'},
        {'detail': f'PIN code must be equal to {PINCODE_LENGTH} numbers'}
    ]
    DATA_LIST = list(zip(DATA, RESPONSE_CODES, RESPONSES))


class LogIn:
    DATA = [
        {
            'pincode': '111',  # short
        },
        {
            'pincode': '333666999',  # inactive
        },
        {
            'pincode': '000000000',  # not found
        }

    ]
    RESPONSE_CODES = [400, 400, 400, 200]
    RESPONSES = [
        {'detail': f'PIN code must be equal to {PINCODE_LENGTH} numbers'},
        {'detail': 'Pin-code not found'},
        {'detail': 'Inactive terminal'}
    ]
    DATA_LIST = list(zip(DATA, RESPONSE_CODES, RESPONSES))


class Item:
    def __init__(self, number, status, t_type='t.basic'):
        self.activationTerminal = None
        self.itemNumber = number
        self.status = status
        self.activationDate = '1945-07-16'
        self.type = t_type
        self.price = 500
        self.startTime = 'any_time_in_the_past'


class ItemStatus:
    def __init__(self, items):
        self.items = items

    async def set(self, *args):
        dictionary = list(args[0].keys())
        values = list(args[0].values())
        index = int(dictionary[0].split('.')[1])
        self.items[index].status = values[0]
        self.items[index].activationTerminal = values[1]
        self.items[index].activationDate = values[2]


item_status1 = ItemStatus([Item(number=129, t_type='t.discounted', status='activated'),
                           Item(number=129, t_type='t.certificate', status='not activated'), ])
item_status2 = ItemStatus([Item(number=129, t_type='t.certificate', status='not activated'),
                           Item(number=129, status='activated')])


class ToList:
    def to_list(self):
        pass


class ItemData:
    item_status1 = ItemStatus([Item(number=129, status='not activated'),
                               Item(number=129, status='activated')])
    item_status2 = ItemStatus([Item(number=129, status='activated'),
                               Item(number=129, status='not activated'), ])
    RESPONSE_CODES = [503, 400, 200, 200]
    MOCK_DB_CHECK = [False, True, True, True]
    MOCK_ITEM_STATUS = [False, None, item_status1, item_status2]
    RESPONSES = [
        {'detail': 'Database is not available'},
        {"detail": 'Item not found'},
        {'Item status': "not activated"},
        {
            'Status': item_status2.items[0].status,
            'Activate datetime': item_status2.items[0].activationDate,
            'type': str(item_status2.items[0].type).split('.')[1],
            'price': item_status2.items[0].price,
            'time': item_status2.items[0].startTime,
        }
    ]
    DATA_LIST = list(zip(MOCK_DB_CHECK, MOCK_ITEM_STATUS, RESPONSE_CODES, RESPONSES))


class Activate:
    item_status1 = ItemStatus([Item(number=129, status='activated'),
                               Item(number=129, status='not activated'), ])
    item_status2 = ItemStatus([Item(number=129, status='not activated'),
                               Item(number=129, status='activated')])
    ITEM = [
        {"item_number": "7684bsc150"},
        {"item_number": "7684bsc150"},
        {"item_number": "7684bsc150"},
        {"item_number": "7684bsc150"}
    ]
    MOCK_DB_CHECK = [False, True, True, True]
    MOCK_ITEM_STATUS = [False, None, item_status1, item_status2]
    RESPONSE_CODES = [503, 400, 400, 200]
    RESPONSES = [
        {'detail': 'Database is not available'},
        {"detail": 'not found'},
        {"detail": 'Additional problems'},
        {
            'Status': item_status2.items[1].status,
            'Activate datetime': item_status2.items[0].activationDate,
            'type': str(item_status2.items[0].type).split('.')[1],
            'price': item_status2.items[0].price,
            'time': item_status2.items[0].startTime,
        }
    ]
    DATA_LIST = list(zip(ITEM, MOCK_DB_CHECK, MOCK_ITEM_STATUS, RESPONSE_CODES, RESPONSES))


class Statistics:
    MOCK_DB_CHECK = [False, True]
    res1 = ToList()

    RESULT_ORDERS = res1

    DATA_WITH_DATE = [
        {"date": "2022-10-18T00:00:00.000+00:00",
         "delta_date": 1,
         "SessionId": 2
         },
        {
            "date": "2022-10-18T00:00:00.000+00:00",
            "delta_date": 1,
            "SessionId": 2
        }
    ]

    RESPONSE_CODES = [503, 200]

    RESPONSES = [
        {'detail': 'Database is not available'},
        {
            'basic': {
                'activated': 0,
                'not activated': 0,
            },
            'advanced': {
                'activated': 0,
                'not activated': 0,
            },
            'other': {
                'activated': 0,
                'not activated': 0,
            },
        }
    ]

    W_DATA_LIST = list(zip(MOCK_DB_CHECK, DATA_WITH_DATE, RESPONSE_CODES, RESPONSES))

    DATA_WO_DATE = [
        {
            "date": "2022-10-18T00:00:00.000+00:00",
            "delta_date": 10
        },
        {
            "date": "2022-10-18T00:00:00.000+00:00",
            "delta_date": 10
        }
    ]
    WO_DATA_LIST = list(zip(MOCK_DB_CHECK, DATA_WO_DATE, RESPONSE_CODES, RESPONSES))
