from ftw.pdfgenerator.layout.customizable import CustomizableLayout
from zope.component import adapts
from zope.interface import Interface
from ftw.blog import _
from ftw.pdfgenerator.interfaces import IBuilder
from zope.i18n import translate
from ftw.blog.interfaces import IBlog


class BlogLayout(CustomizableLayout):
    adapts(IBlog, Interface, IBuilder)

    template_directories = ['templates']
    template_name = 'blog_layout.tex'

    def get_render_arguments(self):
        args = super(BlogLayout, self).get_render_arguments()

        args['_'] = lambda *a, **kw: translate(_(*a, **kw),
                                               context=self.request)

        return args

    def before_render_hook(self):
        self.use_babel()
        self.use_package('inputenc', options='utf8', append_options=False)
        self.use_package('fontenc', options='T1', append_options=False)
        self.use_package('ae,aecompl')
        self.use_package(
            'geometry', options='left=35mm,right=20mm,top=20mm,bottom=25mm',
            append_options=False)
        self.use_package(
            'hyperref', options='colorlinks=false,breaklinks=true,'
            'linkcolor=black,pdfborder={0 0 0}', append_options=False)

        self.use_package('helvet')
        self.use_package('titlesec', 'compact')
        self.use_package('fancyhdr')
        self.use_package('enumitem')
        self.use_package('lastpage')
        self.use_package('scrtime')
