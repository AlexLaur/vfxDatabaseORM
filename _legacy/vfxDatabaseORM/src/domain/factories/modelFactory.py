class ModelFactory(object):
    @staticmethod
    def build(model_class, raw_values):

        if not raw_values:
            raise Exception("TODO")

        # TODO raise if missing value

        kwargs = {}

        fields = model_class.get_fields()
        for field in fields:
            for value_name, value in raw_values.items():
                if value_name != field.db_name:
                    continue
                kwargs[field.name] = value

        return model_class(**kwargs)
