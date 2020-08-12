from django import forms
import crispy_forms.helper
import crispy_forms.layout
import crispy_forms.bootstrap


class FeedbackForm(forms.Form):
    rating = forms.TypedChoiceField(choices=(
        ("1", "\U0001F640\uFE0F The worst"),
        ("2", "\U0001F63E\uFE0F Bearable"),
        ("3", "\U0001F408\uFE0F Eh"),
        ("4", "\U0001F638\uFE0F Good but not perfect"),
        ("5", "\U0001F63B\uFE0F Loved it"),
    ), coerce=int, required=True, label="How would you rate the experience overall?")
    liked = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5
        }), label="What did you like?", required=False
    )
    disliked = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5
        }),
        label="What could've gone better? (Feel free to be really honest, we won't cry. Ok maybe a little 🙈)",
        required=False
    )
    other_comments = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5
        }), label="Any other comments?", required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = crispy_forms.helper.FormHelper()
        self.helper.layout = crispy_forms.layout.Layout(
            crispy_forms.bootstrap.InlineRadios('rating'),
            'liked',
            'disliked',
            'other_comments'
        )

        self.helper.add_input(crispy_forms.layout.Submit('submit', 'Submit'))
