from VK import VK


class User(VK):
    __FRIENDS = []          # list of User class
    __GROUPS = {}           # list of group IDs in ['items']
    __IS_FRIENDS_INIT = False
    __IS_GROUPS_INIT = False
    __INFO = {}

    def __init__(self, user_id=None, user_info=None):
        """
        Create new User ether from id or from dictionary user_info
        :param user_id:
        :param user_info:
        """
        if user_info:
            self.__INFO = user_info
        elif user_id:
            self.__INFO = User.get_users_info([user_id])[0]
        else:
            raise Exception("wrong user creation")  # TODO: handle this

    def __str__(self):
        return f'https://vk.com/id{self.get_id()}'

    @staticmethod
    def get_users_info(user_list):
        """
        :param user_list: list of VK user ids
        :return: set of VK user properties
        """
        ids_string = ','.join((str(i) for i in user_list))
        response_users_info = VK.req(
            'https://api.vk.com/method/users.get',
            params={
                'user_ids': ids_string,
                'access_token': VK.get_token(),
                'v': '5.89',
                'fields': 'is_closed,can_access_closed',
            }
        )
        return response_users_info.json()['response']

    @staticmethod
    def get_users(ids):
        """
        :param ids: list of VK users ID (string or integer)
        :return: list of class User
        """
        response_users_info = User.get_users_info(ids)
        user_list = [User(user_info=user_info) for user_info in response_users_info]
        return user_list

    def update_friends_list(self):
        response = VK.req(
            'https://api.vk.com/method/friends.get',
            params={
                'user_id': self.get_id(),
                'access_token': VK.get_token(),
                'v': '5.89',
            }
        )
        friends_id = response.json()['response']['items']
        friends_list = User.get_users(friends_id)
        return friends_list

    def update_groups_list(self):
        response = VK.req(
            'https://api.vk.com/method/groups.get',
            params={
                'user_id': self.get_id(),
                'access_token': VK.get_token(),
                'v': '5.89',
            }
        )
        return response.json()['response']

    def get_friends(self):
        if not self.__IS_FRIENDS_INIT:
            self.__FRIENDS = self.update_friends_list()
            self.__IS_FRIENDS_INIT = True
        return self.__FRIENDS

    def get_groups(self):
        if not self.__IS_GROUPS_INIT:
            self.__GROUPS = self.update_groups_list()
            self.__IS_GROUPS_INIT = True
        return self.__GROUPS['items']

    def groups_has_but_friends_not(self):
        all_fr_groups = set()
        fr_list = self.get_friends()
        for i in range(len(fr_list)):
            if not (fr_list[i].is_closed() or fr_list[i].is_deleted):
                all_fr_groups |= set(fr_list[i].get_groups())
        unique_groups_id = set(self.get_groups()) - all_fr_groups
        return VK.get_groups_info(list(unique_groups_id))

    def get_id(self):
        return self.__INFO['id']

    def is_closed(self):
        return self.__INFO.get('is_closed', True)

    def is_deleted(self):
        return bool(self.get_info().get('deactivated', None))

    def get_info(self):
        return self.__INFO
