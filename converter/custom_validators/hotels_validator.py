from validator import Validator

class HotelValidator(Validator):
    def __init__(self):
        super(HotelValidator, self).__init__()

    def validate(self, data):
        super(HotelValidator, self).keep_count()
        errors = []
        # ratings validation 0 - 3
        try:
            s = data["stars"]
            rating = int(s)
            if rating < 0 or rating > 3:
                errors.append({
                    f'record {self.count}': f'Rating failed validation. Expected 0 < rating <= 3, got {rating}'
                })
        except Exception as e:
            errors.append({
                    f'record {self.count}': f'Rating failed validation. Expected an integer, got {s}: {type(s)} --> {str(e)}'
                })
        self.errors = self.errors + errors