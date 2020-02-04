from urllib.parse import urlparse

class Validator():
    def __init__(self):
        self.count = 0
        self.errors = []

    def keep_count(self):
        self.count += 1

    def validate(self, data):
        self.keep_count()
        errors = []
        #  name validation : <= 100 characters
        namecount = len(data['name'])
        if namecount == 0 or namecount > 100:
            errors.append({
                f'record {self.count}': f'Name failed validation. Expected 0 < length <= 100, got {namecount}'
            })

        # ratings validation 0 - 5
        try:
            s = data["stars"]
            rating = int(s)
            if rating < 0 or rating > 5:
                errors.append({
                    f'record {self.count}': f'Rating failed validation. Expected 0 < rating <= 5, got {rating}'
                })
        except Exception as e:
            errors.append({
                    f'record {self.count}': f'Rating failed validation. Expected an integer, got {s}: {type(s)} --> {str(e)}'
                })

        # url validation (syntactically correct)
        parse_result = urlparse(data['url'])
        if parse_result.scheme == '' or parse_result.netloc == '':
            errors.append({
                f'record {self.count}': f'URL failed validation. got {data["url"]}'
            })
        self.errors = self.errors + errors
