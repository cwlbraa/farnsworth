
from wiki.hooks import WikiDefaultHookset

from utils.variables import ANONYMOUS_USERNAME

class ProjectWikiHookset(WikiDefaultHookset):
    def _perm_check(self, wiki, user):
        return user.is_authenticated() and \
          user.is_active and \
          user.username != ANONYMOUS_USERNAME

    def can_create_page(self, wiki, user):
        return self._perm_check(wiki, user)

    def can_edit_page(self, page, user):
        return self._perm_check(page.wiki, user)

    def can_delete_page(self, page, user):
        return self._perm_check(page.wiki, user) and \
          (user.is_staff or user.is_superuser)

    def can_view_page(self, page, user):
        return True

def parse(wiki, content):
    return content
