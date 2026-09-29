FEATURE_ORDER = ('nitrogen','phosphorus','potassium','ph','moisture','temperature','humidity','rainfall')
def numeric_vector(features): return [[float(features[key]) for key in FEATURE_ORDER]]
