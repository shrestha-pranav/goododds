from django import forms

class PlayGameForm(forms.Form):
    amount = forms.IntegerField(
        label="Amount", initial=1000, min_value=100, max_value=10000)

    odds   = forms.TypedChoiceField(
        label="Odds", coerce=str, empty_value="Odds (Default 2:3)",
        choices=[
            ("2:3", "The good odds! 2:3"),
            ("1:2", "The coin-flip 1:2"), 
            ("1:100", "For the truly brave 1:100")
        ]
        )
