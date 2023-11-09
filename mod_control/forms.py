import json
from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms.widgets import Select
from wtforms import SelectMultipleField,SubmitField,SelectField,IntegerField,FloatField,StringField
#from mod_deeplearning.model import getColumNames
from mod_preprocess.form import PreprocessForm
from datetime import datetime
def trtoEnCharacterWithoutSpace(x):

    x = x.replace(' ','')
    x = x.lower()
    x = x.replace('_','')
    x = x.replace('ç','c')
    x = x.replace('ı','i')
    x = x.replace('ü','u')
    x = x.replace('ğ','g')
    x = x.replace('ö','o')
    x = x.replace('ş','s')
    return x.capitalize()



oznitelik_listesi        = ["Smf","Smfdolar","Ptf","Ptfdolar","Arzislemhacmi","Talepislemhacmi",'Blokeslesmemiktari',
                           'Saatlikeslesmemiktari', 'Eslesmemiktari', 'Minalisfiyati',
                           'Maxalisfiyati', 'Minsatisfiyati', 'Maxsatisfiyati', 'Mineslemefiyati',
                           'Maxeslesmefiyati','Gerceklesendogalgaz', 'Gerceklesenbarajli', 'Gerceklesenlinyit',
                           'Gerceklesenakarsu', 'Gercekleseni̇thalkomur', 'Gerceklesenruzgar',
                           'Gerceklesengunes', 'Gerceklesenfueloil', 'Gerceklesenjeotermal',
                           'Gerceklesenasfaltitkomur', 'Gerceklesentaskomur',
                           'Gerceklesenbiyokutle', 'Gerceklesennafta', 'Gerceklesenlng',
                           'Gerceklesenuluslararasi']
#oznitelik_listesi = getColumNames()

oznitelik_listesi_values = [trtoEnCharacterWithoutSpace(x) for x in oznitelik_listesi]
metrikler                = ['mean_squared_error','root_mean_squared_error','mean_absolute_error','mean_absolute_percentage_error',
                            'mean_squared_logarithmic_error','cosine_similarity','logcosh']

losses                   = ['mean_squared_error','mean_absolute_error','mean_absolute_percentage_error','mean_squared_logarithmic_error','cosine_similarity','log_cosh']
class ChosenSelect(Select):

    def __init__(self, multiple=False, renderer=None, options={}):
        """
            Initiate the widget. This offers you two general options.
            First off it allows you to configure the ChosenSelect to
            allow multiple options and it allows you to pass options
            to the chosen select (this will produce a json object)
            that chosen will get passed as configuration.

                :param multiple: whether this is a multiple select
                    (default to `False`)
                :param renderer: If you do not want to use the default
                    select renderer, you can pass a function that will
                    get the field and options as arguments so that
                    you can customize the rendering.
                :param options: a dictionary of options that will
                    influence the chosen behavior. If no options are
                    given `width: 100%` will be set.
        """
        super(ChosenSelect, self).__init__(multiple=multiple)
        self.renderer = renderer
        options.setdefault('width', '100%')
        self.options = options

    def __call__(self, field, **kwargs):
        """
            Render the actual select.

                :param field: the field to render
                :param **kwargs: options to pass to the rendering
                    (i.e. class, data-* and so on)

            This will render the select as is and attach a chosen
            initiator script for the given id afterwards considering
            the options set up in the beginning.
        """
        kwargs.setdefault('id', field.id)
        # currently chosen does not reflect the readonly attribute
        # we compensate for that by automatically setting disabled,
        # if readonly if given
        # https://github.com/harvesthq/chosen/issues/67
        if kwargs.get("readonly"):
            kwargs['disabled'] = 'disabled'
        html = []
        # render the select
        if self.renderer:
            html.append(self.renderer(self, field, **kwargs))
        else:
            html.append(super(ChosenSelect, self).__call__(field, **kwargs))
        # attach the chosen initiation with options
        html.append(
            '<script>$("#%s").chosen(%s);</script>\n'
            % (kwargs['id'], json.dumps(self.options))
        )
        # return the HTML (as safe markup)
        return Markup('\n'.join(html))


class DeepLearningForm(FlaskForm):

    testDay                  = StringField(label='Test Edilecek Tarih')#,default= datetime.now().strftime("%m/%d/%Y"))
    selectHours = SelectField(label='Kaç Saatlik Tahmin', choices=['2','4','8','12','24'],
                                default='4')
    gonder = SubmitField(label='Tahmin Et')