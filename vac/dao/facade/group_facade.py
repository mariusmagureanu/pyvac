__author__ = 'mariusmagureanu'
from .base_facade import BaseFacade


class GroupFacade(BaseFacade):

    def __init__(self):
        from vac.dao.entities.model import Group
        super(GroupFacade, self).__init__(Group)

    def add_cache(self, cache_name, group_name):
        """
        Assigns a cache to a given group. If the
        cache already belongs to another group, then
        this dependency will be updated.
        :param cache_name: The name of the cache(node).
        :param group_name: The name of the group.
        :return:
        """
        from .node_facade import NodeFacade
        node_facade = NodeFacade()
        node = node_facade.find_one_based_on_field('name', cache_name)
        group = self.find_one_based_on_field('name', group_name)

        assert (node is not None)
        assert (group is not None)
        if node.group is not None \
                and node in node.group.caches:
            node.group.caches.remove(node)
            node.group.save()

        if node not in group.caches:
            group.caches.append(node)
            group.save()
            node.group = group
            node.save()

    def create_group(self, name):
        """
        Creates a group with the given name.
        :param name: The name of the new group.
        :return:
        """
        from vac.dao.entities.model import Group
        g = Group(name=name)
        self.save(g)

    def remove_cache(self, cache_name, group_name):
        """
        Removes a cache from a given group.
        :param cache_name: Cache(node) name.
        :param group_name: Group name.
        :return:
        """
        from .node_facade import NodeFacade
        node_facade = NodeFacade()
        node = node_facade.find_one_based_on_field('name', cache_name)
        group = self.find_one_based_on_field('name', group_name)

        assert (group is not None)
        assert (node is not None)
        node.group = None
        node.save()
        if node in group.caches:
            group.caches.remove(node)
            group.save()

    def clear_caches(self, group_name):
        """
        Clears the list of caches assigned to
        the given group.
        :param group_name: Group name.
        :return:
        """
        group = self.find_one_based_on_field('name', group_name)
        assert (group is not None)
        del group.caches[:]
        group.save()

    def get_nodes_as_tuples(self, group_name):
        """
        Helper method, it it being considered
        for refactoring.
        :param group_name: Group name.
        :return:
        """
        group = self.find_one_based_on_field('name', group_name)
        nodes = [
            (n.agent_host,
             n.agent_username,
             n.agent_password,
             n.name) for n in group.caches]
        return nodes
