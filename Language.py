import random

class Language:
    """All words and language variations"""
    def __init__(self, type):
        """
        :param dyn_resource: Language.
        """
        if type == None:
            type = "beer"

        self.type = type

    def get_imbibed(self):
        words = ['imbibed', 'swallowed', 'drunk', 'glugged', 'bulldozed', 'finished', 'demolished', 'polished off', 'slurped', 'necked', 'downed', 'supped', 'enjoyed']
        return random.choice(words)

    def get_session(self):
        words = ['in this session NotLikeThis', 'during this sesh KomodoHype', 'in this marathon SeemsGood', 'during this stream YouDontSay', 'during this one', 'today CoolStoryBob', 'in their life! Kappa']
        return random.choice(words)

    def get_alcoholic(self):
        words = ['big-ass', 'large', 'standard', 'beautiful', 'small']

        if self.type == 'beer':
            ext = ['alcoholic', 'boozy', 'whoop-ass', 'adult', '10%']
            words.extend(ext)
        elif self.type == 'water':
            ext = ['hydrating', 'sparkling', 'still', 'spring-derived']
            words.extend(ext)
        elif self.type == 'tea':
            ext = ['steaming', 'infused']
            words.extend(ext)
        elif self.type == 'coffee':
            ext = ['steaming', 'strong', 'black', 'white', 'filtered', 'ground']
            words.extend(ext)

        return random.choice(words)
