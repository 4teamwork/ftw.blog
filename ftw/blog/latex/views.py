from DateTime import DateTime
from ftw.blog import _
from ftw.blog.interfaces import IBlog
from ftw.blog.interfaces import IBlogEntry
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.view import MakoLaTeXView
from ftw.pdfgenerator.view import RecursiveLaTeXView
from Products.ATContentTypes.interfaces.image import IATImage
from Products.ATContentTypes.lib.imagetransform import ATCTImageTransform
from zope.component import adapts
from zope.i18n import translate
from zope.interface import Interface


class BlogView(RecursiveLaTeXView):
    adapts(IBlog, Interface, ILaTeXLayout)

    template_directories = ['templates']
    template_name = 'blog.tex'

    def get_render_arguments(self):
        blog = self.context
        args = super(BlogView, self).get_render_arguments()
        args.update({
            'title': blog.Title(),
            '_': lambda *a, **kw: translate(_(*a, **kw), context=self.request),
        })
        return args

    def render_children(self):
        """Render LaTeX views of children and return the LaTeX content.
        """

        latex = []

        # If the export was started on this object and "paths" are passed
        # from folder_contents, we should only export the selected objects.
        if self.context == self.layout.context:
            paths = self.request.get('paths', None)
        else:
            paths = None

        for brain in self.context.getFolderContents(
                {
                    'sort_order': 'descending',
                }):
            obj = brain.getObject()
            if paths and '/'.join(obj.getPhysicalPath()) not in paths:
                continue

            data = self.layout.render_latex_for(obj)
            if data:
                latex.append(data)

        return '\n'.join(latex)


class BlogEntryView(MakoLaTeXView):
    adapts(IBlogEntry, Interface, ILaTeXLayout)

    template_directories = ['templates']
    template_name = 'blogentry.tex'

    def get_render_arguments(self):
        blogentry = self.context
        args = super(BlogEntryView, self).get_render_arguments()

        args.update({
            'title': self.convert(blogentry.Title()),
            'text': self.convert(blogentry.getText()),
            'owner': self.convert(str(blogentry.getOwner())),
            'categories':
                ', '.join([cat.Title() for cat in blogentry.getCategories()]),
            'tags': ', '.join(blogentry.tags),
            '_': lambda *a, **kw: translate(_(*a, **kw), context=self.request),
        })

        # date
        if blogentry.getEffectiveDate():
            date = blogentry.getEffectiveDate().strftime('%d. %b %Y')
        else:
            date = translate(_(u'latex_unpublished', default=u'Unpublished'),
                             context=self.request)
        args.update({'date': date})

        # leadimage
        if blogentry.getLeadimage():
            latex_lead_img = self._generate_includegraphics_latex(
                blogentry.getLeadimage(), r'\linewidth')
            args.update({
                'leadimage': latex_lead_img,
            })

        # images in blogentry container
        latex_images = []
        images = blogentry.getFolderContents({
            'object_provides': IATImage.__identifier__
        })
        for image in images:
            latex_img = self._generate_includegraphics_latex(
                image.getObject().getImage(), r'0.45\linewidth')
            latex_images.append(u'\\fbox{%s}' % latex_img)
        args.update({'images': '\n'.join(latex_images)})

        return args

    def _generate_includegraphics_latex(self, image, width):
        name = '%s_image' % image.UID()

        self.layout.use_package('graphicx')
        self.layout.get_builder().add_file(
            '%s.jpg' % name, self.get_raw_image_data(image))

        return r'\includegraphics[width=%s]{%s}' % (width, name)

    def get_raw_image_data(self, image):
        transformer = ATCTImageTransform()
        img = transformer.getImageAsFile(img=image)

        if img is not None:
            return img.read()

        elif isinstance(image.data, str):
            return image.data

        else:
            return image.data.read()
