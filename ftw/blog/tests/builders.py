from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder import builder_registry


class BlogBuilder(ArchetypesBuilder):
    portal_type = 'Blog'

builder_registry.register('blog', BlogBuilder)


class BlogEntryBuilder(ArchetypesBuilder):
    portal_type = 'BlogEntry'

builder_registry.register('blog entry', BlogEntryBuilder)
