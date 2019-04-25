import json

from rest_framework.renderers import JSONRenderer


class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the article can't be created
        # or something similar due to missing fields), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        errors =''
        try:
            errors = data.get('errors', None)
        except:
            pass  


        if errors:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            return super(ArticleJSONRenderer, self).render(data)


        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'article': data
        })
