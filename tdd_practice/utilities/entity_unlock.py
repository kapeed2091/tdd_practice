from enum import Enum
from ib_common.constants import BaseEnumClass


class EntityEnum(BaseEnumClass, Enum):
    tournament = 'TOURNAMENT'


class TournamentEntityEnum(BaseEnumClass, Enum):
    round_robin = 'ROUND_ROBIN'
    knock_out = 'KNOCK_OUT'
    round_robin_play_off = 'ROUND_ROBIN_PLAY_OFF'
    round_robin_knock_out = 'ROUND_ROBIN_KNOCK_OUT'
    one_vs_one_series = 'ONE_VS_ONE_SERIES'
    tri_series = 'TRI_SERIES'
    best_of_n = 'BEST_OF_N'
    kbc_type = 'KBC_TYPE'
    lb_type = 'LB_TYPE'
    multi_round_lb_type = "MULTI_ROUND_LB_TYPE"


class EntityUnlock(object):
    def __init__(self, user_ids, game_id=-1):
        from ib_gamification.models import UserUnlockedEntity, Entity

        self.user_ids = user_ids
        self.game_id = game_id
        entities = Entity.get_entities()
        self.user_unlocked_entity_dict = \
            UserUnlockedEntity.get_unlocked_entities(
                user_ids=self.user_ids, game_id=self.game_id)

        entity_type_id_dict = dict()
        entity_id_type_dict = dict()
        for ei in entities:
            entity_type_id_dict[ei['entity_type']] = ei['id']
            entity_id_type_dict[ei['id']] = ei['entity_type']
            child_entities = ei['child_entities']
            for child_entity in child_entities:
                entity_type_id_dict[child_entity['entity_type']] = \
                    child_entity['id']
                entity_id_type_dict[child_entity['id']] = \
                    child_entity['entity_type']

        self.entity_type_id_dict = entity_type_id_dict
        self.entity_id_type_dict = entity_id_type_dict

    def check_entities(self, user_entity_dict):
        user_entity_summary_dict = dict()
        for user_id, entities_req in user_entity_dict.items():
            try:
                unlocked_entity_ids = self.user_unlocked_entity_dict[user_id]
            except KeyError:
                unlocked_entity_ids = list()

            unlocked_entities = list()
            for entity_id in unlocked_entity_ids:
                unlocked_entities.append(self.entity_id_type_dict[entity_id])

            missing_entities_in_req = set(entities_req) - set(unlocked_entities)
            unlocked_entities_in_req = \
                set(entities_req) - set(missing_entities_in_req)

            if len(missing_entities_in_req) == 0:
                success = True
            else:
                success = False

            user_entity_summary_dict[user_id] = {
                'unlocked_entities': unlocked_entities_in_req,
                'missing_entities': missing_entities_in_req,
                'success': success
            }
        return user_entity_summary_dict

    def get_unlocked_tournament_categories(self, user_id):
        user_entity_dict = {user_id: TournamentEntityEnum.get_list_of_values()}
        user_entity_summary_dict = self.check_entities(
            user_entity_dict=user_entity_dict)[user_id]

        return list(user_entity_summary_dict['unlocked_entities'])

    def get_locked_resources(self, user_id):
        from ib_gamification.constants.general import ResourceEntity
        user_entity_dict = {user_id: ResourceEntity.get_list_of_values()}

        user_entity_summary_dict = self.check_entities(
            user_entity_dict=user_entity_dict)[user_id]

        return list(user_entity_summary_dict['missing_entities'])

    def check_if_leaderboards_are_unlocked(self, user_id):
        from ib_gamification.constants.general import LevelUnlockEntityEnum

        user_entity_dict = {user_id: [LevelUnlockEntityEnum.leaderboard.value]}

        user_entity_summary_dict = self.check_entities(
            user_entity_dict=user_entity_dict)[user_id]

        if LevelUnlockEntityEnum.leaderboard.value in \
                user_entity_summary_dict['missing_entities']:
            return False

        return True

    def check_if_hall_of_fames_are_unlocked(self, user_id):
        from ib_gamification.constants.general import LevelUnlockEntityEnum

        user_entity_dict = {user_id: [LevelUnlockEntityEnum.hall_of_fame.value]}

        user_entity_summary_dict = self.check_entities(
            user_entity_dict=user_entity_dict)[user_id]

        if LevelUnlockEntityEnum.hall_of_fame.value in \
                user_entity_summary_dict['missing_entities']:
            return False

        return True

    def validate_tournament_category_unlocked(
            self, tournament_category, user_ids, user_id_wise_username=None,
            team_hash_key_wise_user_ids=None):

        user_id_wise_team_hash_key = {}
        if team_hash_key_wise_user_ids:
            for team_hash_key, team_user_ids in \
                    team_hash_key_wise_user_ids.items():
                for user_id in team_user_ids:
                    user_id_wise_team_hash_key[user_id] = team_hash_key

        locked_participant_names = list()
        for user_id in user_ids:
            unlocked_t_categories = self.get_unlocked_tournament_categories(
                user_id=user_id)
            if tournament_category not in unlocked_t_categories:
                if user_id_wise_username:
                    locked_participant_names.append(
                        user_id_wise_username[user_id])
                else:
                    locked_participant_names.append(
                        user_id_wise_team_hash_key[user_id])

        if not locked_participant_names:
            return

        from django_swagger_utils.drf_server.exceptions import BadRequest
        if len(locked_participant_names) == 1:
            from ib_tournament.constants.exception_messages import \
                TOURNAMENT_CATEGORY_LOCKED_FOR_PARTICIPANT
            raise BadRequest(
                TOURNAMENT_CATEGORY_LOCKED_FOR_PARTICIPANT[0].format(
                    locked_participant_names[0]),
                TOURNAMENT_CATEGORY_LOCKED_FOR_PARTICIPANT[1])
        else:
            from ib_tournament.constants.exception_messages import \
                TOURNAMENT_CATEGORY_LOCKED_FOR_PARTICIPANTS
            raise BadRequest(
                TOURNAMENT_CATEGORY_LOCKED_FOR_PARTICIPANTS[0].format(
                    ", ".join(locked_participant_names)),
                TOURNAMENT_CATEGORY_LOCKED_FOR_PARTICIPANTS[1])
